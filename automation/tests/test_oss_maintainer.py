import io
import json
import tempfile
import unittest
from contextlib import redirect_stderr
from datetime import datetime, timezone
from pathlib import Path
from unittest.mock import patch

from automation.oss_maintainer import (
    GitHubRestClient,
    PlanRejected,
    apply_plan,
    build_openai_request,
    build_plan,
    enrich_plan,
    main,
    parse_openai_result,
    redact_public_text,
    validate_ai_suggestion,
    validate_policy,
)


ROOT = Path(__file__).resolve().parents[2]


def load_json(relative: str) -> dict:
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


class PolicyTests(unittest.TestCase):
    def test_rejects_unsupported_policy_version(self):
        policy = load_json("automation/maintenance-policy.json")
        policy["version"] = 999

        self.assertIn("unsupported policy version: 999", validate_policy(policy))

    def test_rejects_unknown_action_type(self):
        policy = load_json("automation/maintenance-policy.json")
        policy["allowed_actions"].append("merge_pull_request")
        self.assertIn(
            "allowed_actions contains unsupported value: merge_pull_request",
            validate_policy(policy),
        )

    def test_stale_closure_is_disabled_by_default(self):
        policy = load_json("automation/maintenance-policy.json")
        self.assertFalse(policy["stale"]["enabled"])

    def test_rejects_incomplete_nested_policy(self):
        policy = load_json("automation/maintenance-policy.json")
        policy["stale"] = {"enabled": False}
        self.assertTrue(validate_policy(policy))

    def test_rejects_boolean_max_mutations(self):
        policy = load_json("automation/maintenance-policy.json")
        policy["max_mutations_per_run"] = True
        self.assertIn("max_mutations_per_run must be at least 1", validate_policy(policy))

    def test_rejects_boolean_stale_minimum_days(self):
        policy = load_json("automation/maintenance-policy.json")
        policy["stale"]["minimum_days"] = False
        self.assertIn("stale policy has invalid values", validate_policy(policy))


