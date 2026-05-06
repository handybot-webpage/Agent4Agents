# 03 — Question protocol

The cost of a clarifying question is the human's attention. Spend it sparingly.

## Before asking, check
1. Is the answer in `01-constitution.md`? → do not ask, proceed.
2. Is the answer in an ADR linked from the charter? → do not ask, proceed.
3. Is the answer in a MODULE.md for a touched module? → fetch and read, then proceed.
4. Is the decision REVERSIBLE? → declare default, proceed (silence-as-proceed).
5. Is the decision IRREVERSIBLE per the constitution's irreversibility list?
   → ask, in the format below.

## Reversible decisions: silence-as-proceed
Format your message:

> **Default:** <chosen action>
> **Reasoning:** <one sentence>
> **Alternatives considered:** <A: tradeoff>, <B: tradeoff>
> **Proceeding unless objected.**

Append the decision to `tasks/silent-decisions-log.md` with timestamp,
default, alternatives, and the charter ID. Then execute.

## Irreversible decisions: blocking question
Format:

> **Blocking question:** <one sentence>
> A: <option> — <tradeoff>
> B: <option> — <tradeoff>
> C: <option> — <tradeoff>  (optional)
> **My recommendation:** A, because <reasoning>.

Wait for the human's reply. Do not proceed.

## Hard limits per turn
- At most ONE blocking question per turn.
- At most THREE silent-default declarations per turn (more = your charter
  scope is too vague; revise the charter, do not flood with defaults).
- Never ask a question and a default in the same turn — pick one mode.

## What gets you blocked by a hook
- Asking a question whose answer is reachable from the loaded context.
- Declaring REVERSIBLE on a path matching the irreversibility list.
- Exceeding the per-turn limits above.
