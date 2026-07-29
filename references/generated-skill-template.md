# Template — every generated project skill

```markdown
---
name: <prefix>-<domain>
description: <what it does> + pushy trigger contexts specific to this project
(mention the project name, the line, and the phrases the owner actually uses).
---

# <Skill title>

## Canon (read first, never re-decide)
- Canon root: <location + id>
- Sources of truth: <files + ids>. Content flows FROM these THROUGH the pipeline.
  Never hand-type, duplicate, or invent canonical content.
- This line's tracker: <LINE>_TRACKER.json at canon root — one JSON per delivery line.
- Memory tiers: SESSION_STATE.md, plus <tier 2 / tier 3 files, or "none">. Precedence per
  `memory-tiers.md`: most version-specific file wins for version-specific facts; the
  locked-architecture tier wins for locked ones.
- Locked: <list>. Design-controlled (change via logged decision only): <list>.
- Open questions <Q ids>: flag, don't invent.

## Session loop
- Open: read SESSION_STATE.md at canon root → resume the stated next step. No preamble.
- Close / `/consolidate`: write decision-log entry → update SESSION_STATE.md and this
  line's tracker JSON (statuses, evidence baseline, issues, suite_version if skills
  changed). Bump `meta.revision` and append a `log` entry on every tracker write.

## Tool constraints
<Project-discovered connector quirks, phrased defensively: if a tool isn't
connected, ask the owner to reconnect rather than proceeding from memory.>

## Dependencies
- `task-orchestrator` — standing dependency for bundled or repeated work (see
  `canon-first-workflow.md`'s task-orchestrator integration section). Route any
  DRAFT step that repeats a subtask across many items (per-row tracker
  updates, per-card content passes, per-module verification checks) through it
  rather than looping serially in one context. If not installed, note the gap
  here rather than silently omitting it.
- <any other standing dependencies this skill has — installed public skills it
  orchestrates rather than duplicates, e.g. pdf, xlsx, frontend-design.>

## Canon-first workflow
<Verbatim from canon-first-workflow.md: search canon before generating anything;
the six-step sequence (search, summarise, identify missing, plan, tasks,
produce-after-approval); check task-orchestrator and the project's own
installed skills before acting; surface conflicts, never invent a resolution.>

## Work loop & MCP use
<Verbatim from skill-baseline.md sections 1-2, with this skill's own VERIFY
checks named explicitly.>

## Tunable vs locked
<What this skill may change, what it may only report on, and whether it fixes
or reports when a gate fails.>

## Working rules
<Copied from working-rules.md, trimmed to what applies to this skill's class.>

## Procedures
<The skill's actual loops, as explicit numbered step sequences — e.g.
render pipeline: data source → generator → verify counts → proof → sync.>

## Uses these installed skills
<Named list — e.g. pdf, xlsx, frontend-design, engineering:testing-strategy —
with when to invoke each. This skill orchestrates; it does not duplicate them.>
```

Every generated skill is checked against the five-point baseline in
`skill-baseline.md` before it is packaged. Missing any point = fails review.

Class notes:
- **Canon skill**: mostly the Canon block, style system, naming, spec tables. No procedures beyond verification.
- **Line skill**: procedures + phase plan + its line's tracker section. First task of a NEW class is always that class's tracker.
- **Ops skill**: cross-line procedure (QA checklist, playtest protocol, engagement lifecycle).
- **Orchestrator**: routing table only — which class member handles what; build order.