class PlanningTests(unittest.TestCase):
    def setUp(self):
        self.policy = load_json("automation/maintenance-policy.json")
        self.now = datetime(2026, 7, 18, tzinfo=timezone.utc)

    def test_issue_missing_reproduction_gets_one_request(self):
        plan = build_plan(
            load_json("automation/fixtures/issue-opened.json"), self.policy, self.now
        )
        self.assertEqual(["add_label", "comment"], [item["type"] for item in plan["actions"]])
        self.assertIn(
            "<!-- oss-maintainer:request-details:v1 -->", plan["actions"][1]["body"]
        )

    def test_existing_marker_prevents_duplicate_comment(self):
        event = load_json("automation/fixtures/issue-opened.json")
        event["context"]["existing_markers"] = ["oss-maintainer:request-details:v1"]
        plan = build_plan(event, self.policy, self.now)
        self.assertNotIn("comment", [item["type"] for item in plan["actions"]])

    def test_pull_request_never_emits_protected_action(self):
        plan = build_plan(
            load_json("automation/fixtures/pull-request-opened.json"), self.policy, self.now
        )
        self.assertTrue(
            set(item["type"] for item in plan["actions"])
            <= {"add_label", "comment", "report"}
        )

    def test_schedule_emits_report_without_closing(self):
        plan = build_plan(
            load_json("automation/fixtures/scheduled-run.json"), self.policy, self.now
        )
        self.assertEqual(["report"], [item["type"] for item in plan["actions"]])

    def test_invalid_policy_returns_no_actions(self):
        policy = {"version": 1}
        plan = build_plan(load_json("automation/fixtures/issue-opened.json"), policy, self.now)
        self.assertEqual([], plan["actions"])
        self.assertTrue(plan["notices"])

    def test_unsupported_policy_version_returns_no_actions(self):
        policy = load_json("automation/maintenance-policy.json")
        policy["version"] = 999

        plan = build_plan(load_json("automation/fixtures/issue-opened.json"), policy, self.now)

        self.assertEqual([], plan["actions"])
        self.assertIn("unsupported policy version: 999", plan["notices"])

    def test_object_allowed_actions_fails_closed(self):
        policy = load_json("automation/maintenance-policy.json")
        policy["allowed_actions"] = {"add_label": True}
        plan = build_plan(load_json("automation/fixtures/issue-opened.json"), policy, self.now)
        self.assertEqual([], plan["actions"])
        self.assertIn("allowed_actions must be a list", plan["notices"])

    def test_nested_object_allowed_action_fails_closed(self):
        policy = load_json("automation/maintenance-policy.json")
        policy["allowed_actions"] = [{}]
        plan = build_plan(load_json("automation/fixtures/issue-opened.json"), policy, self.now)
        self.assertEqual([], plan["actions"])
        self.assertIn("allowed_actions entries must be strings", plan["notices"])

    def test_nested_list_allowed_action_fails_closed(self):
        policy = load_json("automation/maintenance-policy.json")
        policy["allowed_actions"] = [[]]
        plan = build_plan(load_json("automation/fixtures/issue-opened.json"), policy, self.now)
        self.assertEqual([], plan["actions"])
        self.assertIn("allowed_actions entries must be strings", plan["notices"])

    def test_non_numeric_failure_count_fails_closed(self):
        event = load_json("automation/fixtures/issue-opened.json")
        event["context"]["failure_count"] = "two"
        plan = build_plan(event, self.policy, self.now)
        self.assertEqual([], plan["actions"])
        self.assertIn("event context has invalid failure_count", plan["notices"])

    def test_object_replay_identifier_fails_closed(self):
        event = load_json("automation/fixtures/issue-opened.json")
        event["context"]["processed_delivery_ids"] = [{"id": "prior"}]
        plan = build_plan(event, self.policy, self.now)
        self.assertEqual([], plan["actions"])
        self.assertIn("event context has invalid processed_delivery_ids", plan["notices"])

    def test_object_marker_fails_closed(self):
        event = load_json("automation/fixtures/issue-opened.json")
        event["context"]["existing_markers"] = [{"marker": "prior"}]
        plan = build_plan(event, self.policy, self.now)
        self.assertEqual([], plan["actions"])
        self.assertIn("event context has invalid existing_markers", plan["notices"])

    def test_malformed_issue_returns_no_actions(self):
        event = load_json("automation/fixtures/issue-opened.json")
        event["issue"] = []
        plan = build_plan(event, self.policy, self.now)
        self.assertEqual([], plan["actions"])
        self.assertIn("malformed_issue", plan["notices"])

    def test_malformed_pull_request_returns_no_actions(self):
        event = load_json("automation/fixtures/pull-request-opened.json")
        event["pull_request"] = []

        plan = build_plan(event, self.policy, self.now)

        self.assertEqual([], plan["actions"])
        self.assertIn("malformed_pull_request", plan["notices"])

    def test_protected_pull_request_returns_no_actions(self):
        event = load_json("automation/fixtures/pull-request-opened.json")
        event["pull_request"]["labels"] = ["security"]

        plan = build_plan(event, self.policy, self.now)

        self.assertEqual([], plan["actions"])
        self.assertIn("protected_label", plan["notices"])

    def test_security_label_bypasses_ordinary_comments(self):
        event = load_json("automation/fixtures/issue-opened.json")
        event["issue"]["labels"] = ["security"]
        plan = build_plan(event, self.policy, self.now)
        self.assertNotIn("comment", [item["type"] for item in plan["actions"]])

    def test_processed_delivery_id_returns_empty_plan(self):
        event = load_json("automation/fixtures/issue-opened.json")
        event["context"]["processed_delivery_ids"] = [event["delivery_id"]]
        plan = build_plan(event, self.policy, self.now)
        self.assertEqual([], plan["actions"])

    def test_action_count_never_exceeds_mutation_budget(self):
        policy = load_json("automation/maintenance-policy.json")
        policy["max_mutations_per_run"] = 1
        plan = build_plan(load_json("automation/fixtures/issue-opened.json"), policy, self.now)
        self.assertLessEqual(len(plan["actions"]), 1)

    def test_stop_loss_prevents_mutations_after_two_failures(self):
        event = load_json("automation/fixtures/issue-opened.json")
        event["context"]["failure_count"] = 2
        plan = build_plan(event, self.policy, self.now)
        self.assertEqual([], plan["actions"])
        self.assertIn("stop_loss", plan["notices"])

    def test_issue_classification_never_introduces_a_missing_label(self):
        policy = load_json("automation/maintenance-policy.json")
        policy["label_rules"] = [{"label": "bug", "keywords": ["crash"]}]
        event = load_json("automation/fixtures/issue-opened.json")
        event["issue"] = {
            "title": "How should I configure this?",
            "body": "reproduction: install\nenvironment: macOS",
            "labels": [],
        }
        plan = build_plan(event, policy, self.now)
        self.assertTrue(
            all(item.get("label") == "bug" for item in plan["actions"] if item["type"] == "add_label")
        )

    def test_stale_closure_requires_enabled_policy_and_every_predicate(self):
        event = {
            "delivery_id": "stale-001",
            "event_name": "schedule",
            "issue": {
                "number": 99,
                "labels": ["waiting-for-author"],
                "updated_at": "2026-06-01T00:00:00Z",
            },
            "context": {"existing_markers": ["oss-maintainer:waiting-for-author:v1"]},
        }
        disabled_plan = build_plan(event, self.policy, self.now)
        self.assertNotIn("close_waiting_issue", [item["type"] for item in disabled_plan["actions"]])

        enabled_policy = load_json("automation/maintenance-policy.json")
        enabled_policy["stale"]["enabled"] = True
        enabled_plan = build_plan(event, enabled_policy, self.now)
        self.assertIn("close_waiting_issue", [item["type"] for item in enabled_plan["actions"]])
        close_action = next(
            item for item in enabled_plan["actions"] if item["type"] == "close_waiting_issue"
        )
        self.assertEqual(
            {"eligible": True, "marker_present": True, "protected": False},
            {key: close_action[key] for key in ("eligible", "marker_present", "protected")},
        )

        for field, value in (
            ("labels", []),
            ("labels", ["waiting-for-author", "security"]),
            ("updated_at", "2026-07-17T00:00:00Z"),
        ):
            rejected_event = json.loads(json.dumps(event))
            rejected_event["issue"][field] = value
            rejected_plan = build_plan(rejected_event, enabled_policy, self.now)
            self.assertNotIn(
                "close_waiting_issue", [item["type"] for item in rejected_plan["actions"]]
            )
        event["context"]["existing_markers"] = []
        no_notice_plan = build_plan(event, enabled_policy, self.now)
        self.assertNotIn("close_waiting_issue", [item["type"] for item in no_notice_plan["actions"]])

    def test_report_does_not_consume_the_mutation_budget(self):
        policy = load_json("automation/maintenance-policy.json")
        policy["stale"]["enabled"] = True
        policy["max_mutations_per_run"] = 1
        event = {
            "delivery_id": "stale-report-budget-001",
            "event_name": "schedule",
            "issue": {
                "labels": ["waiting-for-author"],
                "updated_at": "2026-06-01T00:00:00Z",
            },
            "context": {"existing_markers": ["oss-maintainer:waiting-for-author:v1"]},
        }
        plan = build_plan(event, policy, self.now)
        self.assertEqual(
            ["report", "close_waiting_issue"], [item["type"] for item in plan["actions"]]
        )


