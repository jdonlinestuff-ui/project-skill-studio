# Memory tiers — SESSION_STATE.md and the optional second tier

A studio needs one file that answers "where are we, what's next". Some projects grow a
second and third, because a coding agent reads a different file from the one a design
session reads, and a fast-moving build line changes faster than a locked architecture doc.

**One tier is the default. Two or three are legitimate. Silent duplication is not.**

## The tiers

| tier | file | owns | changes |
|---|---|---|---|
| 1 | `SESSION_STATE.md` at canon root | where we are, the single next step, active lines, open questions, issues, decisions awaiting the owner | rewritten at every session close |
| 2 *(optional)* | agent project-memory — conventionally `CLAUDE.md`, at the working root the coding agent opens | locked architecture, invariants, the locked product spec, "never invent an answer for these" questions | rarely; a change here is a logged decision |
| 3 *(optional)* | condensed working memory — e.g. `PROJECT_STATE.md`, beside the build line | the fast-moving detail of one active line: current build version, what shipped in it, what to read first | as often as the line ships |

Tier 2 exists because coding agents read a project-memory file automatically at the start
of every session, and that file is the only one guaranteed to be seen. Tier 3 exists
because tier 2 goes stale the moment it tries to hold version-specific facts.

Most projects need tier 1 only. Add a tier when a real second reader exists — not in
anticipation of one.

## Precedence — most version-specific wins

**For a version-specific fact** (what is built, which version ships, what the current
behaviour is), read in order 3 → 1 → 2, and the *first* file that carries the fact wins.
Tier 3 is closest to the build; tier 2 is furthest.

**For a locked fact** (architecture decisions, invariants, the locked spec), the order
inverts: tier 2 wins, and a tier-1 or tier-3 file that contradicts it is reporting a drift,
not a change. Locked values change through a logged decision, never through a state file
being rewritten.

**Session open** reads tier 1 first regardless — it holds the next step — then consults
the others as the work touches them. Nothing about a second tier changes the rule that a
session opening with "what is my next step" is answered from `SESSION_STATE.md`.

## The four rules that keep tiers from lying

1. **Every tier names the others, with the precedence rule stated in the file itself.** A
   reader who opens exactly one file must learn from it that the others exist. A tier-2
   file that doesn't mention tier 3 will be trusted for facts it isn't authoritative on.
2. **A tier holding knowingly-superseded content says so above that content**, in the file,
   at the top of the affected section — "the sections below describe the original design;
   where they disagree with X, X is correct". Superseded content kept as historical record
   is legitimate; superseded content that reads as current is not.
3. **No tier duplicates another's owned fact.** Cross-reference instead. Two files stating
   the same version number is two things to update and one thing that will be forgotten.
4. **One copy of each tier file.** Two `PROJECT_STATE.md`s in different folders is the same
   failure as two trackers with the same name — see `tracker-schema.md`'s write discipline,
   which applies here unchanged.

## Registering the tiers

Whatever tiers a project runs are recorded once — in `SESSION_STATE.md`'s canonical-sources
table, with each file's location and what it owns — and every generated skill's Canon block
points at that table rather than restating it. A tier nobody registered is a file the next
session won't know to read.
