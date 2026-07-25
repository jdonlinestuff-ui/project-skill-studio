# Tracker Shell spec v1.0

Every dashboard any studio skill emits conforms to this shell. Conformance is
checked **at skill creation**, not retrofitted: a skill that emits a
non-conforming dashboard fails creation review and the tracker flags it as an
issue.

**The shell is data-driven: swap the DATA block only.** Item content lives in one
DATA object at the foot of the file; layout, theming and interaction are shared.
A new dashboard for a different line replaces DATA and the title/source labels —
nothing else.

**Canonical copy-from sources** (project's own canon store, not this skill):

| Artefact | Role |
|---|---|
| `Tracker Dashboard.dc.html` + `support.js` | the shell itself — authoritative |
| `Design Tracker Dashboard (compiled, standalone).html` | compiled instance, physical line |
| `Online Dev Tracker Dashboard (compiled, standalone).html` | compiled instance, digital line |

Record their IDs in the project's canon skill. `references/tracker-shell-reference.html`
in this skill is a **plain-HTML approximation** for projects with no component
runtime; where the two differ, the project's own shell wins.

## 1. Source of truth
The JSON tracker is truth; HTML is a regenerated view of it. Never treat the
HTML as the record, and never hand-edit it as a way of recording state.

## 2. Static bake, mobile-first — MANDATORY
- All content is **statically baked into the HTML**. The page must render fully
  with JavaScript disabled or blocked; JS is enhancement only.
- Single-column stack on narrow screens; 44px bar buttons; wide grids scroll
  horizontally inside a bordered panel rather than reflowing into unreadable columns.
- **Print-safe:** every control carries a `noprint` class and is hidden under
  `@media print`, so the same page prints as a clean status report.
- Rationale: a JS-dependent dashboard rendered blank on a phone in real use.
  Assume the owner opens this on mobile first.

## 3. Status vocabulary (fixed)
| Status | Glyph | Label |
|---|---|---|
| pass | `✓` U+2713 | PASS |
| fail | `✕` U+2715 | FAIL |
| pending | `~` tilde | PEND |
| blocked | `■` U+25A0 | BLOCK |
| na | `–` U+2013 | N/A |

Labels are abbreviated so a mark fits a narrow grid cell without wrapping.

Each renders as **glyph + word + tint** — never colour alone (accessibility,
greyscale printing, colour-blind readers). Domain labels may alias a status
(INSTALLED→pass, REINSTALL→fail, PARKED→blocked), but the glyph/word/tint set
itself is fixed and not extended per project.

## 4. Badge axis — build state
Build state travels on its own axis, visually distinct from the check marks:
`INTEGRATED` (solid header fill) · `TESTED` (tinted fill) · `BUILDING` (outline)
· `PROTOTYPE` (outline) — plus `PROPOSED` and `OPEN` for queue rows. A row can
be TESTED while individual checks still read PEND; that combination is the whole
point of separating the axes. Versions and `built_against` render as muted mono
text beneath the item name, never as a status colour.

## 5. Item actions — the trio
`!` EXPLAIN · `✓` PROCEED · `+` IMPROVE — 30px circular mono buttons on every
actionable row. They **toggle**: pressing the same one again unmarks it.
IMPROVE reveals a per-row textarea whose text is appended to that item's line in
the compiled prompt.

Untouched items stay **pending**; there is no HOLD action, because doing nothing
already means held.

## 6. Bar flags (five, fixed)
`✎ CREATE PROMPT` (primary — the single sync action) · `RESET` ·
`↺ REFRESH BUILD` · `⇄ CANON SYNC` · `↻ REFRESH DATA`

Never add separate Save/Export buttons that duplicate CREATE PROMPT. Marked
actions and notes compile into one paste-ready prompt for the next session.
RESET clears marks made in this sitting; it does not alter tracker state.

## 7. Check names (build lines)
Six checks, abbreviated to three letters in the grid header:

| Check | Header |
|---|---|
| Typecheck | `TYP` |
| Unit | `UNI` |
| Golden files | `GLD` |
| Multi-client | `MUL` |
| Code security | `SEC` |
| Privacy | `PII` |

## 8. Evidence discipline
Every non-pending status carries an evidence string stating what was actually
run or observed ("tsc 0 errors; 26 assertions; golden 2/3 tiers reproduce").
A status asserted without evidence fails review. **Absent evidence, an item is
pending — not pass.** This is what stops a tracker drifting from reality.

## 9. Section order (fixed)
1. **Header** — mono eyebrow (project · line), serif title, right-aligned source
   label + baseline date + who maintains it
2. **Metrics strip** — auto-fit tiles counting each build state, proofs awaiting,
   gates pending
3. **Action key** — explains every control before first use, opening with the
   sync contract: *Claude cannot see edits made here. Mark rows, then press
   Create prompt and paste the result into chat.*
4. **Sticky bar** — the five flags, scheme switcher, marked count, data stamp
5. **Prompt textarea** — appears in place once CREATE PROMPT is pressed
6. **Main grid** — the line's primary items with check marks and evidence
7. **Queues** — proof queue, gate status, decisions pending
8. **Open issues** — severity mark + note
9. **Risk register** — exposure · cause · control
10. **Budget & cost** — per-line bar, spend state, total remaining
11. **Timeline & milestones** — dotted rail, labelled *target dates, not commitments*
12. **Next actions** — numbered, with an owner per row
13. **Update log** — accent-ruled entries, newest first
14. **Footer** — active scheme name and the shell's reuse note

A dashboard that reorders these fails conformance: the owner learns one layout,
not one per skill. Sections with no data are omitted, not left empty.

## 10. Typography slots
Three slots, not three specific fonts — a project fills them from its own system:
a **display serif** for headings, a **UI sans** for body and controls, and a
**mono** for evidence strings, IDs, hashes and versions. Mono on evidence is
load-bearing: it makes a fabricated-looking value visually obvious.

## 11. Colour schemes (four)
Revises the v1.0 black-on-white-only rule. Four schemes ship; default is Ink.
Owner-facing dashboards stay working tools — schemes vary contrast and warmth,
not decoration, and no scheme carries product branding.

| Token | Ink (default) | Parchment | Mono HC | Slate dark |
|---|---|---|---|---|
| bg | `#FFFFFF` | `#FAF7F0` | `#FFFFFF` | `#14181D` |
| panel | `#FFFFFF` | `#FFFDF8` | `#FFFFFF` | `#1B2027` |
| text | `#111418` | `#1A1A1A` | `#000000` | `#E8EDF2` |
| muted | `#4A5158` | `#5A5145` | `#2B2B2B` | `#A3AEBA` |
| line | `#D6DAE0` | `#DED5C4` | `#000000` | `#2E3742` |
| accent | `#1F4E79` | `#7A5E23` | `#000000` | `#7FB2E5` |
| pass | `#186A3B` | `#2F5D34` | `#000000` | `#6FD08C` |
| fail | `#A32020` | `#96261F` | `#000000` | `#F58A80` |
| blocked | `#8A4B00` | `#8A5A12` | `#000000` | `#E8B366` |

Measured worst-case contrast (all pairs, AA threshold 4.5:1): Ink 5.94,
Parchment 5.13, Mono HC 14.16, Slate dark 6.81 — all pass.

**A project's own schemes must be audited, not assumed.** The source project's
four are `Canon v6` (default), `Slate console`, `Dark console`, `Mono print`.
Auditing Canon v6 numerically found real failures that eyeballing had missed:

| Pair | Ratio | |
|---|---|---|
| ink `#101D3D` on bg `#F6ECD6` | 14.14 | AA |
| accentText `#A8843C` on bg `#F6ECD6` | **2.97** | fails AA and AA-large |
| accentText `#A8843C` on panel `#FFFAEE` | 3.34 | AA-large only |
| muted `#7A6E55` on bg | 4.27 | AA-large only |
| na mark `#9A8F75` on tint | **2.67** | fails |
| pending mark `#A97605` on tint | 3.45 | AA-large only |

The darkened gold was adopted to fix a contrast issue, and it does improve on the
lighter `#C9A961` — but at 2.97 on cream it still fails for the small mono labels
it is actually used on. Darkening to roughly `#7A5E23` clears AA on both bg and
panel.

**Verify contrast numerically, never by eye.** Mono HC relies on glyph, weight
and border rather than hue, so it survives greyscale printing.

Ship an **in-page scheme switcher**. It is a JS enhancement over the
statically-baked default scheme (§2) — with JS blocked the page still renders in
the default and the switcher is simply absent.

`references/dashboard-sample-generator.py` renders all four schemes to PNG and
prints the contrast table. Run it when changing any token.

## 12. Sync loop
Owner marks items → CREATE PROMPT → pastes into the next session → Claude
applies the edits to the tracker JSON → regenerates the HTML → delivers both.
