# Modern Three Departments and Six Ministries Governance

This profile borrows the separation-of-duties logic of the historical Three Departments and Six Ministries to add a proposal-review-execution-validation chain to complex or high-risk Codex projects. It is a modern project-governance analogy, not a historical simulation and not a requirement to create nine task windows.

## Activation and persistence

The user may add `three-departments six-ministries structure` or `three-departments and six-ministries profile` to the activation command, for example:

```text
my project commander, efficiency mode, three-departments six-ministries structure
```

When the calling task is already the active commander, a profile phrase alone reconciles the current organization. It must not create another commander or duplicate employees.

Copy or reconcile the [governance template](../assets/GOVERNANCE.template.md) at:

```text
.codex/project-commander/GOVERNANCE.md
```

Headquarters is the only writer. Keep it local and untracked by default and never store secrets, raw transcripts, or hidden reasoning.

## Three Departments: separate decision stages

| Function | Modern responsibility | Required output | Boundary |
| --- | --- | --- | --- |
| Secretariat / Zhongshu | Convert the user's objective into a definition of done, dependency graph, task contracts, risks, and options | reviewable proposal packet | does not approve its own high-risk proposal or expand execution scope |
| Chancellery / Menxia | Independently challenge scope, evidence, conflicts, Token budget, authority, and acceptance criteria | `APPROVED`, `RETURNED`, or `EVIDENCE NEEDED` with reasons | read-only by default; does not rewrite the user's objective under cover of review |
| Department of State Affairs / Shangshu | Decompose, schedule, dispatch, hand off, integrate, and reconcile only approved work | ministry mission packets, dispatch record, integration evidence | does not bypass review or silently change an approved objective |

The commander is the sole mediator and remains accountable for the complete result. The user remains the authority; historical labels confer no additional permission.

## Six Ministries: a functional pool

| Function | Modern responsibility | Typical Codex outcome |
| --- | --- | --- |
| Personnel / Libu | roster, role distinctness, capacity, titles, adoption, reassignment proposals | `ORG_CHART.md`, role contracts, gap/overlap reports |
| Revenue / Hubu | Token governance, model routing, context reuse, budgets, data and asset inventory | the unique Employee00 budget review, downgrade and stop-loss advice |
| Rites / Libu | documentation, UX/content standards, unified reporting, stakeholder-ready packaging | docs, standards, report package; external sending still needs authority |
| War / Bingbu | code, content, analysis, media, or other primary production | bounded verified deliverables with one writer per scope |
| Justice / Xingbu | independent QA, security, compliance, defect severity, evidence gates | read-only review, test evidence, risk ruling; remediation is a separate mission |
| Works / Gongbu | tooling, builds, automation, integration, environments, release preparation | build scripts, automation, integration artifacts; deployment still needs authority |

Employee00 remains unique and maps to the Revenue function. Never create a second Token Governance window. Ministries are functional labels, not mandatory manager tasks.

## Governance gates and mission lifecycle

1. **Propose:** Secretariat produces a packet with objective, done condition, dependencies, conflicts, candidate unique owners, budget, and validation.
2. **Review:** Chancellery independently returns `APPROVED`, `RETURNED`, or `EVIDENCE NEEDED`. The author of a high-risk proposal cannot be its final reviewer.
3. **Decide:** headquarters resolves objections or missing evidence. Only approved work becomes ready.
4. **Execute:** State Affairs maps approved work to one ministry function, one department, and one accountable production employee, then writes a compact handoff.
5. **Flow:** whenever an employee completes, headquarters validates it and immediately unlocks compatible downstream work without waiting for unrelated employees.
6. **Quality gate:** Justice or Chancellery reviews the evidence. A producer cannot independently approve its own high-risk deliverable.
7. **Close:** headquarters reconciles the ledger, governance record, and real validation surface before integrated reporting.

Every task-ledger row records its governance-gate state. `RETURNED` and `EVIDENCE NEEDED` work cannot be dispatched. A material scope, budget, or risk change requires re-review.

## Fold functions to fit the project

| Context | Suggested mapping | Constraint |
| --- | --- | --- |
| Small / Economy | 2–3 delivery windows combine compatible functions | high-risk proposal and independent validation stay separate |
| Balanced / Normal | 3–5 delivery windows separate proposal, production, and quality when useful | Employee00 does not count toward delivery WIP |
| Efficiency / complex | 5–7 delivery windows with actual ready work | never create nine mechanically; mark unused functions unstaffed |

An employee may carry compatible functions but still has one department, one primary accountable outcome, one writable scope, and one current primary mission. Incompatible combinations include high-risk proposer plus final reviewer, producer plus independent approver of the same output, and Token Governance plus production ownership.

## Reusable mechanisms from public GitHub Skills

This profile adapts general mechanisms rather than depending on repository-specific commands:

- [CCPM](https://github.com/automazeio/ccpm): explicit dependencies, parallelism, conflicts, ready/blocked state, and completion-triggered unlocking.
- [TDD Multi-Agent Orchestration](https://github.com/glebis/claude-skills/blob/main/tdd/SKILL.md): context isolation, phase separation, checkpoints, and failure stop conditions.
- [Code Review and Quality](https://github.com/addyosmani/agent-skills/blob/main/skills/code-review-and-quality/SKILL.md): independent review, evidence, and multidimensional quality gates.
- [Quality Playbook](https://github.com/github/awesome-copilot/blob/main/skills/quality-playbook/SKILL.md): role maps, phase entry/exit gates, written handoffs, and persistent progress records.

Codex sidebar task windows, headquarters-only ledger writing, and user authority remain the governing constraints.
