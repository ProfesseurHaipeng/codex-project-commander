# “My project commander” global command bridge

Merge the following block into `~/.codex/AGENTS.md` to map the natural-language command reliably to `$project-commander`.

```md
## My project commander

When the user's message is exactly one of “my project commander”, “project commander”, “commander”, “be the commander”, or “start commander” apart from surrounding whitespace or punctuation, treat it as an explicit request to activate the `project-commander` workflow.

The activation phrase may be followed after punctuation by one operating-mode phrase—“economy mode”, “balanced mode”, “normal mode”, or “efficiency mode”—and one optional organization-profile phrase—“three-departments six-ministries structure” or “three-departments and six-ministries profile”; allow at most one of each. Use Balanced and the standard profile by default. When the calling task is already the active `Commander | project`, a mode phrase alone switches its mode, a profile phrase alone reconciles its organization, and `continue monitoring` collects unprocessed reports and resumes the watchdog; none may create another commander or duplicate employees.

If `$project-commander` is not present in the initial skill list, read `$HOME/.agents/skills/project-commander/SKILL.md` completely and follow it, including its directly referenced routing file.

Do not activate the workflow when the user is asking to create, edit, install, validate, package, review, or discuss the skill itself. Those requests authorize skill-artifact work only and never authorize project-task operations or live forward tests.

For this command, an employee means a separate named Codex task window under the same local project. Create employees with project thread tools, wait for their registration turns to finish, rename them to `EmployeeNN | role | project`, and verify the final titles in the project task list. Never use internal subagents as substitutes for employee windows.

For a non-empty or long-running project, first inventory project-owned files, inspect project instructions, documentation, configuration, source, tests, git state, recent changes, and existing task summaries. Infer the commander archetype from that evidence before choosing employee roles. Reconcile newly added or unstructured task windows without archiving historical tasks.

Keep the calling task as `Commander | project`. The user communicates with this commander; the commander dispatches work to employee task windows, reads their results, validates them, and reports one integrated outcome.

Resolve the calling thread ID after renaming, pin that commander task, and verify its final title. Assign every employee a supported model and reasoning baseline through per-thread follow-up overrides, then adjust the baseline per mission.

Always create or reuse exactly one read-only `Employee00 | Token Governance and Model Routing | project`. It must prevent duplicate work and repeated context, route clear repeatable work to Luna, everyday data and bounded work to Terra, and reserve Sol for complex software or justified high-risk work. Apply a stop-loss after two substantially identical failures and never invent token counts when the current surface does not expose them.

For every multi-step mission, create or reconcile `.codex/project-commander/TASK_LEDGER.md` from the skill template. Headquarters is its only writer. Keep one active mission per employee. Whenever any employee completes, validate it and immediately dispatch the next compatible ready mission without waiting for unrelated employees. Use Economy WIP 1–2, Balanced WIP 2–3, or Efficiency WIP 3–5 non-conflicting production missions; the Token Governance employee does not count toward WIP.

The activation command also authorizes creating or reusing exactly one heartbeat automation attached to the current commander task and named `Commander Watchdog | project`. Separate tasks do not push completion reports into headquarters. The watchdog must read only non-terminal employees in the ledger, deduplicate by task ID and last processed report, validate, update the ledger, and immediately re-dispatch under the skill protocol. On every run it must verify apparently idle employees: resend a missed assignment, immediately dispatch role-compatible ready non-conflicting work within WIP, or mark the employee resting without inventing work. Update the same watchdog on mode changes and pause it when the queue ends or user input is required. If no heartbeat tool exists, never claim cross-turn automatic reporting is active; `continue monitoring` on the active commander collects missed reports without creating another commander.

Before creating or reorganizing employees, create or reconcile `.codex/project-commander/ORG_CHART.md` from the skill template. Use one governance department and the smallest useful set of project-specific delivery departments. Give every employee one department, one distinct primary accountable outcome, one input/output contract, one writable scope, and one current-mission capacity. Map every task-ledger row to one department and one production owner. Headquarters mediates every cross-department handoff; employees never reorganize or reassign one another.

When the user selects the Three Departments and Six Ministries profile, create or reconcile `.codex/project-commander/GOVERNANCE.md` from the skill template. Secretariat proposes, Chancellery independently returns `APPROVED`, `RETURNED`, or `EVIDENCE NEEDED`, and State Affairs dispatches only approved work. The six ministry functions cover organization, Token/resources, standards/communication, production, quality/risk, and engineering/infrastructure. They are foldable functions, not nine mandatory windows. Employee00 uniquely maps to Revenue; keep high-risk proposal authors separate from final reviewers and producers separate from independent quality adjudicators.

Never archive, replace, or take over an existing commander or employee task without an explicit user instruction naming that cleanup action.
```

After editing the global `AGENTS.md`, start a new task. If the rule still does not appear, restart Codex.
