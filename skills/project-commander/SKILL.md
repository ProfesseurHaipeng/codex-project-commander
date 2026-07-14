---
name: project-commander
description: Turn a new or long-running local Codex project into a Project Commander workforce of named sidebar task windows. Use when the user says “my project commander”, “be the project commander”, “start project commander”, “我的总指挥”, or asks Codex to inspect an existing project, understand its files and task history, reorganize current and newly added project tasks into employees, assign supported model and reasoning profiles, pin the commander, dispatch work, validate results, and report through one headquarters task. Employees must be persistent project task windows, never subagents.
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

Use [scripts/project_inventory.py](scripts/project_inventory.py) for a read-only project-wide file inventory when Python is available.

## Interpret the command

Treat the exact commands “my project commander” and “我的总指挥” as explicit authorization to:

- establish the calling task as headquarters;
- inventory the target project's owned files and inspect its structure, documentation, configuration, source, recent changes, and current state;
- inspect active and recent task windows in the same project;
- reorganize newly added or unstructured project tasks into a coherent employee roster when their purpose is clear;
- create missing employee task windows;
- rename, brief, steer, inspect, and consolidate employee tasks;
- select supported per-employee model and reasoning baselines, then override them per mission when useful;
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
4. Reuse healthy structured employees.
5. Adopt a newly added or unstructured task only when its history clearly matches a needed role. Send a role configuration, then rename it to `EmployeeNN | <role> | <project>`.
6. Preserve historical and ambiguous task titles. Mention them in the project map instead of silently repurposing them.
7. Create new employee tasks only for missing responsibilities. Use the smallest roster that covers distinct deliverables.
8. Never archive tasks during automatic reorganization.

On later invocations, repeat this inventory, discover newly added task windows, reconcile them with the roster, refresh stale role context, and pin headquarters again.

## Create and settle employee windows

Create a registration prompt containing:

- role, project, path, and commander title;
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

1. Choose a baseline model profile and reasoning effort from the routing reference according to role, project risk, and expected work.
2. Record the selected model and effort in the headquarters roster.
3. Send a `ROLE CONFIGURATION` follow-up through `send_message_to_thread` using that model and reasoning override. Require a concise acknowledgement and read-only standby.
4. Override the baseline again on later missions when task complexity changes.

Avoid `ultra` for standing employees because it may create nested delegation and weaken the one-commander hierarchy. Use the lowest capability and reasoning effort that reliably meets the mission.

## Receive and decompose work

When the user gives headquarters a mission:

1. Convert it into a testable completion condition.
2. Refresh relevant project state before dispatching.
3. Split work only where ownership, outputs, and validation can be separated.
4. Assign one owner for every writable file or overlapping subsystem.
5. Keep integration decisions in headquarters.
6. Execute small or tightly coupled work directly when delegation would add more coordination than value.
7. Dispatch independent read-heavy work in parallel and serialize conflicting write-heavy work.

Include all necessary context in every assignment. The user should not need to repeat project history to employees.

## Dispatch a bounded mission

Send assignments with this contract:

```text
MISSION
Objective:
Why this matters:
Owned scope/files:
Read-only context:
Allowed actions:
Forbidden or out-of-scope actions:
Deliverable:
Validation required:
Definition of done:
Blocker protocol:
Report format:
```

Never send vague prompts such as “handle the backend” or “improve the project.” Give every employee a concrete output and stop condition.

## Monitor, validate, and report

Independent tasks do not directly message one another. Implement automatic reporting operationally:

1. Require each employee to end with the structured report.
2. Use `read_thread` to inspect progress and completed results.
3. Read at meaningful intervals; do not busy-poll.
4. Route corrections with `send_message_to_thread` using an appropriate model and reasoning override.
5. Reassign a blocker only within existing authority.
6. Ask the user when a missing choice, permission, credential, or external change materially affects the result.

Headquarters owns final quality. Inspect diffs, tests, builds, rendered artifacts, browser state, documents, or other relevant surfaces. Reconcile conflicting conclusions and send failed work back with exact evidence.

Report an integrated result containing:

- commander charter and project map on first activation;
- reorganized and newly created employee roster;
- each employee's baseline model and reasoning effort;
- what is complete and how it was validated;
- remaining risks, exclusions, or blockers;
- decisions that truly require the user.

Do not expose chain-of-thought, dump raw employee transcripts, or claim exhaustive project understanding without evidence.
