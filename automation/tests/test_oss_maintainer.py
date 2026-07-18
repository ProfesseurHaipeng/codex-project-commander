import json
import unittest
from datetime import datetime, timezone
from pathlib import Path

from automation.oss_maintainer import (
    build_openai_request,
    build_plan,
    enrich_plan,
    parse_openai_result,
    redact_public_text,
    validate_ai_suggestion,
    validate_policy,
)


ROOT = Path(__file__).resolve().parents[2]


def load_json(relative: str) -> dict:
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


class PolicyTests(unittest.TestCase):
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

    def test_malformed_issue_returns_no_actions(self):
        event = load_json("automation/fixtures/issue-opened.json")
        event["issue"] = []
        plan = build_plan(event, self.policy, self.now)
        self.assertEqual([], plan["actions"])
        self.assertIn("malformed_issue", plan["notices"])

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


class AiBoundaryTests(unittest.TestCase):
    def test_redacts_common_sensitive_patterns(self):
        source = (
            "email person@example.com token sk-example123 "
            "-----BEGIN PRIVATE KEY----- secret -----END PRIVATE KEY-----"
        )
        redacted = redact_public_text(source)
        self.assertNotIn("person@example.com", redacted)
        self.assertNotIn("sk-example123", redacted)
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
