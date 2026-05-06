# 05 — Bridge protocol (handshakes between Compact and gstack)

Frozen. The exact handshakes that wire Compact's data layer to gstack's
workflow engine. Skill bindings (which skills run when) live in
`04-skill-bindings.md`; this file specifies the data flow.

## Charter → /freeze handshake
Run at the start of every Tier 1 / Tier 2 task.

1. Read `agent-context/30-active-charter.md`. Extract every line under
   `## In-scope`.
2. Compute the **deepest common parent directory** of all in-scope globs.
   - All globs share a parent (e.g. `src/auth/login.ts` and
     `src/auth/session.ts` → `src/auth/`): freeze to that parent.
   - Globs span disjoint roots (e.g. `src/auth/*` and `tests/auth/*`):
     for Tier 1, the charter is malformed — request charter revision.
     For Tier 2, freeze to the deepest common parent of the union
     (often the repo root); gstack's hook will allow but the tier
     rubric's adversarial-review (`/codex`) will catch out-of-scope edits.
3. Invoke `/freeze` with that directory.
4. Confirm in your first message: "Freeze bound to `<dir>/` per charter."

## /qa output → evidence.md handshake
Run at the end of any task that touched UI.

1. After `/qa` completes, gstack writes results under
   `~/.gstack/projects/<slug>/qa/<timestamp>/` (transcript, screenshots,
   regression test names).
2. Open `tasks/<id>.evidence.md`. In the `## Tests` table, append one row
   per regression test: name, pass/fail, runner output one-liner.
3. In the `## UI evidence` section, link the screenshot path and record
   the captured commit SHA.
4. Do not paraphrase gstack's outputs — link the actual artifacts.

## /review output → evidence.md handshake
Run at the end of any Tier 1+ task.

1. `/review` produces a bug list and (for obvious issues) auto-applied
   fixes. Capture the fix commits' SHAs in `evidence.md` `## Notes`.
2. Any flagged-but-not-fixed bugs become entries in
   `tasks/pending-decisions.md` with the recommendation copied verbatim.

## /codex output → ADR or evidence.md handshake
Run before `/ship` on Tier 2 tasks.

1. `/codex` returns one of: agree, disagree-with-reasoning, adversarial-flag.
2. **Agree:** record in `evidence.md` `## Notes`: "codex: agree, <date>".
3. **Disagree:** the disagreement is a decision point. Either revise the
   change, or write an ADR documenting why we proceeded against codex's
   recommendation. Do not silently ignore disagreements.
4. **Adversarial-flag (security/correctness):** block `/ship`. Resolve or
   write a superseding ADR.

## /learn → ADR promotion handshake
Run during `/retro`, weekly or after every Tier 2.

1. Read `~/.gstack/projects/<slug>/learnings.jsonl`. Group by topic.
2. Any topic with ≥3 distinct entries is an **ADR candidate**: the pattern
   is recurring enough to deserve durable governance, not session memory.
3. For each candidate, write a new ADR with timestamp prefix, append a
   row to `agent-context/10-adr-index.md`, and prune the related
   learnings (gstack's `/learn` supports prune).
4. ADRs supersede learnings, never the reverse.

## Approval handshake (Tier 2)
1. Agent writes the charter with all fields except `Charter-Approved-By:`.
2. Agent commits the charter with a clear message.
3. **A non-agent identity** edits the charter to add the
   `Charter-Approved-By: <github-username>` line and commits separately.
4. Agent verifies the trailer was added by a non-agent commit before
   proceeding past the planning phase.

## Cache-stability rule for the bridge
Never edit files numbered `00-` through `05-` as part of a task. Bridge
edits are themselves Tier 2 changes requiring a new ADR.
