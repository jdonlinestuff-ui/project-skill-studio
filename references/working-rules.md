# Working rules embedded in generated skills

1. **Canon discipline.** No canonical value is invented, altered, or duplicated.
   Content flows from the single source through the pipeline. Unconfirmed values
   are logged as open questions and flagged to the owner — never silently assumed.
   Divergence between a derivative (e.g. digital version) and canon is either fixed
   or documented as an explicit additive enhancement.
2. **Decision logging.** Anything design-controlled changes only via a dated
   decision-log entry. The decision lists what it flags stale; the tracker
   propagates staleness to dependents automatically.
3. **Modular design (build lines).** Every concept is an independently
   re-authorable module with its own contract and tests. Changes are re-authored
   and tested at module level — never whole-package rebuilds. Cross-module
   coupling fails review.
4. **Proof gate (visual output).** Card renders, page layouts, UI visuals go to
   the owner as proofs BEFORE the build continues. Nothing unapproved ships.
5. **Local-first prototyping (code lines).** Local dev loop (build + typecheck +
   tests) until gameplay/product is validated; defer hosting/deploy decisions.
6. **Leverage existing skills first.** Check installed plugin and public skills
   before writing anything new; generated skills orchestrate them.
7. **Defensive tooling.** If a required connector isn't available, stop and ask
   the owner to reconnect; never proceed from memory on canonical content.
8. **Surgical fixes.** Owner feedback arrives as numbered, per-item corrections;
   respond with targeted fixes to exactly those items, not rebuilds.
9. **Source-sync invariant.** The canon store is only authoritative if the work
   actually landed there. Work done in another surface (a separate agent
   session, a local checkout, a handoff to another tool) can leave canon
   several versions stale while looking current. Before trusting a version
   number, verify it against the artefacts themselves, and treat any
   unsynced-source discovery as an issue to raise, not a detail to absorb.
10. **Research live.** Platform/framework facts for a new target are verified by
   live search at decision time, never from memory.
11. **No floating questions.** Every open question has a Q id, an owner-facing
    flag, and a documented interim assumption. Session close leaves nothing untracked.
12. **Canon-first generation.** Before generating any task, design, code, or
    documentation, search the project's connected canon store and treat what's
    found there as authoritative — never assume when canonical information
    exists. If assets conflict, surface the conflict rather than inventing a
    resolution. Follow the six-step sequence and check task-orchestrator plus
    the project's own installed skills first; see `canon-first-workflow.md`.

See `skill-baseline.md` for the work loop, the MCP-first rule, and the
five-point checklist every generated skill must satisfy.
