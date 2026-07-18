import argparse
import json
import os
import re
import urllib.request
from datetime import datetime, timezone
from pathlib import Path


SUPPORTED_ACTIONS = frozenset({"add_label", "comment", "report", "close_waiting_issue"})
MUTATING_ACTIONS = frozenset({"add_label", "comment", "close_waiting_issue"})
REQUIRED_POLICY_KEYS = frozenset(
    {
        "version",
        "allowed_actions",
        "label_rules",
        "required_issue_sections",
        "markers",
        "protected_labels",
        "stale",
        "max_mutations_per_run",
        "ai",
    }
)


def validate_policy(policy: dict) -> list[str]:
    if not isinstance(policy, dict):
        return ["policy must be an object"]
    errors = [
        f"missing policy key: {key}" for key in sorted(REQUIRED_POLICY_KEYS - policy.keys())
    ]
    allowed_actions = policy.get("allowed_actions", [])
    if not isinstance(allowed_actions, list):
        return errors + ["allowed_actions must be a list"]
    for action in allowed_actions:
        if action not in SUPPORTED_ACTIONS:
            errors.append(f"allowed_actions contains unsupported value: {action}")
    if not isinstance(policy.get("max_mutations_per_run"), int) or policy.get(
        "max_mutations_per_run", 0
    ) < 1:
        errors.append("max_mutations_per_run must be at least 1")
    label_rules = policy.get("label_rules")
    if not isinstance(label_rules, list) or any(
        not isinstance(rule, dict)
        or not isinstance(rule.get("label"), str)
        or not isinstance(rule.get("keywords"), list)
        or not all(isinstance(keyword, str) for keyword in rule.get("keywords", []))
        for rule in label_rules or []
    ):
        errors.append("label_rules must contain label and keyword list entries")
    if not isinstance(policy.get("required_issue_sections"), list) or not all(
        isinstance(section, str) for section in policy.get("required_issue_sections", [])
    ):
        errors.append("required_issue_sections must be a list")
    if not isinstance(policy.get("protected_labels"), list) or not all(
        isinstance(label, str) for label in policy.get("protected_labels", [])
    ):
        errors.append("protected_labels must be a list")
    if not isinstance(policy.get("markers"), dict) or not isinstance(
        policy.get("markers", {}).get("request_details"), str
    ):
        errors.append("markers.request_details must be a string")
    stale = policy.get("stale")
    stale_keys = {"enabled", "minimum_days", "required_label", "excluded_labels"}
    if not isinstance(stale, dict) or stale_keys - stale.keys():
        errors.append("stale policy is incomplete")
    elif (
        not isinstance(stale["enabled"], bool)
        or not isinstance(stale["minimum_days"], int)
        or stale["minimum_days"] < 0
        or not isinstance(stale["required_label"], str)
        or not isinstance(stale["excluded_labels"], list)
        or not all(isinstance(label, str) for label in stale["excluded_labels"])
    ):
        errors.append("stale policy has invalid values")
    ai = policy.get("ai")
    if not isinstance(ai, dict) or not isinstance(ai.get("enabled"), bool) or not isinstance(
        ai.get("model"), str
    ):
        errors.append("ai policy is incomplete")
    return errors


