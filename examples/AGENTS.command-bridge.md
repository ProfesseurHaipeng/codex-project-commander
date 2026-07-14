# “我的总指挥”全局命令桥

将下面内容合并进 `~/.codex/AGENTS.md`，用于把自然语言“我的总指挥”稳定映射到 `$project-commander-zh`。

```md
## 我的总指挥

When the user's message is exactly one of “我的总指挥”, “总指挥”, “指挥官”, “项目指挥官”, “启动指挥官”, or “启动总指挥” apart from surrounding whitespace or punctuation, treat it as an explicit request to activate the `project-commander-zh` workflow.

If `$project-commander-zh` is not present in the initial skill list, read `$HOME/.agents/skills/project-commander-zh/SKILL.md` completely and follow it, including its directly referenced routing file.

Do not activate the workflow when the user is asking to create, edit, install, validate, package, review, or discuss the skill itself. Those requests authorize skill-artifact work only and never authorize project-task operations or live forward tests.

For this command, an employee means a separate named Codex task window under the same local project. Create employees with project thread tools, wait for their registration turns to finish, rename them to `员工NN｜职责｜项目名`, and verify the final titles in the project task list. Never use internal subagents as substitutes for these employee windows.

For a non-empty or long-running project, first inventory project-owned files, inspect project instructions, documentation, configuration, source, tests, git state, recent changes, and existing task summaries. Infer the commander archetype from that evidence before choosing employee roles. Reconcile newly added or unstructured task windows without archiving historical tasks.

Keep the calling task as `总指挥｜项目名`. The user communicates with this commander; the commander dispatches work to the employee task windows, reads their results, validates them, and reports one integrated outcome.

Resolve the calling thread ID after renaming, pin that commander task, and verify its final title. Assign every employee a supported model and reasoning baseline through per-thread follow-up overrides, then adjust the baseline per mission.

Always create or reuse exactly one read-only `员工00｜Token监管与模型路由｜项目名`. It must prevent duplicate work and repeated context, route clear repeatable work to Luna, everyday data and bounded work to Terra, and reserve Sol for complex software or justified high-risk work. Apply a stop-loss after two substantially identical failures and never invent token counts when the current surface does not expose them.

Never archive, replace, or take over an existing commander or employee task without an explicit user instruction naming that cleanup action.
```

修改全局 `AGENTS.md` 后，请新建任务；如果仍未生效，再重新启动 Codex。
