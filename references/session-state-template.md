# SESSION_STATE.md template

Lives at the canon root. Rewritten (not appended) at every session close / `/consolidate`.
Tier 1 of `memory-tiers.md` — if the project runs a second or third tier, this file
registers them in the canonical-sources table below and states which wins for what.

```markdown
# SESSION_STATE — <Project Name>
Updated: <ISO date> · Suite: v<N>

## Where we are
One short paragraph: current phase/milestone, last thing completed and verified.
If the line is gated on one thing, say what — a gate is more useful than a summary.

## Next step
The single next action, stated so a fresh session can start it without questions.

## Canonical sources — one file per line
| File | ID / path | Notes |
|---|---|---|
Tracker JSONs (one per line), the memory-tier files if any, and the dashboard shell.
Note any connector quirk that affects writes here (e.g. no delete tool → every write adds
a file; a dashboard pointed at a file id needs repointing when the id changes).

## Active lines
| Line | State |
|---|---|
Phase, status, and what each is blocked on. Cancelled lines stay listed, marked CANCELLED
with the date, until the decision log entry is written.

## Decisions awaiting owner
D-ids with one line each. These are blocking someone, so they sit above the reference
material, not below it.

## Open questions (do not invent — confirm with owner)
| # | Question | Blocks | Current assumption |
|---|---|---|---|

## Issues
I-ids with severity, highest first. An issue is a condition that has happened; a risk is
something that would hurt if it did. Numbered defects live in the line's tracker, not here.

## Recent decisions
Last 3–5, one line each, with decision-log filename.

## Housekeeping
Superseded files to retire (name, id and size — sizes matter when names collide), and
anything the owner must clean up manually.
```

Rules: terse; no history dump (that's the decision log); a session opening with
"what is my next step" is answered by reading this file, verbatim, then acting.

Two things this file does NOT hold: numbered defect tickets (they belong in the line's
tracker, `DASHBOARD_SPEC.md` §4h) and locked architecture (tier 2, if the project has one).
Both get a pointer from here, never a copy.
