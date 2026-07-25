# SESSION_STATE.md template

Lives at the canon root. Rewritten (not appended) at every session close / `/consolidate`.

```markdown
# SESSION_STATE — <Project Name>
Updated: <ISO date> · Suite: v<N>

## Where we are
One short paragraph: current phase/milestone, last thing completed and verified.

## Next step
The single next action, stated so a fresh session can start it without questions.

## Active lines
| Line | Phase | Status |
|---|---|---|

## Open questions (do not invent — confirm with owner)
| # | Question | Blocks | Current assumption |
|---|---|---|---|

## Recent decisions
Last 3–5, one line each, with decision-log filename.

## Stale items
Anything flagged stale by a decision, awaiting rework.
```

Rules: terse; no history dump (that's the decision log); a session opening with
"what is my next step" is answered by reading this file, verbatim, then acting.
