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
- Reuse and organize suitable existing task windows without destroying historical tasks.
- Create only the missing employee task windows under the same local project.
- Assign each employee a supported model profile and reasoning-effort baseline.
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

## Use

The most reliable invocation is explicit:

```text
Use $project-commander to start the project commander in this Codex project.
```

You can also say:

```text
my project commander
```

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

## Operating model

```text
User
  ↓ communicates through one task
Commander | project
  ├─ Employee01 | product and requirements | project
  ├─ Employee02 | research | project
  ├─ Employee03 | architecture | project
  ├─ Employee04 | implementation | project
  └─ Employee05 | testing and validation | project
```

Separate tasks do not push messages to one another automatically. Operationally, employees finish with a standard report and the commander reads, validates, and integrates their results.

## Safety boundaries

- Creating, editing, installing, validating, packaging, reviewing, or publishing this skill never authorizes operations on real project tasks.
- Only an explicit command inside the intended target project authorizes employee-window setup.
- Internal subagents never substitute for visible employee task windows.
- One employee owns each writable file or overlapping subsystem at a time.
- Existing tasks are not archived, replaced, or taken over without explicit user authorization.
- The skill does not independently authorize publishing, deployment, purchases, external messages, production changes, or secret access.

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
