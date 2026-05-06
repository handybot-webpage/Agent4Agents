# ADR 0003 — Claude Code is the primary agent harness

- **Status:** Accepted
- **Date:** 2026-05-05
- **Supersedes:** —
- **Superseded by:** —

## Context
Project Compact's enforcement layer (hooks, permissions, subagents) requires
features that vary across agent harnesses. We must pick one as the primary
target so hook scripts and subagent definitions have a concrete contract,
while keeping the data layer portable.

Considered:
- **Claude Code.** Native `PreToolUse`/`PostToolUse`/`Stop` hooks, OS-level
  permission allowlists, `.claude/agents/` subagent format, mature prompt
  caching. Markdown-first.
- **Cursor.** Strong UX, weaker hook story, no first-class subagent format.
- **Codex CLI.** Plan mode is excellent; hooks and permissions less mature.
- **Vendor-neutral via AGENTS.md only.** Documents work across tools but
  enforcement does not transfer.

## Decision
Project Compact targets Claude Code as the primary harness. Specifically:

- Hooks live in `.claude/settings.json` and `.claude/hooks/`.
- Subagents live in `.claude/agents/*.md`.
- Permission allowlists/denylists are configured in `.claude/settings.json`.
- An `AGENTS.md` symlink (`CLAUDE.md` → `AGENTS.md`) provides cross-tool
  documentation; the *enforcement* layer is Claude-specific.

## Consequences
- Switching primary harness later requires porting `.claude/` to the new
  harness's equivalent. The data layer (`docs/adr/`, `agent-context/`,
  `tasks/`, `MODULE.md`) is portable as-is.
- We accept a vendor dependency. Mitigation: enforcement scripts (e.g.
  `compact-check`) are written in Python with no Anthropic SDK dependency,
  so they work locally and in CI regardless of which agent invoked them.
- Other tools (Cursor, Codex) can be used by individual contributors but
  do not get enforcement guarantees. Their PRs go through the same CI
  required-check, which catches violations regardless of authoring tool.
