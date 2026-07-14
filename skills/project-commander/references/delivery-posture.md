# Delivery posture and launch-first protocol

Use this protocol for missions that include deployment, release, go-live, launch, or production changes. It is independent of operating mode: operating mode controls WIP, model cost, and Token use; delivery posture controls verification depth, launch order, and incident response.

## Select a posture

| Posture | Goal | Default verification |
| --- | --- | --- |
| Launch-first | Reach a usable live result quickly | Pass the minimum launch gate, deploy, then move non-blockers to post-launch hardening |
| Balanced delivery | Balance speed and reliability | Changed-path checks, build, and critical smoke before deployment |
| Strict release | Reduce high-impact risk first | Broader test, security, compliance, performance, or migration checks before deployment |

When the user clearly says `launch first`, `deploy now`, or equivalent, select Launch-first without asking again. Select Strict release when the user explicitly requests full verification, compliance review, or strict release. If urgency would materially change the plan and is unclear, ask once:

> Should this prioritize going live quickly, or completing broader checks first?

If the user does not answer and a safe reversible path exists, state the assumption and use Balanced delivery. A posture phrase changes the plan but never expands authority; deployment, publication, or production changes still require explicit user authorization.

## Minimum launch gate

Run only applicable checks related to the change, not an unrelated full audit:

- the artifact builds or starts and one critical-path smoke check passes;
- no known secret or credential is exposed;
- an authentication or authorization sanity check passes when relevant;
- applicable payment, privacy, data-loss, and legal/compliance critical risks are not deferred;
- destructive database or schema changes have a verified backup, restore, or equivalent recovery path;
- a practical fix-forward path exists and rollback capability is available when necessary;
- the user explicitly authorized this deployment or launch.

When an applicable gate fails, report the concrete blocker without expanding into a project-wide security audit. After fixing it, rerun only affected checks.

## Deferrable work

Usually defer exhaustive suites unrelated to the changed path, noncritical refactors, low-severity warnings, optional documentation, visual edge cases, nonblocking performance polish, and broad hardening scans unrelated to this launch.

Record each deferred item in the ledger's Post-launch hardening table with severity, deferral reason, owner, evidence, trigger or due date, and next action. Batch related low-risk items instead of creating a separate employee or immediate mission for every small issue.

## Fix forward and rollback

Prefer fix-forward for reversible, noncritical defects. Do not repeatedly roll back and redeploy for minor issues. Roll back only for active material harm such as total unavailability, data corruption or loss, authentication/payment/privacy/critical-security impact, legal exposure, or an explicit user instruction.

After two substantially identical deploy, rollback, or verification cycles, stop that route, preserve evidence, and replan. Repeated rollback is not proof of rigor.

## Token constraints

- Reuse still-valid recent build, test, and release evidence; do not rerun unchanged full suites.
- Run one minimum targeted check per applicable gate, then rerun only affected checks after a fix.
- Prefer Luna for routine packaging, inventories, and repetitive release preparation; Terra for bounded releases and data work; reserve Sol for complex incidents, high-risk migrations, or critical adjudication.
- Compress post-launch hardening into batches so low-risk tail work does not occupy premium models or multiple windows indefinitely.

## Close the launch loop

After deployment, validate the real live health surface and critical path, then update the ledger with version, time, evidence, known issues, hardening queue, and owners. When only deferrable work remains, report what is live, current risk, and follow-up timing instead of treating every improvement as a launch prerequisite.
