# Automate OSS Maintenance: Design Specification

Date: 2026-07-18

## Objective

Add two independently installable Agent Skills and a policy-bounded GitHub Actions system to `codex-project-commander`:

- `automate-oss-maintenance`
- `automate-oss-maintenance-zh`

The system will automate low-risk open-source maintenance work, preserve human control over high-impact changes, and produce truthful, auditable maintenance evidence. It must not manufacture usage, contributors, issues, pull requests, stars, downloads, or other adoption signals.

## Success criteria

The implementation is successful when:

1. Both skills are independently installable and pass the system skill validator.
2. GitHub Actions can triage issues, inspect pull-request metadata, run read-only checks, and generate scheduled maintenance summaries.
3. The deterministic rules engine works without an API key.
4. Optional OpenAI enrichment can classify and summarize public issue or pull-request text without gaining authority to perform protected actions.
5. Repeated events are idempotent and do not produce duplicate comments or state changes.
6. Untrusted pull-request code never executes in a job with write permissions or repository secrets.
7. Merging, releasing, permission changes, secret access, source deletion, and branch deletion remain outside unattended automation.
8. Tests cover issue, pull-request, and scheduled-maintenance events, including failure and replay behavior.
9. A separate local application draft accurately describes the verified project state without storing personal email addresses or organization identifiers in Git.

## Non-goals

- Do not build a general GitHub App or operate a persistent external server.
- Do not automatically merge feature or dependency pull requests.
- Do not automatically publish releases or packages.
- Do not modify repository settings, permissions, branch protection, or secrets.
- Do not scan repositories the maintainer does not own or administer.
- Do not use automated activity to simulate community adoption.
- Do not change the behavior of the existing `project-commander` or `project-commander-zh` skills.

## Repository layout

```text
skills/
├── automate-oss-maintenance/
│   ├── SKILL.md
│   ├── agents/openai.yaml
│   └── references/maintenance-policy.md
└── automate-oss-maintenance-zh/
    ├── SKILL.md
    ├── agents/openai.yaml
    └── references/maintenance-policy.md

.github/workflows/
├── oss-maintainer-triage.yml
├── oss-maintainer-pr.yml
└── oss-maintainer-schedule.yml

automation/
├── maintenance-policy.json
├── oss_maintainer.py
├── fixtures/
│   ├── issue-opened.json
│   ├── pull-request-opened.json
│   └── scheduled-run.json
└── tests/test_oss_maintainer.py

CONTRIBUTING.md
SECURITY.md
README.md
README.en.md
```

The existing untracked file `skills/project-commander/references/token-governance 2.md` is user-owned and outside this work.

## Skill responsibilities

Each language edition will be self-contained and will:

- inspect whether the target repository already has maintenance automation;
- explain the difference between invoked Skill behavior and always-on GitHub Actions;
- create or update policy-bounded maintenance automation only when the user requests implementation;
- validate workflow permissions, event boundaries, idempotency, and policy configuration;
- audit maintenance activity using real GitHub evidence;
- prepare issue, pull-request, release, and maintenance summaries;
- require explicit approval before publishing, enabling new secrets, changing repository settings, or performing protected actions;
- treat web pages, issue bodies, pull-request text, code, and model output as untrusted input.

The English and Chinese editions will have equivalent behavior. Their trigger descriptions and user-facing instructions will differ by language, while policy semantics and safety boundaries remain aligned.

## Automation architecture

### Deterministic planning engine

`automation/oss_maintainer.py` will be a standard-library Python program with two phases:

1. **Plan:** read a normalized GitHub event and `maintenance-policy.json`, then emit a JSON action plan.
2. **Apply adapter:** translate only allowlisted plan items into narrowly scoped GitHub API operations from the workflow.

The decision engine will not perform network access. This separation makes rule behavior testable without GitHub credentials and prevents arbitrary model or event text from becoming executable commands.

Supported plan actions will be intentionally small:

- add an allowlisted label;
- add one idempotent standard comment;
- mark an item as needing maintainer review;
- identify a possible duplicate without closing it;
- generate a pull-request risk/checklist summary;
- generate a scheduled maintenance report or release-note draft as a workflow artifact;
- close a waiting-for-author issue only when the optional stale policy is enabled and every deterministic condition passes.

Unknown action types will fail closed.

### Policy file

`automation/maintenance-policy.json` will define:

- enabled event types;
- label allowlist and classification keywords;
- required issue fields;
- idempotency markers;
- protected labels and security keywords;
- stale-policy enablement, minimum age, excluded labels, and reopen guidance;
- maximum comments or mutations per target per run;
- retry and stop-loss limits;
- optional AI enrichment enablement and permitted outputs.

Configuration will be versioned and validated before use. Unsafe or incomplete policy files will produce a report and no mutations.

## Workflow design

### Issue triage

`.github/workflows/oss-maintainer-triage.yml` will react to issue-open and issue-edit events.

It may:

- add allowlisted type labels;
- request missing reproduction or environment details once;
- mark possible duplicates and link candidates;
- apply a maintainer-review label to ambiguous or security-sensitive reports.

