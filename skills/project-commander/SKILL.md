---
name: project-commander
description: Create and operate a visible project-task workforce under one commander. Use when the user says “我的总指挥”, “你是总指挥”, “启动总指挥”, or asks for AI employees as named Codex task windows under a local project. Employees must be separate persistent project tasks in the sidebar, never subagents. The commander creates and names those tasks, dispatches work, selects per-turn model and reasoning settings when authorized, reads their reports, validates results, and gives the user one consolidated answer.
---

# Project Commander

Act as the user's only communication interface. Treat the current task as headquarters and visible project tasks as persistent employees.

## Separate authoring from execution

When the user asks to create, edit, install, validate, package, review, or explain this skill, work only on the skill artifact. Do not create, rename, message, pin, archive, or otherwise operate project tasks as part of skill development or testing.

Activate the workforce only when the user issues the command inside the intended target project and asks or expects the command to run there. Treat forward-testing that would create live project tasks as a side effect requiring explicit user approval.

## Enforce the employee invariant

An employee is a separate, persistent Codex project task window created with the project thread-creation tool. It must appear under the same local project in the sidebar and have its own title, transcript, and thread ID.

Never use `spawn_agent`, an internal subagent, the Subagents panel, a terminal tab, or a file as a substitute for an employee window. This distinction is the central requirement of the skill.

Read [references/dispatch-and-routing.md](references/dispatch-and-routing.md) before bootstrapping the team or selecting model and reasoning overrides.

## Interpret the command

Treat the exact command “我的总指挥” as explicit authorization to:

- establish the current task as headquarters;
- create a small set of visible employee tasks under the current local project;
- rename, brief, steer, inspect, and consolidate those employee tasks;
- select per-dispatch model and reasoning overrides from combinations exposed by the current tool schema;
- keep the user-facing conversation in headquarters.

Do not treat this authorization as permission for destructive actions, publishing, purchases, external messages, production changes, secret access, or unrelated scope expansion. Preserve the normal approval boundary for every employee.

## Use the correct execution surface

Use project thread tools for this workflow because the user explicitly wants persistent, visible sidebar task windows. Prefer the current equivalents of:

- `list_projects`
- `create_thread`
- `list_threads`
- `read_thread`
- `send_message_to_thread`
- `set_thread_title`
- `set_thread_archived`

Do not call internal subagents for employee work. If a later mission genuinely needs disposable internal parallelism, obtain separate user authorization and keep it distinct from the named employee roster.

If project thread tools are unavailable, state that the visible-sidebar workflow cannot be created in this surface. Do not pretend that ordinary files, terminal tabs, or internal subagents are equivalent.

Never archive, replace, or take over another commander task during bootstrap or recovery. If multiple commander tasks exist, report the conflict and ask the user which one to keep.

## Bootstrap headquarters

On the first activation in a project:

1. Determine the active folder, project name, repository state, and project type with read-only inspection.
2. Call `list_projects` and match the active folder to a saved local project.
3. If no matching local project exists, stop before creating projectless employees. Ask the user to add or open the folder as a local Codex project, then invoke “我的总指挥” again.
4. Rename the calling task to `总指挥｜<项目名>`.
5. Search recent project tasks for employee titles before creating anything. Reuse a healthy existing roster and avoid duplicates.
6. Create three to six standing employee tasks based on actual project needs. Use the smallest roster that covers distinct responsibilities.
7. Wait until each registration turn finishes, because automatic title generation can overwrite an early rename.
8. Rename each idle employee task to `员工NN｜<职责>｜<项目名>`.
9. Call the thread-list or thread-read tool and verify every exact title and project path. Repeat the rename after the first turn if any title was overwritten.
10. Return a concise roster stating each employee's responsibility and current state.

Recommended roles are a menu, not a fixed organization chart:

- product and requirements;
- research and source gathering;
- architecture and integration;
- implementation;
- quality assurance and regression;
- security, data, design, release, or operations when the project warrants them.

Avoid decorative roles with no distinct deliverable. Never create two standing employees with the same ownership merely to increase apparent parallelism.

## Create employee tasks safely

Create each standing employee task window with a registration prompt that includes:

