# Canon-first workflow — mandatory for generation requests

Applies to every generated skill, and to this studio itself, whenever a request
asks for a task, a design, code, or documentation. It is the concrete
instantiation of the work loop's DRAFT step (search → summarise → plan → tasks)
and PROOF gate (approval before producing the deliverable) — see
`skill-baseline.md` §1. VERIFY / REVISE / REGISTER continue to apply once the
deliverable exists; this file only governs what happens before it does.

## The rule

Before generating anything, search the project's connected canon store — most
commonly Google Drive, but a git repo or local canon folder is equally in
scope — for relevant canonical assets, and treat what is found there as
authoritative. **Do not assume when canonical information already exists.** If
two canonical assets conflict, surface the conflict; never invent a resolution
or silently pick one side.

## The six steps

1. **Search canonical assets.** Query the connected canon store for anything
   relevant to the request — data files, specs, prior decisions, trackers.
2. **Summarise relevant information.** State what canon already says, in the
   requester's terms, before proposing anything new.
3. **Identify missing information.** Name what canon does not cover. This
   becomes an open question (per the no-floating-questions rule), not a gap to
   fill from memory.
4. **Generate a plan.** The plan cites which canonical assets it rests on and
   which open questions it carries forward unresolved.
5. **Generate implementation tasks.** Break the plan into the smallest
   reviewable units — this is DRAFT-sized work, not the whole deliverable.
6. **Produce the deliverable only after the plan is approved.** Code, design
   output, or documentation is generated only once the owner has reviewed
   steps 1–5. Producing it earlier is a PROOF-gate violation regardless of how
   confident the plan looks.

## Key skills to consider for every request

Two checks before acting, every time:

- **`task-orchestrator`** — if the request bundles independent pieces of work,
  repeats a subtask across many items, or asks which skill/model should handle
  something, decompose and dispatch through it rather than doing everything
  serially in one pass.
- **The project's own installed skills** (its canon skill and whichever
  line/ops skills apply) — check these before writing new logic. A studio skill
  that rebuilds what an installed project skill already owns is exactly the
  duplication Phase 2's reuse rule exists to prevent. This studio
  (`project-skill-studio`) itself is one of these for scaffolding and tracker
  duties; it does not replace a project's own canon or line skills once built.

## Conflict, not invention

When canonical assets disagree — two trackers with different revisions of the
same fact, a spec and a reference implementation that no longer match, a
decision log entry that contradicts a locked value — name the conflict
explicitly, cite both sources, and stop short of resolving it unilaterally
unless the resolution is itself already canon (e.g. a dated decision entry that
supersedes an older one). Resolving silently is worse than flagging: it hides
the disagreement instead of letting the owner settle it.
