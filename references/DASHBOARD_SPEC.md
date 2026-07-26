# Status Dashboard Shell — reusable dashboard spec v3.0

Project-agnostic. This is the visual and data contract for every dashboard built with the
`status-dashboard` skill. Sections 6–11 are literal and apply verbatim to any project.
Where the text says "canon", read "the project's source-of-truth folder"; where it names a
`cra-*` skill, read "the skill that owns that delivery line". Section 8 is an EXAMPLE
roster from the project this shell was designed on — replace it with the host project's own lines, keeping the pattern (one JSON source per line, six check columns, six sizes).

Reference implementation: `online-dev-tracker-dashboard_v8.html` (live-fetch build) and
`Tracker Dashboard.dc.html` (design source).
**This spec is a visual contract, not a style suggestion.** A dashboard built from it must
be pixel-comparable to the reference: same type sizes, same chip shape, same round action
buttons, same spacing. Sections 9–11 give the literal CSS and markup — copy them, do not
re-derive them. If a value is not listed here, take it from the reference file.

**v3.0 changes the data model.** The dashboard is a VIEW over a canon JSON source that it
fetches at run time (§3). Status data is never baked into the HTML — an embedded snapshot
exists only as a clearly-labelled offline fallback. Read §3 before §9–11.

Things that went wrong the last time this was rebuilt, all now specified below:
`rem`-based font sizes, glyph-only 14px status squares, square 4px action buttons,
bordered table cells, 8px radii, and `font:` shorthands with no family.

---

## 1. What is fixed vs what each skill supplies

FIXED (never re-invent per skill)
- every value in sections 9–11: type scale, colours, spacing, radii, control geometry
- section order, grid columns, prompt protocol
- status vocabulary and the glyph+word+tint marks
- the four colour schemes and the in-page scheme switcher
- print rules (`.noprint`, no controls on paper)

SUPPLIED BY THE SKILL
- the **source URL** (`TRACKER_SOURCE`) and the canon JSON behind it (section 3)
- nothing else. Title, source label, check-column names and currency all arrive in
  `meta` from the source file — a skill that hard-codes them has already drifted.

---

## 2. Status vocabulary — one set, all skills

| key | glyph | word | meaning |
|---|---|---|---|
| `pass` | ✓ | PASS | verified by evidence that exists now |
| `fail` | ✕ | FAIL | ran and did not pass |
| `pending` | ~ | PEND | not yet run / not yet evidenced |
| `blocked` | ■ | BLOCK | cannot run until an upstream issue clears |
| `na` | – | N/A | does not apply to this row |

Rules
- **Glyph AND word AND tint always travel together.** A bare glyph, a bare colour square,
  or a colour-only cell is a spec violation — the word is what survives greyscale.
- `pending` is the default. Never mark `pass` on code review alone.
- Build-state badges are a separate axis: `INTEGRATED / TESTED / BUILDING / PROTOTYPE`
  (`PROPOSED / PENDING` in queues). No new badge words without a canon decision.
- Severity and exposure reuse the marks: High → ✕, Med → ~, Low → –.
- Rows open by definition (decisions) carry NO status badge.
- A mark is normally evidence-derived and read-only in the browser. §4e's feedback mark is
  the one deliberate exception — facilitator-set, not evidence-derived — and it says so in
  its own prose rather than quietly breaking the read-only rule everywhere else.

---

## 3. Data contract — the tracker reads its source, it does not remember it

**A tracker is a VIEW, never a copy.** Baked-in data is the failure mode this shell exists
to prevent: the moment a status is typed into the HTML it starts lying, and nobody can
tell how stale it is. The dashboard loads `DESIGN_TRACKER.json` (or the line's equivalent
canon source) at run time and renders whatever it finds.

### 3.1 Source of truth

One JSON file per delivery line, in the project's source-of-truth folder, named in the
dashboard header (e.g. `DESIGN_TRACKER.json`, `ONLINE_DEV_TRACKER.json`). The dashboard never writes
to it — writes happen only through Claude, via the CREATE PROMPT protocol (§5).

### 3.2 Load modes, in priority order

A dashboard implements **A and C**, and always supports **B**:

**A — Live fetch (default).** A `TRACKER_SOURCE` constant holds the source URL. On load,
and again on every ↻ REFRESH DATA, the page does `fetch(TRACKER_SOURCE, {cache:'no-store'})`
and renders the response. The stamp then reads `data as at <fetch time> · <source>`.
Acceptable URLs: a Drive direct-download link
(`https://drive.google.com/uc?export=download&id=<FILE_ID>`), a published-to-web link, or
a relative path when the JSON sits beside the HTML.

**B — MCP re-issue (whenever no URL is reachable, and for any structural change).** The
user presses ↻ REFRESH DATA, presses CREATE PROMPT, and pastes. Claude reads the source
through the Drive connector, re-derives every status from current evidence, and re-issues
the dashboard. This is the only path that can also add rows, change sections, or resolve
evidence — a browser fetch can only re-render what is already in the JSON.

**C — Snapshot fallback (degraded, never silent).** An `EMBEDDED` object holds the last
known-good payload so the file still opens offline or when the fetch fails (CORS, revoked
link, no network). When it is used the dashboard MUST show a full-width banner above the
metric strip:
`⚠ SNAPSHOT — live source unreachable. Showing data as at <embedded timestamp>.` in
`600 12px/1.45 IBM Plex Mono,monospace` on the `fail` tint, and the header stamp must read
`SNAPSHOT` rather than a fetch time. Never render snapshot data as if it were live.

### 3.3 Source payload shape

