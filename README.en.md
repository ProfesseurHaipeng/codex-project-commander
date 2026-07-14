# Codex Project Commander

[中文说明](README.md) · [English](README.en.md)

An open-source Codex skill that turns a new or long-running local project into a commander-led workforce of named task windows. It first understands the project files, current state, and task history; then it pins one commander task and organizes separate sidebar tasks as employees.

> An employee is a persistent Codex task window in the same local project, not a subagent, terminal tab, or fictional role.

This repository contains two independently installable editions:

| Edition | Skill directory | Explicit invocation |
| --- | --- | --- |
| English | `skills/project-commander` | `$project-commander` |
| 中文版 | `skills/project-commander-zh` | `$project-commander-zh` |

Install one language edition to avoid overlapping implicit triggers.

## What it solves

Long-running projects become difficult to coordinate when research, implementation, tests, and decisions are mixed into one ever-growing task. Project Commander separates the work:

- The commander receives goals, decomposes work, dispatches missions, validates results, and reports one integrated outcome.
- Employee windows retain independent conversations, roles, task histories, and thread IDs.
- The user communicates with headquarters instead of repeating context to every worker.

## Core capabilities

- Inspect a new or established local Codex project before choosing its workforce.
- Build an evidence-backed map of project-owned files, Git state, documentation, source, tests, and recent work.
- Infer a project-specific commander archetype for product development, content operations, data analysis, film production, business operations, or Codex skill development.
- Create `.codex/project-commander/ORG_CHART.md` with one governance department and project-specific delivery departments derived from real deliverables.
- Optionally use a modern Three Departments and Six Ministries profile with proposal, independent review, approved execution, and functional ministry pools instead of mechanically creating nine windows.
- Give every employee window one department, primary accountable outcome, input/output contract, writable scope, and validation responsibility.
- Reuse and organize suitable existing task windows without destroying historical tasks.
- Create only the missing employee task windows under the same local project.
- Assign each employee a supported model profile and reasoning-effort baseline.
- Maintain one `Employee00 | Token Governance and Model Routing | project` task to prevent repeated reads, duplicate missions, and model overuse.
- Route work through Sol, Terra, and Luna policy tiers, or equivalent supported models when GPT-5.6 is unavailable.
- Persist the decomposed dependency graph and live queue in `.codex/project-commander/TASK_LEDGER.md` for recovery and completion audits.
- Validate and reassign an employee immediately after that employee finishes instead of waiting for a global batch barrier.
- Create one commander-thread heartbeat at first dispatch to discover employee completion, read and deduplicate reports, validate, and re-dispatch without assuming cross-window push delivery.
- Audit apparently idle windows on every heartbeat: resend missed work, dispatch compatible ready work, or let them rest when no real work exists.
- Offer Economy, Balanced/Normal, and Efficiency modes that tune WIP, model posture, checkpoint cadence, and Token use.
- Offer Launch-first, Balanced delivery, and Strict release postures so urgent deployments pass a minimum gate and defer nonblockers instead of looping on checks.
- Keep app validation non-adversarial: never attack the project app or proactively access unrelated sensitive data.
- When chat is the user's only API-key path, give one notice and proceed without echoing, forwarding, persisting, or repeatedly lecturing.
- Rename tasks after registration settles, verify exact titles, and pin the commander.
- Define mission scope, file ownership, forbidden actions, deliverables, validation, and completion criteria.
- Collect employee reports, inspect evidence, request corrections, and perform final validation.

## Install

### Ask Codex to install it

```text
Use $skill-installer to install skills/project-commander from:
https://github.com/ProfesseurHaipeng/codex-project-commander
```

### Install manually

```bash
git clone https://github.com/ProfesseurHaipeng/codex-project-commander.git
mkdir -p ~/.agents/skills
cp -R codex-project-commander/skills/project-commander ~/.agents/skills/project-commander
```

Restart Codex if the skill does not appear immediately.

### Install for Claude Code

The same Agent Skills-compatible package can be installed for Claude Code:

```bash
mkdir -p ~/.claude/skills
cp -R codex-project-commander/skills/project-commander ~/.claude/skills/project-commander
```

