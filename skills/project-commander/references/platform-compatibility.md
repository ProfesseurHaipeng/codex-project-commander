# Cross-platform compatibility and graceful degradation

This protocol separates three different facts: loading a skill, using a model provider, and creating employee windows. Probe capabilities before activating the commander. Never infer tools from a product or model name.

## Three compatibility levels

### Level A: full employee-window mode

Use only when the host provides all of the following:

- native Agent Skills or equivalent system instructions;
- persistent, named, listable, readable project tasks that can receive later messages;
- a way to bind headquarters and employees to the same project directory;
- verifiable titles and stable task IDs;
- a headquarters-attached heartbeat or automation tool before promising cross-turn automatic redispatch.

Codex desktop is Level A when its project-task tools are available. Employees are real sidebar project tasks. Without a heartbeat, employee windows remain usable but monitoring falls back to the manual `continue monitoring` command.

### Level B: persistent-session commander

Use when the host natively loads the skill and can save, resume, or name sessions, but lacks Codex-equivalent project task windows. Headquarters must:

- inspect the project and maintain the organization and ledger;
- represent departments and roles as accountable ledger units;
- use only session, branch, or delegation features actually published by the host;
- bring results back to the current commander session for validation;
- never claim Codex sidebar employees, pinning, cross-window push delivery, or an automatic watchdog.

Temporary subagents may perform short host-authorized work, but never name them `EmployeeNN` or present them as persistent employee windows.

### Level C: single-session commander

Use when the host accepts a prompt or one skill but has no persistent task orchestration. In one session, maintain:

- the project charter;
- organization and one accountable owner per deliverable;
- the `.codex/project-commander/TASK_LEDGER.md` queue;
- Sol/Terra/Luna capability tiers and Token stop-loss;
- only the WIP allowed by the selected operating mode;
- validation, state update, and next-task selection after every completed task.

Never fabricate windows, employee reports, background work, or automatic callbacks.

## Platform and provider map

| Name | Type | Loading path | Default level and limit |
| --- | --- | --- | --- |
| OpenAI Codex / Codex | Agent host | `.agents/skills` or another Codex-supported skill directory | A with project-task tools; otherwise B/C |
| Claude Code (sometimes called Cloud Code) | Agent host | `.claude/skills` | Native skill; normally B/C, and Claude subagents never impersonate Codex employee windows |
| OpenCode (sometimes called OpenCloud) | Agent host | `.opencode/skills`, `.agents/skills`, or `.claude/skills` | Native skill; choose B/C from real session tools |
| Kimi Code | Agent host | `.kimi-code/skills` or `.agents/skills`; invoke with `/skill:project-commander` when useful | Native skill; choose B/C from real session tools |
| Hermes Agent | Agent host | `hermes skills install owner/repo/skills/project-commander` | Native skills and persistent sessions; B by default, A only with equivalent project-task tools |
| OpenAI API | Model/API | Called by a compatible agent host or given the portable prompt | C by itself; an API does not create task windows |
| MiniMax | Model/API and tool ecosystem | OpenAI/Anthropic-compatible endpoint; may back Codex, Claude Code, or OpenCode | Level comes from the host, not the model |
| MiniMax Codex | Codex host + MiniMax model | Configure the official MiniMax Codex custom provider and install this skill | A when Codex task tools exist; model switching does not change employee rules |
| DeepSeek (including the alias DeepSea) | Model/API | Called by an OpenAI/Anthropic-compatible host | Host determines level; never hardcode volatile model IDs |
| Doubao / Volcengine Ark | Model/API | Called by an OpenAI-SDK-compatible agent host | Host determines level; the API itself does not load skills |
| Kimi model/API | Model/API | Called by Kimi Code or another compatible host | Kimi Code loads skills natively; API-only use is C |
| Hermes backend/API | Agent/API | Native Hermes skill or an OpenAI-compatible frontend connection | C in a chat-only frontend; B in a native Hermes session |

## Capability probe order

1. Identify the host's actual skill discovery path or skill tool.
2. Enumerate callable project-task, session, rename, pin, message, and automation capabilities.
3. Select A, B, or C and record it in the ledger as `Compatibility level`.
4. Inspect available providers, models, and reasoning efforts, then map actual choices to Sol, Terra, and Luna.
5. If only one model exists, control Token use through reasoning effort, WIP, context compression, and validation depth. Never fabricate three models.
6. Upgrade or downgrade when host capabilities change while preserving the ledger and accepted evidence.

## Provider-neutral model routing

- Luna: the lowest-cost current-host option that can reliably complete a clear repeatable task.
- Terra: the balanced option for bounded everyday analysis, data organization, documentation, and routine implementation.
- Sol: the option for complex software, cross-system judgment, or justified high-risk adjudication.

Never bind a provider's fixed model name permanently to a tier. Prefer the live model catalog, quota/cost signals, context window, and reasoning options. When unavailable, record capability classes and never invent usage or price.

## Portable-prompt entry

If the host cannot discover a directory-based skill, place [the portable commander prompt](../assets/PORTABLE_COMMANDER_PROMPT.md) in its system or developer instructions. That entry guarantees only Level C governance. Upgrade only when the host explicitly exposes Level A or B capabilities.

Across every platform, preserve the security boundary, one-primary-mission rule, Token stop-loss, non-adversarial app validation, and the one-notice/no-echo/no-persistence API-key protocol.