class AiBoundaryTests(unittest.TestCase):
    def test_redacts_common_sensitive_patterns(self):
        source = (
            "email person@example.com token sk-example123 ghp_abcdefghijklmnopqrstuvwxyz1234567890 "
            "api_key=credential-value "
            "-----BEGIN PRIVATE KEY----- secret -----END PRIVATE KEY-----"
        )
        redacted = redact_public_text(source)
        self.assertNotIn("person@example.com", redacted)
        self.assertNotIn("sk-example123", redacted)
        self.assertNotIn("ghp_abcdefghijklmnopqrstuvwxyz1234567890", redacted)
        self.assertNotIn("credential-value", redacted)
        self.assertNotIn("BEGIN PRIVATE KEY", redacted)

    def test_redacts_private_key_crossing_truncation_boundary(self):
        source = (
            "x" * 11_970
            + "-----BEGIN PRIVATE KEY----- secret -----END PRIVATE KEY-----"
        )
        redacted = redact_public_text(source)
        self.assertLessEqual(len(redacted), 12_000)
        self.assertNotIn("BEGIN PRIVATE KEY", redacted)

    def test_openai_request_uses_strict_allowlisted_schema(self):
        request = build_openai_request("public issue", ["bug", "documentation"], "gpt-5.6")
        schema = request["text"]["format"]
        self.assertEqual("json_schema", schema["type"])
        self.assertTrue(schema["strict"])
        self.assertEqual(
            ["bug", "documentation"], schema["schema"]["properties"]["label"]["enum"]
        )

    def test_parses_first_output_text_item(self):
        response = {
            "output": [{"content": [{"type": "output_text", "text": '{"label": "bug", "summary": "Crash"}'}]}]
        }
        self.assertEqual({"label": "bug", "summary": "Crash"}, parse_openai_result(response))

    def test_ai_suggestion_cannot_introduce_action_or_label(self):
        suggestion = {
            "label": "merge-now",
            "summary": "ship it",
            "action": "merge_pull_request",
        }
        self.assertEqual([], validate_ai_suggestion(suggestion, {"bug", "documentation"}))

    def test_valid_ai_suggestion_only_returns_allowed_plan_items(self):
        actions = validate_ai_suggestion(
            {"label": "bug", "summary": "A concise public summary."}, {"bug", "documentation"}
        )
        self.assertEqual(["add_label", "report"], [item["type"] for item in actions])

    def test_enrichment_redacts_before_injected_transport(self):
        policy = load_json("automation/maintenance-policy.json")
        policy["ai"]["enabled"] = True
        event = load_json("automation/fixtures/issue-opened.json")
        event["issue"]["body"] = "email person@example.com token sk-example123"
        captured = {}

        class Response:
            def __enter__(self):
                return self

            def __exit__(self, *args):
                return False

            def read(self):
                return b'{"output": [{"content": [{"type": "output_text", "text": "{\\\"label\\\": \\\"bug\\\", \\\"summary\\\": \\\"Public summary.\\\"}"}]}]}'

        def transport(request, timeout):
            captured["payload"] = request.data.decode("utf-8")
            return Response()

        enriched = enrich_plan(
            {"version": 1, "event_key": "test", "actions": [], "notices": []},
            event,
            policy,
            "test-token",
            transport,
        )
        self.assertNotIn("person@example.com", captured["payload"])
        self.assertNotIn("sk-example123", captured["payload"])
        self.assertEqual(["add_label", "report"], [item["type"] for item in enriched["actions"]])

    def test_incomplete_response_has_no_enrichment_actions(self):
        policy = load_json("automation/maintenance-policy.json")
        policy["ai"]["enabled"] = True
        event = load_json("automation/fixtures/issue-opened.json")

        class Response:
            def __enter__(self):
                return self

            def __exit__(self, *args):
                return False

            def read(self):
                return b'{"status": "incomplete", "output": [{"content": [{"type": "output_text", "text": "{\\\"label\\\": \\\"bug\\\", \\\"summary\\\": \\\"Do not use.\\\"}"}]}]}'

        enriched = enrich_plan(
            {"version": 1, "event_key": "test", "actions": [], "notices": []},
            event,
            policy,
            "test-token",
            lambda request, timeout: Response(),
        )
        self.assertEqual([], enriched["actions"])
        self.assertIn("ai_no_valid_suggestion", enriched["notices"])

    def test_protected_plan_skips_ai_transport_and_preserves_actions(self):
        policy = load_json("automation/maintenance-policy.json")
        policy["ai"]["enabled"] = True
        plan = {
            "version": 1,
            "event_key": "protected-001",
            "actions": [{"type": "report", "format": "markdown"}],
            "notices": ["protected_label"],
        }

        def transport(request, timeout):
            self.fail("protected content must not be sent to OpenAI")

        enriched = enrich_plan(
            plan,
            load_json("automation/fixtures/issue-opened.json"),
            policy,
            "test-token",
            transport,
        )

        self.assertEqual(plan["actions"], enriched["actions"])
        self.assertIn("ai_skipped_protected_content", enriched["notices"])


