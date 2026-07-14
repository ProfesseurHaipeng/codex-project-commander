# Token governance and cost protection

Use this protocol for every roster and mission. Optimize for the lowest token and model cost that still satisfies the user's acceptance criteria. Savings never justify skipping required validation or silently lowering quality below the requested standard.

## Contents

1. [Standing department](#standing-department)
2. [Measure honestly](#measure-honestly)
3. [Three-tier model policy](#three-tier-model-policy)
4. [Mission budget ledger](#mission-budget-ledger)
5. [Pre-dispatch review](#pre-dispatch-review)
6. [Context-reuse rules](#context-reuse-rules)
7. [Stop-loss and escalation](#stop-loss-and-escalation)
8. [Token Governance report](#token-governance-report)

## Standing department

Maintain one read-only employee:

```text
Employee00 | Token Governance and Model Routing | <project>
```

This employee audits plans and reports to headquarters. It does not perform production work, send assignments to other employees, or create more workers.

Headquarters remains accountable for every routing and stop decision. Do not add a second supervisor layer.

## Measure honestly

Use actual token, credit, model, reasoning, or remaining-context signals only when the current Codex surface or callable tool exposes them. Examples may include session status, usage views, or tool-returned usage fields.

When exact usage is unavailable:

- record model family, reasoning effort, number of turns, repeated reads, duplicate missions, and retry count as observable proxies;
- label projections as `estimated`, never `measured`;
- never invent token counts, prices, savings percentages, or account limits.

## Three-tier model policy

Resolve the actual selectable model values from the current task-tool schema. Use the named GPT-5.6 family when exposed; otherwise map each tier to the closest supported equivalent.

| Cost tier | Preferred family | Default reasoning | Use for |
| --- | --- | --- | --- |
| Tier 1: protected high capability | Sol | Medium; High only with evidence | complex software architecture, cross-system debugging, ambiguous high-value work, security-sensitive review, final high-risk adjudication |
| Tier 2: balanced daily work | Terra | Medium | data organization, research synthesis, documentation, standard implementation, routine analysis, integration checks |
| Tier 3: efficient volume work | Luna | Light/Low | extraction, classification, transformation, inventory, repetitive checks, structured summaries, clear high-volume runs |

Do not use Sol merely because it is available. Do not use Terra when a deterministic Luna mission has a clear schema and acceptance check. Do not use Luna for work whose ambiguity or failure cost exceeds the likely savings.

Run the Token Governance employee itself on Luna with Light/Low reasoning by default. Move it to Terra only when the routing decision contains genuine ambiguity or conflicting evidence. It normally never needs Sol.

Use Max only after headquarters records why High is insufficient. Never select Ultra automatically; it may add unmanaged delegation and weaken the one-commander structure.

## Mission budget ledger

Create one concise entry before each dispatch:

```text
TOKEN BUDGET ENTRY
Mission:
Owner:
User value:
Duplicate check:
Reusable context:
Smallest sufficient deliverable:
Proposed model tier:
Proposed reasoning:
Why lower tier may fail:
Stop-loss:
Usage telemetry available: yes | no
Estimate or measured baseline:
Token Governance verdict: approve | downgrade | consolidate | stop | replan
```

Update it after completion:

```text
TOKEN BUDGET RESULT
Turns/retries:
Repeated reads avoided:
Duplicate missions prevented:
Model or effort change:
Measured usage: <only if exposed> | unavailable
Quality/validation result:
Reusable evidence added:
Next saving action:
```

Keep the ledger in headquarters or the Token Governance task response unless the user asks for a durable project artifact. Do not add noisy tracking files to the project by default.

## Pre-dispatch review

Token Governance checks:

1. Does an existing employee already hold the relevant context?
2. Has the same question already been answered or tested?
3. Can headquarters finish the work cheaper than opening another task?
4. Can one mission replace several overlapping missions?
5. Can the employee receive file pointers and a delta instead of full copied context?
6. Is the deliverable smaller than the prompt without losing acceptance evidence?
7. Is Luna sufficient? If not, is Terra sufficient?
8. Is the requested reasoning effort higher than the task needs?
9. What exact condition stops retries or triggers escalation?

Reject or consolidate a mission when these questions reveal avoidable duplication.

## Context-reuse rules

- Maintain one concise project brief and evidence index in headquarters.
- Refresh by Git diff, modification time, inventory delta, or targeted search before rereading unchanged files.
- Send employees only the role-relevant charter slice, changed facts, exact file pointers, and acceptance criteria.
- Keep follow-up work in the employee that already owns the context unless separation materially improves quality or safety.
- Prefer targeted search, batched reads, and deterministic scripts over repeated open-ended exploration.
- Do not paste raw employee transcripts into another task. Send a distilled result plus evidence pointers.
- Do not ask several employees the same question unless independent verification is explicitly valuable; state the distinct method each reviewer must use.
- Cap routine reports to the outcome, changes, validation, evidence, risk, and next action.
- Poll only at meaningful checkpoints. Idle polling spends turns without producing evidence.

## Stop-loss and escalation

Stop the current route when:

- two attempts fail for substantially the same reason;
- a worker rereads the same unchanged evidence without a new hypothesis;
- more context is being collected without changing the decision;
- multiple employees converge on duplicate work;
- the deliverable grows beyond what the user needs.

After stopping:

1. preserve the evidence already collected;
2. state the failed assumption;
3. reduce or reformulate the mission;
4. choose a different method before choosing a stronger model;
5. escalate Luna to Terra or Terra to Sol only when the failure demonstrates missing capability, ambiguity handling, or validation depth.

## Token Governance report

```text
TOKEN GOVERNANCE REPORT
Status: efficient | watch | waste-detected | stopped
Mission reviewed:
Duplicate work:
Context reuse:
Recommended model/reasoning:
Downgrade or escalation:
Stop-loss:
Measured usage: <value and source> | unavailable
Estimated signals:
Expected saving action:
Quality risk:
Headquarters decision needed:
```

Keep recommendations concise. The goal is to prevent waste, not to create a second stream of long supervisory commentary.
