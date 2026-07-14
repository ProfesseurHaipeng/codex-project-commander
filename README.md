# Codex Project Commander｜我的总指挥

一个专门面向 Codex 本地项目的开源 SKILL：无论项目刚建立还是已经运行很久，都先理解项目文件、当前状态和任务历史，再把当前任务设为置顶“总指挥”，并归整同一项目侧边栏中的独立员工任务窗口。

> 这里的“员工”是独立 Codex 项目任务窗口，不是子智能体、终端标签页或虚构角色。

## 它解决什么问题

项目变复杂以后，所有调研、开发、测试和讨论挤在一个任务里，会导致上下文越来越乱。Project Commander 把工作拆成清晰的长期窗口：

- 总指挥：接收用户目标、拆解任务、分配工作、验收和统一汇报。
- 员工窗口：各自保留独立对话、职责、任务历史和 thread ID。
- 用户只需要与总指挥沟通，不需要反复向每个窗口解释背景。

## 核心能力

- 在同一本地项目下创建 3–6 个独立员工任务窗口。
- 接管长期运行的既有项目，建立全项目文件地图并识别当前工作阶段。
- 扫描现有与近期新增任务窗口，复用、归类和重新配置适合的员工窗口。
- 根据项目类型自动形成产品研发、内容运营、数据分析、影视制作或 Codex Skill 开发等总指挥画像。
- 在员工首轮登记结束后统一命名，并复查自动标题是否覆盖了名称。
- 为每名员工设置当前 Codex 环境支持的模型与推理基线，并按任务难度动态覆盖。
- 自动定位、命名并置顶总指挥窗口。
- 为每次派工定义目标、范围、文件所有权、禁止事项、交付物和验收标准。
- 并行处理独立的只读工作，避免多个员工同时修改同一文件。
- 读取员工任务结果、处理阻塞、验证产物，再向用户汇总。
- 恢复已有员工编制，避免重复创建窗口。

## 安装

### 方式一：让 Codex 安装

把本仓库地址交给 `$skill-installer`，并指定技能目录：

```text
使用 $skill-installer 安装这个仓库中的 skills/project-commander：
https://github.com/ProfesseurHaipeng/codex-project-commander
```

### 方式二：手动安装

```bash
git clone https://github.com/ProfesseurHaipeng/codex-project-commander.git
mkdir -p ~/.agents/skills
cp -R codex-project-commander/skills/project-commander ~/.agents/skills/project-commander
```

如果技能没有立即出现在 Codex 中，请重新启动 Codex。Codex 当前的用户级技能目录是 `$HOME/.agents/skills`。

## 使用

最可靠的显式调用方式：

```text
使用 $project-commander 在当前项目启动“我的总指挥”。
```

也可以输入：

```text
我的总指挥
```

自然语言属于隐式技能匹配，安装技能较多时不应把它当成绝对可靠的命令。若希望“我的总指挥”稳定映射到该 SKILL，可把 [AGENTS.command-bridge.md](examples/AGENTS.command-bridge.md) 中的内容合并进 `~/.codex/AGENTS.md`。

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

## 工作方式

```text
用户
  ↓ 只与一个窗口沟通
总指挥｜项目名
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
│   └── AGENTS.command-bridge.md
└── skills/
    └── project-commander/
        ├── SKILL.md
        ├── agents/openai.yaml
        ├── scripts/project_inventory.py
        └── references/
            ├── dispatch-and-routing.md
            └── existing-project-onboarding.md
```

## 官方资料

- [Build skills](https://learn.chatgpt.com/docs/build-skills)
- [Custom instructions with AGENTS.md](https://learn.chatgpt.com/docs/agent-configuration/agents-md)
- [Projects, chats, and tasks](https://learn.chatgpt.com/docs/projects)
- [Models](https://learn.chatgpt.com/docs/models)
- [Config basics](https://learn.chatgpt.com/docs/config-file/config-basic)

## License

[MIT](LICENSE)
