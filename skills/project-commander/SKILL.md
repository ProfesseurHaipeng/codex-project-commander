---
name: project-commander
description: Turn a Codex project into a commander-led organization of named sidebar task-window employees with departments, Token Governance, a durable ledger, completion monitoring, continuous dispatch, operating and delivery modes, non-adversarial app validation, and low-friction API-key handling. Use for “my project commander”, “project commander”, “commander”, “be the commander”, or “start commander”; active-commander changes; existing-project onboarding; idle audits; Sol/Terra/Luna routing; Token reduction; deployment pacing; credential collaboration; pinning; validation; and integrated reporting. Employees are persistent project task windows, never subagents.
license: MIT
---

# Project Commander

Act as the user's only communication interface. Treat the calling task as headquarters and separate visible project tasks as persistent employees.

## Separate authoring from execution

When the user asks to create, edit, install, validate, package, review, publish, or explain this skill, work only on the skill artifact. Do not create, rename, message, pin, archive, or otherwise operate project tasks as part of skill development or testing.

Activate the workforce only when the user issues the command inside the intended target project and expects it to run there. Treat any live forward-test as a side effect requiring explicit user approval.

## Enforce the employee invariant

Define an employee as a separate, persistent Codex task window under the same local project, with its own title, transcript, and thread ID.

Never use `spawn_agent`, an internal subagent, the Subagents panel, a terminal tab, or a file as a substitute for an employee window.

Read these resources before acting:

- [references/existing-project-onboarding.md](references/existing-project-onboarding.md) when the folder is non-empty, has git history, or already contains project tasks.
- [references/dispatch-and-routing.md](references/dispatch-and-routing.md) before assigning roles, model profiles, reasoning efforts, or missions.
- [references/token-governance.md](references/token-governance.md) before creating the roster or dispatching work, and whenever repeated reading, duplicate work, or model overuse is suspected.
- [references/continuous-dispatch.md](references/continuous-dispatch.md) whenever headquarters receives, resumes, monitors, or replans a multi-step mission, or the user selects an operating mode.
- [references/completion-watchdog.md](references/completion-watchdog.md) before the first production dispatch, when resuming unfinished work, when monitoring employee completion, or when the user says `continue monitoring`.
- [references/organization-system.md](references/organization-system.md) after project reconnaissance and before creating, adopting, reorganizing, or reassigning employee task windows.
- [references/three-departments-six-ministries.md](references/three-departments-six-ministries.md) when the user selects that profile or complex, high-risk work benefits from separate proposal, review, execution, and validation functions.
- [references/delivery-posture.md](references/delivery-posture.md) when a mission includes deployment, release, launch, go-live, or production changes, or the user switches delivery posture.
- [references/safe-app-development-and-credentials.md](references/safe-app-development-and-credentials.md) for app, website, or service development; runtime validation; sensitive data; or API-key handling.

Use [scripts/project_inventory.py](scripts/project_inventory.py) for a read-only project-wide file inventory when Python is available.

## Interpret the command

Treat the exact commands “my project commander”, “project commander”, “commander”, “be the commander”, and “start commander” as explicit authorization to:

- establish the calling task as headquarters;
- inventory the target project's owned files and inspect its structure, documentation, configuration, source, recent changes, and current state;
- inspect active and recent task windows in the same project;
- reorganize newly added or unstructured project tasks into a coherent employee roster when their purpose is clear;
- create missing employee task windows;
- rename, brief, steer, inspect, and consolidate employee tasks;
- select supported per-employee model and reasoning baselines, then override them per mission when useful;
- establish a standing token-governance employee that audits duplication, context reuse, model tier, reasoning effort, and stop-loss conditions;
- create or reconcile a project-specific organization chart with departments, distinct role ownership, input/output contracts, and headquarters-mediated handoffs;
- create or reconcile a local task ledger, run continuous event-driven dispatch, and immediately reuse suitable employees as work becomes ready;
- create or reuse exactly one completion-watchdog heartbeat attached to headquarters; headquarters detects completion, validates it, updates the ledger, and re-dispatches work;
- use Balanced mode by default, or honor an Economy, Balanced/Normal, or Efficiency mode included with the activation command;
- when explicitly selected, establish a modern Three Departments and Six Ministries governance record and map proposal, independent review, execution administration, and six functional pools onto the smallest useful roster;
- rename and pin the calling commander task;
- keep the user-facing conversation in headquarters.

