# Tracker Shell spec v1.0

Every dashboard any studio skill emits conforms to this shell. Conformance is
checked **at skill creation**, not retrofitted: a skill that emits a
non-conforming dashboard fails creation review and the tracker flags it as an
issue. Nominate one skill's dashboard as the reference implementation and diff
new ones against it.

## 1. Source of truth
The JSON tracker is truth; HTML is a regenerated view of it. Never treat the
HTML as the record, and never hand-edit it as a way of recording state.

## 2. Static bake, mobile-first — MANDATORY
- All content is **statically baked into the HTML**. The page must render fully
  with JavaScript disabled or blocked; JS is enhancement only.
- Single-column stack on narrow screens, 44px minimum touch targets, system fonts.
- Rationale: a JS-dependent dashboard rendered blank on a phone in real use.
  Assume the owner opens this on mobile first.

## 3. Status vocabulary (fixed)
| Status | Glyph | Word |
|---|---|---|
| pass | ✓ | PASS |
| fail | ✗ | FAIL |
| pending | ◦ | PENDING |
| blocked | ▲ | BLOCKED |
| na | – | N/A |

Each renders as **glyph + word + tint** — never colour alone (accessibility,
greyscale printing, colour-blind readers). Domain labels may alias a status
(INSTALLED→pass, REINSTALL→fail, PARKED→blocked), but the glyph/word/tint set
itself is fixed and not extended per project.

## 4. Badge axis
Secondary metadata — versions, `depends_on`, the canon version an item was built
against — renders as neutral badges on a separate visual axis from status.
Never encode metadata as a status colour.

## 5. Item actions — the trio
`!` EXPLAIN · `✓` PROCEED · `+` IMPROVE

Untouched items stay **pending**; there is no HOLD action, because doing nothing
already means held.

## 6. Bar flags (five)
`✎ CREATE PROMPT` (primary — the single sync action) · `↻ REFRESH DATA` ·
`↺ REFRESH BUILD` · `⇄ CANON SYNC` · `⚑ RAISE ISSUE`

Never add separate Save/Export buttons that duplicate CREATE PROMPT. Marked
actions and notes compile into one paste-ready prompt for the next session.

## 7. Check names (build lines)
`TYPECHECK` · `UNIT` · `GOLDEN` · `MULTICLIENT` · `REVIEW` · `PRIVACY`

## 8. Evidence discipline
Every non-pending status carries an evidence string stating what was actually
run or observed ("tsc 0 errors; 26 assertions; golden 2/3 tiers reproduce").
A status asserted without evidence fails review. **Absent evidence, an item is
pending — not pass.** This is what stops a tracker drifting from reality.

## 9. Colour schemes (four)
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

**Verify contrast numerically, never by eye.** Mono HC relies on glyph, weight
and border rather than hue, so it survives greyscale printing. If a project
supplies a brand accent, check it before use: a mid-tone gold on cream, for
instance, typically fails AA for body text and needs darkening (`#A8843C` →
`#7A5E23`) or restricting to large text.

`references/dashboard-sample-generator.py` renders all four schemes to PNG and
prints the contrast table. Run it when changing any token.

## 10. Sync loop
Owner marks items → CREATE PROMPT → pastes into the next session → Claude
applies the edits to the tracker JSON → regenerates the HTML → delivers both.
