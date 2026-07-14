# Codex Project Commander｜我的总指挥

[中文说明](README.md) · [English](README.en.md)

一个专门面向 Codex 本地项目的开源 SKILL：无论项目刚建立还是已经运行很久，都先理解项目文件、当前状态和任务历史，再把当前任务设为置顶“总指挥”，并归整同一项目侧边栏中的独立员工任务窗口。

仓库同时提供两个可独立安装的版本：中文版 `project-commander-zh` 与英文版 `project-commander`。中文版元数据直接包含“总指挥、我的总指挥、Codex 总指挥”等关键词，便于在 GitHub 与 Codex 中检索。

> 这里的“员工”是独立 Codex 项目任务窗口，不是子智能体、终端标签页或虚构角色。

## 它解决什么问题

项目变复杂以后，所有调研、开发、测试和讨论挤在一个任务里，会导致上下文越来越乱。Project Commander 把工作拆成清晰的长期窗口：

- 总指挥：接收用户目标、拆解任务、分配工作、验收和统一汇报。
- 员工窗口：各自保留独立对话、职责、任务历史和 thread ID。
- 用户只需要与总指挥沟通，不需要反复向每个窗口解释背景。

## 核心能力

- 在同一本地项目下保留 1 名 Token 监管员工，并按需要创建 3–6 个实际交付员工任务窗口。
- 接管长期运行的既有项目，建立全项目文件地图并识别当前工作阶段。
- 扫描现有与近期新增任务窗口，复用、归类和重新配置适合的员工窗口。
- 根据项目类型自动形成产品研发、内容运营、数据分析、影视制作或 Codex Skill 开发等总指挥画像。
- 建立 `.codex/project-commander/ORG_CHART.md`，按项目交付物划分治理部门与项目专属交付部门。
- 可选“现代化三省六部架构”，用中书立案、门下审议、尚书执行和六部职能池建立书面治理门，而不是机械创建九个窗口。
- 为每个员工窗口分配唯一部门、主要负责成果、输入输出合同、可写范围和验收责任。
- 在员工首轮登记结束后统一命名，并复查自动标题是否覆盖了名称。
- 为每名员工设置当前 Codex 环境支持的模型与推理基线，并按任务难度动态覆盖。
- 固定设置一名 `员工00｜Token监管与模型路由｜项目名`，专门阻止重复读取、重复派工和模型过度使用。
- 按 Sol、Terra、Luna 三级策略选择最低足够模型，并在当前环境不支持 GPT-5.6 时映射到等价档位。
- 把完整任务拆成依赖图，持久记录在 `.codex/project-commander/TASK_LEDGER.md`，随时恢复和核对完成状态。
- 任意员工完成后立即验收并续派下一项适配任务，不等待最慢窗口完成整批工作。
- 提供节省、中等（普通）和效率三种模式，用 WIP、模型与检查频率共同控制速度和 Token。
- 自动定位、命名并置顶总指挥窗口。
- 为每次派工定义目标、范围、文件所有权、禁止事项、交付物和验收标准。
- 并行处理独立的只读工作，避免多个员工同时修改同一文件。
- 读取员工任务结果、处理阻塞、验证产物，再向用户汇总。
- 恢复已有员工编制，避免重复创建窗口。

## 安装

请选择一种语言安装，避免两个版本因触发词重叠而同时被隐式调用。

| 版本 | 技能目录 | 显式调用 |
| --- | --- | --- |
| 中文版 | `skills/project-commander-zh` | `$project-commander-zh` |
| English | `skills/project-commander` | `$project-commander` |

### 方式一：让 Codex 安装

中文版：

```text
使用 $skill-installer 安装这个仓库中的 skills/project-commander-zh：
https://github.com/ProfesseurHaipeng/codex-project-commander
```

英文版：

```text
Use $skill-installer to install skills/project-commander from:
https://github.com/ProfesseurHaipeng/codex-project-commander
```

### 方式二：手动安装

```bash
git clone https://github.com/ProfesseurHaipeng/codex-project-commander.git
mkdir -p ~/.agents/skills
cp -R codex-project-commander/skills/project-commander-zh ~/.agents/skills/project-commander-zh
```

如果技能没有立即出现在 Codex 中，请重新启动 Codex。Codex 当前的用户级技能目录是 `$HOME/.agents/skills`。

## 使用

最可靠的显式调用方式：

```text
使用 $project-commander-zh 在当前项目启动“我的总指挥”。
```

也可以输入：

