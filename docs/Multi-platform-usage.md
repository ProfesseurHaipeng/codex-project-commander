# Project Commander multi-platform usage

## Distinguish an agent host from a model provider

Codex, Claude Code, OpenCode, Kimi Code, and Hermes are agent hosts that can run tools and load skills. OpenAI, MiniMax, DeepSeek, and Doubao are commonly model/API providers. The model reasons; the host reads files, runs tools, saves sessions, and creates tasks. They are not interchangeable.

This skill therefore runs at one of three levels:

1. Full employee windows when the host exposes persistent named project tasks, messaging, renaming, and monitoring.
2. Persistent-session commander when the host saves sessions but lacks Codex-equivalent employee windows.
3. Single-session commander when only the skill or portable prompt can maintain the charter, organization, ledger, and queue.

## Codex and OpenAI

Install the English edition at `~/.agents/skills/project-commander`. Codex desktop can use full employee-window mode when its project-task tools exist; Codex CLI or another surface without those tools degrades gracefully.

The OpenAI API does not itself load local skills or create task windows. Load the skill in an agent host that calls the API. For a host that accepts only system/developer instructions, use `skills/project-commander/assets/PORTABLE_COMMANDER_PROMPT.md`.

## Claude Code (Cloud Code)

Copy the skill to `~/.claude/skills/project-commander`. Claude Code loads the organization, Token, ledger, safety, and delivery rules natively. Without Codex-equivalent project tasks, use persistent-session or single-session mode and never impersonate employee windows with Claude subagents.

## OpenCode (OpenCloud)

OpenCode discovers `.opencode/skills`, `.agents/skills`, and `.claude/skills`. Install at `~/.config/opencode/skills/project-commander` or reuse `~/.agents/skills`. Select Level B or C from OpenCode's actual session capabilities.

## Kimi Code and the Kimi model

Copy the skill to `~/.kimi-code/skills/project-commander` or `~/.agents/skills/project-commander`. Invoke explicitly with `/skill:project-commander`. The Kimi API by itself is a model provider and requires a compatible host or portable prompt.

## MiniMax and MiniMax Codex

MiniMax provides OpenAI/Anthropic-compatible endpoints for agent tools. Its official documentation also describes a Codex custom provider. Configure MiniMax in Codex from that official page, then install this skill in the Codex skill directory. This host-plus-model combination is what this repository calls “MiniMax Codex.” Employee-window support still comes from the Codex surface, not the MiniMax model.

Do not hardcode a current MiniMax model name in the skill. Remap Sol, Terra, and Luna from the live catalog as models change.

## DeepSeek (DeepSea) and Doubao

DeepSeek can be used through an OpenAI/Anthropic-compatible agent host; Doubao/Volcengine Ark can be used through an OpenAI-SDK-compatible host. Neither API reads `SKILL.md` by itself. Install the skill in the host, then configure the provider there.

## Hermes

Hermes supports direct GitHub skill installation:

```bash
hermes skills install ProfesseurHaipeng/codex-project-commander/skills/project-commander
```

Use persistent-session commander mode in native Hermes sessions. A chat-only frontend connected through the Hermes OpenAI-compatible API defaults to single-session mode. Upgrade only if the frontend or control plane exposes real project-task capabilities.

## Provider-neutral Token routing

- Luna: the lowest-cost option that can complete clear repeatable work.
- Terra: the balanced option for bounded analysis, data, documentation, and routine implementation.
- Sol: complex software, cross-system work, or justified high-risk adjudication.

If the host exposes one model only, control spend through reasoning effort, WIP, context compression, and validation depth. Never fabricate a model switch. Stop and replan after two substantially identical failures.
