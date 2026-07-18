# Security policy

## Reporting vulnerabilities

GitHub Private Vulnerability Reporting is the intended private reporting route for this repository. Its enablement cannot be verified from the local repository evidence available here, so publication remains blocked until a maintainer enables and verifies it in GitHub.

Until that verification is complete, do not include vulnerability details, credentials, private keys, access tokens, or reproduction steps in a public issue. Do not invent an alternate reporting channel from local repository contents. A maintainer must publish and verify a private route before inviting reports through it.

## Automation safeguards

The local maintenance policy treats security-labelled work as protected and prevents ordinary automated comments for it. The optional `OPENAI_API_KEY` is a repository Secret name for optional enrichment; it must not be committed to files, test fixtures, logs, or documentation examples containing a real value.

Local workflow and policy files do not prove GitHub configuration, repository permissions, Secret values, or private-reporting availability. Verify those states in the repository settings before making a security-operation decision.