def build_plan(event: dict, policy: dict, now: datetime) -> dict:
    errors = validate_policy(policy)
    plan = {
        "version": 1,
        "event_key": event.get("delivery_id", "unknown") if isinstance(event, dict) else "unknown",
        "actions": [],
        "notices": errors.copy(),
    }
    if errors:
        return plan
    if not isinstance(event, dict):
        plan["notices"].append("event must be an object")
        return plan

    context = event.get("context", {})
    if not isinstance(context, dict):
        plan["notices"].append("event context must be an object")
        return plan
    failure_count = context.get("failure_count", 0)
    if not isinstance(failure_count, int) or isinstance(failure_count, bool):
        plan["notices"].append("event context has invalid failure_count")
        return plan
    if failure_count >= 2:
        plan["notices"].append("stop_loss")
        return plan
    processed_delivery_ids = context.get("processed_delivery_ids", [])
    if not isinstance(processed_delivery_ids, list) or not all(
        isinstance(delivery_id, str) for delivery_id in processed_delivery_ids
    ):
        plan["notices"].append("event context has invalid processed_delivery_ids")
        return plan
    if event.get("delivery_id") in set(processed_delivery_ids):
        plan["notices"].append("replayed_delivery")
        return plan

    event_name = event.get("event_name")
    existing_markers = context.get("existing_markers", [])
    if not isinstance(existing_markers, list) or not all(
        isinstance(marker, str) for marker in existing_markers
    ):
        plan["notices"].append("event context has invalid existing_markers")
        return plan
    markers = set(existing_markers)
    if event_name == "issues":
        issue = event.get("issue", {})
        if not isinstance(issue, dict):
            plan["notices"].append("malformed_issue")
            return plan
        labels = _label_names(issue.get("labels", []))
        if labels & set(policy["protected_labels"]):
            plan["notices"].append("protected_label")
            return plan
        text = f"{issue.get('title', '')}\n{issue.get('body', '')}".lower()
        label = next(
            (
                rule["label"]
                for rule in policy["label_rules"]
                if any(keyword.lower() in text for keyword in rule["keywords"])
            ),
            next(
                (
                    rule["label"]
                    for rule in policy["label_rules"]
                    if rule["label"] == "question"
                ),
                None,
            ),
        )
        if label and "add_label" in policy["allowed_actions"] and label not in labels:
            plan["actions"].append({"type": "add_label", "label": label})
        marker = policy["markers"]["request_details"]
        missing = [
            section
            for section in policy["required_issue_sections"]
            if section.lower() not in text
        ]
        if missing and marker not in markers and "comment" in policy["allowed_actions"]:
            plan["actions"].append(
                {
                    "type": "comment",
                    "marker": marker,
                    "body": f"<!-- {marker} -->\nPlease add: {', '.join(missing)}.",
                }
            )
    elif event_name == "pull_request":
        if (
            "add_label" in policy["allowed_actions"]
            and any(rule["label"] == "needs-review" for rule in policy["label_rules"])
        ):
            plan["actions"].append({"type": "add_label", "label": "needs-review"})
    elif event_name == "schedule":
        if "report" in policy["allowed_actions"]:
            plan["actions"].append({"type": "report", "format": "markdown"})
        if _can_close_waiting_issue(event.get("issue", {}), policy, markers, now):
            plan["actions"].append(
                {
                    "type": "close_waiting_issue",
                    "reason": "stale_waiting_for_author",
                }
            )
    plan["actions"] = _within_mutation_budget(
        plan["actions"], policy["max_mutations_per_run"]
    )
    return plan


def _label_names(labels: list[object]) -> set[str]:
    if not isinstance(labels, list):
        return set()
    return {
        label["name"] if isinstance(label, dict) and isinstance(label.get("name"), str) else label
        for label in labels
        if isinstance(label, str) or (isinstance(label, dict) and isinstance(label.get("name"), str))
    }


def _can_close_waiting_issue(
    issue: dict, policy: dict, markers: set[str], now: datetime
) -> bool:
    if not isinstance(issue, dict):
        return False
    stale = policy["stale"]
    if not stale["enabled"] or "close_waiting_issue" not in policy["allowed_actions"]:
        return False
    labels = _label_names(issue.get("labels", []))
    if stale["required_label"] not in labels:
        return False
    if labels & (set(policy["protected_labels"]) | set(stale["excluded_labels"])):
        return False
    waiting_marker = policy["markers"].get(
        "waiting_for_author", "oss-maintainer:waiting-for-author:v1"
    )
    if waiting_marker not in markers:
        return False
    try:
        updated_at = parse_now(issue["updated_at"])
    except (KeyError, TypeError, ValueError):
        return False
    return (now - updated_at).days >= stale["minimum_days"]


def _within_mutation_budget(actions: list[dict], budget: int) -> list[dict]:
    accepted = []
    mutation_count = 0
    for action in actions:
        if action["type"] in MUTATING_ACTIONS:
            if mutation_count >= budget:
                continue
            mutation_count += 1
        accepted.append(action)
    return accepted


REDACTION_PATTERNS = (
    (
        re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"),
        "[REDACTED_EMAIL]",
    ),
    (re.compile(r"\bsk-[A-Za-z0-9_-]{8,}\b"), "[REDACTED_TOKEN]"),
    (
        re.compile(
            r"-----BEGIN [A-Z ]*PRIVATE KEY-----.*?-----END [A-Z ]*PRIVATE KEY-----",
            re.DOTALL,
        ),
        "[REDACTED_PRIVATE_KEY]",
    ),
)


def redact_public_text(value: str) -> str:
    redacted = value
    for pattern, replacement in REDACTION_PATTERNS:
        redacted = pattern.sub(replacement, redacted)
    return redacted[:12000]


