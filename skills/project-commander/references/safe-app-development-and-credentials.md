# Non-adversarial app development and credential handling

Use this protocol for apps, websites, services, APIs, desktop software, mobile software, and other engineering missions. The goal is normal development, runtime validation, and delivery—not turning product work into an attack exercise or repeatedly interrupting the user with credential warnings.

## Cross-tool compatibility

Keep the portable Agent Skills structure: YAML frontmatter in `SKILL.md` with a clear `name` and `description`; detailed guidance in directly linked `references/`; templates in `assets/`; deterministic helpers in `scripts/`. Do not rely on host-specific frontmatter extensions for essential safety boundaries.

Codex discovers the skill from `.agents/skills/` or user skill directories. Claude Code can discover the same skill from `.claude/skills/` or user skill directories. Host permissions and sandboxing are enforced by the host; this protocol limits what headquarters should attempt. Sidebar employee creation, naming, pinning, and monitoring still require Codex project-task tools. Claude Code may load the general organization, Token, delivery, and credential rules, but its subagents never impersonate Codex employee windows.

## No adversarial self-testing

Within this skill, do not launch attack programs or attack traffic merely to “verify security,” even when the target belongs to the user or runs locally. This includes:

- exploitation, privilege bypass, authentication bypass, or injection payloads;
- brute force, credential stuffing, password spraying, token theft, or session hijacking;
- malware, destructive payloads, denial of service, port scanning, or adversarial probing;
- penetration testing or red-team operations against real users, production, third parties, or the project app;
- reading, copying, or probing sensitive data unrelated to the current mission.

Do not automatically create attack-test, penetration-test, or red-team employee missions. If the user explicitly asks for that work, this skill does not run the attack simulation; state the boundary briefly and offer non-adversarial alternatives.

## Normal app validation

Prefer delivery-relevant, non-adversarial checks:

- compile, build, launch, unit tests, integration tests, and changed-path regression;
- normal-user-flow smoke tests in a browser, simulator, or real device;
- static analysis, type checks, dependency-advisory review, permission configuration checks, and input-validation tests;
- error handling, offline behavior, upgrade, and recovery paths using test data;
- checks for accidental secrets in clients, source, logs, screenshots, or commits.

Do not make broad security scanning a default prerequisite for ordinary app deployment unless the user selects Strict release. Prefer fix-forward and use the delivery posture to separate launch blockers from post-launch hardening.

## Minimize sensitive-data access

- Do not proactively search, open, or summarize `.env` files, private keys, credential stores, access tokens, cookies, real-user data, payment data, health data, or unrelated sensitive content.
- Use only the minimum required fields when the current mission genuinely needs them and the user explicitly provides them or authorizes the exact source.
- Never write sensitive values into the task ledger, organization chart, employee messages, source, Git, logs, screenshots, test fixtures, or final reports.
- Do not forward raw credentials to employee windows. Headquarters performs the credential-dependent step in the current task, or the user configures the corresponding environment before work continues.
- Never claim that content sent in chat has been deleted, retracted, or erased.

## Low-friction API-key handling

First offer one simple environment-variable, platform Secret field, or key-management path. Do not give a security lecture.

If the user says they cannot use another method, no usable input surface exists, or they explicitly insist on providing an API key in the current chat:

1. Allow them to proceed; do not block the mission.
2. Give exactly one concise notice: `You may provide it here. Prefer a temporary, revocable, least-privilege key; I will not echo it or write it to the project, ledger, or logs.`
3. After receipt, do not repeat the warning, quote the full or partial key, or forward it in employee messages.
4. Use it only for the currently authorized mission, preferably through a temporary process environment or a host-provided Secret input. Do not persist it to files or system configuration unless the user explicitly asks.
5. If the current tools cannot use the value without echoing, persisting, or forwarding it, state that technical limitation briefly and give the shortest workable action without lecturing.

Posting a key in chat does not authorize committing it, embedding it in a client, sharing it, or using it in another project. After completion, do not keep reminding the user. Only when the key is found in a client, repository, or log should headquarters identify the exact location and the shortest remediation in one sentence.

## Reporting

Report only the non-adversarial checks used, whether sensitive data was accessed, whether a credential was used ephemerally, any concrete exposure location, and the shortest remaining user action. Never output credential values, attack instructions, or unrelated security prose.
