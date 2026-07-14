# 多平台兼容与能力降级协议

本协议把“能加载 SKILL”“能使用某个模型”和“能创建员工窗口”严格分开。实际启动总指挥前先完成能力探测；不以产品名或模型名推断工具。

## 三个兼容等级

### A 级：完整员工窗口模式

仅当宿主同时提供下列能力时启用：

- 原生读取 Agent Skills 或等价系统指令；
- 持久、命名、可枚举、可读取、可继续发送消息的项目任务窗口；
- 能把总指挥与员工绑定到同一项目目录；
- 能验证标题和稳定任务 ID；
- 若要承诺跨轮次自动续派，还必须有附着于总指挥的心跳或自动化工具。

Codex 桌面端在项目任务工具齐全时属于 A 级。员工是真实侧边栏任务窗口。没有心跳时仍可使用员工窗口，但监听降为手动“继续巡检”。

### B 级：持久会话总指挥模式

宿主原生加载 SKILL，并能保存、恢复或命名会话，但没有 Codex 等价项目任务窗口时使用。总指挥应：

- 读取项目、建立组织架构和任务账本；
- 把部门与岗位作为账本中的责任单元；
- 只使用宿主明确公开的会话、分支或委派能力；
- 将结果收回当前总指挥会话验收；
- 不声称存在 Codex 侧边栏员工、置顶、跨窗口推送或自动监听。

临时子智能体可以完成宿主允许的短任务，但永远不命名为“员工NN”，也不冒充长期员工窗口。

### C 级：单会话总指挥模式

宿主只能加载提示词或单个 SKILL、没有持久任务编排工具时使用。总指挥在一个会话里维护：

- 项目画像；
- 组织架构和唯一成果负责人；
- `.codex/project-commander/TASK_LEDGER.md` 队列；
- Sol/Terra/Luna 能力档位与 Token 止损；
- 一次只推进符合当前 WIP 的任务；
- 每个任务结束后的验收、状态更新和下一项选择。

不得创建虚假窗口、虚构员工报告、声称后台仍在工作或承诺自动回报。

## 平台与提供商映射

| 名称 | 类型 | 加载方式 | 默认等级与限制 |
| --- | --- | --- | --- |
| OpenAI Codex / Codex | Agent 宿主 | `.agents/skills` 或 Codex 支持的技能目录 | 有项目任务工具为 A；否则 B/C |
| Claude Code（用户口语 Cloud Code） | Agent 宿主 | `.claude/skills` | 原生 SKILL；通常 B/C，不把 Claude 子智能体冒充 Codex 员工窗口 |
| OpenCode（用户口语 OpenCloud） | Agent 宿主 | `.opencode/skills`、`.agents/skills` 或 `.claude/skills` | 原生 SKILL；按真实会话工具选择 B/C |
| Kimi Code | Agent 宿主 | `.kimi-code/skills` 或 `.agents/skills`，可用 `/skill:project-commander-zh` | 原生 SKILL；按真实会话工具选择 B/C |
| Hermes Agent | Agent 宿主 | `hermes skills install owner/repo/skills/project-commander-zh` | 原生 SKILL 与持久会话；默认 B，只有出现等价项目任务工具才升 A |
| OpenAI API | 模型/API | 由兼容 Agent 宿主调用，或注入便携提示词 | C；API 本身不创建任务窗口 |
| MiniMax | 模型/API 与独立工具生态 | OpenAI/Anthropic 兼容端点；也可作为 Codex/Claude Code/OpenCode 的模型提供商 | 等级由宿主决定，不由 MiniMax 模型决定 |
| MiniMax Codex | Codex 宿主 + MiniMax 模型 | 按 MiniMax 官方 Codex 自定义 provider 配置，并安装本 SKILL | Codex 工具齐全为 A；模型切换不改变员工规则 |
| DeepSeek（含用户口语 DeepSea） | 模型/API | 由 OpenAI/Anthropic 兼容宿主调用 | 等级由宿主决定；不硬编码易变模型 ID |
| 豆包 / 火山方舟 | 模型/API | 由兼容 OpenAI SDK/Agent 宿主调用 | 等级由宿主决定；API 本身不加载 SKILL |
| Kimi 模型/API | 模型/API | 由 Kimi Code 或其他兼容宿主调用 | Kimi Code 可原生加载；纯 API 为 C |
| Hermes 后端/API | Agent/API | Hermes 原生技能，或通过 OpenAI 兼容 API 接入前端 | 前端只提供聊天时为 C；Hermes 原生会话为 B |

## 能力探测顺序

1. 识别当前宿主实际公开的技能目录或技能工具。
2. 列出真实可调用的项目任务、会话、重命名、置顶、读写消息和自动化能力。
3. 选择 A、B 或 C，记录在任务账本“兼容等级”字段。
4. 再读取可选模型/提供商和推理强度，把实际选择映射到 Sol、Terra、Luna。
5. 如果只有一个模型，使用推理强度、WIP、上下文压缩和验收深度控制 Token；不得伪造三种模型。
6. 平台能力变化时可升级或降级，但必须保留账本和已验收证据。

## 提供商中立模型路由

- Luna：当前宿主中能够可靠完成清晰重复任务的最低成本选项。
- Terra：能够完成有边界日常分析、数据整理、文档和常规实现的平衡选项。
- Sol：复杂软件、跨系统判断或有依据的高风险裁决选项。

不得把某个供应商的固定模型名永久绑定到档位。优先读取当前模型目录、价格/额度信号、上下文窗口和推理选项。不可见时按能力类别记录，不虚构用量或价格。

## 便携提示词入口

如果宿主不能发现目录式 SKILL，把 [便携总指挥提示词](../assets/PORTABLE_COMMANDER_PROMPT.md) 放入其 system/developer instructions。此入口只保证 C 级治理；只有宿主随后明确提供 A/B 级工具时才能升级。

无论平台如何，安全边界、一次只做一项主任务、Token 止损、非攻击式 APP 验收、API Key 一次提示且不回显不落盘等规则保持不变。
