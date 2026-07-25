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
9. **Research live.** Platform/framework facts for a new target are verified by
   live search at decision time, never from memory.
10. **No floating questions.** Every open question has a Q id, an owner-facing
    flag, and a documented interim assumption. Session close leaves nothing untracked.