def build_openai_request(
    text: str, labels: list[str], model: str = "gpt-5.6"
) -> dict:
    return {
        "model": model,
        "input": [
            {
                "role": "system",
                "content": "Classify public OSS maintenance text. Return only the required schema.",
            },
            {"role": "user", "content": redact_public_text(text)},
        ],
        "text": {
            "format": {
                "type": "json_schema",
                "name": "oss_maintenance_suggestion",
                "strict": True,
                "schema": {
                    "type": "object",
                    "properties": {
                        "label": {"type": "string", "enum": labels},
                        "summary": {"type": "string", "maxLength": 500},
                    },
                    "required": ["label", "summary"],
                    "additionalProperties": False,
                },
            }
        },
    }


def parse_openai_result(response: dict) -> dict:
    if not isinstance(response, dict):
        return {}
    if "status" in response and response["status"] != "completed":
        return {}
    for item in response.get("output", []):
        if not isinstance(item, dict):
            continue
        for content in item.get("content", []):
            if not isinstance(content, dict):
                continue
            if content.get("type") == "output_text":
                try:
                    result = json.loads(content["text"])
                except (KeyError, TypeError, json.JSONDecodeError):
                    return {}
                return result if isinstance(result, dict) else {}
    return {}


def validate_ai_suggestion(suggestion: dict, labels: set[str]) -> list[dict]:
    if not isinstance(suggestion, dict) or set(suggestion) != {"label", "summary"}:
        return []
    if suggestion["label"] not in labels or not isinstance(suggestion["summary"], str):
        return []
    summary = suggestion["summary"].strip()
    if not summary or len(summary) > 500:
        return []
    return [
        {"type": "add_label", "label": suggestion["label"], "source": "ai_suggestion"},
        {"type": "report", "body": summary, "source": "ai_suggestion"},
    ]


def post_openai_response(
    payload: dict, token: str, transport=urllib.request.urlopen
) -> dict:
    request = urllib.request.Request(
        "https://api.openai.com/v1/responses",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
        method="POST",
    )
    with transport(request, timeout=20) as response:
        return json.loads(response.read().decode("utf-8"))


def enrich_plan(
    plan: dict,
    event: dict,
    policy: dict,
    token: str | None,
    transport=urllib.request.urlopen,
) -> dict:
    enriched = {
        **plan,
        "actions": list(plan.get("actions", [])),
        "notices": list(plan.get("notices", [])),
    }
    if validate_policy(policy) or not policy["ai"].get("enabled", False):
        enriched["notices"].append("ai_disabled")
        return enriched
    if not token:
        enriched["notices"].append("ai_unavailable")
        return enriched

    target = event.get("issue") or event.get("pull_request") or {}
    if not isinstance(target, dict):
        enriched["notices"].append("ai_malformed_event")
        return enriched
    source = f"{target.get('title', '')}\n{target.get('body', '')}"
    labels = [rule["label"] for rule in policy["label_rules"]]
    try:
        response = post_openai_response(
            build_openai_request(source, labels, policy["ai"].get("model", "gpt-5.6")),
            token,
            transport,
        )
        suggestions = validate_ai_suggestion(parse_openai_result(response), set(labels))
    except Exception:
        enriched["notices"].append("ai_enrichment_failed")
        return enriched
    if not suggestions:
        enriched["notices"].append("ai_no_valid_suggestion")
        return enriched

    mutation_count = sum(
        action.get("type") in MUTATING_ACTIONS for action in enriched["actions"]
    )
    for action in suggestions:
        if action["type"] not in policy["allowed_actions"]:
            continue
        if action["type"] in MUTATING_ACTIONS:
            if mutation_count >= policy["max_mutations_per_run"]:
                continue
            mutation_count += 1
        enriched["actions"].append(action)
    return enriched


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def parse_now(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00")).astimezone(timezone.utc)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    commands = parser.add_subparsers(dest="command", required=True)
    plan_parser = commands.add_parser("plan")
    plan_parser.add_argument("--event", type=Path, required=True)
    plan_parser.add_argument("--policy", type=Path, required=True)
    plan_parser.add_argument("--event-name", choices=("issues", "pull_request", "schedule"))
    plan_parser.add_argument("--now", required=True)
    plan_parser.add_argument("--output", type=Path, required=True)
    enrich_parser = commands.add_parser("enrich")
    enrich_parser.add_argument("--plan", type=Path, required=True)
    enrich_parser.add_argument("--event", type=Path, required=True)
    enrich_parser.add_argument("--policy", type=Path, required=True)
    enrich_parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)

    if args.command == "plan":
        event = load_json(args.event)
        if args.event_name:
            event["event_name"] = args.event_name
        plan = build_plan(event, load_json(args.policy), parse_now(args.now))
    else:
        plan = enrich_plan(
            load_json(args.plan),
            load_json(args.event),
            load_json(args.policy),
            os.environ.get("OPENAI_API_KEY"),
        )
    args.output.write_text(
        json.dumps(plan, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
