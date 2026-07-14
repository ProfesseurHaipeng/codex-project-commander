# Continuous dispatch and durable task ledger

Use this protocol whenever headquarters receives, resumes, or replans a multi-step mission. It replaces batch barriers with event-driven dispatch while keeping one active mission per employee.

## Contents

1. [Create the ledger](#create-the-ledger)
2. [Represent the work](#represent-the-work)
3. [Select an operating mode](#select-an-operating-mode)
4. [Run the event loop](#run-the-event-loop)
5. [Monitor progress without busy polling](#monitor-progress-without-busy-polling)
6. [Resume and reconcile](#resume-and-reconcile)

## Create the ledger

Copy [../assets/TASK_LEDGER.template.md](../assets/TASK_LEDGER.template.md) to:

```text
.codex/project-commander/TASK_LEDGER.md
```

Create parent directories when needed. Headquarters is the only writer. Employees report through their task windows; headquarters validates the evidence and updates the ledger.

Keep the ledger local and untracked by default. Do not edit `.gitignore` without user authorization. Warn the user before committing the ledger because it may contain project plans or internal evidence pointers. Never store secrets, credentials, hidden reasoning, raw transcripts, or full file contents in it.

Update the ledger when:

- headquarters accepts or changes a user objective;
- a task becomes ready, starts, blocks, stalls, enters review, or completes;
- an employee is assigned, released, or reassigned;
- a dependency, model tier, reasoning effort, retry cap, or acceptance check changes;
- a mode changes.

## Represent the work

Convert the objective into a dependency graph. Give every task:

- a stable ID;
- one testable outcome;
- dependency IDs;
- department and primary role from `.codex/project-commander/ORG_CHART.md`;
- one owner or `unassigned`;
- one state: `backlog`, `ready`, `running`, `blocked`, `review`, `done`, `cancelled`, or `stalled`;
- owned files or scope;
- model tier, reasoning effort, and budget class;
- a next meaningful checkpoint;
- acceptance evidence and the next action.

Keep one active mission per employee. Queue later tasks in the ledger instead of sending several simultaneous assignments to one window. Preserve context by returning related follow-up work to the employee that already knows the subsystem when that does not create a conflict.

Mark a task `ready` only when all dependencies are `done` and its required authority and inputs exist. Treat a real integration or dependency barrier as a barrier; do not invent a global batch barrier.

## Select an operating mode

Default to Balanced mode. A mode controls work-in-progress, dispatch urgency, checkpoint cadence, and Token posture. It never expands authority, weakens safety, skips validation, or overrides the stop-loss.

| Mode | English triggers | WIP target | Routing posture | Checkpoints |
| --- | --- | --- | --- | --- |
| Economy | `economy mode` | 1–2 production missions | Luna first; Terra only when justified; Low/Light default | sparse, milestone-based |
| Balanced | `balanced mode`, `normal mode` | 2–3 production missions | Luna/Terra by task; Medium only when needed | normal meaningful checkpoints |
| Efficiency | `efficiency mode` | 3–5 non-conflicting production missions | immediate continuous dispatch; Terra default for bounded work; Sol only with evidence | more frequent event/checkpoint reads, never busy polling |

Count the Token Governance employee outside the production WIP target. Reduce WIP below the target when file ownership, dependencies, task-tool limits, or project risk require it. Never create filler work merely to reach a target.

Allow a mode in the activation command, for example `my project commander, efficiency mode`. When headquarters is already active, a mode-only trigger changes the ledger and future routing; it does not create another commander or duplicate employees.

## Run the event loop

After decomposing and recording the mission:

1. Recompute all `ready` tasks.
2. Rank them by dependency impact, user value, risk reduction, context reuse, and cheapest sufficient model.
3. Fill available WIP slots with non-conflicting tasks whose department and role match an available employee.
4. Send exactly one mission to each chosen employee and mark it `running`.
5. Read employee tasks at completion events or meaningful checkpoints.
6. On any employee completion, validate the reported evidence immediately.
7. If validation passes, mark the task `done`, release its ownership, and recompute dependencies.
8. Immediately assign the highest-value compatible `ready` task to that employee or another idle suitable employee.
9. If validation fails, move the task to `review`, `blocked`, or `stalled`, record the evidence, and replan within the retry cap.
10. Continue until every required task is `done`, `cancelled` by authority, or explicitly blocked on the user or external state.

Do not wait for the slowest employee before continuing unrelated work. Wait for all current tasks only when a named downstream task genuinely depends on all of them.

## Monitor progress without busy polling

Do not label an employee lazy. Classify only observable task state.

Record for each employee:

- current task and start event;
- last meaningful update or evidence;
- next promised checkpoint;
- blocker, retry count, and changed hypothesis;
- next compatible queued task.

Read progress when a task reports completion, reaches a promised checkpoint, needs a dependency decision, or appears inconsistent with the latest project state. Avoid timer-based chatter that produces no evidence.

If a checkpoint passes without meaningful progress:

1. send one concise check-in asking for current evidence, blocker, and next action;
2. if the next meaningful inspection still shows no new evidence, mark the task `stalled`;
3. preserve useful evidence, apply the stop-loss when applicable, and either narrow, replan, downgrade, escalate with justification, or reassign;
4. record why the change is expected to improve the outcome.

An employee in read-only standby is `ready`, not stalled. A task waiting on a named dependency is `blocked`, not stalled.

## Resume and reconcile

At activation or resumption:

1. read the existing ledger if present;
2. compare every non-terminal entry with current files, Git state, and the matching task window;
3. compare its department and accountable role with the current organization chart;
4. preserve stable task IDs and evidence pointers;
5. correct stale departments, owners, states, dependencies, and model assignments;
6. add newly discovered user requirements and project work;
7. recompute the ready queue and restart the event loop.

Treat the ledger as a compact operational index, not unquestionable truth. Current project evidence and verified task results win when they disagree with an old entry.