```jsonc
{
  "meta": {
    "line": "online-dev",
    "title": "Digital Dev Tracker",
    "sourceLabel": "05_TEAMS_APP_v0.6_SOURCE",
    "checkNames": ["Typecheck","Unit","Golden files","Multi-client","Code security","Privacy"],
    "currency": "AUD",
    "revision": 47,                    // increments on every write by Claude
    "generatedAt": "2026-07-25T10:12:00+10:00"
  },
  "modules":     [[name, builtAgainst, badge, [6 status keys], evidenceNote], …],
  "proofs":      [[ref, name, badge, note], …],
  "gates":       [[ref, name, badge, note], …],
  "decisions":   [[ref, title, "OPEN", note], …],
  "issues":      [[ref, "High"|"Med"|"Low", note], …],
  "risks":       [[ref, "High"|"Med"|"Low", title, cause, control], …],
  "budget":      [[ref, lineItem, budgetAmount, spentAmount, note], …],
  "milestones":  [[ref, "YYYY-MM-DD", title, "done"|"next"|"pending"|"blocked", note], …],
  "nextActions": [[n, action, owner], …],
  "feedback":    [[ref, raisedBy, text, targetRef, mark, owner, priority, timeline, note], …],
  "projects":    [[ref, name, status, people, tasks, thisWeek], …],
  "people":      [[name, projectRef, tasks, note], …],
  "log":         [[when, what], …]
}
```

`meta` drives the header title, the source label, the check-column names and the currency —
so a second line needs a new JSON file, not a new HTML file. The row arrays are positional
and identical across lines; a skill that needs a different column set changes
`meta.checkNames`, not the shell.

### 3.4 Freshness rules

- Header stamp always states BOTH the moment data was fetched and `meta.generatedAt`
  (when Claude last wrote the source): `data as at 14:02 · source 2026-07-25 rev 47`.
- `generatedAt` older than **7 days** → append a `~ STALE` chip beside the stamp.
- Older than **30 days**, or `meta` missing → the snapshot banner treatment of §3.2C, worded
  `⚠ SOURCE STALE — re-run REFRESH DATA before trusting this view.`
- A failed fetch is never silent and never falls through to an empty section.
- Sections whose arrays are absent are omitted; sections present but empty render their
  heading with `— none —` in `400 12px/1.45 Helvetica Neue,Helvetica,Arial,sans-serif`
  muted, so the reader can tell empty from missing.

### 3.5 Content discipline (unchanged, and enforced in the JSON, not the HTML)

- `evidenceNote` states the evidence or names the gap with ids (`(I6)`, `(S8)`). No note = no claim.
- Totals, percentages and metric counts are DERIVED at render, never stored.
- Statuses change only when evidence changes, and every change adds a `log` entry.

---

## 4. Sections, in order

1. Header · 2. Metric strip · 3. How-this-works panel · 4. Sticky control bar ·
5. Prompt output · 6. Portfolio Roster · 7. People & Allocation · 8. Module grid
(legend above) · 9. Queues (Proofs, Gates, Decisions) · 10. Open Issues · 11. Risk
Register · 12. Budget & Cost · 13. Timeline & Milestones · 14. Next Actions ·
15. Feedback & Suggestions · 16. Update Log

Drop sections with no data; never reorder what remains. (v3.2 note: Portfolio Roster and
People & Allocation are new, inserted before Module Grid because they're overview-level —
a portfolio comes before per-line detail. This is the second one-time insertion; §4e was
the first. Once shipped, an insertion becomes part of the fixed order like everything else
— "never reorder" governs from here forward, not retroactively.)

### 4b. Risk register
Issue = has happened. Risk = would hurt if it did. Never duplicate one as the other;
reference the issue id in the cause line. Four parts, no more: exposure (High/Med/Low),
risk (the thing going wrong), cause (evidence state, with ids), control (the gate, flag or
sequencing that holds it — if none exists, say so plainly). Closure is logged.

### 4c. Budget & cost
Plain numbers in DATA; the shell formats and totals. State chip is computed:
`– UNSPENT` (0) · `✓ ON TRACK` (<85%) · `~ WATCH` (85–100%) · `✕ OVER` (>100%).
One line per committed or forecast cost centre. Costs a decision hasn't released stay at
zero with the blocking id in the note. Currency is set once, in `money()`.

### 4d. Timeline & milestones
Dates are TARGETS and the section header says so. States: `done` (title greys back),
`next` (exactly one), `pending`, `blocked` (note names the blocking id). One line per
milestone that changes what the project can do. Dependencies stated in the note
("Gated on M4"). Slipping a date is a tracker change and gets a log line.

### 4e. Feedback & Suggestions — a facilitator dashboard, not a voting app

This section exists for one specific use: **a single facilitator records the room's
reaction during a live review**, not a multi-person live-voting system with logins,
identity, or a running tally. No vote count anywhere in this section — a running number
invites gaming the count and implies a rigour ("N people voted") the dashboard cannot
actually back, since the dashboard never verifies who touched it. What it needs is
simpler and more honest: **a status, set once, by whoever is holding the room's pen.**

**Row fields**: `ref` (F1, F2…) · `raisedBy` (free text, optional — a name, "Table 2", or
blank for an unattributed or facilitator-paraphrased note) · `text` (the suggestion or
comment) · `targetRef` (an existing M/B/R/I/D/module ref this is about, or blank for a
fresh idea with no home yet) · `mark` · `owner` (optional, filled once someone is assigned
to action it — same free-text convention as Next Actions) · `priority` (`High`/`Med`/`Low`,
the same three words as everywhere else — no fourth priority vocabulary) · `timeline`
(a target date, same "target, not a commitment" convention as Milestones) · `note`.

**Mark** is `pass`/`pending`/`fail` under the hood, rendered with domain words exactly the
way severity already borrows the marks in §2: `✓ INTERESTED` (pass tint) ·
`~ UNDECIDED` (pending tint, the default) · `✕ NOT INTERESTED` (fail tint). Unlike every
other chip in this spec, **this one is clickable** — the facilitator cycles it directly
(pending → interested → not interested → pending) rather than it being derived from
evidence. State it as clickable in the row markup itself; do not let a reader assume every
chip in the dashboard behaves this way, because none of the others do.

**Attribution is always optional, on both fields.** The dashboard is as often filled in by
one person transcribing for a room as it is by named individuals, and the spec should not
force a choice the facilitator hasn't made. Leave `raisedBy` blank for a group note.