Codex discovers `.agents/skills`; Claude Code discovers `.claude/skills`. The core `SKILL.md`, `references/`, `assets/`, and `scripts/` remain portable, while `agents/openai.yaml` is OpenAI/Codex presentation metadata. Claude Code can load the general organization, Token, delivery, and credential rules, but sidebar employees still require Codex project-task tools and Claude subagents do not substitute for them. See [Codex Build skills](https://developers.openai.com/codex/skills/) and [Claude Code Skills](https://code.claude.com/docs/en/slash-commands).

## Use

The most reliable invocation is explicit:

```text
Use $project-commander to start the project commander in this Codex project.
```

You can also say:

```text
my project commander
project commander
commander
be the commander
start commander
```

You may combine activation with a mode:

```text
my project commander, economy mode
my project commander, balanced mode
my project commander, efficiency mode
```

For complex or high-risk projects, select the governance profile too:

```text
my project commander, efficiency mode, three-departments six-ministries structure
```

When headquarters is already active, send `economy mode`, `balanced mode`, `normal mode`, or `efficiency mode` alone to switch modes without creating another commander.
A profile phrase alone reconciles the current organization without creating another commander or duplicate employees.

Natural-language invocation uses implicit skill matching and is not guaranteed when many skills are installed. For a durable command mapping, merge [AGENTS.command-bridge.en.md](examples/AGENTS.command-bridge.en.md) into `~/.codex/AGENTS.md`.

## Existing-project onboarding

In a long-running project, the commander does not apply a fixed employee template. It:

1. inventories project-owned files and records exclusions;
2. reads applicable instructions, orientation docs, manifests, configuration, source, tests, Git state, and recent changes;
3. infers the project domain, lifecycle stage, objective, stack, risks, and validation surfaces;
4. produces a project-specific commander charter;
5. classifies current tasks as headquarters, structured employees, employee candidates, historical tasks, or ambiguous tasks;
6. reuses only clearly suitable tasks and preserves project history;
7. assigns supported model and reasoning baselines through follow-up role configuration;
8. renames, resolves, pins, and verifies the commander task.

“Read the whole project” means evidence-backed coverage. Dependencies, generated output, caches, binaries, VCS internals, and likely secrets are not blindly loaded into context.

## Token Governance and three-tier routing

Every roster contains one read-only control employee:

```text
Employee00 | Token Governance and Model Routing | project
```

It checks whether another employee already has the context, whether files or investigations are being repeated, whether missions overlap, whether tasks can be consolidated, and whether a stronger model is justified. It performs no production work and creates no subordinate workers.

| Tier | Model family | Default use |
| --- | --- | --- |
| 1 | Sol | complex software, cross-system debugging, ambiguous high-value work, high-risk final validation |
| 2 | Terra | data organization, research, documentation, standard implementation, routine analysis |
| 3 | Luna | extraction, classification, transformation, inventories, repetitive checks, high-volume runs |

Start with the lowest sufficient tier. Every Luna-to-Terra or Terra-to-Sol escalation needs a recorded reason. After two substantially identical failures, stop and change the method before increasing model strength or reasoning. When the surface does not expose actual token usage, report observable proxies instead of inventing counts.

## Continuous dispatch, task ledger, and modes

Headquarters first records the complete objective, definition of done, dependencies, owner, state, model, checkpoint, evidence, and next action in the local task ledger. Each employee runs one primary mission at a time; later work remains queued.

Whenever any employee finishes, headquarters validates it, releases ownership, unlocks dependencies, and immediately sends the next compatible ready mission. It waits for a group only when a real downstream dependency requires the whole group.

| Mode | Production WIP | Default posture |
| --- | --- | --- |
| Economy | 1–2 | Luna/Low first, sparse checkpoints |
| Balanced/Normal | 2–3 | Luna or Terra by mission, balanced default |
| Efficiency | 3–5 non-conflicting missions | completion-triggered reassignment, Terra for bounded work, Sol still requires evidence |

Headquarters is the ledger's only writer. The file stays local and untracked by default and stores no secrets, raw transcripts, or hidden reasoning. Progress monitoring uses evidence, promised checkpoints, blockers, and retries; it never labels a worker lazy without observable state.

## Three delivery postures

Delivery posture is independent of operating mode. For deployment, release, go-live, or production-change work, headquarters asks once whether speed or broader checks matters only when the user has not made the priority clear. It does not ask again when the user already said to launch first or deploy now.

| Delivery posture | Behavior |
| --- | --- |
| Launch-first | Pass the minimum launch gate, perform the authorized deployment, and move nonblockers to post-launch hardening |
| Balanced delivery | Run changed-path checks, build, and critical smoke before launch |
| Strict release | Run broader tests, security, compliance, or migration checks for high-impact or explicitly strict work |

Launch-first never defers applicable credential, authorization, payment, privacy, data-loss, legal/compliance, destructive-migration recovery, or critical-smoke gates. Otherwise it reuses valid evidence, reruns only affected checks, prefers fix-forward, and avoids repeated rollback and full-suite loops for minor defects. A posture phrase never expands deployment authority.

## Project organization system

After reconnaissance, headquarters creates the organization before creating employees:

```text
Commander | project
├─ Governance department
│  └─ Employee00 | Token Governance and Model Routing | project
└─ Project-specific delivery departments
   ├─ Employee01 | distinct role | project
   ├─ Employee02 | distinct role | project
   └─ EmployeeNN | distinct role | project
```

Departments and roles follow the actual deliverables. A software project may use product planning, architecture and implementation, and quality and release; content may use research and strategy, editorial production, and visual/distribution QA; data may use data quality, analysis/modeling, and reporting/validation.

Headquarters manages employees directly and does not create department-manager windows by default. Every work item belongs to one department and one production owner. Headquarters mediates cross-department handoffs using accepted outputs and compact evidence. The organization chart defines who owns what; the task ledger tracks what is happening now.

### Optional: modern Three Departments and Six Ministries governance

When selected, headquarters also creates `.codex/project-commander/GOVERNANCE.md`. The Secretariat function turns the goal into a reviewable proposal, the Chancellery independently returns `APPROVED`, `RETURNED`, or `EVIDENCE NEEDED`, and State Affairs dispatches only approved work into six functional pools: organization, Token/resources, standards/communication, production, quality/risk, and engineering/infrastructure.

These functions are foldable, not nine fixed windows. A small project may map them onto 2–3 delivery employees, while high-risk proposal authors remain separate from final reviewers and producers remain separate from independent quality adjudicators. The unique Employee00 maps to the Revenue function and stays read-only.

The design adapts dependency/conflict queues from [CCPM](https://github.com/automazeio/ccpm), context isolation from [TDD Multi-Agent Orchestration](https://github.com/glebis/claude-skills/blob/main/tdd/SKILL.md), independent evidence gates from [Code Review and Quality](https://github.com/addyosmani/agent-skills/blob/main/skills/code-review-and-quality/SKILL.md), and phase gates plus written handoffs from [Quality Playbook](https://github.com/github/awesome-copilot/blob/main/skills/quality-playbook/SKILL.md).

## Operating model

```text
User
  ↓ communicates through one task
Commander | project
  ├─ Employee00 | Token Governance and Model Routing | project
  ├─ Employee01 | product and requirements | project
  ├─ Employee02 | research | project
  ├─ Employee03 | architecture | project
  ├─ Employee04 | implementation | project
  └─ Employee05 | testing and validation | project
```

Separate tasks do not push messages to one another automatically, and desktop notifications do not write reports into headquarters. The commander creates one `Commander Watchdog | project` heartbeat attached to itself, using a low, normal, or fast cadence according to the operating mode. It reads only non-terminal employees in the ledger, deduplicates new reports, validates them, updates the ledger, and immediately re-dispatches. It pauses when the queue ends or user input is required.

The watchdog also verifies whether an apparently idle window is truly idle. It first rules out unprocessed completion, a missed mission message, still-running work, pending review, and dependency blockers. When role-compatible, dependency-complete, non-conflicting work fits the WIP limit, it dispatches immediately. Otherwise it marks the employee resting without standby chatter or filler work.

If the current Codex surface lacks task-heartbeat or Scheduled capability, headquarters can only monitor at low frequency while its current turn stays active. It reports that cross-turn automatic handoff cannot be guaranteed instead of pretending employees can push results.

## Safety boundaries

- Creating, editing, installing, validating, packaging, reviewing, or publishing this skill never authorizes operations on real project tasks.
- Only an explicit command inside the intended target project authorizes employee-window setup.
- Internal subagents never substitute for visible employee task windows.
- One employee owns each writable file or overlapping subsystem at a time.
- Existing tasks are not archived, replaced, or taken over without explicit user authorization.
- The skill does not independently authorize publishing, deployment, purchases, external messages, production changes, or secret access.
- App, website, service, and API validation defaults to builds, normal flows, tests, static checks, dependency advisories, and test data. It does not run attacks, exploits, brute force, credential stuffing, malicious payloads, denial of service, port scans, penetration tests, or red-team traffic.
- It does not proactively read unrelated `.env` files, private keys, cookies, real-user, payment, or health data, and never writes sensitive values into ledgers, employee messages, source, Git, logs, or reports.
- API keys use an environment variable or Secret field first. If the user cannot use another path or insists on chat, headquarters gives one concise notice and proceeds without echoing, forwarding, persisting, or repeatedly lecturing.

OpenAI still recommends environment variables and prohibits embedding keys in clients or repositories. The chat fallback is not authorization to share or persist a key; it only avoids repeatedly blocking a user who has no other input path. See [OpenAI API key safety](https://help.openai.com/en/articles/5112595-best-practices-for-api-key-safety).

## Repository structure

```text
.
├── README.md                    # 中文
├── README.en.md                 # English
├── LICENSE
├── docs/
├── examples/
│   ├── AGENTS.command-bridge.md
│   └── AGENTS.command-bridge.en.md
└── skills/
    ├── project-commander/       # English skill
    └── project-commander-zh/    # 中文 SKILL
```

## Official references

- [Build skills](https://learn.chatgpt.com/docs/build-skills)
- [Custom instructions with AGENTS.md](https://learn.chatgpt.com/docs/agent-configuration/agents-md)
- [Projects, chats, and tasks](https://learn.chatgpt.com/docs/projects)
- [Models](https://learn.chatgpt.com/docs/models)

## License

[MIT](LICENSE)
