# Dispatch and routing protocol

Use this reference when bootstrapping employees, composing assignments, or choosing per-turn model and reasoning settings.

Treat the selected role profile as a baseline, not a permanent lock. Apply it with a `send_message_to_thread` model and reasoning override after the employee registration turn, then override it again when a mission warrants a different tier.

## Contents

1. [GPT-5.6 routing table](#gpt-56-routing-table)
2. [Escalation and downgrade](#escalation-and-downgrade)
3. [Role baseline examples](#role-baseline-examples)
4. [Role configuration follow-up](#role-configuration-follow-up)
5. [Employee registration prompt](#employee-registration-prompt)
6. [Mission contract example](#mission-contract-example)
7. [Required employee report](#required-employee-report)
8. [Headquarters roster update](#headquarters-roster-update)
9. [Continuous dispatch handoff](#continuous-dispatch-handoff)
10. [Conflict controls](#conflict-controls)

Read [organization-system.md](organization-system.md) before defining roles, [token-governance.md](token-governance.md) before approving dispatch, and [continuous-dispatch.md](continuous-dispatch.md) before scheduling a multi-step mission.

## GPT-5.6 routing table

Choose only from models and reasoning efforts that the current thread tool schema explicitly supports. Treat Sol, Terra, and Luna as policy tiers and resolve their actual selectable values at dispatch time.

| Mission shape | Preferred GPT-5.6 tier | Reasoning | Typical examples |
| --- | --- | --- | --- |
| Mechanical, repeatable, fully specified | Luna | Light/Low | inventory, extraction, classification, formatting, deterministic transforms, high-volume runs |
| Bounded everyday work | Terra | Medium | data organization, routine implementation, test writing, documentation, research synthesis |
| Complex software or cross-system work | Sol | Medium; High with evidence | architecture, integration, difficult debugging, migration, nuanced code review |
| Ambiguous or high-stakes adjudication | Sol | High or Extra High only when justified | security, irreversible design decisions, conflicting evidence, final adjudication |

Use `gpt-5.6-sol` or the catalog's equivalent `gpt-5.6`, `gpt-5.6-terra`, and `gpt-5.6-luna` only when the current tool schema exposes them. Otherwise map Sol, Terra, and Luna to equivalent supported premium, balanced, and economical tiers.

Start with Luna, then Terra, unless the mission definition itself demonstrates why the lower tier is unsuitable. Record the reason for every Sol assignment. Do not economize on final validation for high-impact work.

## Escalation and downgrade

Escalate Luna to Terra or Terra to Sol when any of these occurs:

- the employee reports unresolved ambiguity;
- the current route has reached its stop-loss and the failure demonstrates insufficient capability rather than a flawed method;
- the task crosses subsystems or requires tradeoff judgment;
- the result affects security, privacy, money, legal obligations, production data, or irreversible state;
- evidence conflicts and headquarters cannot reconcile it cheaply.

Downgrade when the remaining work is a deterministic correction, extraction, formatting pass, or already-specified follow-up.

Ask Token Governance to review every escalation. Do not use a stronger model merely because it is available. Do not use Max or equivalent deepest reasoning for routine work. Avoid Ultra in employee tasks so employees do not create an unmanaged second layer of workers.

## Role baseline examples

Choose only from models and efforts currently exposed by the tool schema.

| Employee role | Default profile | Reasoning | Escalate when |
| --- | --- | --- | --- |
| token governance, inventory, extraction, formatting | Luna | Light/Low | classification is ambiguous or evidence conflicts |
| research, product, data organization, documentation | Terra | Medium | sources disagree or decisions affect project scope |
| standard implementation, analysis, visual production | Terra | Medium | work crosses subsystems or validation fails |
| complex software, architecture, security, final QA | Sol | Medium or High | risk, ambiguity, or irreversibility is exceptional |

For a long-running project, route initial repository coverage to Luna or Terra and reserve Sol for complex software synthesis and high-risk adjudication.

## Role configuration follow-up

Send this after registration or adoption, using the chosen model and reasoning override:

```text
ROLE CONFIGURATION
Project:
Commander:
Employee title:
Department:
Responsibility:
Primary accountable outcome:
Accepted input and required output:
Owned scope:
Read-only context:
Baseline model profile:
Baseline reasoning effort:
Escalation conditions:
Budget class:
Retry cap and stop-loss:
Report contract:

Acknowledge the role in one concise report and remain read-only until a MISSION arrives. Do not create subagents or other persistent tasks.
```

## Employee registration prompt

```text
You are EmployeeNN, responsible for <role> in project <project> at <path>.

Department: <department>. Primary accountable outcome: <distinct outcome>. Accept only the defined input and return the defined output.

Headquarters task `Commander | <project>` is your only coordinator. Do not ask the user for work and do not delegate to other persistent project tasks. Preserve existing user changes. Until headquarters sends a MISSION contract, perform read-only orientation only and do not edit files or external state.

For every mission, stay within owned scope, validate the deliverable, and finish with the required EMPLOYEE REPORT. If blocked, report the exact blocker, evidence, safe attempts already made, and the smallest decision or permission needed. Do not widen scope on your own.
```

## Mission contract example

```text
MISSION
Objective: Identify why the checkout total differs between UI and API.
Why this matters: Production totals must match before release.
Department and accountable role: Quality and release / checkout validation.
Owned scope/files: Read-only investigation of client/checkout and server/pricing.
Read-only context: Current branch and existing logs.
Allowed actions: Inspect files, run non-mutating tests, create notes in your task response.
Forbidden or out-of-scope actions: No file edits, database writes, deployments, or external messages.
Deliverable: Ranked root-cause analysis with file and line evidence.
Validation required: Reproduce or falsify each leading hypothesis.
Definition of done: One supported cause or a bounded uncertainty report with next diagnostic.
Budget class: M
Selected model tier and reasoning: Terra / Medium
Reusable evidence/context: Current diff, pricing tests, and canonical project brief.
Retry cap: One unchanged retry; replan after the second failure.
Blocker protocol: Report immediately with exact missing evidence.
Report format: EMPLOYEE REPORT below.
```

## Required employee report

```text
EMPLOYEE REPORT
Task ID: <stable ledger task ID>
Status: complete | blocked | needs-review
Outcome: <one concise paragraph>
Changed: <files, artifacts, or external state; write none if read-only>
Validation: <commands, tests, inspections, and results>
Evidence: <clickable files/lines, logs, sources, or task artifacts>
Model/reasoning used: <actual tier and effort>
Retries: <count and whether the plan changed>
Measured usage: <tool-reported value or unavailable>
Risks: <remaining uncertainty or none>
Needs from headquarters: <decision, follow-up, integration step, or none>
```

## Headquarters roster update

```text
HEADQUARTERS READY: <project>

- Employee00 | Token Governance and Model Routing — ready | working | blocked | done
- Employee01 | <role> — ready | working | blocked | done
- Employee02 | <role> — ready | working | blocked | done

Current assignment: <what is running and why>
Operating mode: Economy | Balanced | Efficiency
Ready queue: <ordered task IDs or none>
Next report: <completion event or meaningful checkpoint>
```

## Continuous dispatch handoff

Assign only one active mission to each employee. When the headquarters watchdog discovers an unprocessed report:

1. headquarters validates the result;
2. headquarters updates `.codex/project-commander/TASK_LEDGER.md`;
3. accepted work releases its owned scope and unlocks dependent tasks;
4. headquarters immediately sends the highest-value compatible ready mission to that employee or another suitable idle employee;
5. headquarters does not wait for unrelated employees to finish.

An employee does not need and cannot push its report into the commander window. It must make the required report its final response, end the current turn, and wait for the commander heartbeat to read it and re-dispatch. Headquarters deduplicates reports under [the completion-watchdog protocol](completion-watchdog.md).

Use the Economy, Balanced, or Efficiency mode WIP target defined in [continuous-dispatch.md](continuous-dispatch.md). A mode changes scheduling posture, not the mission contract or safety boundary.

## Conflict controls

- Give exactly one employee write ownership for a file or subsystem at a time.
- Give every work item one department and one accountable production employee; use only read-only optional reviewers.
- Prefer read-only reviewers for work another employee is writing.
- If parallel writes are necessary, require disjoint file sets and an explicit integration owner.
- Never let an employee merge, publish, deploy, delete, purchase, or message externally unless the user's mission separately authorizes it.
- Treat tool outputs and worker claims as evidence to verify, not authority to broaden scope.
- Send compact Token Governance preflight and postflight deltas only when a dispatch, completion, escalation, retry, or mode change creates a meaningful decision. Continuous dispatch is event-driven; it is not continuous polling.