```text
我的总指挥
总指挥
指挥官
项目指挥官
启动指挥官
启动总指挥
```

还可以组合模式：

```text
我的总指挥，节省模式
我的总指挥，中等模式
我的总指挥，效率模式
```

复杂或高风险项目可以同时选择治理架构：

```text
我的总指挥，效率模式，三省六部架构
```

总指挥已经启动时，单独发送 `节省模式`、`中等模式`、`普通模式` 或 `效率模式` 即可切换；不会新建第二个总指挥。
单独发送“三省六部架构”或“三省六部模式”只校准现有组织，也不会创建第二名总指挥或重复员工。

自然语言属于隐式技能匹配，安装技能较多时不应把它当成绝对可靠的命令。若希望“我的总指挥”稳定映射到中文版 SKILL，可把 [AGENTS.command-bridge.md](examples/AGENTS.command-bridge.md) 中的内容合并进 `~/.codex/AGENTS.md`。

## 老项目接管模式

在已经使用很久的 Codex 项目中输入命令后，总指挥会先完成接管，而不是立即套用固定员工模板：

1. 清点项目自有文件、Git 状态、近期变更、说明文档、配置、源码和测试。
2. 对依赖、生成物、缓存、二进制和敏感文件只登记元数据，不盲目载入上下文。
3. 根据文件和任务历史判断项目领域、阶段、目标、风险和验收表面。
4. 生成适应该项目的总指挥职责画像。
5. 扫描同一项目的现有和近期新增任务窗口。
6. 复用已有员工，归整用途明确的新窗口，保留历史与用途不明的任务。
7. 为员工分配模型与推理强度基线，发送岗位配置并等待确认。
8. 把总指挥窗口改名、定位、置顶并复查。

自动归整不会归档、删除、替换或接管历史任务。存在多个总指挥或用途不明的窗口时，SKILL 会报告冲突并请用户决定。

## Token 监管部与三级模型

每个项目固定保留一名只读监管员工：

```text
员工00｜Token监管与模型路由｜项目名
```

监管员在派工前检查是否已有员工掌握上下文、是否重复读取同一文件、是否出现重叠任务、是否可以合并任务，以及是否真的需要更强模型。它不承担生产工作，也不会再创建下级员工。

默认模型策略：

| 档位 | 模型家族 | 主要用途 |
| --- | --- | --- |
| 第一档 | Sol | 复杂软件、跨系统调试、高歧义高价值工作、高风险最终验收 |
| 第二档 | Terra | 数据整理、调研、文档、标准实现与常规分析 |
| 第三档 | Luna | 提取、分类、转换、清单、重复检查和批量跑量 |

所有任务优先尝试最低足够档位。Luna 升 Terra、Terra 升 Sol 必须记录原因；同一路线两次实质相同失败后先止损和更换方法，不能靠不断提高模型与推理强度硬跑。界面没有公开真实 Token 用量时，只报告轮次、重试、重复读取等代理信号，不虚构数值。

## 持续派工、任务账本与三种模式

总指挥收到任务后，先把完整目标、完成定义、依赖、负责人、状态、模型、检查点和证据写入本地任务账本。每名员工一次只执行一条主任务线；后续工作留在队列。

任意员工完成后，总指挥立即验收、释放文件所有权、解锁依赖并续派，不等待其他无关员工。只有真实下游依赖全部当前任务时才等待整组。

| 模式 | 实际交付任务 WIP | 默认策略 |
| --- | --- | --- |
| 节省模式 | 1–2 | Luna/低推理优先，检查点稀疏 |
| 中等模式（普通模式） | 2–3 | Luna/Terra 按任务分配，默认平衡 |
| 效率模式 | 3–5 个互不冲突任务 | 完成即续派，有边界工作优先 Terra，Sol 仍需依据 |

账本由总指挥唯一写入，默认不加入 Git，也不保存秘密、原始对话全文或隐藏思维过程。巡检只依据最后实质证据、承诺检查点、阻塞和重试判断“待命、受阻或停滞”，不会主观给员工贴“偷懒”标签。

## 项目组织架构系统

总指挥在熟悉项目后先建立组织架构，再创建员工：

```text
总指挥｜项目名
├─ 治理部门
│  └─ 员工00｜Token监管与模型路由｜项目名
└─ 项目专属交付部门
   ├─ 员工01｜不同职责｜项目名
   ├─ 员工02｜不同职责｜项目名
   └─ 员工NN｜不同职责｜项目名
```

