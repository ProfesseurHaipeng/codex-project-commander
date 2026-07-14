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
4. Follow the host-declared project instruction hierarchy first, treating it as read-only policy, then inspect README files, architecture docs, manifests, build/test configuration, and entry points.
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

Use mixed roles for mixed projects. Choose one to six delivery roles by distinct deliverables, operating mode, and ready work, not by a fixed template or quota.

Add `Employee00 | Token Governance and Model Routing | project` to every archetype. It is a mandatory read-only control role and does not replace a deliverable-owning employee.

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

Reuse tasks already named `EmployeeNN | role | project` when their recent history still matches the role. Refresh the role configuration if project scope changed.

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
5. Read and reconcile `.codex/project-commander/ORG_CHART.md`, or create it from the bundled template.
6. Read and reconcile `.codex/project-commander/TASK_LEDGER.md`, or create it from the bundled template when work is multi-step.
7. Rename and resolve headquarters, then pin it.
8. Inventory and read relevant task windows.
9. Reuse or create the single Token Governance employee before other expensive dispatches.
10. Ask Token Governance to identify duplicate departments and overlapping roles, then propose the lowest sufficient model tier for each distinct role; headquarters applies the decision.
11. Reuse, adopt, or create the smallest useful deliverable-owning roster and map each employee to one department and one primary outcome.
12. Settle titles after registration turns complete.
13. Assign model, reasoning, token budget, and stop-loss baselines with `ROLE CONFIGURATION` follow-ups.
14. Verify exact titles, project paths, role acknowledgements, organization mapping, and pin success.
15. Report the charter, file coverage, organization chart, task-ledger mode and queue, roster, model profiles, token controls, and exclusions.

## Later activation sequence

1. Refresh file inventory, git state, and recent project changes.
2. Re-evaluate lifecycle stage and commander charter.
3. Discover new and unstructured project tasks.
4. Reconcile the organization chart with current deliverables and task windows without archiving or replacing history.
5. Resolve department gaps, role overlaps, and obsolete responsibilities before changing titles.
6. Reconcile every non-terminal task-ledger entry with the current organization, files, and employee windows, then recompute the ready queue.
7. Ask Token Governance to audit repeated reads, duplicate missions, overlapping roles, retries, and model overuse since the prior pass.
8. Refresh employee roles and model baselines where responsibilities changed.
9. Create only missing roles and avoid duplicate employees.
10. Re-pin headquarters and verify its title.
11. Resume continuous dispatch and report organization changes, immediate reassignments, and prevented Token waste.
