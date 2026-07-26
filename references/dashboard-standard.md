# Dashboard contract — pointer

**`DASHBOARD_SPEC.md` (v3.0) in this folder is the authority.** Read it, not this
file. This page exists only to record what changed and to stop anyone building
from the superseded rules below.

Reference build: **`dashboard-reference.html`** — copy it, point `TRACKER_SOURCE`
at the line's JSON, replace the `EMBEDDED` seed. Building from spec prose instead
of copying the reference is how drift starts.

## What v3.0 changed, and why it matters

| | Superseded (Tracker Shell v1.0) | v3.0 |
|---|---|---|
| Data | statically baked into the HTML | **live fetch** of a JSON source at run time |
| JS | enhancement only; page had to work with JS off | JS is **required** for the live path; the offline path is an announced snapshot |
| Default surface | black on white | black on **cream** |
| Type | three slots, sizes unspecified | **six px sizes only**, every `font:` shorthand ends with a family |

**The reversal is deliberate, not a drift.** v1.0's static-bake rule was
generalised from an earlier artefact and it is incompatible with the thing this
shell exists to prevent: *the moment a status is typed into HTML it starts lying,
and nobody can tell how stale it is.* A dashboard is a **view over a source**,
never a copy of it. Offline use is served by an `EMBEDDED` snapshot that must
announce itself — never by pretending baked data is current.

## Non-negotiables most likely to drift

- **px only, and every `font:` shorthand ends with a family.** A family-less
  shorthand is invalid CSS and silently renders at 16px — the single biggest
  cause of drift. When unsure, write `font-size` and `font-family` separately.
- **Six sizes**: 27 / 26 / 15 px serif titles, 14 / 15 / 13 px control and chip
  glyphs, **12 px for anything containing words**, 10 px small-caps chrome.
- **Status marks are glyph + word + tint**, 24px tall, radius 3px — `✓ PASS`,
  `~ PEND`, `✕ FAIL`, `■ BLOCK`, `– N/A`. The word is what survives greyscale
  and colour-blindness; never a bare glyph, never colour alone.
- **Action buttons are 30px circles**, 2px border, three per actionable row.
  Selected **inverts to a solid ink fill** — not a tint, ring, tick or animation.
  One selection per row; tapping again clears it. No hover-only affordance.
- **Scheme switcher is four swatch buttons**, never a `<select>`. Selection lives
  in state, never in the DOM alone, so it survives a re-render or data refresh.
- **Radii** 4 / 3 / 2 / 50%. Never 8px. Never a border on an individual cell.

## Data discipline

Metric counts, budget totals and percentages are **derived at render, never
stored**. A missing array omits its section; an empty array renders the heading
with `— none —`, so the reader can tell empty from missing. An **issue** has
happened; a **risk** would hurt if it did. Exactly one milestone is `next`, and a
blocked row names what blocks it. Refs are unique project-wide: M, B, R, I, D.
Placeholder numbers must say so in the note and raise a next action asking for
the real ones.

## Prompt protocol

The dashboard never writes to its source. The user marks rows, presses CREATE
PROMPT, and pastes the block into chat — the only channel back. The emitted block
names the revision the user was viewing, so a write can be re-based if the source
moved on. Keep the how-this-works panel on every dashboard saying exactly that.

## Naming

The spec calls the source constant `TRACKER_SOURCE`; the upstream skill body
calls it `DASHBOARD_SOURCE`. The reference defines `TRACKER_SOURCE` and aliases
`DASHBOARD_SOURCE` to it so either name works. Pick one per project and say which.