**Getting it out of the room.** No email-send or spreadsheet-export integration ships with
this section — that needs a real connector decision (a mail tool, a sheet-writing
integration) and is explicitly deferred, not silently built. Two things already cover most
of the need without any new integration: the page prints cleanly per the existing
print-safe rule, so `Print → Save as PDF` is a written record with zero new code; and
Create Prompt's output (§5) is a plain text block, which pastes into an email body or a
spreadsheet cell exactly as it pastes into Claude. If a project wants a one-click "email
this" or "export CSV" beyond copy-paste, raise it as its own decision — don't fold it into
this section's build silently.

**Promoting a suggestion.** PROCEED on a feedback row (§5's ordinary trio, unchanged
meaning) means "turn this into a real tracked item on the next write" — Claude reads the
marked rows, and a promoted suggestion becomes a new Next Action, Decision, or module note
depending on what it actually is, with the feedback row then closed out in the log. A
feedback row is never itself a permanent record; it is a capture surface that empties into
the sections that already have one.

**Also usable for sprint planning — no schema change, because the fields are already free
text.** `timeline` renders as plain escaped text with no date parsing anywhere in the
reference (verified, not assumed — check before relying on this if you fork the build); a
row can hold `"Sprint 14"` there exactly as it holds `"2026-08-05"` elsewhere. This section
is a captured-backlog list either way, and "which sprint" is one more thing a facilitator
can record about a row, same as who raised it or who owns it.

**Two things that stay separate on purpose, not by oversight:**
- `priority` is priority, not size. Sizing (points, t-shirt, hours) is a different axis
  that agile teams often — and regrettably — collapse into priority; don't repeat that
  here. If a project needs sizing, put it in `note` ("est. M") or extend the row with a
  project-specific field and document the extension, rather than overloading `priority`.
- The interest `mark` (§ above) is a stakeholder's reaction during a review. A sprint
  commitment is a planner's decision, often made later, often by someone else. Reusing one
  clickable chip for both would silently merge two different decisions into one field —
  record sprint commitment in `note` or `timeline` instead of repurposing `mark`.

**What this section deliberately does not give you**: capacity or velocity math, a
burndown, or a dedicated Sprint view with its own summary strip. That's a materially
bigger feature — closer to Budget's spend-bar treatment than to a captured-suggestions
list — and building it here would turn a "simple feedback action" into an agile-board
clone. If a project genuinely needs that, it's its own section and its own decision, not
a quiet extension of this one.

---

### 4f. Portfolio Roster — status across every project, not one line's detail

For a resource/portfolio tracker instance: one row per project, `meta.line` set to
something like `"portfolio"` or `"resources"` rather than a single build line. Every
other section (Module Grid, Risk Register, Budget…) is absent for this instance and
omitted per §3.4 — a portfolio view and a per-line detail view are different instances
of the same shell, not the same page wearing two hats.

**Fields**: `ref` (P1, P2…) · `name` · `status` · `people` (a count) · `tasks` (a count) ·
`thisWeek` (one line — key update or milestone for that project this week; expected to be
replaced weekly, not accumulated — the Update Log is where history lives, not this field).

**Status** aliases the fixed marks with domain words, the same pattern as severity (§2)
and the feedback interest mark (§4e): `✓ ON TRACK` (pass) · `~ AT RISK` (pending) ·
`■ BLOCKED` (blocked) · `✕ CANCELLED` (fail) · `– NOT STARTED` (na). Evidence-derived and
read-only, like every mark except §4e's — a project's status is something Claude or a
facilitator sets from the underlying line's own tracker, not something invented here.

**`people` and `tasks` — derived if the roster exists, recorded if it doesn't.** If §4g's
People & Allocation section has rows for a given project, its `people` count and `tasks`
count are DERIVED from that roster at render time — never independently typed, because two
numbers claiming to describe the same fact is exactly the drift this spec exists to
prevent. If no People roster is present for this tracker instance (a lighter-weight
portfolio view with no per-person breakdown), `people`/`tasks` are recorded directly on the
project row instead. A tracker instance picks one mode per section pair, not both at once.

### 4g. People & Allocation — task counts, never stored as a total

One row per person **per project** — someone working across three projects gets three
rows, not one row with a hand-added-up number. **Totals are always computed at render**,
summing every row for that name across every `projectRef`: this is the same "derived,
never stored" rule as Budget's percentage and Milestone counts, applied to a person's
total task count so it can never silently drift from the rows it's built from.

**Fields**: `name` · `projectRef` (an id from §4f) · `tasks` (a count for that person on
that one project) · `note`.

No seniority, role, or capacity/velocity math here — see §4e's sprint-planning note for
why capacity modelling is explicitly out of scope for this spec generally, not just for
feedback rows. This section counts tasks per person per project. That's the whole job.

## 5. Controls and the prompt protocol

## 5. Controls and the prompt protocol

Every actionable row carries the same trio (geometry in §10.7):
`!` EXPLAIN · `✓` PROCEED · `+` IMPROVE (opens an inline direction field).
Selected = filled with the theme ink. Re-clicking the same choice clears it.

Bar flags: REFRESH BUILD (full clean pipeline, re-stamp baseline) · CANON SYNC (re-pull
canon_versions, re-verify `built_against`).

**↻ REFRESH DATA is a live re-read, not a flag.** Pressing it re-fetches `TRACKER_SOURCE`
immediately (§3.2A) and re-renders from the response — no page reload, no rebuild. It also
sets the REFRESH DATA line in the prompt, so that if the fetch failed, or the user wants
Claude to re-derive statuses from evidence rather than merely re-read the file, pasting the
prompt does the deeper job (§3.2B). Button states: idle `↻ REFRESH DATA` → `↻ REFRESHING…`
during the fetch → back to idle with a new stamp, or the §3.2C banner on failure.

Create prompt emits, and copies to clipboard:

```
Sync the <line> tracker (<date>) — source <sourceLabel> rev <meta.revision>:
- REFRESH DATA: …            (if flagged)
- REFRESH BUILD: …           (if flagged)
- CANON SYNC: …              (if flagged)
- <ROW ID> <choice>[: <typed direction>]
- F<n> mark:<interested|not-interested|undecided>   (feedback rows only, if the mark moved from its last-known state)
```

A feedback row's mark is compiled as its own line, separate from the ordinary
`!`/`✓`/`+` choice line — a row can carry both (e.g. mark:interested AND an IMPROVE
detail) in the same prompt. `undecided` is only emitted if the mark was previously
something else and got cleared back; the default state is never emitted as a no-op line.

The revision number matters: it tells Claude which version of the source the user was
looking at, so a write can be refused or re-based if the source moved on.

The dashboard never mutates canon — the pasted prompt is the only channel back to Claude,
and the how-this-works panel says so on every dashboard.

**Write path.** Claude edits `DESIGN_TRACKER.json` (bump `meta.revision`, set
`meta.generatedAt`, append a `log` entry), uploads it to the canon folder, and tells the
user what changed. The HTML is only re-issued when the SHELL changes — a data change needs
no new HTML at all. That is the point of the split.

---

## 6. Colour schemes — exact values

`Canon v6` is the default; RESET returns to it. Each scheme is a complete token set:

```js
'Canon v6':      { bg:'#F6ECD6', panel:'#FFFAEE', ink:'#101D3D', headerBg:'#101D3D', headerFg:'#F6ECD6',
                   muted:'#7A6E55', line:'#E3D2A8', zebra:'#FBF4E3', accent:'#C9A961', onAccent:'#101D3D',
                   accentText:'#A8843C', body:'#4A4535', field:'#FFFDF7', tested:'#E7D9B4', testedFg:'#101D3D' }
'Slate console': { bg:'#EEF0F1', panel:'#FBFCFC', ink:'#1B2227', headerBg:'#1B2227', headerFg:'#EEF0F1',
                   muted:'#6F787D', line:'#DBE0E2', zebra:'#F4F6F6', accent:'#2F7D74', onAccent:'#FFFFFF',
                   accentText:'#2F7D74', body:'#3C464C', field:'#FFFFFF', tested:'#D6E7E4', testedFg:'#1B2227' }
'Dark console':  { bg:'#14171B', panel:'#1C2127', ink:'#E7E4DC', headerBg:'#242B33', headerFg:'#E7E4DC',
                   muted:'#8B939B', line:'#2C333B', zebra:'#20262D', accent:'#E0A93A', onAccent:'#14171B',
                   accentText:'#E0A93A', body:'#C3C8CD', field:'#161A1F', tested:'#3A424B', testedFg:'#E7E4DC' }
'Mono print':    { bg:'#F2F2F0', panel:'#FFFFFF', ink:'#111111', headerBg:'#111111', headerFg:'#FFFFFF',
                   muted:'#6E6E6E', line:'#DADADA', zebra:'#F7F7F5', accent:'#111111', onAccent:'#FFFFFF',
                   accentText:'#4A4A4A', body:'#333333', field:'#FFFFFF', tested:'#DDDDDD', testedFg:'#111111' }
```

Mark tints, per scheme (`{colour, tint}`):

| mark | Canon v6 | Slate | Dark | Mono |
|---|---|---|---|---|
| pass | #1E7A45 / #E4F2E9 | #1F6B45 / #E1EFE7 | #4CC38A / #17301F | #111111 / #E6E6E4 |
| fail | #B3261E / #FBE6E4 | #B4482F / #F9E7E2 | #F2665B / #331A19 | #111111 / #CFCFCD |
| pending | #A97605 / #F8EED6 | #9A6B12 / #F6EEDD | #E0A93A / #332714 | #6E6E6E / #EDEDEB |
| blocked | #141414 / #E8E4DA | #1B2227 / #E4E7E9 | #C3C8CD / #2A2F35 | #111111 / #C2C2C0 |
| na | #9A8F75 / #F1EADA | #8D969B / #EEF1F2 | #6B7178 / #22272D | #9A9A98 / #F4F4F2 |

On Canon v6 accent TEXT is `#A8843C`, not `#C9A961` — gold on cream fails contrast (I3).

---

## 7. Type — one table, every element, px only

This is the complete inventory. If an element is not listed, it is
`400 12px/1.45 Helvetica Neue,Helvetica,Arial,sans-serif`. Nothing on the page may use a
size that does not appear in this table.