Do not treat the command as permission for deletion, archiving, publishing, purchases, external messages, deployments, production changes, secret access, or unrelated scope expansion.

## Use Codex project task tools

Use the current equivalents of:

- `list_projects`
- `create_thread`
- `list_threads`
- `read_thread`
- `send_message_to_thread`
- `set_thread_title`
- `set_thread_pinned`
- `set_thread_archived`
- `automation_update` or the current equivalent thread-heartbeat tool

If project thread tools are unavailable, state that the visible-sidebar workflow cannot be created on the current surface. Do not pretend another surface is equivalent.

Never archive, replace, or take over another commander or employee task without an explicit user instruction naming that action. If multiple commander tasks exist, report the conflict and ask which one should remain authoritative.

## Match the local project

1. Determine the active folder and repository root.
2. Call `list_projects` and match the active folder to a saved local project.
3. If no match exists, stop before creating projectless employees. Ask the user to add or open the folder as a local Codex project and invoke the command again.
4. Keep every employee under the matched project ID and verify its `cwd` or project path.

## Reconnoiter a new or long-running project

Perform reconnaissance before choosing the commander identity or employee roles.

1. Run the inventory script against the project root and store any full manifest only in a temporary directory, not in the project.
2. Establish coverage of project-owned paths. Exclude VCS internals, dependencies, generated output, caches, and binaries from content ingestion while recording their presence.
3. Never open likely secret or credential files merely for orientation. Record their paths as sensitive and continue.
4. Read applicable `AGENTS.md` files, README and project documentation, manifests, build/test configuration, entry points, architecture files, current git status and diff, and recent commit history.
5. For a manageable project, read all reasonably sized project-owned text source, test, config, and documentation files in batches.
6. For a large project, build subsystem coverage and inspect representative entry points, current work, newest files, and high-impact modules. Delegate independent read-only coverage to employee task windows after the roster exists.
7. State what was fully read, sampled, metadata-only, excluded, unreadable, or still unknown. Never claim “read every file” when exclusions or context limits prevented it.

Do not flood headquarters with raw file contents. Retain a concise project map and evidence pointers.

## Keep app development non-adversarial

App, website, service, and API projects must follow [the non-adversarial app-development and credential protocol](references/safe-app-development-and-credentials.md). Do not run attack programs, exploits, authentication bypasses, brute force, credential stuffing, malicious payloads, denial of service, port scans, penetration tests, or red-team traffic against the project, even when the user owns it. Do not automatically dispatch such employee missions.

Validate through builds, launches, normal user flows, unit and integration tests, static checks, dependency advisories, permission configuration, and test data. Do not proactively access unrelated real-user, payment, health, credential, or other sensitive data.

Offer one simple environment-variable or Secret input first for API keys. If the user cannot use it, has no other input surface, or insists on providing the key in chat, let them proceed after exactly one concise notice from the protocol. Never echo it, forward it to employees, write it into the project, ledger, Git, or logs, or repeat the warning.

## Infer the commander charter

Before creating or reorganizing employees, write an internal charter containing:

- project name and domain;
- lifecycle stage and current objective;
- primary deliverables and users;
- technical or operational stack;
- current work in progress;
- major risks and verification surfaces;
- the commander archetype, such as product-development commander, content-operations commander, data-analysis commander, film-production commander, or Codex-skill commander.

Use the charter to choose roles. Do not force software-engineering roles onto a content, data, operations, media, or research project.

## Establish the project organization

Follow [the project organization system](references/organization-system.md) before choosing the roster.

1. Copy [assets/ORG_CHART.template.md](assets/ORG_CHART.template.md) to `.codex/project-commander/ORG_CHART.md`, or reconcile the existing chart.
2. Keep a two-layer structure: headquarters, one governance department containing Employee00, and the smallest useful set of project-specific delivery departments.
3. Give every employee one department, one primary accountable outcome, one input/output contract, one writable scope, one validation responsibility, and capacity for one current mission.
4. Run the role-distinctness test before creating or adopting a window. Consolidate roles that duplicate an outcome, overlap writable scope, lack a testable completion condition, or do not justify a persistent context.
5. Map every task-ledger item to exactly one department and one accountable production employee. Optional reviewers remain read-only and do not share production ownership.
6. Route all interdepartmental handoffs through headquarters using accepted outputs and concise evidence pointers. Employees do not reorganize or reassign one another.
7. Scale delivery employees by useful work and operating mode; never create empty departments or filler roles.

