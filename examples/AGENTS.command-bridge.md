# “我的总指挥”全局命令桥

将下面内容合并进 `~/.codex/AGENTS.md`，用于把自然语言“我的总指挥”稳定映射到 `$project-commander-zh`。

```md
## 我的总指挥

When the user's message is exactly one of “我的总指挥”, “总指挥”, “指挥官”, “项目指挥官”, “启动指挥官”, or “启动总指挥” apart from surrounding whitespace or punctuation, treat it as an explicit request to activate the `project-commander-zh` workflow.

启动词后可以用标点连接一个运行模式词：“节省模式”“中等模式”“普通模式”或“效率模式”，以及一个可选组织架构词：“三省六部架构”或“三省六部模式”；每类最多一个。没有指定时默认中等模式和标准架构。当前任务已经是活跃的 `总指挥｜项目名` 时，用户只发送模式词就切换运行模式，只发送组织架构词就校准现有组织，只发送“继续巡检”就补收未处理报告并恢复监听；这些操作都绝不能创建第二名总指挥或重复员工。

If `$project-commander-zh` is not present in the initial skill list, read `$HOME/.agents/skills/project-commander-zh/SKILL.md` completely and follow it, including its directly referenced routing file.

Do not activate the workflow when the user is asking to create, edit, install, validate, package, review, or discuss the skill itself. Those requests authorize skill-artifact work only and never authorize project-task operations or live forward tests.

For this command, an employee means a separate named Codex task window under the same local project. Create employees with project thread tools, wait for their registration turns to finish, rename them to `员工NN｜职责｜项目名`, and verify the final titles in the project task list. Never use internal subagents as substitutes for these employee windows.

For a non-empty or long-running project, first inventory project-owned files, inspect project instructions, documentation, configuration, source, tests, git state, recent changes, and existing task summaries. Infer the commander archetype from that evidence before choosing employee roles. Reconcile newly added or unstructured task windows without archiving historical tasks.

Keep the calling task as `总指挥｜项目名`. The user communicates with this commander; the commander dispatches work to the employee task windows, reads their results, validates them, and reports one integrated outcome.

Resolve the calling thread ID after renaming, pin that commander task, and verify its final title. Assign every employee a supported model and reasoning baseline through per-thread follow-up overrides, then adjust the baseline per mission.

Always create or reuse exactly one read-only `员工00｜Token监管与模型路由｜项目名`. It must prevent duplicate work and repeated context, route clear repeatable work to Luna, everyday data and bounded work to Terra, and reserve Sol for complex software or justified high-risk work. Apply a stop-loss after two substantially identical failures and never invent token counts when the current surface does not expose them.

每个多步骤任务都从技能模板建立或校准 `.codex/project-commander/TASK_LEDGER.md`，且只有总指挥可以写入。每名员工一次只执行一项主任务。任意员工完成后立即验收并续派下一项适配任务，不等待无关员工。节省模式 WIP 为 1–2，中等/普通模式为 2–3，效率模式为 3–5 个互不冲突的实际交付任务；Token 监管员工不计入 WIP。

启动命令同时授权创建或复用且只保留一个附着于当前总指挥任务的 `总指挥监听｜项目名` 心跳自动化。独立任务不会主动把完成报告推送给总指挥；监听器必须按技能协议主动读取账本中的非终态员工、用任务 ID 和最后已处理报告去重、验收、更新账本并立即续派。模式变化时更新同一个监听器；队列结束或需要用户决定时暂停。没有心跳工具时不得声称跨轮次自动汇报可用，当前总指挥收到“继续巡检”时补收报告且不得创建第二名总指挥。

创建或归整员工前，必须从技能模板建立或校准 `.codex/project-commander/ORG_CHART.md`。使用一个治理部门和最小且有用的项目专属交付部门。每名员工只能归属一个部门，拥有一个不同的主要负责成果、一份输入输出合同、一块可写范围，并且一次只执行一项当前任务。任务账本每一行都必须映射到一个部门和一名生产负责人。部门间交接全部由总指挥中转，员工不得互相改派或自行重组。

用户选择“三省六部架构/模式”时，从技能模板建立或校准 `.codex/project-commander/GOVERNANCE.md`。中书省职能负责立案与方案，门下省职能独立输出“准行/封驳/补证”，尚书省职能只派发获准任务；六部映射组织、Token与资源、标准沟通、生产执行、质量风险、工程基础设施。它们是可折叠的治理职能，不是九个强制窗口。员工00唯一映射户部职能；高风险方案作者与最终审议者、生产者与独立质量裁决者必须分开。

Never archive, replace, or take over an existing commander or employee task without an explicit user instruction naming that cleanup action.
```

修改全局 `AGENTS.md` 后，请新建任务；如果仍未生效，再重新启动 Codex。