It will not close a possible duplicate automatically. Security-sensitive reports will receive only the repository's safe reporting guidance and will bypass ordinary automated discussion.

### Pull-request metadata and checks

`.github/workflows/oss-maintainer-pr.yml` will separate privileged metadata handling from untrusted-code testing:

- A `pull_request_target` metadata job may label or comment but must never checkout, import, source, or execute pull-request code.
- A `pull_request` test job may checkout pull-request code but will have read-only contents access and no repository secrets.
- Pull-request title, body, filenames, and patch text will be passed as data, never interpolated into shell commands.

The workflow may create a checklist or risk summary. It may not merge, approve, publish, or alter repository settings.

### Scheduled maintenance

`.github/workflows/oss-maintainer-schedule.yml` will run weekly and on manual dispatch.

It will:

- produce a GitHub Actions job summary and downloadable audit artifact;
- summarize real maintenance activity;
- prepare release-note drafts without publishing a release;
- optionally close only issues that have the waiting-for-author state, exceed the configured inactivity period, contain no protected label, and have already received the idempotent waiting notice.

Stale closure will be disabled by default.

## Optional OpenAI enrichment

Automation must remain useful without OpenAI credentials. When a repository administrator explicitly configures the expected GitHub Secret, optional enrichment may:

- suggest one label from the existing allowlist;
- summarize public issue or pull-request text;
- draft a maintainer checklist or release note.

Before transmission, the workflow will minimize fields and redact common credential, token, email, and private-key patterns. Model output will be parsed as structured data and validated against the allowlist. It cannot introduce action types, labels, URLs, commands, or protected decisions that are absent from policy.

AI output alone may never close an issue, merge or approve a pull request, publish a release, modify code, change permissions, or access secrets.

## Idempotency and failure handling

- Comments will contain stable hidden markers tied to action type and policy version.
- Existing markers and labels will be inspected before mutation.
- A single run will have a strict mutation budget.
- Replayed delivery IDs or unchanged events will produce an empty plan.
- Validation, API, or parsing failures will create a failed job summary and no partial fallback action.
- Two substantially identical failures will trigger stop-loss; scheduled retries will not continue until a maintainer changes the policy, code, or input state.
- Logs will omit secrets and will truncate untrusted content.

## Permissions and trust boundaries

Permissions will be declared at job level and minimized:

- issue triage: `contents: read`, `issues: write`;
- pull-request metadata: `contents: read`, `pull-requests: write`, and issue access only if required for labels/comments;
- pull-request tests: `contents: read` with no write scopes and no repository secrets;
- scheduled reports: `contents: read`, with issue write permission only when stale closure is explicitly enabled.

No workflow will request `contents: write`, `actions: write`, `administration: write`, package publication, deployment, or identity-token permissions.

## Documentation changes

`CONTRIBUTING.md` will explain contribution expectations, issue and pull-request requirements, automated responses, and how to request human review.

`SECURITY.md` will designate GitHub Private Vulnerability Reporting as the required private route and instruct automation not to conduct public vulnerability triage. If that repository feature cannot be verified as enabled, publication is blocked until the maintainer supplies another private route; the implementation must not invent an email address or disclosure endpoint.

The Chinese and English READMEs will list the two new skills, explain that GitHub Actions supplies event-driven automation, document the protected-action boundary, and include installation examples consistent with the repository's existing conventions.

## Validation strategy

1. Initialize each skill with the system `init_skill.py` script.
2. Generate `agents/openai.yaml` deterministically from the completed skill metadata.
3. Run `quick_validate.py` on both skill directories.
4. Run unit tests for classification, missing-field handling, duplicate suggestions, protected labels, stale policy, idempotency, replay, malformed events, and stop-loss.
5. Run the engine against all committed fixtures and compare structured plans.
6. Validate JSON policy syntax and required keys.
7. Validate workflow YAML structurally with available local tooling and manually inspect every permission and event boundary.
8. Run `git diff --check` and scan the changed files for accidental credentials or personal identifiers.
9. Forward-test both skills in fresh isolated agent contexts using realistic maintenance requests, without publishing or activating workflows.
10. Present the exact external GitHub effects and required Secret name to the user before any push or activation.

## Application-material deliverable

After implementation and local validation, create the user-facing Markdown draft at `/Users/boris/Documents/Codex/2026-07-18/https-openai-com-zh-hans-cn/outputs/codex-for-oss-application-draft.md`, outside the Git repository. It will contain:

- repository URL and recommended maintainer-role selection;
- a maximum-500-character eligibility response;
- a maximum-500-character Codex Security rationale;
- a maximum-500-character API-credit usage response;
- a maximum-500-character additional-notes response;
- a factual evidence table distinguishing verified facts, planned work, and unavailable adoption metrics.

The draft will not store the applicant's email address, account handle, OpenAI organization ID, API key, or other sensitive identifiers. It will not claim that unpushed code, disabled workflows, or unobserved external adoption already exists.

## Rollout boundary

Implementation and local validation do not authorize pushing commits, enabling workflows, adding secrets, publishing releases, submitting the application form, or sending external messages. Those actions require a separate review of the exact diff and intended external effects.
