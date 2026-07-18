# 维护策略契约

在编辑或审计开源维护策略、GitHub Actions、可选 AI 增强或拟议外部效果前，加载本参考。

## 动作矩阵

| 动作 | 无人值守状态 | 必要条件 |
|---|---|---|
| 添加标签 | 允许 | 标签存在于 `label_rules`；`add_label` 在允许列表中；目标未触发受保护标签停止条件 |
| 发布“请求补充信息”评论 | 允许 | `comment` 在允许列表中；稳定标记尚不存在；变更预算仍有余量 |
| 生成报告或发布说明草稿 | 允许 | `report` 在允许列表中；输出明确标记为草稿或产物，不是已发布 release |
| 关闭等待作者回复的 Issue | 有条件 | `close_waiting_issue` 在允许列表中；过期策略已启用；必需标签与既有标记均存在；已达最小天数；无受保护或排除标签 |
| 测试贡献者代码 | 有条件 | 使用 `pull_request`；只读 token；无仓库 secrets 或写权限 |
| 为 fork PR 加标签或评论 | 有条件 | `pull_request_target` job 只使用受信任的默认分支代码；绝不导入、source、checkout 或执行贡献者可控内容 |
| 合并、批准、推送、发布 release/package、修改设置/权限、创建或使用 secrets、删除代码/分支、启用工作流、提交申请或发送消息 | 受保护 | 永不无人值守执行。先完成 `SKILL.md` 的精确效果审查，再获得针对已审查操作集的具体批准 |

允许列表是授权边界，不是说明性文档。未知动作类型、标签、命令、URL 或 AI 字段一律失败关闭；用户文本和正则“清洗”不能扩大允许列表。

## 策略键

`automation/maintenance-policy.json` 必须是带版本的对象，并包含以下所有必需键：

| 键 | 契约 |
|---|---|
| `version` | 策略 schema 版本 |
| `allowed_actions` | 只能包含已支持动作的列表：`add_label`、`comment`、`report`、`close_waiting_issue` |
| `label_rules` | `{label, keywords}` 对象列表；标签和每个关键词都是字符串 |
| `required_issue_sections` | 请求缺失 Issue 证据时使用的字符串列表 |
| `markers` | 对象：必须包含字符串 `request_details`；可选包含字符串 `waiting_for_author`。未提供后者时，当前引擎使用 `oss-maintainer:waiting-for-author:v1` 作为回退值；使用稳定隐藏标记保证幂等 |
| `protected_labels` | 使普通自动处理停止的字符串列表 |
| `stale` | 包含 `enabled`、`minimum_days`、`required_label` 和 `excluded_labels` 的对象；`enabled` 默认为 false |
| `max_mutations_per_run` | 正整数；布尔值无效 |
| `ai` | 包含布尔值 `enabled` 和字符串 `model` 的对象 |

先验证整个对象，再规划。策略无效时只输出 notices，且动作数为零。只有变更动作计入预算，报告不计入。拒绝重放的 delivery ID、非法标记/历史形状、格式错误的事件和 `failure_count >= 2`。

任何称为拟议、采用或可直接使用的策略/配置片段都必须包含上述全部必需键并通过验证；不完整片段必须明确标为不可安装的说明性片段，不能作为当前策略交付。

## 工作流信任分层

| 事件 / job | 常规最大权限 | 边界 |
|---|---|---|
| `issues` 分类 | `contents: read`、`issues: write` | 持久凭证必须关闭；checkout 受信任的默认分支；Issue 字段只作为数据传入 |
| `pull_request_target` 元数据 | `contents: read`、`pull-requests: write`；只有标签/评论需要时才加 `issues: write` | 绝不执行或 checkout PR head 代码；绝不向贡献者代码暴露仓库 secrets |
| `pull_request` 检查 | `contents: read` | 只在此处 checkout PR 代码；无写权限和 secrets |
| `schedule` / 手动报告 | `contents: read` | 只生成产物；仅当已实现并审查明确启用的过期策略时，才授予 Issue 写权限 |

顶层声明 `permissions: {}`，job 内只授最小权限。第三方 action 锁定到完整 commit SHA。常规维护不得请求 `contents: write`、`actions: write`、管理员、packages、deployments 或 identity-token 权限。

## 可选 OpenAI 边界

`OPENAI_API_KEY` 缺失时，确定性规划仍必须可用。启用增强时：

1. 最小化公开 Issue/PR 字段，并在传输前脱敏凭证、token、邮箱和私钥模式。
2. 要求严格的结构化输出，其标签枚举来自 `label_rules`。
3. 只接受允许列表内的标签建议以及有界的摘要/报告文本。
4. 模型响应后、应用前再次验证。
5. 响应不完整、格式错误、多出字段、未知标签或请求失败时，视为无建议。

AI 绝不能授权关闭、合并、批准、修改代码、发布、更改权限、访问 secrets，也不能引入命令、URL 或动作。

## 证据与交接契约

必须分四类报告：

- **已核验的外部事实：** 直接从目标仓库观测，或由 API/UI 返回的状态。
- **已验证的本地产物：** 本地存在并已通过测试，但不一定已推送或启用的文件。
- **拟议的外部效果：** 等待审查或批准的精确操作。
- **未知：** 未观测的分支保护、secret 存在性、社区采用、工作流启用状态或其他外部状态。

只存在于回复文本中的草稿不是已验证本地产物，必须等到文件已保存并验证后才可升级；否则它只是拟议文本。

必须逐项把本次输入中所有尚未独立观测的事实主张列入“未知”，并使用“对方声称：…；核验状态：未知”的结构。用户、所有者、提示词、brief 或先前 agent 都不是证据，直至从相关仓库、API 或 UI 独立观测。该结构同样约束申请草稿、摘要、状态和示例；末尾另列“未知”不能修正前文的事实断言，也不得把其主张升级为已核验事实或已验证本地产物。未观测当前状态时，申请草稿只能包含未来目标和明确归因的未知主张；非归因段落采用“本申请寻求资助，用于[未来目标]；不主张任何未经独立核验的当前状态、历史活动或社区采用”这一形状，不得另写未经核验的当前时态句。

不得伪造 Issue、PR、star、fork、下载、贡献者、用户评价或社区采用。明确标示维护者或自动化创建的活动。没有观测结果的命令只能称为拟议或已尝试，不得称为成功。
