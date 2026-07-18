# Contributing

Thank you for improving Codex Project Commander and its maintenance tooling. Keep each contribution scoped, review the affected policy or workflow contract before changing it, and include tests for behavior changes.

## Automation boundary

Automated replies are limited to low-risk, policy-allowlisted labels and comments. They are not endorsements, approvals, or merge decisions. Every pull request, issue decision, policy change, workflow change, and release still requires human review by a maintainer.

Do not submit changes that expand a workflow's permissions, run untrusted contributor code in a privileged job, expose Secrets, bypass idempotency markers, or make stale closure opt-out. Protected actions—including merging or approving pull requests, enabling workflows, changing repository settings or permissions, creating Secrets, publishing releases, and deleting branches or source—remain maintainer decisions outside this contribution process.

## Before opening a pull request

1. Keep generated files, credentials, and unrelated formatting changes out of the patch.
2. Update the relevant English and Chinese Skill documentation together when their shared policy boundary changes.
3. Run the applicable local tests. For the maintenance tooling, run:

   ```bash
   python3 -m unittest discover -s automation/tests -v
   ```

4. When changing either maintenance Skill, validate both packages:

   ```bash
   python3 /Users/boris/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/automate-oss-maintenance
   python3 /Users/boris/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/automate-oss-maintenance-zh
   ```

5. Explain the behavior, validation evidence, and any remaining external state that cannot be observed locally.

Report suspected vulnerabilities through the route described in [SECURITY.md](SECURITY.md); do not place sensitive details in a public issue.
