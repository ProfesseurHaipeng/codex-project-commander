# Completion Watchdog and Automatic Re-dispatch

Separate Codex task windows do not push their completed result into the commander task. A desktop completion notification informs the user; it does not deliver an employee report to headquarters. Headquarters must actively monitor employee task state.

## Preferred mechanism: commander-thread heartbeat

Before the first production dispatch, inspect the current tools for thread-heartbeat or automation-update capability. When available:

1. Create or reuse exactly one heartbeat attached to the current commander task, named `Commander Watchdog | <project>`.
2. Use a thread heartbeat, not a standalone scheduled task that creates a new task on every run. The heartbeat must return to headquarters and reuse its context.
3. Record the watchdog name, state, last scan, and next-scan posture in the task ledger. Do not broadcast internal automation IDs to employees without a reason.
4. Use the lowest useful cadence by mode: about 8–10 minutes for Economy, 3–5 minutes for Balanced/Normal, and 1–2 minutes for Efficiency. If the tool supports different legal intervals, choose the closest interval that avoids waste.
5. Use structured automation-tool parameters. Never handwrite or expose raw RRULE directives.
6. Never create a second watchdog. Update the existing one when the operating mode changes.

Use a durable heartbeat prompt equivalent to:

```text
This is a Project Commander completion-watchdog run. Inspect only employee tasks and the ready queue in this exact project's organization chart and task ledger.

1. List relevant task windows under the exact project path.
2. Read only the latest state and final employee report for employees named in the ledger.
3. Compare task ID, evidence, and the last processed report marker; never process the same report twice.
4. On completion or needs-review, validate evidence, update the ledger, release ownership, recompute dependencies, and immediately dispatch one compatible ready mission.
5. On a blocker, resolve it only within existing authority; stop dispatch and report the smallest question when user input is required.
6. Run an idle-capacity audit for every apparently idle employee: first exclude unprocessed reports, missed dispatch, blocked/review work, or a still-running turn; immediately dispatch compatible ready work, otherwise mark the employee resting with a reason.
7. When nothing materially changed, do not message employees, repeat summaries, or invent work.
8. When no running, review, or ready work remains, pause this watchdog. Also pause when progress requires the user.
```

## Completion detection and deduplication

Treat a result as a processable completion only when all apply:

- the employee task is no longer running, or its latest turn clearly ended;
- the latest response includes the required `EMPLOYEE REPORT`;
- the report task ID matches the employee's current ledger task;
- its report marker or final-response time is newer than the ledger's last processed report.

Record each employee's last processed task ID and report time or stable response marker in the ledger. Process a report once. If an employee only says “done” without evidence, move it to review and request the missing evidence instead of overwriting the mission with new work.

## Validate and re-dispatch in one run

When a new report is detected, complete this sequence in the same headquarters run:

1. read the full employee report and necessary evidence;
2. verify the result on the real acceptance surface;
3. update task state and the last processed report marker;
4. release writable ownership and recompute dependencies;
5. select the highest-value role-compatible ready mission;
6. send the next mission contract with `send_message_to_thread`;
7. record successful dispatch before deciding whether a user-facing update is needed.

Do not wait for unrelated employees. Do not ask employees to find their own next work, and never let employees dispatch one another.

## Idle-capacity audit

After processing new reports on every heartbeat, inspect apparently idle roster employees. Read the ledger and latest window state before classifying:

| Classification | Observable evidence | Headquarters action |
| --- | --- | --- |
| Unprocessed completion | employee turn ended but the latest report is not accepted | process the report first; never overwrite the old mission |
| Missed dispatch | the ledger assigns a current task but no successful mission-contract message exists | send it once immediately and record the dispatch result |
| Still working | the window is running or has not reached its promised checkpoint | keep it working and do not double-dispatch |
| In review | a report lacks evidence or validation is unfinished | validate or request evidence; do not send a new primary mission |
| Blocked / dependency wait | a named blocker, dependency, permission, or external state exists | record blocked and resolve only within authority |
| Dispatchable | no current mission and a role-compatible task is ready, approved, dependency-complete, non-conflicting, and allowed by WIP | send the mission contract in this run and mark it running |
| Truly idle | no current mission and no compatible dispatchable task exists | mark `resting` with a reason; send no pointless standby message |

Prioritize missed assigned work, tasks that unlock critical dependencies, tasks closest to retained employee context, higher user value, then the task that succeeds with the cheapest sufficient model.

“Work exists” means real work that is ready, authorized, role-compatible, non-conflicting, and within the selected mode's WIP. Never invent filler, prematurely dispatch dependency- or governance-blocked work, or give production ownership to Token Governance merely to keep a window busy. True idle is not stalled or lazy. Resting employees do not count toward WIP and need no periodic wake-up message. Re-audit on the next heartbeat when work becomes ready or a dependency clears.

## Fallback when heartbeat capability is unavailable

If the current surface lacks a heartbeat/automation tool, Scheduled is disabled, or creation fails:

1. Never claim cross-task automatic reporting is active.
2. While the current commander turn remains active, use the project task list and `read_thread` for low-frequency monitoring and the same idle-capacity audit. Check at roughly 30–60 second intervals and back off when nothing changes.
3. Read only non-terminal employees named in the ledger; do not scan unrelated historical tasks.
4. Before the current turn ends, tell the user accurately that employee results remain in their windows and cross-turn automatic handoff cannot be guaranteed.
5. Mark the watchdog `manual wake required` in the ledger. When the user says `continue monitoring`, collect every unprocessed report and resume dispatch without creating another commander.

## Stop and resume

Pause the single watchdog when any apply:

- every required task is done or cancelled by authority;
- no running, review, or ready work remains;
- progress depends only on a user choice, permission, credential, or external state;
- the user explicitly asks to stop monitoring.

On commander resumption, read the ledger first, scan all non-terminal employee tasks, collect reports completed while the watchdog was inactive, then re-enable the same watchdog. Never delete unrelated automations and never substitute a standalone Scheduled inbox task for the commander heartbeat without explicit user direction.
