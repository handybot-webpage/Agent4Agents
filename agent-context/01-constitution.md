# 01 — Constitution

Frozen invariants. Changes require a superseding ADR and a dedicated PR.

## Project intent
Agents4Agents is infrastructure for building, governing, and operating multi-agent
systems. Project Compact (this directory tree) is the governance layer that
keeps agent work scoped, decisions append-only, and human attention scarce.

## Invariants
1. **Markdown is the data layer.** ADRs, MODULE.md, charters, evidence are
   plain markdown — portable across tools, diff-able, human-readable.
2. **Hooks are the enforcement layer.** Any rule that matters is enforced by a
   hook. Prose without a hook is advisory.
3. **Append-only governance.** ADRs, decision logs, charters, and the indexes
   in `agent-context/10-` and `20-` are append-only. Supersede; never rewrite.
4. **Cache stability is a first-class concern.** The prefix `agent-context/00-`
   through `20-` is byte-stable across hundreds of turns. Edits are batched
   into dedicated PRs.
5. **Silence-as-proceed for reversibles only.** Irreversible decisions block.
6. **One source of truth per fact.** No duplicated content between AGENTS.md
   and `agent-context/`. Symlinks for cross-tool support.

## Irreversibility list
The following changes ALWAYS require explicit human approval, regardless of
how the agent classifies them:

- Database schema migrations
- Adding, removing, or upgrading dependencies
- Breaking changes to a public API or exported interface
- Deletion of any file larger than 50 lines
- Any change touching authentication, authorization, billing, or secrets
- Edits to `agent-context/0*-*.md`, `agent-context/1*-*.md`, `agent-context/2*-*.md`
- Edits to `docs/adr/` (except appending new ADRs)
- Edits to `.claude/`, `.github/workflows/`, or hook scripts

## Tier ceiling
No single PR may exceed Tier 2. A change requiring more than one new ADR is
split across PRs.

## What this constitution does NOT cover
Style, formatting, naming conventions, framework choice, language idioms.
Those belong in linters, formatters, or MODULE.md — not here.
