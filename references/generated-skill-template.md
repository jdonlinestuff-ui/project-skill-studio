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
- Locked: <list>. Design-controlled (change via logged decision only): <list>.
- Open questions <Q ids>: flag, don't invent.

## Session loop
- Open: read SESSION_STATE.md at canon root → resume the stated next step. No preamble.
- Close / `/consolidate`: write decision-log entry → update SESSION_STATE.md and
  PROJECT_TRACKER.json (statuses, stale flags, suite_version if skills changed).

## Tool constraints
<Project-discovered connector quirks, phrased defensively: if a tool isn't
connected, ask the owner to reconnect rather than proceeding from memory.>

## Working rules
<Copied from working-rules.md, trimmed to what applies to this skill's class.>

## Procedures
<The skill's actual loops, as explicit numbered step sequences — e.g.
render pipeline: data source → generator → verify counts → proof → sync.>

## Uses these installed skills
<Named list — e.g. pdf, xlsx, frontend-design, engineering:testing-strategy —
with when to invoke each. This skill orchestrates; it does not duplicate them.>
```

Class notes:
- **Canon skill**: mostly the Canon block, style system, naming, spec tables. No procedures beyond verification.
- **Line skill**: procedures + phase plan + its line's tracker section. First task of a NEW class is always that class's tracker.
- **Ops skill**: cross-line procedure (QA checklist, playtest protocol, engagement lifecycle).
- **Orchestrator**: routing table only — which class member handles what; build order.