部门与岗位根据真实交付物动态生成。例如软件项目可以分为产品规划、架构开发、质量发布；内容项目可以分为调研策略、内容生产、视觉分发质检；数据项目可以分为数据质量、分析建模、报告验证。

默认不创建部门经理窗口，由总指挥直接管理所有员工，避免增加无产出的管理层。每项任务只属于一个部门并只有一名生产负责人；跨部门交接由总指挥使用已验收结果和压缩证据中转。组织架构决定“谁负责什么”，任务账本决定“现在做到哪里”。

### 可选：现代化三省六部治理

启用后，总指挥还会建立 `.codex/project-commander/GOVERNANCE.md`：中书省职能把目标写成可审议方案，门下省职能独立给出“准行、封驳或补证”，尚书省职能只把获准任务派给六部职能。六部对应组织任用、Token与资源、标准沟通、生产执行、质量风险、工程基础设施。

这些是可折叠职能，不是九个固定窗口。小项目可以由 2–3 个交付员工兼任相容职能；高风险方案作者与最终审议者、生产者与独立质量裁决者必须分开。唯一员工00归入户部职能，继续只读监管 Token 与模型路由。

设计参考了 [CCPM](https://github.com/automazeio/ccpm) 的依赖/冲突队列、[TDD Multi-Agent Orchestration](https://github.com/glebis/claude-skills/blob/main/tdd/SKILL.md) 的上下文隔离、[Code Review and Quality](https://github.com/addyosmani/agent-skills/blob/main/skills/code-review-and-quality/SKILL.md) 的独立质量门，以及 [Quality Playbook](https://github.com/github/awesome-copilot/blob/main/skills/quality-playbook/SKILL.md) 的阶段门和书面交接。

## 工作方式

```text
用户
  ↓ 只与一个窗口沟通
总指挥｜项目名
  ├─ 员工00｜Token监管与模型路由｜项目名
  ├─ 员工01｜产品与需求｜项目名
  ├─ 员工02｜调研与资料｜项目名
  ├─ 员工03｜架构与方案｜项目名
  ├─ 员工04｜开发与实现｜项目名
  └─ 员工05｜测试与验收｜项目名
```

独立任务之间不会自动互相发送消息。总指挥通过项目任务工具派工、读取状态和结果，因此“自动汇报”的实际含义是：员工按统一格式结束任务，总指挥主动收集、验证并整合这些报告。

## 安全边界

- 编写、安装、校验或讨论本 SKILL 时，不允许创建或修改真实项目任务。
- 只有用户在目标项目内明确运行命令时，才允许建立员工窗口。
- 不使用子智能体冒充员工窗口。
- 不让多个员工同时拥有同一文件或子系统的写权限。
- 未经用户明确授权，不归档、替换或接管现有任务。
- SKILL 不自动扩大到发布、部署、购买、外部消息、生产数据或秘密信息操作。

## 更便利地使用 Codex

完整中文指南见 [Codex便利使用指南](docs/Codex便利使用指南.md)，内容包括：

- 项目、任务与工作树如何分工；
- 如何用 `AGENTS.md` 保存长期规则；
- 什么时候使用 Skills；
- 模型和推理强度如何选择；
- 如何减少上下文污染与并行写入冲突；
- 如何建立可验证的完成标准。

## 项目结构

```text
.
├── README.md
├── LICENSE
├── docs/
│   └── Codex便利使用指南.md
├── examples/
│   ├── AGENTS.command-bridge.md
│   └── AGENTS.command-bridge.en.md
└── skills/
    ├── project-commander/          # English
    │   ├── SKILL.md
    │   ├── agents/openai.yaml
    │   ├── scripts/project_inventory.py
    │   └── references/
    └── project-commander-zh/       # 中文
        ├── SKILL.md
        ├── agents/openai.yaml
        ├── assets/ORG_CHART.template.md
        ├── assets/TASK_LEDGER.template.md
        ├── scripts/project_inventory.py
        └── references/
            ├── continuous-dispatch.md
            ├── dispatch-and-routing.md
            ├── existing-project-onboarding.md
            ├── organization-system.md
            └── token-governance.md
```

## 官方资料

- [Build skills](https://learn.chatgpt.com/docs/build-skills)
- [Custom instructions with AGENTS.md](https://learn.chatgpt.com/docs/agent-configuration/agents-md)
- [Projects, chats, and tasks](https://learn.chatgpt.com/docs/projects)
- [Models](https://learn.chatgpt.com/docs/models)
- [Config basics](https://learn.chatgpt.com/docs/config-file/config-basic)

## License

[MIT](LICENSE)
