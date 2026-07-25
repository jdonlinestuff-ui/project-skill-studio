# Dashboard standard

A static HTML view regenerated from PROJECT_TRACKER.json. The JSON is truth.

## Visual
- Plain black-on-white, high-contrast, system fonts. NO brand theming — the
  owner-facing dashboard is a working tool, not a deliverable.
- Sections: stale items (top, if any) → skills roster → lines/items → backlog →
  decisions → open questions. Suite version + updated date in the header.

## Interaction standard (locked pattern)
- Every item defaults to **pending**; untouched items require no action (no HOLD button).
- Actionable items carry three buttons: **EXPLAIN** (queue a request for Claude to
  explain the item), **PROCEED** (approve/advance it), **IMPROVE** (opens a small
  text field for the owner's improvement note).
- One single **Create prompt** button compiles every marked action + note into a
  ready-to-paste sync prompt for the next Claude session (plain text block, copy
  button). Never provide separate Save and Export buttons that do the same thing.
- Code-line dashboards add two extra global actions:
  - **REFRESH BUILD** — queues "run the full clean pipeline across all modules"
  - **CANON SYNC** — queues "diff the build against canon and report divergence"
- No localStorage/sessionStorage (fails in Claude.ai artifacts) — state lives in
  JS memory; the Create-prompt output is how state leaves the page.

## Sync loop
Owner marks items → Create prompt → pastes into next session → Claude applies the
edits to PROJECT_TRACKER.json → regenerates the dashboard HTML → delivers both.
