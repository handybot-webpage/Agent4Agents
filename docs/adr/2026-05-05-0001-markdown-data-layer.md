# ADR 0001 — Markdown is the data layer

- **Status:** Accepted
- **Date:** 2026-05-05
- **Supersedes:** —
- **Superseded by:** —

## Context
Project Compact governs multi-agent work via files: ADRs, MODULE.md, charters,
evidence, decision logs. Those files are read by humans, by Claude Code, and
by any future tool that may replace it. We need a format that is:

- diff-able (git is the source of truth)
- portable across agent harnesses (Claude Code, Cursor, Codex, future tools)
- editable by humans without special tooling
- parseable by simple shell or Python scripts (for hooks)

## Decision
All Project Compact data is plain Markdown with conventional headings. No
YAML frontmatter unless required by an external tool. No JSON. No SQLite. No
custom DSL. Schema is enforced by hooks parsing the markdown, not by the
storage format itself.

## Consequences
- Hooks must tolerate small variations (whitespace, casing). Use lenient
  parsing; fail loudly only on missing required sections.
- We accept the risk of malformed markdown breaking hooks. Mitigation: a
  `compact-check lint` mode that validates structure and runs in CI.
- We forgo the type-safety of structured config. Net positive: portability
  and human-editability outweigh the cost.
- If a future need demands structured data (e.g. a query interface over
  ADRs), build a derived index on top — do not change the source format.