| element | exact declaration |
|---|---|
| dashboard title | `700 27px/1.15 Libre Baskerville,Georgia,serif` |
| metric number | `700 26px/1 Libre Baskerville,Georgia,serif` |
| section title | `700 15px/1.2 Libre Baskerville,Georgia,serif` |
| key-panel circle glyph | `600 14px/1 IBM Plex Mono,monospace` |
| in-row action glyph (`!`, `✓`) | `600 13px/1 IBM Plex Mono,monospace` |
| in-row action glyph (`+` only) | `600 15px/1 IBM Plex Mono,monospace` |
| chip / badge glyph `<span>` | `font-size:13px` (inherits the chip's weight and family) |
| status chip, build badge, state chip | `600 12px/1 IBM Plex Mono,monospace` |
| column header (incl. the six check labels) | `600 12px/1.2 IBM Plex Mono,monospace` |
| row title / module name / line item | `600 12px/1.4` (mono for module names and refs, sans for prose titles) |
| row ref, money figure | `600 12px/1.4 IBM Plex Mono,monospace` |
| version line, owner, milestone date, log date | `400–500 12px/1.35–1.45 IBM Plex Mono,monospace` |
| body note, evidence, cause, control, action text | `400 12px/1.45 Helvetica Neue,Helvetica,Arial,sans-serif` |
| key-panel intro, key-panel description | `400 12px/1.45 Helvetica Neue,Helvetica,Arial,sans-serif` |
| key-panel control name | `700 12px/1.2 IBM Plex Mono,monospace` |
| bar button (primary, ghost, toggle) | `700 12px/1 IBM Plex Mono,monospace` (ghost `600`) |
| detail textarea, prompt output | `400 12px/1.5` (textarea sans, prompt output mono) |
| snapshot / stale banner | `600 12px/1.45 IBM Plex Mono,monospace` |
| empty-section `— none —` | `400 12px/1.45 Helvetica Neue,Helvetica,Arial,sans-serif` |
| eyebrow, header meta, metric label, SCHEME label, scheme buttons, marked-count, data stamp, section right-label, footer | `400–600 10px/1–1.5 IBM Plex Mono,monospace` |

So the whole page uses exactly six sizes: **27, 26, 15** (serif titles only), **14/15/13**
(control and chip glyphs only), **12** (everything with words in it), **10** (small-caps
chrome). There is no 11px, no 11.5px, no 13px text, no `rem`.

Rules
- **px only.** No `rem`, no `em`, no `%` font sizes.
- **Every `font:` shorthand MUST end with a family** — including the one-off cases above.
  A family-less shorthand is invalid CSS and silently renders at 16px. This has been the
  single biggest cause of drift; when in doubt write `font-size` + `font-family`
  separately rather than the shorthand.
- Three families only. Body prose: `Helvetica Neue,Helvetica,Arial,sans-serif`.
  Ids/labels/chips/buttons: `IBM Plex Mono,monospace`. Titles and metric numbers:
  `Libre Baskerville,Georgia,serif`.
- Weight vocabulary: 400 body, 500 meta, 600 labels/chips/titles-in-rows, 700 buttons and
  serif titles. No 300, no 800.
- Load: `https://fonts.googleapis.com/css2?family=Libre+Baskerville:wght@400;700&family=IBM+Plex+Mono:wght@400;500;600&display=swap`

---

## 8. EXAMPLE line roster — replace with the host project's

The rows below come from the project this shell was designed on. Keep the SHAPE (title,
source JSON, what a row means, six check labels, which sections matter) and substitute
your own lines.

### 8.1 Swap-in recommendations per skill

| skill | title | source JSON | a row is | `meta.checkNames` | sections that matter |
|---|---|---|---|---|---|
| cra-online-dev-tracker | Digital Dev Tracker | 05_TEAMS_APP_v0.6_SOURCE | an app module | TYP · UNI · GLD · MUL · SEC · PII | all (reference build) |
| cra-design-tracker | Programme Tracker | DESIGN_TRACKER.json | a delivery line | CANON · DRAFT · REVIEW · QA · PRINT · SHIP | metrics, queues, risks, budget, milestones |
| cra-card-design | Card Deck Tracker | card_data.py v6 | a card set | DATA · ART · TYPE · PROOF · WEBP · CANON | grid, proofs, issues |
| cra-manual-design | Manual Registry | manual registry v6 | a manual / cheatsheet / supplement | COPY · LAYOUT · RULES QA · VERSION · PDF · REGISTERED | grid, decisions, milestones |
| cra-box-design | Packaging Tracker | v6 brand system | a packaging part | COPY · ART · DIELINE · BLEED · PROOF · CANON | grid, proofs, budget |
| cra-print-production | Print Pack Tracker | print_ready_deck_v6 | an artefact heading to the printer | BLEED · TRIM · COLOUR · FONTS · RENDER · PACKAGED | grid, issues, budget, milestones |
| cra-game-publishing | Publishing Tracker | publisher brief | a publisher / channel / proof round | TEMPLATE · UPLOAD · PROOF · APPROVAL · FULFIL · CONTRACT | grid, decisions, budget, milestones |
| cra-game-marketing | Commercial Tracker | pricing model v1 | a channel or collateral piece | POSITION · COPY · ASSET · PRICE · LIVE · MEASURED | grid, budget, milestones |
| cra-client-engagement | Engagement Tracker | engagement record | a booked or proposed engagement | SCOPED · QUOTED · BOOKED · PREPPED · DELIVERED · REPORTED | grid, milestones, budget, risks |
| cra-workshop-design | Workshop Build Tracker | Workshop Manual v1.2 | a workshop module or framework pack | DESIGN · TIMING · MATERIALS · MAPPING · PILOTED · SIGNED OFF | grid, decisions, milestones |
| cra-playtest | Playtest Tracker | playtest log | a session | PLANNED · RUN · CAPTURED · ANALYSED · FED BACK · CLOSED | grid, issues, milestones |
| cra-balance-tuning | Balance Tracker | Scoring_Matrix v3.0 | a tuning question | SIM · EVIDENCE · RECO · REVIEWED · DECIDED · APPLIED | grid, decisions, risks |
| cra-rules-qa | Rules QA Tracker | canon rules set | a consistency sweep area | CARDS · MANUALS · CHEATSHEETS · SCORING · PACKS · DIGITAL | grid, issues, milestones |
| cra-expansion-design | Expansion Tracker | base 65-card canon | an expansion pack | SCOPE · MAPPING · CARDS · FACILITATION · QA · RELEASED | grid, decisions, budget |
| cra-platform-compliance | Compliance Gate Tracker | live platform policies | a platform | POLICY READ · MANIFEST · A11Y · PRIVACY · TEST · SUBMITTED | gates, issues, risks, milestones |
| cra-teams-app-dev | (uses the online-dev tracker) | — | — | — | — |
| cra-hosting-ops | Hosting Tracker | deployment plan | an environment or pipeline stage | IAC · BUILD · DEPLOY · MONITOR · BACKUP · COST | grid, risks, budget (planning only) |
| cra-mobile-dev | Mobile Tracker | GATED — awaiting Q10 | a mobile surface | — | milestones + risks only |
| cra-collab-integrations | Surface Tracker | integration brief | a collaboration surface | SPEC · AUTH · BOT · PRIVACY · TEST · SHIPPED | grid, gates, risks |

Fewer than six checks is fine — drop columns rather than invent gates nobody runs. Refs
stay unique programme-wide (M/B/R/I/D/AP/PG prefixes). Gated skills show the gate, not a
build grid pretending work is underway. cra-design-tracker's rows are the other trackers.

---

## 9. Page frame — exact

```css
body{margin:0;background:var(--bg);color:var(--ink);
     font-family:Helvetica Neue,Helvetica,Arial,sans-serif;}
.wrap{max-width:1080px;margin:0 auto;padding:32px 24px 64px;}
@media print{.noprint{display:none!important}}
```

Every panel and table container:
`background:var(--panel); border:1px solid var(--line); border-radius:4px;`
**Radius is 4px for containers, 3px for chips/buttons/fields, 2px for badges, 50% for the
action circles. Never 8px. Never a border on individual table cells** — rows are separated
by a single `border-top:1px solid var(--line)` and nothing else.

---

## 10. Component recipes — copy these

### 10.1 Header
```html
<div style="padding-bottom:14px;display:flex;flex-wrap:wrap;align-items:flex-end;
            justify-content:space-between;gap:12px;border-bottom:3px solid var(--ink)">
  <div style="display:flex;flex-direction:column;gap:6px">
    <div style="font:600 10px/1 IBM Plex Mono,monospace;letter-spacing:0.18em;color:var(--accentText)">CYBER RISK ASSESSMENT · ONLINE DEV</div>
    <div style="font:700 27px/1.15 Libre Baskerville,Georgia,serif;letter-spacing:-0.01em">Digital Dev Tracker</div>
  </div>
  <div style="font:400 10px/1.5 IBM Plex Mono,monospace;text-align:right;color:var(--muted)">source v0.6<br>baselined 2026-07-25</div>
</div>
```

### 10.2 Metric strip
Grid `repeat(auto-fit,minmax(120px,1fr))`, gap 10px, margin-top 18px.
Card: panel + 1px line + radius 4px, `padding:12px 12px 11px`, column flex, gap 4px.
Number `700 26px/1 Libre Baskerville,Georgia,serif`; label `500 10px/1.3 IBM Plex Mono,monospace; letter-spacing:0.1em; color:var(--muted)`.

### 10.3 How-this-works panel
Container: panel, `border:1px solid var(--line)`, `border-left:4px solid var(--accent)`,
radius 4px, `padding:16px 18px`, margin-top 22px.
Intro `400 12px/1.45 Helvetica Neue,Helvetica,Arial,sans-serif;color:var(--body)`,
margin-bottom 14px.
Key items: grid `repeat(auto-fit,minmax(210px,1fr))`, gap `14px 18px`. Each item is a
30px circle (same geometry as §10.7) + name `700 12px/1.2 IBM Plex Mono,monospace` +
desc `400 12px/1.45 Helvetica Neue,Helvetica,Arial,sans-serif;color:var(--muted)`.

Six items, in this order, each circle filled EXACTLY as listed — the three row controls
are deliberately distinct from each other at a glance (fill, not just glyph):

| # | glyph | name | circle background | glyph colour | border |
|---|---|---|---|---|---|
| 1 | `!` | EXPLAIN | `var(--panel)` | `var(--ink)` | `2px solid var(--accent)` |
| 2 | `✓` | PROCEED | `var(--ink)` | `var(--bg)` | `2px solid var(--ink)` |
| 3 | `+` | IMPROVE | `var(--accent)` | `var(--onAccent)` | `2px solid var(--ink)` |
| 4 | `↻` | REFRESH BUILD | `var(--panel)` | `var(--ink)` | `2px solid var(--ink)` |
| 5 | `◇` | CANON SYNC | `var(--panel)` | `var(--ink)` | `2px solid var(--ink)` |
| 6 | `↻` | REFRESH DATA | `var(--accent)` | `var(--onAccent)` | `2px solid var(--ink)` |

Glyphs are literal characters — `!`, `✓`, `+`, `↻`, `◇`. No icon font, no SVG, no emoji.

### 10.4 Sticky control bar
```css
position:sticky; top:0; z-index:20; background:var(--bg);
padding:10px 0; display:flex; flex-wrap:wrap; gap:8px; align-items:center;
border-bottom:1px solid var(--line);
```
Primary: `background:var(--ink);color:var(--bg);border:2px solid var(--ink);border-radius:3px;height:44px;padding:0 20px;font:700 12px/1 IBM Plex Mono,monospace;letter-spacing:0.08em`.
Ghost/toggle: same box, `background:transparent;color:var(--ink);font-weight:600`; when
active swap to ink fill (REFRESH DATA fills with `--accent`/`--onAccent`).
Right cluster: marked-count and data stamp, both
`400 10px/1.3 IBM Plex Mono,monospace;color:var(--muted)`, stacked, right-aligned.

### 10.5 Scheme switcher (in the bar, before the right cluster)
Label `SCHEME` at `500 10px/1 IBM Plex Mono,monospace;letter-spacing:0.1em;color:var(--muted)`.
Four buttons, one per scheme: `height:32px;padding:0 9px;border-radius:3px;border:1.5px solid var(--ink);font:600 10px/1 IBM Plex Mono,monospace;letter-spacing:0.06em`,
transparent → ink-filled when active. Each shows three 9px circles (headerBg, accent, bg)
overlapping by `margin-left:-3px`, then the label CANON / SLATE / DARK / MONO.
**A `<select>` is not an acceptable substitute.**

### 10.6 Status chip — the one visual that must never drift
```html
<div title="Golden files: PEND"
     style="display:flex;align-items:center;justify-content:center;gap:3px;height:24px;
            border-radius:3px;font:600 12px/1 IBM Plex Mono,monospace;letter-spacing:0.02em;
            background:var(--tint);color:var(--mark)">
  <span style="font-size:13px">~</span>PEND
</div>
```
Legend chips are identical with `padding:0 9px` and gap 4px. Build-state badges:
`height:24px;padding:0 8px;border-radius:2px;font:600 12px/1 IBM Plex Mono,monospace;
letter-spacing:0.02em` with the badge colours of §6.

### 10.7 Action buttons — 30px circles, always three
```html
<div class="noprint" style="display:flex;gap:6px;justify-content:flex-end">
  <button title="Explain" style="width:30px;height:30px;border-radius:50%;cursor:pointer;
    font:600 13px/1 IBM Plex Mono,monospace;border:2px solid var(--ink);
    background:transparent;color:var(--ink)">!</button>
  <button title="Proceed" style="…same as above…">✓</button>
  <button title="Improve" style="width:30px;height:30px;border-radius:50%;cursor:pointer;
    font:600 15px/1 IBM Plex Mono,monospace;border:2px solid var(--ink);
    background:transparent;color:var(--ink)">+</button>
</div>
```
In-row buttons are OUTLINE by default (transparent fill, ink glyph, 2px ink border) —
the coloured fills of §10.3 belong to the key panel only, where they teach the icon.

**Selected state — the tap must be visible without hover, on touch and in print.**

| control | unselected | selected / active |
|---|---|---|
| in-row `!` `✓` `+` | `background:transparent; color:var(--ink); border:2px solid var(--ink)` | `background:var(--ink); color:var(--bg)` (border unchanged) |
| REFRESH BUILD, CANON SYNC | `background:transparent; color:var(--ink)` | `background:var(--ink); color:var(--bg)` |
| ↻ REFRESH DATA | `background:transparent; color:var(--ink)` | `background:var(--accent); color:var(--onAccent)`; label `↻ REFRESHING…` while the fetch is in flight |
| scheme button | `background:transparent; color:var(--ink)` | `background:var(--ink); color:var(--bg)` |

Rules
- The change is a **full fill inversion**, not a tint, an outline thickening or an opacity
  shift — it has to read at arm's length on a phone and survive greyscale print.
- Only ONE of the three row controls can be selected at a time; choosing another moves the
  fill. Tapping the selected one again clears it and the row returns to all-outline.
- Selection state lives in `state.choices`, never in the DOM alone — a re-render (scheme
  switch, data refresh) must restore every fill, and the marked-count in the bar must
  agree with what is filled on screen.
- No hover-only affordance: `:hover` may change the cursor, nothing else. Touch devices
  never see hover.
- Do not add a check-mark overlay, ring, shadow or animation to indicate selection. Fill
  inversion is the whole vocabulary.

IMPROVE reveals a textarea directly
below the row: field bg, `1.5px solid var(--accent)`, radius 3px,
`400 12px/1.5 Helvetica Neue,Helvetica,Arial,sans-serif`, `min-height:52px`, `width:100%`.

**The detail field must span the whole row.** If it sits inside the row's grid it needs
`grid-column:1/-1` (plus `padding:2px 0`); if it sits outside the grid, `padding:0 14px 12px`.
Without the span it collapses into the first column and renders as a ~50px stub — the
exact defect seen in the first rebuild.

**Re-renders must repopulate it.** The typed value lives in `state.details`; any redraw
(scheme switch, mark toggle) recreates the textarea, so the sync pass has to write the
stored value back — otherwise the prompt carries text the user can no longer see.

### 10.8 Module grid
Scroll container: panel + line + radius 4px, `overflow-x:auto`, inner `min-width:848px`.
Header band and every row use the SAME grid:
`display:grid;grid-template-columns:104px 92px 351px minmax(140px,1fr) 104px;gap:8px`.
Header: `background:var(--headerBg);color:var(--headerFg);padding:9px 14px;
font:600 12px/1.2 IBM Plex Mono,monospace;letter-spacing:0.02em`; the checks cell is a
nested `repeat(6,1fr)` of centred labels.
Row: `padding:11px 14px;align-items:start;border-top:1px solid var(--line)`, zebra
`background:var(--zebra)` on odd rows. Name `600 12px/1.4 IBM Plex Mono,monospace` +
version line `400 12px/1.35 IBM Plex Mono,monospace;color:var(--muted)`. Checks cell:
nested `repeat(6,1fr)` with `gap:3px` of §10.6
chips. Evidence `400 12px/1.45 Helvetica Neue,Helvetica,Arial,sans-serif`,
`color:var(--body)`, `text-wrap:pretty`.
Legend sits ABOVE the container, `display:flex;flex-wrap:wrap;gap:8px;margin-bottom:10px`.

### 10.9 Section heading (every section below the grid)
```html
<div style="display:flex;align-items:baseline;gap:12px;margin:30px 0 10px">
  <div style="font:700 15px/1.2 Libre Baskerville,Georgia,serif">Risk Register</div>
  <div style="flex:1;height:1px;background:var(--line)"></div>
  <div style="font:400 10px/1 IBM Plex Mono,monospace;letter-spacing:0.1em;color:var(--accentText)">EXPOSURE · CAUSE · CONTROL</div>
</div>
```

### 10.10 Row grids for the remaining sections
| section | grid-template-columns | notes |
|---|---|---|
| Queues | `62px minmax(140px,220px) 1fr 116px` | ref · name+badge · note · actions |
| Open Issues | `52px 84px 1fr 116px` | ref · severity chip · note · actions |
| Risk Register | `52px 84px 1fr 116px` | third cell stacks title, cause, then `CONTROL` label (`600 12px/1.45 IBM Plex Mono,monospace`, accentText) + control text (`400 12px/1.45` sans, muted) |
| Budget | `52px 1fr 96px 96px 92px 116px` | ink header band; 5px spend bar (`radius 3px`, track = mark tint, fill = mark colour); total row `border-top:2px solid var(--ink)` |
| Milestones | `92px 22px 1fr 84px 116px` | date · rail · title+note · state chip · actions. Rail = 11px dot (filled when done, ring otherwise, `2px solid` mark colour) + 2px connector `var(--line)` that stops on the last row |
| Next Actions | `34px 1fr 104px 116px` | n · action · owner · actions |
| Feedback & Suggestions | `52px 1fr 108px 92px 96px 116px` | ref · text (raisedBy + targetRef stacked beneath, muted mono) · mark chip (clickable — see §4e) · owner · priority+timeline stacked · actions |
| Portfolio Roster | `52px 1fr 128px 76px 76px 1fr` | ref · name · status chip · people count · tasks count · thisWeek |
| People & Allocation | `1fr 96px 76px 1fr` | name (repeat rows for multi-project people) · projectRef · tasks · note |
| Update Log | `186px 1fr` | `border-left:2px solid var(--accent)`, `background:var(--zebra)`, gap 2px between entries |

All of these sit inside the standard panel container, rows separated by
`border-top:1px solid var(--line)`, padding `11–12px 14px`.

---

## 12. Delivery — artifact, Publish/Share, and Cowork live artifacts

Ship the dashboard as a real **artifact**, not a file handed over as a download — one
self-contained `.html`, inline CSS/JS, no build step (already this spec's whole shape).
That is what makes Publish/Share and an embed code possible at all.

**Two sharing paths exist and are not interchangeable — verify current mechanics live
before relying on this table, since plans and features change:**

| | Regular artifact (any Claude chat) | Cowork live artifact |
|---|---|---|
| Data source | this spec's `fetch(TRACKER_SOURCE)` to a plain URL | Cowork's own connected-app layer (Slack, Linear, Drive…), refreshed by Cowork when opened |
| Built where | any Claude.ai chat, Claude Code, or Cowork | inside a Cowork session on Claude Desktop only |
| Sharing | Publish (Free/Pro/Max, public link) or Share (Team/Enterprise, org-internal) | Share only, Team/Enterprise only — unavailable on Pro/Max |
| Runs in | any browser; no Claude account needed once published | Claude Desktop app only; viewer needs it installed |
| **Embeddable on a website?** | **Yes** — "Get embed code" + an allowed-domains list | **No** — the share link opens in Desktop, not a browser embed |
| Versioning | whatever this project's own tracker/log does | automatic, per Cowork session |
| Portability | one file, works from `file://`, a repo, a Drive preview | local to the creator's machine; doesn't follow to another device |

**If the actual goal is embedding on a website, the regular-artifact path is the one that
does that.** Cowork live artifacts do not produce a web-embeddable output, full stop — so
"build it as a Cowork artifact so it can be embedded" is not achievable as stated; the two
halves of that request point at different features. Default to the regular-artifact path
(this spec's existing model, Publish or Share, embed code) unless a request specifically
needs Cowork's connector-refresh behaviour and is explicit about giving up website
embedding and cross-device portability in exchange.

**A genuine Cowork live artifact** has to be built inside an actual Cowork session on
Claude Desktop, described in natural language with the connectors named up front ("a
tracker pulling from Drive and Linear"). It cannot be produced by authoring a static HTML
file outside Cowork and calling it one — the connector wiring and automatic versioning are
Cowork's own infrastructure, not something `fetch(TRACKER_SOURCE)` replicates, and hand-
authoring a file cannot retroactively grant it Cowork's refresh or sharing behaviour.

---

## 11. Conformance check before shipping a dashboard

Compare against the reference at 1080px wide. All must be true:

- [ ] the HTML contains NO status data — it fetches `TRACKER_SOURCE` and renders the response
- [ ] a failed fetch shows the snapshot banner and a `SNAPSHOT` stamp, never silent stale data
- [ ] header stamp shows fetch time plus `meta.generatedAt` and revision; >7 days adds `~ STALE`
- [ ] title, source label, check names and currency come from `meta`, not from the HTML
- [ ] ↻ REFRESH DATA re-fetches live and re-renders without a page reload
- [ ] every rendered size is one of 27 / 26 / 15 / 15 / 14 / 13 / 12 / 10 px and appears in
      the §7 table — audit with:
      `[...new Set([...document.querySelectorAll('*')].filter(e=>e.children.length===0&&e.textContent.trim()).map(e=>getComputedStyle(e).fontSize))]`
- [ ] no `rem`/`em` font sizes anywhere; every `font:` shorthand ends with a family
- [ ] all table text measures 12px; chrome labels 10px; titles 27/15/26px serif; no 11px,
      no 11.5px, no 13px text (13/14/15px exist only as control and chip glyphs)
- [ ] status marks show glyph + word + tint, 24px tall, radius 3px — no bare glyphs
- [ ] action buttons are 30px circles with 2px borders, three per actionable row, outline
      until selected, then ink-filled
- [ ] tapping a row control inverts it to a solid ink fill; tapping it again clears it;
      selecting another moves the fill (only one selected per row) — verified on touch,
      with no hover involved
- [ ] selection survives a re-render and the marked-count matches what is filled on screen
- [ ] key panel shows all six controls with the exact circle fills of §10.3 (EXPLAIN pale
      with accent ring, PROCEED ink-filled, IMPROVE accent-filled)
- [ ] scheme switcher is four swatch buttons, not a `<select>`
- [ ] containers radius 4px, chips/buttons 3px, badges 2px; no 8px radii
- [ ] no borders on individual cells; rows separated by one 1px line
- [ ] module grid columns `104/92/351/1fr/104`, min-width 848px, no sideways scroll at 900px
- [ ] Canon v6 is the default scheme — used when no scheme is set, on first load, and
      after RESET; the CANON switcher button renders active on open
- [ ] IMPROVE field spans the full row width and survives a re-render with its text intact
- [ ] print preview: controls hidden, every mark still readable in greyscale
- [ ] Create prompt copies the exact format in §5
- [ ] the Feedback mark is the ONLY clickable status chip in the dashboard; every other
      chip is read-only and evidence-derived — verify no other section lets a click change
      a mark directly
- [ ] Feedback rows render with `raisedBy` and `targetRef` blank without layout breakage;
      an empty `feedback` array omits the section per the normal absent-array rule (§3.4)
- [ ] a person appearing on multiple People & Allocation rows shows a per-person total
      that is SUMMED AT RENDER, never a stored total — verify by editing one row's `tasks`
      and confirming the displayed total changes without touching a second field
- [ ] Portfolio Roster's `people`/`tasks` counts come from the People roster when one
      exists for that tracker instance, and from the row's own fields when it doesn't —
      never both at once for the same project
