# Project organization system

Use this protocol after reconnaissance and before creating, adopting, or reassigning employee task windows. The organization chart defines who owns each kind of outcome; the task ledger defines what is currently running.

## Contents

1. [Create the organization chart](#create-the-organization-chart)
2. [Use a two-layer structure](#use-a-two-layer-structure)
3. [Design departments from deliverables](#design-departments-from-deliverables)
4. [Define every employee role](#define-every-employee-role)
5. [Route work and handoffs](#route-work-and-handoffs)
6. [Scale by operating mode](#scale-by-operating-mode)
7. [Reconcile long-running projects](#reconcile-long-running-projects)
8. [Optional Three Departments and Six Ministries governance](#optional-three-departments-and-six-ministries-governance)

## Create the organization chart

Copy [../assets/ORG_CHART.template.md](../assets/ORG_CHART.template.md) to:

```text
.codex/project-commander/ORG_CHART.md
```

Headquarters is the only writer. Keep the file local and untracked by default. Do not change `.gitignore` or commit the chart without user authorization. Store no secrets, raw transcripts, hidden reasoning, or copied file contents.

Create or update the chart when:

- the commander first understands the project;
- the project phase, primary deliverables, or risk profile changes;
- an employee is created, adopted, reassigned, or released;
- two roles overlap or a deliverable has no owner;
- the operating mode changes the useful workforce size.

## Use a two-layer structure

Use this hierarchy:

```text
Commander | project
├─ Governance department
│  └─ Employee00 | Token Governance and Model Routing | project
└─ Project-specific delivery departments
   ├─ Employee01 | distinct role | project
   ├─ Employee02 | distinct role | project
   └─ EmployeeNN | distinct role | project
```

Do not create department-head task windows by default. The commander directly coordinates every employee. Add another management layer only when the user explicitly requests it and its coordination value clearly exceeds its Token cost.

Departments are organizational groups, not substitute employees. Every real employee remains a visible, persistent Codex project task window.

## Design departments from deliverables

Create the smallest set of departments that covers distinct outcome lanes. Adapt names and roles to project evidence.

| Project archetype | Typical delivery departments | Distinct outcome lanes |
| --- | --- | --- |
| Product/software | Product and planning; architecture and implementation; quality and release | requirements, design/code, tests/integration/release checks |
| Content operations | Research and strategy; editorial production; visual and distribution QA | source-backed topics, drafts/assets, review/channel packaging |
| Data analysis | Data quality; analysis and modeling; reporting and validation | trusted inputs, calculations, charts/reports and independent checks |
| Film/media | Development; production; post-production and continuity | script/storyboard, camera/audio/assets, edit/continuity/master QA |
| Codex skill/plugin | Research and workflow design; skill authoring; validation and publication | source rules, SKILL/resources, validation/docs/release |
| Business operations | Process and policy; data and execution; audit and rollout | approved process, operating records/implementation, controls/launch |

For mixed projects, create mixed departments around deliverables rather than copying a fixed template. Do not create a department with no ready or expected work.

## Define every employee role

Give each employee exactly one primary role. Record:

- department and employee title;
- primary outcome owned;
- accepted input and required output;
- writable scope and read-only dependencies;
- validation responsibility;
- baseline model, reasoning, and escalation conditions;
- one current mission capacity;
- backup or reassignment rule.

Apply the distinctness test before creating or adopting a worker:

1. Does this employee own an outcome that no existing employee owns?
2. Is its writable scope disjoint from every concurrent writer?
3. Can headquarters determine when its work is complete?
4. Is a separate persistent context worth the Token and coordination cost?

If any answer is no, consolidate or redesign the role. Never create two employees with the same primary outcome merely to keep both busy.

An employee may perform related secondary duties in Economy mode, but record only one primary accountable outcome and never combine conflicting writer and independent-review roles on the same work item.

## Route work and handoffs

Map every task-ledger row to one department and one accountable employee. Optional read-only reviewers may be named, but there is only one production owner.

Use headquarters-mediated handoffs:

1. the source employee completes and validates its owned output;
2. headquarters verifies the evidence and updates the task ledger;
3. headquarters packages only the accepted output, changed facts, file pointers, and acceptance criteria;
4. headquarters sends that compact handoff to the destination employee;
5. the destination employee acknowledges the input and begins one bounded mission.

Employees do not directly reassign one another or change the organization chart. Cross-department decisions, conflicts, and integration remain with headquarters.

## Scale by operating mode

Count delivery employees separately from the mandatory Token Governance employee.

| Mode | Typical active delivery roster | Organization posture |
| --- | --- | --- |
| Economy | 1–2 employees | combine adjacent duties carefully; keep independent validation when risk requires it |
| Balanced | 2–4 employees | separate planning/production/validation where useful |
| Efficiency | 3–6 employees | use more distinct outcome lanes, but only for ready, non-conflicting work |

Roster size is a ceiling guided by useful work, not a quota. WIP limits in the continuous-dispatch protocol still control simultaneous missions. A larger roster may include standby employees with valuable retained context.

## Reconcile long-running projects

When an organization chart already exists:

1. compare it with current deliverables, project phase, files, and task windows;
2. preserve healthy roles and stable employee titles;
3. map newly added task windows only when their histories clearly match an uncovered role;
4. mark gaps, overlaps, obsolete roles, and ambiguous windows;
5. reassign roles through headquarters before changing titles;
6. never archive, replace, or take over a historical task without explicit user authorization;
7. update both the organization chart and task ledger before new dispatch.

Do not churn the organization during an active mission unless a conflict, blocker, or changed objective makes the current structure invalid.

## Optional Three Departments and Six Ministries governance

When the user explicitly selects the profile, follow [Modern Three Departments and Six Ministries Governance](three-departments-six-ministries.md) in full and create `.codex/project-commander/GOVERNANCE.md`.

The organization chart still answers where each employee belongs and which outcome it owns. The governance record answers who proposed the work, who independently reviewed it, whether it is approved, how it was handed off, and who performed the quality gate. Never expand the profile mechanically into nine task windows. Combine compatible functions by project size and mark unused functions unstaffed; keep high-risk proposal and final review, production and independent quality adjudication, and Token Governance and production ownership separate.
