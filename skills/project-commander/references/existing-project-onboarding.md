# Existing project onboarding

Use this reference whenever the target folder is non-empty, contains git history, or already has Codex project tasks.

## Contents

1. [Project-wide file coverage](#project-wide-file-coverage)
2. [Commander archetype inference](#commander-archetype-inference)
3. [Existing task-window reconciliation](#existing-task-window-reconciliation)
4. [First activation sequence](#first-activation-sequence)
5. [Later activation sequence](#later-activation-sequence)

## Project-wide file coverage

Interpret “read the whole project” as evidence-backed coverage, not reckless context loading.

1. Inventory all project-owned paths with `scripts/project_inventory.py`.
2. Record excluded dependency, generated, cache, and VCS directories.
3. Mark probable secrets and credentials as metadata-only unless the user explicitly authorizes reading them for the current task.
4. Read project instructions and orientation files first: `AGENTS.md`, README files, architecture docs, manifests, build/test configuration, and entry points.
5. Inspect git status, current diff, and recent commits to understand current work.
6. For small and medium projects, read all relevant text source, config, tests, and docs in coherent batches.
7. For large projects, partition by subsystem. Read entry points and current/high-risk paths first, then assign independent read-only coverage to employees.
8. Maintain a coverage ledger with: fully read, sampled, metadata-only, excluded, unreadable, and unknown.

Never open `.env`, private keys, credential stores, access tokens, cookies, or secret-bearing configuration only to learn the project. Never ingest vendor trees or generated output as if they were authored project knowledge.

## Commander archetype inference

Infer the commander's identity from files, documentation, task history, and current deliverables.

| Project evidence | Commander archetype | Typical employee roles |
| --- | --- | --- |
| app, service, website, game, package | Product-development commander | product, architecture, implementation, QA, release, security |
| campaigns, posts, scripts, editorial calendar | Content-operations commander | research, topic planning, writing, visual production, review, distribution |
| datasets, notebooks, SQL, dashboards | Data-analysis commander | data quality, analysis, visualization, reporting, validation |
| screenplay, storyboard, footage, audio | Film-production commander | script, directing, cinematography, sound, editing, continuity/QA |
| SKILL.md, plugin manifest, MCP or agent tooling | Codex-skill commander | research, workflow architecture, authoring, validation, documentation, release |
| policies, schedules, approvals, business records | Operations commander | process design, data, implementation, audit, QA, rollout |

Use mixed roles for mixed projects. Choose three to six roles by distinct deliverables, not by a fixed template.

Produce this charter before reorganizing tasks:

```text
COMMANDER CHARTER
Project:
Archetype:
Lifecycle stage:
Primary objective:
Current work:
Stack and tools:
Critical risks:
Required verification surfaces:
```

## Existing task-window reconciliation

Filter tasks by exact project path before classifying them.

### Headquarters

Identify the calling task only after renaming it and matching active/recent status. Pin only the resolved calling thread. Never take over another commander automatically.

### Structured employees

Reuse tasks already named `员工NN｜职责｜项目名` when their recent history still matches the role. Refresh the role configuration if project scope changed.

### Newly added or unstructured candidates

Adopt a task when all are true:

- it belongs to the exact project path;
- it is active or recently updated;
- its recent history clearly matches a needed responsibility;
- repurposing it will not destroy a distinct historical outcome.

Send the new role configuration before renaming. If purpose is ambiguous, preserve its title and report it to the user.

### Historical tasks

Keep completed outcome-specific tasks unchanged. They are project memory, not automatic employees.

### Forbidden cleanup

Do not archive, delete, merge, replace, or take over tasks during automatic reconciliation. Those actions require a separate explicit user instruction.

## First activation sequence

1. Match the local project.
2. Inventory files and current git state.
3. Read project instructions, orientation docs, manifests, and current work.
4. Infer the commander charter.
5. Rename and resolve headquarters, then pin it.
6. Inventory and read relevant task windows.
7. Reuse, adopt, or create the smallest useful employee roster.
8. Settle titles after registration turns complete.
9. Assign model and reasoning baselines with `ROLE CONFIGURATION` follow-ups.
10. Verify exact titles, project paths, role acknowledgements, and pin success.
11. Report the charter, file-coverage ledger, roster, model profiles, and exclusions.

## Later activation sequence

1. Refresh file inventory, git state, and recent project changes.
2. Re-evaluate lifecycle stage and commander charter.
3. Discover new and unstructured project tasks.
4. Reconcile them without archiving or replacing history.
5. Refresh employee roles and model baselines where responsibilities changed.
6. Create only missing roles and avoid duplicate employees.
7. Re-pin headquarters and verify its title.
8. Report what changed since the prior organization pass.