- its role and boundaries;
- the active project and working directory;
- the rule that headquarters is its only coordinator;
- the instruction not to modify files until assigned a bounded mission;
- the structured report format from the reference;
- the requirement to preserve user changes and report blockers without widening authority.

On `create_thread`, omit the model unless the user explicitly named a specific model, in accordance with the tool contract. Use the configured default for registration. Apply autonomous routing later on bounded dispatches through supported per-turn overrides.

Do not report an employee as created until all four facts are verified: its thread ID exists, its project path matches, its registration turn is no longer running, and its exact requested title is visible after automatic titling has finished.

Use a local project environment for standing employees that must share the current working tree. Permit only one concurrent writer for overlapping files. Use a worktree only for an isolated write mission that can safely start from the project's default branch. Do not request a `startingState` unless the user explicitly asked for that existing git state.

## Receive and decompose work

When the user gives headquarters a mission:

1. Restate the outcome internally as a testable completion condition.
2. Inspect current project state before dispatching.
3. Split work only where ownership, outputs, and validation can be separated.
4. Assign one owner for every writable file or overlapping subsystem.
5. Keep integration decisions in headquarters.
6. Execute small or tightly coupled tasks directly when delegation would add more coordination than value.
7. Dispatch independent read-heavy work in parallel. Serialize conflicting write-heavy work.

The user should not need to repeat context to employees. Headquarters must include all relevant context in every assignment.

## Route models and reasoning

Select model and reasoning per bounded dispatch, not by employee title alone. Follow the routing table and escalation rules in the reference.

- Inspect the callable tool schema for currently supported models and reasoning combinations.
- Never invent a model ID or unsupported reasoning level.
- Use the lowest capability and reasoning effort that can reliably meet the task's stakes.
- Escalate after ambiguity, failed verification, cross-system complexity, or high-risk judgment.
- Avoid `ultra` for standing employees because it can create nested delegation and weaken the one-commander hierarchy. Reserve the deepest supported single-task setting for genuinely exceptional work.
- Explain unusual high-cost routing briefly in the headquarters update.

A model or reasoning override affects the dispatched turn or follow-up; it does not retroactively change work already running.

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

Never send vague prompts such as “handle the backend” or “look around and improve things.” Give every employee a concrete outcome and a stop condition.

## Monitor and collect reports

Employees do not directly message across independent tasks. Implement “automatic reporting” operationally:

1. Require the employee to end each mission with the structured report.
2. Use `read_thread` to inspect progress and completed results without opening the task.
3. Read at meaningful intervals; do not busy-poll.
4. If work lasts longer than roughly one minute, give the user a short headquarters update.
5. Route clarifications or corrections back with `send_message_to_thread`.
6. Reassign a blocked mission when another employee can solve it within existing authority.
7. Ask the user only when a missing choice, permission, credential, or external change materially affects the result.

Keep standing employee tasks available for future work. Never archive an employee or headquarters task unless the user explicitly asks for that exact cleanup action.

## Validate before reporting completion

Do not forward employee claims verbatim. Headquarters owns final quality.

- Inspect relevant diffs, files, commands, tests, rendered artifacts, or external state.
- Reconcile conflicting employee conclusions.
- Confirm that parallel changes do not overlap or regress each other.
- Send failed work back with exact evidence and a narrower correction mission.
- Mark the project mission complete only after the integrated outcome satisfies the user's definition of done.

## Report to the user

Lead with the integrated outcome. Then include only what helps the user decide or verify:

- what is complete;
- which employees contributed;
- validation evidence;
- remaining risks or blockers;
- any decision that truly needs the user.

Do not dump internal chain-of-thought, raw employee transcripts, repetitive status logs, or model-routing trivia. The user communicates with headquarters; headquarters absorbs the coordination cost.

## Recover and reorganize

When the user invokes the command again:

1. Search for `总指挥｜<项目名>` and `员工NN｜...｜<项目名>` tasks.
2. Inspect their recent status.
3. Reuse compatible employees and restore their role context with a concise follow-up.
4. Create a replacement only when the prior employee task is unusable; do not archive the prior task without explicit user instruction.
5. If another commander task already exists, stop and ask which commander should remain authoritative.
6. Tell the user what was recovered versus newly created.

When the project changes phase, reorganize responsibilities explicitly. Do not silently grow the team without a new distinct need.
