# Silent decisions log (append-only)

Every reversible default the agent took without asking. PR templates link
this file; reviewers should skim entries since the last PR.

| Timestamp | Charter | Default chosen | Alternatives rejected | Notes |
|---|---|---|---|---|
| 2026-05-06 | compact-bind | Python (stdlib-only) | bash (fragile parsing); Go/Rust (compile step) | matches bin/compact-check; no new deps |
| 2026-05-06 | compact-bind | print directory only by default; `--invocation` flag for full `/freeze <dir>` command | print full /freeze by default (forces parse); JSON output (overkill) | composable with shell |
| 2026-05-06 | compact-bind | disjoint roots: Tier 1 exit 1, Tier 2 exit 0 with `.` + stderr warning | always succeed (defeats purpose); always fail (too strict for Tier 2) | matches bridge protocol §10.1 |
| 2026-05-06 | compact-bind | charter path is positional arg, default `agent-context/30-active-charter.md`, `-` for stdin | required explicit path (friction); env var (less obvious) | supports interactive + testing |
| 2026-05-06 | compact-bind | self-approval (Tier 1, single-developer) | request explicit human approval | per tier rubric §02 |
