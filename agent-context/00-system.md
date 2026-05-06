# 00 — System

You are an agent operating under Project Compact. This file is FROZEN: do not edit
it as part of any task. Edits to this file invalidate the prompt cache for every
agent in the project.

## Load order
The files in `agent-context/` are loaded in numerical order and form a stable,
cache-aligned prefix. Files `00-` through `20-` are frozen (rare edits, dedicated
PR). File `30-active-charter.md` is the only file that changes per task.

## Operating loop
1. Read the active charter (`30-active-charter.md`).
2. Cite, in your first message, the ADRs and modules the charter links.
3. Plan in-scope edits only. Out-of-scope edits are a protocol violation.
4. For each ambiguity, classify as REVERSIBLE or IRREVERSIBLE.
   - REVERSIBLE: declare default + reasoning, proceed unless human objects.
     Append the decision to `tasks/silent-decisions-log.md`.
   - IRREVERSIBLE: ask one multiple-choice question, wait.
5. Fill `tasks/<id>.evidence.md` before claiming the task done.

## What you must NOT do
- Edit any file in `agent-context/` numbered `00-` through `20-`.
- Edit any accepted ADR in `docs/adr/`. Supersede with a new ADR instead.
- Touch paths outside the active charter's `in-scope` list.
- Ask a clarifying question whose answer is in constitution, an ADR, or a
  MODULE.md you have not read.
- Claim "done" without populated evidence.

## Cache discipline
- Append, never edit. New ADRs append to `10-adr-index.md`. New modules append
  to `20-module-index.md`. Charter addenda go below the original charter.
- Do not preload `MODULE.md` files. Fetch on demand only for touched modules.
- Long-running verifier work: lead agent does a small Read every ~4 min to keep
  the cache window warm.
