# 30 — Active charter

**Source:** [`tasks/vic-benchmark.charter.md`](../tasks/vic-benchmark.charter.md)

---

# Charter — vic-benchmark

**Tier:** 2
**Goal:** Scaffold the Vehicle Interior Cleaning (VIC) benchmark — paper-inspired by CleanUpBench (arxiv 2508.05543), domain-shifted to vehicle interiors, targeting NVIDIA Isaac Sim.

## In-scope
- `benchmarks/vehicle-interior-cleaning/**`
- `docs/adr/2026-05-09-0005-vic-benchmark.md`
- `agent-context/10-adr-index.md` (append-only)
- `agent-context/20-module-index.md` (append-only)
- `agent-context/30-active-charter.md` (cache tail)
- `tasks/vic-benchmark.evidence.md`
- `tasks/silent-decisions-log.md` (append-only)

## Out-of-scope
- everything else

## Linked ADRs
- ADR-0001, ADR-0002, ADR-0003, ADR-0004 (existing)
- ADR-0005 (new, written as part of this task)

## Acceptance evidence
- SPEC.md ≥4 tasks, ≥5 metrics, ≥3 vehicle classes
- MODULE.md with owner/API/invariants
- Python scaffold with graceful Isaac-import fallback
- ≥4 pure-Python tests pass on macOS
- README.md documents Linux+RTX requirement honestly

## Charter-Approved-By
handybot-webpage (project owner via AskUserQuestion irreversible-decision approval, 2026-05-09)
