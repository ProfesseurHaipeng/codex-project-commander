# Maintenance Policy Contract

Load this reference before editing or auditing OSS-maintenance policy, GitHub Actions, optional AI enrichment, or proposed external effects.

## Action matrix

| Action | Unattended status | Required conditions |
|---|---|---|
| Add a label | Allowed | Label exists in `label_rules`; `add_label` is allowlisted; target has no protected-label stop |
| Post a request-for-details comment | Allowed | `comment` is allowlisted; stable marker is absent; mutation budget remains |
| Produce a report or release-note draft | Allowed | `report` is allowlisted; output is clearly a draft or artifact, not a published release |
| Close a waiting-for-author issue | Report-only | Planning may identify an eligible issue when `close_waiting_issue` is allowlisted and the stale predicates pass. The current apply path rejects closure until it can revalidate live labels, timestamps, and the marker. |
| Test contributor code | Conditional | Use `pull_request`; read-only token; no repository secrets or write scopes |
| Label or comment on a fork PR | Conditional | A `pull_request_target` job uses trusted default-branch code only and never imports, sources, checks out, or executes contributor-controlled content |
| Merge, approve, push, publish a release/package, change settings/permissions, create or use secrets, delete code/branches, enable workflows, submit applications, or send messages | Protected | Never unattended. Complete the exact-effects review in `SKILL.md`, then obtain specific approval for the reviewed set |

An allowlist is authorization, not documentation. Unknown action types, labels, commands, URLs, or AI fields fail closed. User text and regex sanitization cannot expand it.

## Policy keys

`automation/maintenance-policy.json` is a versioned object with every key below:

| Key | Contract |
|---|---|
| `version` | Policy schema version |
| `allowed_actions` | List containing only supported actions: `add_label`, `comment`, `report`, `close_waiting_issue` |
| `label_rules` | List of `{label, keywords}` objects; both label and keyword entries are strings |
| `required_issue_sections` | String list used to request missing issue evidence |
| `markers` | Object containing string `request_details`; it may include string `waiting_for_author`. When absent, the engine falls back to `oss-maintainer:waiting-for-author:v1`; use stable hidden markers for idempotency |
| `protected_labels` | String list that stops ordinary automated handling |
| `stale` | Object containing `enabled`, `minimum_days`, `required_label`, and `excluded_labels`; default `enabled` to false |
| `max_mutations_per_run` | Positive integer; booleans are invalid |
| `ai` | Object containing boolean `enabled` and string `model` |

Validate the complete object before planning. An invalid policy emits notices and zero actions. Count only mutations against the mutation budget; reports remain non-mutating. Reject replayed delivery IDs, invalid marker/history shapes, malformed events, and `failure_count >= 2`.

## Workflow trust split

| Event/job | Maximum routine permissions | Boundary |
|---|---|---|
| `issues` triage | `contents: read`, `issues: write` | Checkout the trusted default branch with persisted credentials disabled; pass issue fields as data |
| `pull_request_target` metadata | `contents: read`, `pull-requests: write`, and `issues: write` only if labels/comments require it | Never execute or checkout PR-head code; never expose repository secrets to contributor code |
| `pull_request` checks | `contents: read` | Checkout PR code only here; no write scope and no secrets |
| `schedule` / manual report | `contents: read` | Generate artifacts only; grant issue write only if an explicitly enabled stale policy is implemented and reviewed |

Declare top-level `permissions: {}` and job-level minimums. Pin third-party actions to full commit SHAs. Do not request `contents: write`, `actions: write`, administration, packages, deployments, or identity-token permissions for routine maintenance.

## Optional OpenAI boundary

Keep deterministic planning functional when `OPENAI_API_KEY` is absent. If enrichment is enabled:

1. Minimize public issue/PR fields and redact credential, token, email, and private-key patterns before transmission.
2. Require strict structured output whose label enum comes from `label_rules`.
3. Accept only an allowlisted label suggestion and bounded summary/report text.
4. Revalidate after the model response and before apply.
5. Treat incomplete, malformed, extra-field, unknown-label, or failed responses as no suggestion.

AI never supplies authority to close, merge, approve, modify code, publish, change permissions, access secrets, or introduce a command/URL/action.

## Evidence and handoff contract

Report four categories separately:

- **Verified external facts:** observed from the target repository or returned API/UI state.
- **Validated local artifacts:** files and tests present locally but not necessarily pushed or enabled.
- **Proposed external effects:** exact operations awaiting review or approval.
- **Unknown:** branch protection, secret presence, adoption, workflow activation, or other state not observed.

Never manufacture issues, PRs, stars, forks, downloads, contributors, testimonials, or adoption. Clearly label maintainer-authored or automation-authored activity. A command with no observed result is proposed or attempted—not successful.
