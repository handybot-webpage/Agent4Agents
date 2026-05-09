# Evidence — compact-bind

**Charter:** [tasks/compact-bind.charter.md](./compact-bind.charter.md)
**Commit SHA:** _populated post-commit; this evidence file is part of the introducing commit_

## Tests

11 inline tests run against `bin/compact-bind` via stdin. All passed.

| # | Name | Charter shape | Expected | Actual | Result |
|---|---|---|---|---|---|
| T1 | active-charter | bin/compact-bind from active charter | out=`bin`, exit 0 | `bin`, 0 | pass |
| T2 | invocation-flag | active charter with `--invocation` | `/freeze bin/`, 0 | `/freeze bin/`, 0 | pass |
| T3 | literal-files | two literal files in single dir | `bin`, 0 | `bin`, 0 | pass |
| T4 | wildcard-glob | `src/auth/*.ts` + literal in same dir | `src/auth`, 0 | `src/auth`, 0 | pass |
| T5 | recursive-glob | `src/**/*.ts` + sibling | `src`, 0 | `src`, 0 | pass |
| T6 | disjoint-tier1 | `src/auth/*` + `tests/auth/*` Tier 1 | exit 1 + stderr | exit 1 + clear error | pass |
| T7 | disjoint-tier2 | `src/auth/*` + `billing/charge.ts` Tier 2 | `.`, 0, stderr warning | `.`, 0, warning | pass |
| T8 | single-literal | one file `src/main.ts` Tier 0 | `src`, 0 | `src`, 0 | pass |
| T9 | addendum-last-wins | original wide scope + addendum narrow | `bin`, 0 | `bin`, 0 | pass |
| T10 | invocation-format | `--invocation` formats `/freeze <dir>/` | `/freeze bin/`, 0 | `/freeze bin/`, 0 | pass |
| T11 | missing-section | charter with no `## In-scope` | exit 2 + clear error | exit 2 + clear error | pass |

## Commands

| # | Command | Exit code | Output |
|---|---|---|---|
| C1 | `chmod +x bin/compact-bind` | 0 | _(silent)_ |
| C2 | `bin/compact-bind` (default path against the active charter) | 0 | `bin` |
| C3 | `bin/compact-bind --invocation` | 0 | `/freeze bin/` |
| C4 | `wc -l bin/compact-bind` | 0 | `192` |
| C5 | `python3 -c '...inspect functions...'` | 0 | 7 functions; algorithmic ones have docstrings |

## UI evidence

N/A — this is a CLI tool, no UI surface.

## Coverage delta (Tier 1+)

N/A — Project Compact does not yet have a formal test runner adopted (no
`tests/` directory, no language toolchain ADR yet). The 11 inline tests
above are run via shell heredocs with explicit assertions on stdout +
exit code. Adopting a test framework is its own future Tier 1 change with
a charter and ADR (see roadmap `ARCHITECTURE.md` §15.2).

## Notes

- **Mid-task finding:** the original `## In-scope` of this very charter
  (which included framework-implicit paths like the silent-decisions log
  and evidence file) was rejected by the script as disjoint-roots in a
  Tier 1 charter. The framework's own tooling caught a real design flaw
  in my charter — exactly the validation the framework is meant to
  provide.
- **Resolution:** charter received an addendum (preserved as history per
  ADR-0002 append-only rule). The pending-decisions log carries the
  question of formalizing "framework-implicit paths" in the bridge
  protocol; that would be a future Tier 2 change with a new ADR.
- **Self-review (simulating /review):** code is stdlib-only, single
  file, 192 lines, 7 functions; algorithmic functions have docstrings;
  exit codes (0/1/2) cleanly distinguish success / charter-malformed /
  script-error. No third-party deps. No SQL injection, command injection,
  or shell-escape paths (script does not execute or shell-out).
- **Cross-model review (`/codex`)** not run in this session — Tier 1
  task, `/codex` is *recommended* not required per `04-skill-bindings.md`.
  In a real session with `/codex` available, the recommended invocation
  would be: `/codex review bin/compact-bind`.
- **`/freeze` invocation:** in a real Claude Code session with gstack
  active, the workflow would be:
    1. `bin/compact-bind --invocation` → outputs `/freeze bin/`
    2. Agent invokes `/freeze bin/` → gstack writes
       `~/.gstack/state/freeze-dir.txt` and PreToolUse hook blocks
       Edit/Write outside `bin/`
  In this session the boundary was respected by discipline.