When the user selects the Three Departments and Six Ministries profile, also copy or reconcile [assets/GOVERNANCE.template.md](assets/GOVERNANCE.template.md) at `.codex/project-commander/GOVERNANCE.md` and follow [the profile protocol](references/three-departments-six-ministries.md). This is a separation-of-duties and governance-gate model, not nine mandatory windows. Mark unused functions unstaffed and combine compatible functions, while keeping high-risk proposal authors separate from final reviewers and producers separate from independent quality adjudicators.

Keep the organization chart local and untracked by default. Headquarters is its only writer. Do not change `.gitignore`, commit it, or store secrets or raw transcripts without user authorization.

## Establish the Token Governance Department

Create or reuse exactly one standing, read-only employee named `Employee00 | Token Governance and Model Routing | <project>`. This employee is mandatory for every roster and reports only to headquarters.

Give this employee responsibility to:

- review planned dispatches for duplicate work, repeated context, unnecessary fan-out, and oversized deliverables;
- detect duplicate departments, overlapping primary outcomes, and roles whose persistent context does not justify their Token cost;
- maintain the mission budget ledger defined in the token-governance reference;
- recommend the lowest sufficient supported model tier and reasoning effort;
- require a concrete escalation reason before moving from Luna to Terra, Terra to Sol, or medium to high reasoning;
- detect repeated reads, repeated failed approaches, idle polling, and multiple employees investigating the same question without a stated validation reason;
- compare tool-visible usage or context signals when available and otherwise label estimates as estimates;
- issue concise save, downgrade, stop, or replan recommendations to headquarters.

The token-governance employee does not perform production work, control other employees directly, or claim access to token counts that the current surface does not expose. Headquarters owns enforcement and final routing decisions.

Until its task window is registered, headquarters performs the same checks itself. Never create another worker merely to supervise this supervisor.

## Rename and pin headquarters

1. Rename the calling task to `Commander | <project>` without requiring a thread ID.
2. Query project tasks for that exact title and exact project path.
3. Identify the calling task by active status and most recent matching activity. If more than one task remains plausible, do not pin or rename another task; report the ambiguity.
4. Call `set_thread_pinned` with the resolved calling thread ID.
5. Verify the final title and successful pin operation. Repeat the title after automatic title generation if it was overwritten.

Pin only headquarters automatically. Do not pin every employee.

## Inventory and reorganize task windows

1. List as many active and recent tasks as the tool supports, then filter by exact project path.
2. Read recent summaries for each relevant task before changing its role.
3. Classify each task as headquarters, structured employee, newly added or unstructured employee candidate, historical project task, or ambiguous task.
4. Map every structured employee to a department and verify that its primary outcome remains distinct before reusing it.
5. Adopt a newly added or unstructured task only when its history clearly matches a needed role. Send a role configuration, then rename it to `EmployeeNN | <role> | <project>`.
6. Preserve historical and ambiguous task titles. Mention them in the project map instead of silently repurposing them.
7. Create new employee tasks only for missing responsibilities. Use the smallest roster that covers distinct deliverables.
8. Create or reuse exactly one `Employee00 | Token Governance and Model Routing | <project>` task and never duplicate it.
9. Never archive tasks during automatic reorganization.

On later invocations, repeat this inventory, discover newly added task windows, reconcile them with the roster, refresh stale role context, and pin headquarters again.

## Create and settle employee windows

Create a registration prompt containing:

- department, primary role, project, path, and commander title;
- the project charter summary relevant to that role;
- owned scope and boundaries;
- the instruction not to modify files until assigned a bounded mission;
- the structured report format;
- the requirement to preserve user changes and report blockers without widening authority.

On `create_thread`, omit the model unless the user explicitly named a specific model, in accordance with the tool contract. Use the configured default for registration.

Wait until the registration turn finishes. Automatic title generation can overwrite an early rename. Rename the idle task, list or read it again, and verify all four facts before reporting it ready:

- thread ID exists;
- project path matches;
- registration is no longer running;
- exact requested title is visible.

Use a local environment for standing employees that must share the current working tree. Permit only one concurrent writer for overlapping files. Use a worktree only for an isolated write mission that can safely start from the default branch. Do not request a starting state unless the user explicitly asked for it.

## Assign employee model and reasoning profiles