def valid_apply_plan(*actions: dict) -> dict:
    return {
        "version": 1,
        "event_key": "delivery-001",
        "actions": list(actions),
        "notices": [],
    }


def valid_apply_target(**overrides: object) -> dict:
    target = {
        "repository": "owner/repository",
        "number": 17,
        "allowed_actions": ["add_label", "comment", "report", "close_waiting_issue"],
        "allowed_labels": ["bug", "documentation", "needs-review"],
        "request_details_marker": "marker:v1",
        "required_issue_sections": ["details"],
        "max_mutations": 2,
        "stale_enabled": True,
    }
    target.update(overrides)
    return target


class FakeGitHubClient:
    def __init__(self, markers: set[str] | None = None):
        self.markers = markers or set()
        self.calls = []

    def has_marker(self, repository, number, marker):
        self.calls.append(("has_marker", repository, number, marker))
        return marker in self.markers

    def add_labels(self, repository, number, labels):
        self.calls.append(("add_labels", repository, number, labels))

    def create_comment(self, repository, number, body):
        self.calls.append(("create_comment", repository, number, body))

    def close_issue(self, repository, number):
        self.calls.append(("close_issue", repository, number))


class ApplyPlanTests(unittest.TestCase):
    def test_applies_allowlisted_actions_and_keeps_report_local(self):
        client = FakeGitHubClient()
        plan = valid_apply_plan(
            {"type": "add_label", "label": "bug"},
            {
                "type": "comment",
                "marker": "marker:v1",
                "body": "<!-- marker:v1 -->\nPlease add: details.",
            },
            {"type": "report", "format": "markdown"},
        )
        target = valid_apply_target(max_mutations=3)

        results = apply_plan(plan, client, target)

        self.assertEqual(
            ["add_labels", "has_marker", "create_comment"],
            [call[0] for call in client.calls],
        )
        self.assertEqual(
            [
                {"type": "add_label", "status": "applied"},
                {"type": "comment", "status": "applied"},
                {"type": "report", "status": "reported"},
            ],
            results,
        )

    def test_existing_marker_skips_comment_after_live_recheck(self):
        client = FakeGitHubClient({"marker:v1"})
        plan = valid_apply_plan(
            {
                "type": "comment",
                "marker": "marker:v1",
                "body": "<!-- marker:v1 -->\nPlease add: details.",
            }
        )

        results = apply_plan(plan, client, valid_apply_target())

        self.assertEqual(["has_marker"], [call[0] for call in client.calls])
        self.assertEqual(
            [{"type": "comment", "status": "skipped_existing_marker"}], results
        )

    def test_unknown_action_rejected_before_any_client_call(self):
        client = FakeGitHubClient()
        plan = valid_apply_plan({"type": "merge_pull_request"})

        with self.assertRaisesRegex(PlanRejected, "unknown action types"):
            apply_plan(plan, client, valid_apply_target())

        self.assertEqual([], client.calls)

    def test_non_string_action_types_are_rejected_before_any_client_call(self):
        for action_type in ([], {}):
            with self.subTest(action_type=action_type):
                client = FakeGitHubClient()

                with self.assertRaisesRegex(PlanRejected, "action type must be a string"):
                    apply_plan(
                        valid_apply_plan({"type": action_type}),
                        client,
                        valid_apply_target(),
                    )

                self.assertEqual([], client.calls)

    def test_disallowed_action_rejected_before_any_client_call(self):
        client = FakeGitHubClient()
        plan = valid_apply_plan({"type": "comment", "marker": "m", "body": "body"})

        with self.assertRaisesRegex(PlanRejected, "unknown action types"):
            apply_plan(plan, client, valid_apply_target(allowed_actions=["report"]))

        self.assertEqual([], client.calls)

    def test_tampered_label_is_rejected_before_any_client_call(self):
        client = FakeGitHubClient()
        plan = valid_apply_plan({"type": "add_label", "label": "maintainer-only"})

        with self.assertRaisesRegex(PlanRejected, "label is not allowed by policy"):
            apply_plan(plan, client, valid_apply_target())

        self.assertEqual([], client.calls)

    def test_tampered_comment_is_rejected_before_any_client_call(self):
        client = FakeGitHubClient()
        plan = valid_apply_plan(
            {"type": "comment", "marker": "other:v1", "body": "arbitrary body"}
        )

        with self.assertRaisesRegex(PlanRejected, "comment is not canonical request-details form"):
            apply_plan(plan, client, valid_apply_target())

        self.assertEqual([], client.calls)

    def test_mutation_budget_rejected_before_any_client_call(self):
        client = FakeGitHubClient()
        plan = valid_apply_plan(
            {"type": "add_label", "label": "bug"},
            {
                "type": "comment",
                "marker": "marker:v1",
                "body": "<!-- marker:v1 -->\nPlease add: details.",
            },
        )

        with self.assertRaisesRegex(PlanRejected, "mutation budget exceeded"):
            apply_plan(plan, client, valid_apply_target(max_mutations=1))

        self.assertEqual([], client.calls)

    def test_malformed_later_action_rejected_before_earlier_mutation(self):
        client = FakeGitHubClient()
        plan = valid_apply_plan(
            {"type": "add_label", "label": "bug"},
            {"type": "comment", "marker": "marker:v1"},
        )

        with self.assertRaisesRegex(PlanRejected, "invalid comment action"):
            apply_plan(plan, client, valid_apply_target())

        self.assertEqual([], client.calls)

    def test_close_requires_all_deterministic_preconditions(self):
        for missing_or_false in ("eligible", "marker_present", "protected"):
            with self.subTest(field=missing_or_false):
                action = {
                    "type": "close_waiting_issue",
                    "eligible": True,
                    "marker_present": True,
                    "protected": False,
                }
                if missing_or_false == "protected":
                    action[missing_or_false] = True
                else:
                    action[missing_or_false] = False
                client = FakeGitHubClient()

                with self.assertRaisesRegex(PlanRejected, "stale close preconditions failed"):
                    apply_plan(valid_apply_plan(action), client, valid_apply_target())

                self.assertEqual([], client.calls)

    def test_disabled_revalidated_stale_policy_rejects_tampered_eligible_close(self):
        client = FakeGitHubClient()
        tampered = valid_apply_plan(
            {
                "type": "close_waiting_issue",
                "eligible": True,
                "marker_present": True,
                "protected": False,
            }
        )

        with self.assertRaisesRegex(PlanRejected, "stale closure disabled by policy"):
            apply_plan(tampered, client, valid_apply_target(stale_enabled=False))

        self.assertEqual([], client.calls)

    def test_protected_close_rejected_before_earlier_label_mutation(self):
        client = FakeGitHubClient()
        plan = valid_apply_plan(
            {"type": "add_label", "label": "bug"},
            {
                "type": "close_waiting_issue",
                "eligible": True,
                "marker_present": True,
                "protected": True,
            },
        )

        with self.assertRaisesRegex(PlanRejected, "stale close preconditions failed"):
            apply_plan(plan, client, valid_apply_target())

        self.assertEqual([], client.calls)

    def test_valid_close_calls_issue_close_once(self):
        client = FakeGitHubClient()
        plan = valid_apply_plan(
            {
                "type": "close_waiting_issue",
                "eligible": True,
                "marker_present": True,
                "protected": False,
            }
        )

        results = apply_plan(plan, client, valid_apply_target())

        self.assertEqual([("close_issue", "owner/repository", 17)], client.calls)
        self.assertEqual([{"type": "close_waiting_issue", "status": "applied"}], results)

    def test_malformed_plan_is_rejected_before_client_call(self):
        client = FakeGitHubClient()

        with self.assertRaisesRegex(PlanRejected, "plan actions must be a list"):
            apply_plan({"version": 1, "event_key": "x", "actions": {}}, client, valid_apply_target())

        self.assertEqual([], client.calls)


