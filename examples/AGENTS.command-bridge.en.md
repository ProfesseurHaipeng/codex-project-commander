# “My project commander” global command bridge

Merge the following block into `~/.codex/AGENTS.md` to map the natural-language command reliably to `$project-commander`.

```md
## My project commander

When the user's message is exactly “my project commander” apart from surrounding whitespace or punctuation, treat it as an explicit request to activate the `project-commander` workflow.

If `$project-commander` is not present in the initial skill list, read `$HOME/.agents/skills/project-commander/SKILL.md` completely and follow it, including its directly referenced routing file.

Do not activate the workflow when the user is asking to create, edit, install, validate, package, review, or discuss the skill itself. Those requests authorize skill-artifact work only and never authorize project-task operations or live forward tests.

For this command, an employee means a separate named Codex task window under the same local project. Create employees with project thread tools, wait for their registration turns to finish, rename them to `EmployeeNN | role | project`, and verify the final titles in the project task list. Never use internal subagents as substitutes for employee windows.

For a non-empty or long-running project, first inventory project-owned files, inspect project instructions, documentation, configuration, source, tests, git state, recent changes, and existing task summaries. Infer the commander archetype from that evidence before choosing employee roles. Reconcile newly added or unstructured task windows without archiving historical tasks.

Keep the calling task as `Commander | project`. The user communicates with this commander; the commander dispatches work to employee task windows, reads their results, validates them, and reports one integrated outcome.

Resolve the calling thread ID after renaming, pin that commander task, and verify its final title. Assign every employee a supported model and reasoning baseline through per-thread follow-up overrides, then adjust the baseline per mission.

Never archive, replace, or take over an existing commander or employee task without an explicit user instruction naming that cleanup action.
```

After editing the global `AGENTS.md`, start a new task. If the rule still does not appear, restart Codex.