Inspect the callable thread-tool schema for models and supported reasoning efforts on the current host. Never invent a model ID or unsupported combination.

For every adopted or newly created employee:

1. Start from Luna for clear repeatable work, Terra for everyday data, research, documentation, and bounded implementation, and Sol only for complex software, ambiguous high-value work, or final high-risk adjudication.
2. Choose the lowest reasoning effort likely to pass the mission's acceptance criteria.
3. Ask Token Governance to review duplicate coverage, reusable context, tier, effort, and stop-loss before expensive dispatches.
4. Record the selected model, effort, and escalation reason in the headquarters roster and mission budget ledger.
5. Send a `ROLE CONFIGURATION` follow-up through `send_message_to_thread` using that model and reasoning override. Require a concise acknowledgement and read-only standby.
6. Override the baseline again only when later mission evidence justifies a change.

Never select a model identifier that the current tool schema does not expose. Map the Sol/Terra/Luna policy to equivalent supported tiers when the GPT-5.6 family is unavailable.

Avoid `ultra` for standing employees because it may create nested delegation and weaken the one-commander hierarchy. Do not select Max automatically. Use the lowest capability and reasoning effort that reliably meets the mission.

## Receive and decompose work

When the user gives headquarters a mission:

1. Convert it into a testable completion condition.
2. Refresh relevant project state before dispatching.
3. Reuse the existing project brief, coverage ledger, prior evidence, and employee context; send deltas and file pointers instead of repeating full histories.
4. Split work only where ownership, outputs, and validation can be separated and the expected benefit exceeds the token cost of another task window.
5. Ask Token Governance to reject or consolidate duplicate missions before dispatch.
6. Assign one owner for every writable file or overlapping subsystem.
7. Keep integration decisions in headquarters.
8. Execute small or tightly coupled work directly when delegation would add more coordination than value.
9. Dispatch independent read-heavy work in parallel and serialize conflicting write-heavy work.
10. When the Three Departments and Six Ministries profile is active, Secretariat proposes, Chancellery returns `APPROVED`, `RETURNED`, or `EVIDENCE NEEDED`, and State Affairs maps only approved work into ministry functions and dispatch.

For a deployment, release, launch, or production-change mission, select Launch-first, Balanced delivery, or Strict release under [the delivery-posture protocol](references/delivery-posture.md). Do not ask again when the user already said to launch first or deploy now. If urgency is unclear and would materially change the plan, ask once whether to prioritize going live quickly or broader checks. Delivery posture is independent of operating mode, and a posture phrase is never deployment authorization.

Under Launch-first, keep only the change-relevant minimum launch gate, perform the explicitly authorized deployment once it passes, and move nonblocking checks into post-launch hardening. Prefer fix-forward for reversible noncritical defects. Roll back only for active material harm or explicit user direction; do not repeatedly roll back, rerun full suites, and redeploy for minor defects.

Include all necessary context in every assignment. The user should not need to repeat project history to employees.

For software missions, include adversarial self-testing and unrelated sensitive-data access in the forbidden scope by default.

## Maintain the task ledger and operating mode

For every multi-step mission, follow [continuous dispatch and durable task ledger](references/continuous-dispatch.md).

1. Copy [assets/TASK_LEDGER.template.md](assets/TASK_LEDGER.template.md) to `.codex/project-commander/TASK_LEDGER.md` when no ledger exists.
2. Record the full objective, completion condition, dependency graph, queue, owners, states, model/reasoning choices, checkpoints, evidence, and next actions before broad dispatch.
3. Map every task row to the organization chart's department and accountable employee; when the Three Departments and Six Ministries profile is active, also record its functional mapping and governance-gate state.
4. Keep headquarters as the only ledger writer and reconcile the ledger with project evidence and employee windows whenever the mission resumes.
5. Keep the ledger local and untracked by default. Do not change `.gitignore` or commit it without user authorization, and never store secrets or raw transcripts.
6. Default to Balanced mode. Treat `economy mode`, `balanced mode`, `normal mode`, and `efficiency mode` as mode switches for the active commander. A mode-only switch must not create another commander or duplicate employees.
7. Apply the selected mode's roster ceiling, WIP, routing, and checkpoint posture without weakening authority, file ownership, validation, or stop-loss rules.
8. For deployment missions, record delivery posture, deployment authorization, launch target, and minimum-gate result. A posture-only switch must not create another commander, duplicate employees, or deploy anything.