class GitHubRestClientTests(unittest.TestCase):
    class Response:
        def __init__(self, payload, link=""):
            self.payload = json.dumps(payload).encode("utf-8")
            self.headers = {"Link": link}

        def __enter__(self):
            return self

        def __exit__(self, *args):
            return False

        def read(self):
            return self.payload

    def test_marker_lookup_follows_pagination(self):
        requests = []
        responses = iter(
            [
                self.Response(
                    [{"body": "first"}],
                    '<https://api.github.com/repos/owner/repository/issues/17/comments?per_page=100&page=2>; rel="next"',
                ),
                self.Response([{"body": "contains marker:v1"}]),
            ]
        )

        def transport(request, timeout):
            requests.append(request)
            return next(responses)

        client = GitHubRestClient("secret-token", transport=transport)

        self.assertTrue(client.has_marker("owner/repository", 17, "marker:v1"))
        self.assertEqual(2, len(requests))
        self.assertTrue(all(request.get_method() == "GET" for request in requests))

    def test_mutation_methods_use_only_issue_metadata_endpoints(self):
        requests = []

        def transport(request, timeout):
            requests.append(request)
            return self.Response({})

        client = GitHubRestClient("secret-token", transport=transport)
        client.add_labels("owner/repository", 17, ["bug"])
        client.create_comment("owner/repository", 17, "body")
        client.close_issue("owner/repository", 17)

        self.assertEqual(["POST", "POST", "PATCH"], [item.get_method() for item in requests])
        self.assertEqual(
            [
                "https://api.github.com/repos/owner/repository/issues/17/labels",
                "https://api.github.com/repos/owner/repository/issues/17/comments",
                "https://api.github.com/repos/owner/repository/issues/17",
            ],
            [item.full_url for item in requests],
        )
        self.assertEqual({"labels": ["bug"]}, json.loads(requests[0].data))
        self.assertEqual({"body": "body"}, json.loads(requests[1].data))
        self.assertEqual({"state": "closed"}, json.loads(requests[2].data))