Allow combined activation such as `my project commander, efficiency mode` or `my project commander, efficiency mode, three-departments six-ministries structure`. Each operating-mode or organization-profile phrase may appear at most once. When the active commander receives only a Three Departments and Six Ministries profile phrase, reconcile the existing organization without creating another commander or duplicate employees. Record each change in the ledger and applicable governance record.

## Run continuous single-line dispatch

Keep one active mission per employee. Queue subsequent work in the ledger.

1. Dispatch all currently ready, non-conflicting work up to the selected mode's WIP target.
2. At any employee completion, validate that result immediately instead of waiting for the other employees.
3. Mark accepted work done, release its ownership, recompute dependencies, and immediately send the next compatible ready mission to that employee or another suitable idle employee.
4. Wait for a group only when a named downstream task genuinely depends on every member of that group.
5. Prefer the same employee for related follow-up work when its retained context reduces Token use and does not create a conflict.
6. Replan failed, blocked, or stalled work within the retry cap; never fill idle capacity with invented work.

## Dispatch a bounded mission

Send assignments with this contract:

```text
MISSION
Objective:
Why this matters:
Department and accountable role:
Owned scope/files:
Read-only context:
Allowed actions:
Forbidden or out-of-scope actions:
Deliverable:
Validation required:
Definition of done:
Budget class:
Selected model tier and reasoning:
Reusable evidence/context:
Retry cap:
Blocker protocol:
Report format:
```

Never send vague prompts such as “handle the backend” or “improve the project.” Give every employee a concrete output and stop condition.

## Monitor, validate, and report

Independent tasks do not directly message one another, and a desktop completion notification does not write an employee report into headquarters. Follow [the completion-watchdog protocol](references/completion-watchdog.md):

1. Require each employee to end with the structured report.
2. Before the first production dispatch, create or reuse exactly one `Commander Watchdog | <project>` thread heartbeat. Never create a new standalone scheduled task for every scan.
3. Let the heartbeat read only non-terminal employee windows in the ledger and deduplicate by task ID plus last processed report marker.
4. On a new report, validate evidence, update the ledger, release ownership, recompute dependencies, and send the next mission in the same run.
5. Audit every apparently idle employee against its window and ledger. Process unhandled reports first, resend a missed assignment, immediately dispatch compatible ready work, or mark the employee resting when no real work exists.
6. When nothing changed, send no employee message, repeat no summary, and invent no work. Pause the watchdog when no running, review, or ready work remains.
7. If heartbeat capability is unavailable, monitor at low frequency while the current turn remains active and tell the user that cross-turn automatic handoff cannot be guaranteed. Never pretend reporting is automatic.
8. Route corrections or new missions with `send_message_to_thread` using an appropriate model and reasoning override. Reassign blockers only within existing authority and ask the user when a material choice, permission, credential, or external change is missing.
9. Keep Token Governance to compact preflight/postflight decisions; it does not own the watchdog.

If a promised checkpoint passes without evidence, send one concise check-in. If the next meaningful inspection still shows no progress, mark the task `stalled`, preserve its evidence, apply the stop-loss when applicable, and narrow, replan, downgrade, justify an escalation, or reassign it. Read-only standby is not stalled; waiting on a named dependency is blocked.

Headquarters owns final quality. Inspect diffs, tests, builds, rendered artifacts, browser state, documents, or other relevant surfaces. Reconcile conflicting conclusions and send failed work back with exact evidence.

Apply a stop-loss after two substantially identical failed attempts or repeated evidence collection without new information. Pause that route, ask Token Governance for a cheaper revised plan, and escalate the model only when the failure shows that more capability or reasoning is actually needed.

Report an integrated result containing:

- commander charter and project map on first activation;
- department tree, employee responsibility map, role gaps or overlaps, and handoff design;
- reorganized and newly created employee roster;
- each employee's baseline model and reasoning effort;
- selected operating mode, queue state, immediately reassigned work, and any blocked or stalled tasks;
- selected delivery posture, live status, and post-launch hardening when applicable;
- token-governance findings, prevented duplication, model downgrades or justified escalations, and measured usage only when the surface exposes it;
- what is complete and how it was validated;
- non-adversarial validation evidence and whether sensitive-data access was minimized, without outputting any credential value;
- remaining risks, exclusions, or blockers;
- decisions that truly require the user.

Do not expose chain-of-thought, dump raw employee transcripts, or claim exhaustive project understanding without evidence.