class ApplyCliTests(unittest.TestCase):
    def write_json(self, directory: str, name: str, value: dict) -> Path:
        path = Path(directory) / name
        path.write_text(json.dumps(value), encoding="utf-8")
        return path

    def test_malformed_policy_fails_before_client_construction(self):
        with tempfile.TemporaryDirectory() as directory:
            plan_path = self.write_json(directory, "plan.json", valid_apply_plan())
            policy_path = self.write_json(directory, "policy.json", {"version": 1})
            with patch("automation.oss_maintainer.GitHubRestClient") as client_class:
                with self.assertRaisesRegex(PlanRejected, "invalid policy"):
                    main(
                        [
                            "apply", "--plan", str(plan_path), "--policy", str(policy_path),
                            "--repository", "owner/repository", "--target-number", "17",
                        ]
                    )
            client_class.assert_not_called()

    def test_malformed_plan_fails_before_client_construction(self):
        with tempfile.TemporaryDirectory() as directory:
            plan_path = self.write_json(directory, "plan.json", {"version": 1, "actions": {}})
            policy_path = self.write_json(
                directory, "policy.json", load_json("automation/maintenance-policy.json")
            )
            with patch("automation.oss_maintainer.GitHubRestClient") as client_class:
                with self.assertRaisesRegex(PlanRejected, "plan actions must be a list"):
                    main(
                        [
                            "apply", "--plan", str(plan_path), "--policy", str(policy_path),
                            "--repository", "owner/repository", "--target-number", "17",
                        ]
                    )
            client_class.assert_not_called()

    def test_disabled_stale_policy_rejects_tampered_close_before_client_construction(self):
        with tempfile.TemporaryDirectory() as directory:
            plan_path = self.write_json(
                directory,
                "plan.json",
                valid_apply_plan(
                    {
                        "type": "close_waiting_issue",
                        "eligible": True,
                        "marker_present": True,
                        "protected": False,
                    }
                ),
            )
            policy_path = self.write_json(
                directory, "policy.json", load_json("automation/maintenance-policy.json")
            )
            with patch("automation.oss_maintainer.GitHubRestClient") as client_class:
                with self.assertRaisesRegex(PlanRejected, "stale closure disabled by policy"):
                    main(
                        [
                            "apply", "--plan", str(plan_path), "--policy", str(policy_path),
                            "--repository", "owner/repository", "--target-number", "17",
                        ]
                    )
            client_class.assert_not_called()

    def test_target_number_must_be_positive(self):
        with redirect_stderr(io.StringIO()):
            with self.assertRaises(SystemExit):
                main(
                    [
                        "apply", "--plan", "plan.json", "--policy", "policy.json",
                        "--repository", "owner/repository", "--target-number", "0",
                    ]
                )
