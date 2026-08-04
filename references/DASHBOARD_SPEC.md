# Status Dashboard Shell — reusable dashboard spec v3.12

Project-agnostic. This is the visual and data contract for every dashboard built with the
`status-dashboard` skill. Sections 6–10 are literal and apply verbatim to any project.
Where the text says "canon", read "the project's source-of-truth folder"; where it names a
`proj-*` skill, read "the skill that owns that delivery line". Section 8 is an EXAMPLE
roster from the project this shell was designed on — replace it with the host project's own lines, keeping the pattern (one JSON source per line, six check columns, six sizes).

Reference implementation: `online-dev-tracker-dashboard_v8.html` (live-fetch build) and
`Tracker Dashboard.dc.html` (design source).
**This spec is a visual contract, not a style suggestion.** A dashboard built from it must
be pixel-comparable to the reference: same type sizes, same chip shape, same round action
buttons, same spacing. Sections 9 and 10 give the literal CSS and markup — copy them, do
not re-derive them. If a value is not listed here, take it from the reference file.
§11 is the conformance checklist to run before shipping; §12 covers delivery.

**v3.0 changes the data model.** The dashboard is a VIEW over a canon JSON source that it
fetches at run time (§3). Status data is never baked into the HTML — an embedded snapshot
exists only as a clearly-labelled offline fallback. Read §3 before §9–10.

### Version history — what each point release changed

The body of this file used to cite version numbers the title had never caught up with.
The record, stated once so no section has to guess:

| version | change |
|---|---|
| v3.0 | the data-model split — dashboard becomes a VIEW over a fetched JSON source (§3) |
| v3.1 | §4e Feedback & Suggestions added — the first one-time section insertion |
| v3.2 | §4f Portfolio Roster + §4g People & Allocation — the second insertion, 14 sections → 16 |
| v3.3 | §3.6 evidence baseline and §4h Defect & Task Register — the third insertion, 16 → 17 |
| v3.4 | §3.7 the ISSUE·PROBLEM·NEEDED row triple and the header Function/Purpose/Objective block, both now standard; §13 reversed — Facilitator and Resources carry the action trio, CREATE PROMPT and the scheme switcher after all, plus a click-to-scope index and dropdown/search filtering unique to a pooled surface |
| v3.5 | Navy added as a fifth colour scheme and promoted to the default (RESET/first-load) in place of Canon v6, which remains available as a named scheme; four schemes → five everywhere §6/§10.5/§11 reference a count |
| v3.6 | Owner batch (2026-07-29): the ISSUE·PROBLEM·NEEDED triple's third line renders as **ASK**, `needed` stays the JSON field name; a `[PARTIAL]` resolution chip crosses with severity (§2); a grey `[UNDEF]` mark covers any row missing its severity/status/rating (§2); the CREATE PROMPT legend/disclaimer block is banned from emitted prompt text (§5); Module Grid gets a filter-by-state control (§10.8); empty sections gain a `meta.retiredSections` opt-out (§3.4); Next Actions gain an optional `priority` chip and a `hold`/`done` pair that prunes completed rows (§4 Next Actions); Feedback & Suggestions gains a guided "track something new" add-row flow (§4e); file citations require the full Drive URL, never a bare id (§3.5); Module Grid columns with no data for this instance carry a `meta.checksNote` explaining what would populate them (§3.3); severity/rating/priority chips may render glyph-only under an explicit `meta.compactChips` opt-in, off by default — the core five status marks keep glyph+word+tint always, no exception (§2) |

| v3.7 | Owner batch (2026-08-03): **the queue is a second channel back to Claude** — where a project runs the Mode D replica (§3.2D), a dashboard may POST a request to the Worker's `/api/queue`, and §5's "the pasted prompt is the only channel" is relaxed to "the only channel that reaches canon". The queue holds *requests*, never canon rows; the §5 write path is still the only thing that edits a tracker, so "the dashboard never mutates canon" is unchanged. A queue-backed dashboard must still offer the paste, because the queue depends on a Worker that a `file://` copy cannot reach. §4e's "track something new" form is promoted from a Feedback-only flow to **the last row of every pane** — same three required fields (what to track · source · measured by), scoped to the pane's tracker or project, and subject to the same §11 rule that its text survives a re-render; §10.7's "always three" gains its one exception — a form row carries a single `+` submit, same geometry, no selected state, because there is no existing row for `!`/`✓` to act on |

| v3.8 | Owner batch (2026-08-03): **the display serif is retired**. Libre Baskerville is replaced by **IBM Plex Mono** for the dashboard title, metric figures and section titles (§7) — two families instead of three, and one fewer webfont request. The font URL must ask for `700`, which it previously did not, or bold titles are synthesised rather than drawn; display sizes take `letter-spacing:-.01em` because mono is wide. **The size scale is unchanged** — 27/26/15 stay as they are, so §11's type audit is untouched |

| v3.9 | Owner batch (2026-08-03): **the nav becomes stacked dividers.** The three-row indented tab tree is replaced by nested surfaces — each level's active tab opens the surface holding the next level's strip, so containment is drawn rather than indented. The folder-tab shape (`border-bottom:none`, top-only radius) was previously applied to rows that sat above other nav rows, where nothing closed them; it is now used only where a surface closes it. Four tokens per scheme are added to §6 (`nav1`, `nav1Line`, `nav2`, `nav2Line`, twenty literal values). Level 3 stops being a tab and becomes an underline strip — lines within one tracker are siblings, not containers. Tab radius goes 4px → 5px (tab corners sit outside their surface). The twist controls and `state.navOpen` are removed: selection reveals the level below, so folding is redundant. Level 1 carries a synthetic `PROJECTS` container tab, which returns to the last project viewed rather than always the first. Geometry, type, tokens and markup are exactly the `Handover - 1c nav tab structure` reference — all nineteen selectors, every declaration. **One addition it does not cover:** levels 2 and 3 now render inside `#panes`, which is not `.noprint`, so the strips and their surfaces are explicitly hidden in `@media print` — without that, printing gained nav chrome it never had. **Known limit:** the strips wrap per §4, and below ~480px a wrapped row's tabs have no surface beneath them, which is the §7 containment rule breaking at phone width; not addressed here. **The type scale is unchanged** — §11's type audit is untouched |

| v3.10 | Owner batch (2026-08-04): **Canon v6 returns as the default scheme**, reversing v3.5's promotion of Navy. Navy remains a named scheme and keeps its leading position in the §10.5 switcher — the switcher order is now explicitly fixed rather than derived from which scheme is default. The `:root` block must mirror the default scheme's literal token set, not merely resemble it: it is the pre-script paint, so a `:root` holding a different scheme's values makes every first load flash. §11's checklist item is inverted accordingly |

| v3.11 | Owner batch (2026-08-04), thirteen changes. **Navy is the default scheme again**, reversing v3.10 one day on; `:root` is regenerated from the `Navy` SCHEMES entry, so the rule that `:root` mirrors the default survives the reversal. **A new `--rule` token per scheme** (five literal values) separates table rows: `--line` is a divider *on* a panel and reads too faint as a row rule. §9 is unchanged — still one 1px line, still no border on individual cells, only the colour moves. **Every section is a `<details>`** (§10.9): populated open, empty and the update log closed, and the count rides on the summary so a shut section still reports — `RISKS 3`, `BUDGET EMPTY`. Section order within a tracker is now populated → module grid → People → **empty** → **update log last**; empty sections above populated ones pushed real work down the page, and history above anything actionable did the same. **An empty section carries a `+`** so the reader can ask for what is missing instead of reading '— none —' with no way to act. **Per-tracker statistics (§10.2b)**: four equal centred blocks — Status, Trackers, Rows, Fail-or-blocked — belonging to the *tracker*, where the strip above previously reported project-wide figures over one line's sections. **IMPROVE is a real dialog (§5b)**, multi-line, reviewable before it is queued; `window.prompt()` gave one line and no way to see what you had typed. Plain text on purpose — the tray payload is plain text all the way to Claude. **`.act` is geometry, not a role**: `wireActions` now binds `.act[data-action]`. Three different controls wear the §10.7 circle, and the bare selector bound the row-action handler to all of them, so the 'anything else to track' + fired twice and queued an item with no ref and no action. **That form now marks into the tray** rather than POSTing straight to `/api/queue` — SEND TO DISPATCHER is again the only thing that transmits. **People (§10.10) is derived from row owners**, not authored: no tracker has ever carried a `person` row, but the rows carry owners, so the section lists each person and their row count, splits compound owners (`Alex + Claude`, `Claude/Code`) into real people, and appears on the overview too. A name is a **filter** — selecting one narrows every tracker and pooled cut to their rows behind a loud banner, because a filtered view that looks unfiltered is how a reader concludes work has vanished. Authored `person` rows still win where they exist. **A Mark column carries a legend** built from the marks actually present (§10.6b): a legend listing marks that are not on the page is worse than none |

| v3.12 | Owner batch (2026-08-04): **the programme hub becomes a specified surface, and an assisted maintenance pass is admitted to canon.** New §14 covers the hub: a fixed tab order (`OVERVIEW · DECISIONS · RISK · PEOPLE · PROJECTS · ORPHANED · DONE`) that does not follow which tab is default — BUDGET was specified and then dropped the same day, with `budget_line` leaving `ALWAYS_SECTIONS` too, because one tracker of nine carries any budget data and a cut that is empty almost everywhere teaches the reader to stop opening it, the same way §10.5 fixes the scheme-switcher order; one pooled table across all trackers carrying `Project | Tracker | Ref | Mark | Details | Owner | actions` in place of the old per-tracker grouping; DECISIONS pooling `decision` + `decision_required`; ORPHANED with its three scan sources; DONE gathering locked, retired and archived; the ADMIN surface; and the refresh scan. **DONE reverses commit `2011e55`** — locked and retired lines were deliberately put on the Overview so they stayed reported; they now report on DONE and appear nowhere on the Overview, and `archivedHTML()` moves with them. **The evidence rules in §2 and §3.5 are relaxed for a maintenance pass**, and this is the change most likely to be regretted, so it is stated here rather than left in a subsection: a pass may now advance a mark from evidence it read in that pass, including to `pass`, which §2 previously forbade on code review alone. The pass runs from a CLI session with the owner present, which is what makes it tolerable. The residual risk is still real — a pass can advance a mark on evidence a human would have judged insufficient, and the `log` entry is the only record of why — so every such mark change must name the evidence it used and which pass wrote it. **§5 gains a third channel**: the queue is now *drained*, by a **Claude Code CLI session** — the owner's decision of 2026-08-04, which replaced an earlier plan for an unattended hourly consumer. The v3.11 sentence "nothing consumes the queue on its own; there is no daemon watching the table" therefore stays true of unattended processes and is kept rather than deleted. What changed is that the consumer may write canon, and that a human is present for every write — the material safety property, and the reason the evidence relaxations above are tolerable at all. The dashboard button reads **SEND TO CLI** |

Things that went wrong the last time this was rebuilt, all now specified below:
`rem`-based font sizes, glyph-only 14px status squares, square 4px action buttons,
bordered table cells, 8px radii, and `font:` shorthands with no family.

---

## 1. What is fixed vs what each skill supplies

FIXED (never re-invent per skill)
- every value in sections 9–11: type scale, colours, spacing, radii, control geometry
- section order, grid columns, prompt protocol
- status vocabulary and the glyph+word+tint marks
- the five colour schemes and the in-page scheme switcher
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
| `undef` | ? | UNDEF | the field this row needs (severity/status/rating) is missing from canon |

Rules
- **Glyph AND word AND tint always travel together.** A bare glyph, a bare colour square,
  or a colour-only cell is a spec violation — the word is what survives greyscale.
- `pending` is the default. Never mark `pass` on code review alone.
- Build-state badges are a separate axis: `INTEGRATED / TESTED / BUILDING / PROTOTYPE`
  (`PROPOSED / PENDING` in queues). No new badge words without a canon decision.
- Severity and exposure reuse the marks: High → ✕, Med → ~, Low → –.
- **A row with no severity/status/rating value renders `? UNDEF`, grey, never a raw
  `undefined` string and never a silently blank cell.** This is a template guard, not a
  canon shortcut — a row that hits `UNDEF` still needs its real value chased down in the
  source tracker; the chip exists so a rendering gap can never masquerade as a real status.
- **`[PARTIAL]` is a resolution state, not a fourth severity word — it crosses with
  severity/rating rather than replacing High/Med/Low.** An optional `resolution` field
  (`"partial"`, the only value defined so far) on an Open Issues or Defect row renders a
  second small chip, `~ PARTIAL`, immediately before the severity/rating chip:
  `[~ PARTIAL][✕ HIGH]`, `[~ PARTIAL][~ MED]`, `[~ PARTIAL][– LOW]`. Omit the field
  entirely for a row that is simply open or simply resolved — `PARTIAL` only appears when
  a row is genuinely both severity-rated and partially, not fully, closed.
- Rows open by definition (decisions) carry NO status badge.
- A mark is normally evidence-derived and **read-only in the browser**. That half of the rule
  is unchanged by v3.12: no chip is clickable except §4e's feedback mark, which is
  facilitator-set rather than evidence-derived and says so in its own prose rather than
  quietly breaking the read-only rule everywhere else.
- **A maintenance pass under §14.6 may advance a mark**, including to `pass`,
  from evidence it read in that pass. This is a v3.12 relaxation of the older rule that a
  mark is never advanced on code review alone, and it is a deliberate trade the owner made
  with the conflict named. The pass runs from a **Claude Code CLI session** with the owner
  present — not an unattended job — which is what makes the relaxation tolerable.
  **State the residual risk rather than discovering it later:** a pass can still advance a
  mark on evidence a human would have judged insufficient, and nothing on the page
  distinguishes such a mark from a considered one afterwards. The `log` entry is the only
  record. So: every mark a maintenance pass changes **must** write a `log` entry naming the
  evidence it used. A mark change with no such entry is a defect, not a status.
- **Severity/rating/priority chips may drop the word under an explicit opt-in, the core
  five status marks never do.** Set `meta.compactChips:true` on a tracker instance and its
  severity, rating and priority chips render glyph-only (`✕` not `✕ HIGH`) — legal ONLY
  because the section carries its own legend (§10.6) spelling out the glyph-to-word mapping
  once, in that section's header. Default is `false`/absent, meaning glyph+word as
  everywhere else; the six-check Module Grid marks, the build-state badges and every other
  status chip in this spec are excluded from `compactChips` and always carry the word —
  this flag touches severity/rating/priority chips only, never the marks the greyscale/
  colour-blind rule in the first bullet exists to protect.

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

**D — Hosted replica (optional, added 2026-08-02).** Where the project mirrors its trackers
into a database behind a Worker, `TRACKER_SOURCE` may point at
`<worker>/api/tracker/<tracker-id>`, which returns the payload of §3.3 verbatim. Nothing else
in the dashboard changes — same parse, same render, same `EMBEDDED` fallback. This exists
because a local path cannot be read from a phone and `file://` blocks `fetch()` outright, so
a double-clicked dashboard degrades to its snapshot with no network involved at all.

**The replica is never the source of truth.** The tracker JSON of §3.1 still is. The replica
re-syncs from the file; the file is never regenerated from the replica, and no write-back
path exists — §5's CREATE PROMPT protocol remains the only channel back. If the two
disagree, the file wins.

Mode D does not retire A or C. The fetch can still fail and the banner rules apply unchanged,
and because a replica read is not a canon read, **the stamp must distinguish them** — show
the replica's own `synced_at` alongside `meta.generatedAt`, since they answer different
questions: when the replica last caught up, versus when Claude last wrote the file. A replica
that is fresh about a file that is stale is the §3.6 trap one layer further out.

Full schema, the `<project>.<line>` id convention, the shape-C record for lines carrying only
narrative canon, sync options and the mixed-row-form extraction trap: `d1-replica.md`.

### 3.3 Source payload shape

```jsonc
{
  "meta": {
    "line": "online-dev",
    "title": "Digital Dev Tracker",
    "eyebrow": "Example Project · ONLINE DEV",   // small caps strap above the title
    "sourceLabel": "ONLINE_DEV_TRACKER.json",
    "checkNames": ["Typecheck","Unit","Golden files","Multi-client","Code security","Privacy"],
    "checkAbbr":  ["TYP","UNI","GLD","MUL","SEC","PII"], // exactly 6, or the shell abbreviates
    "currency": "AUD",
    "revision": 47,                    // increments on every write by Claude
    "generatedAt": "2026-07-25T10:12:00+10:00",
    "maintainer": "Claude",            // who writes this file
    "evidenceBaseline": "v0.6",        // the version the marks below were derived FROM
    "subjectVersion": "v0.20",         // the version actually shipping NOW
    "baselinedAt": "2026-07-25",       // when evidenceBaseline was last re-derived
    "retiredSections": [],             // section keys opted out of "-- none --" forever (§3.4)
    "checksNote": "",                  // why the Module Grid has no six-check data here, and what would populate it (§10.8)
    "compactChips": false              // glyph-only severity/rating/priority chips, opt-in only (§2)
  },
  "modules":     [[name, builtAgainst, badge, [6 status keys], evidenceNote], …],
  "proofs":      [[ref, name, badge, note], …],
  "gates":       [[ref, name, badge, note], …],
  "decisions":   [[ref, title, "OPEN", note], …],
  "issues":      [[ref, "High"|"Med"|"Low", note], …],
  "defects":     [[ref, externalRef, title, "High"|"Med"|"Low", mark, targetRef, foundIn, fixedIn, note], …],
  "risks":       [[ref, "High"|"Med"|"Low", title, cause, control], …],
  "budget":      [[ref, lineItem, budgetAmount, spentAmount, note], …],
  "milestones":  [[ref, "YYYY-MM-DD", title, "done"|"next"|"pending"|"blocked", note], …],
  "nextActions": [[n, action, owner, priority?, hold?, done?], …],  // priority/hold/done optional, §4i
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

`checkAbbr` is optional: supply exactly six abbreviations or the shell derives them from
`checkNames`. `eyebrow` and `maintainer` are optional display fields. The three baseline
fields are not optional once a tracker describes a build that ships independently of it —
see §3.6.

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
- **`generatedAt` measures when the file was last written, not whether what it says is
  still true.** A tracker rewritten this morning about a build from three versions ago is
  fresh by this rule and wrong in fact. That second axis is §3.6, and it is the one that
  actually catches a stale dashboard.

### 3.5 Content discipline (unchanged, and enforced in the JSON, not the HTML)

- `evidenceNote` states the evidence or names the gap with ids (`(I6)`, `(S8)`). No note = no claim.
- Totals, percentages and metric counts are DERIVED at render, never stored.
- Statuses change only when evidence changes, **or when a §14.6 maintenance pass re-derives
  them**, and every change adds a `log` entry. The re-derived case additionally records which
  pass wrote it, so a reader can tell a bulk re-derivation from a considered judgement at a
  glance instead of having to reconstruct it.
- **A file citation is the full Drive URL, never a bare file id.** Any row or log entry
  that names a specific file for the reader to act on (open, review, delete) writes
  `https://drive.google.com/file/d/<FILE_ID>/view` in full — a bare id like `1WvrbBno85…`
  is not clickable and forces the reader to hand-build the link themselves. This applies to
  every register (Issues, Defects, Decisions, log), not just one section.

### 3.6 Evidence baseline — the version the marks describe

A tracker describes a subject: an app build, a print deck, a manual set. **The subject
moves on its own schedule and the tracker does not automatically follow it.** Every mark
in the file was derived from one particular version of that subject, and if the subject
has since shipped past it, every mark is a claim about something that no longer exists.

Freshness (§3.4) cannot see this. Rewriting the file re-stamps `generatedAt` whether or not
a single mark was re-derived, so a tracker can be simultaneously written-today and
describing-a-build-from-a-month-ago. That combination is the most dangerous state a
dashboard can be in, because every visible staleness signal reads green.

Three fields, all in `meta`:

| field | means |
|---|---|
| `evidenceBaseline` | the subject version the marks below were actually derived from |
| `subjectVersion` | the version now shipping, per canon — regardless of whether it was inspectable |
| `baselinedAt` | the date `evidenceBaseline` was last re-derived from real evidence |

**The degrade rule.** When `evidenceBaseline` ≠ `subjectVersion`, the dashboard MUST:

1. Render a full-width banner above the metric strip, in the same treatment as §3.2C's
   snapshot banner but on the `pending` tint:
   `~ PROVISIONAL — marks derived from <evidenceBaseline>; <subjectVersion> is shipping. Re-derive before trusting status.`
2. Append `~ PROVISIONAL` beside the header stamp, alongside any `~ STALE` chip — the two
   are independent conditions and both can be true at once.
3. Render every `pass` mark in the Module Grid with the `pending` tint and a `*` suffix on
   the word (`✓ PASS*`), the footnote reading *"derived from `<evidenceBaseline>`, not
   re-verified against `<subjectVersion>`"*. The glyph and word do not change — a reader
   comparing two dashboards must still see the same vocabulary — but nothing evidenced
   against a superseded version may present as unqualified truth.
4. Leave `pending`, `blocked`, `fail` and `na` marks untouched. Degrading is only ever
   applied to claims of success; a pending mark is already making no claim.

**What it does not do.** The rule never advances or clears a mark, and never guesses what
the newer version does. It marks the whole set as provisional and says why. Re-deriving is
a §3.2B MCP re-issue against real evidence — the only path that can change a status.

**Recording the gap properly.** A baseline mismatch is a real condition and belongs in the
issue register too, with the id cited from the affected rows' `evidenceNote` (the
`(I6)`/`(S8)` convention of §3.5). The banner tells a reader looking at the page; the issue
tells anyone reading the source. Both, not either.

**When the subject is the tracker itself** — a design or programme tracker whose rows are
other trackers — set both fields to the same value and the rule is inert. Do not omit them
to achieve the same effect: an absent baseline is indistinguishable from one nobody
thought about.

### 3.7 Row content — the ISSUE · PROBLEM · NEEDED triple, and the header purpose block

Every section in §4 that documents a `note` field may render it as a flat string, as
written throughout this file — that stays valid and is the right choice for a short,
self-contained line (a budget variance, a milestone date). It is the wrong choice for
anything a reader has to act on, because a single sentence conflates three different
questions a facilitator actually needs answered separately: what is this, why does it
matter, and what has to happen next.

Where a row is something someone will decide or action on — Decisions, Open Issues, Next
Actions, and any Facilitator/Resources row pooled from them — author it as a **triple**
instead of a flat `note`:

| field | answers |
|---|---|
| `issue` | what is this, stated as a fact, not a question |
| `problem` | why it matters — the consequence of leaving it as-is |
| `needed` | what has to happen, and who from, to close it — **rendered as ASK**, not NEEDED (v3.6); the JSON field name stays `needed` so existing tracker data does not need a migration, only the on-page label changed |

This is an authoring step, not a string-splitting trick — no heuristic reliably turns one
paragraph into three parts that actually answer three different questions. A row missing
any of the three does not get a partial triple; write it as a flat `note` instead, or flag
it back to the source tracker as incomplete.

**Rendering.** Each line is prefixed with its label in the accent colour
(`<b>ISSUE </b>`, `<b>PROBLEM </b>`, `<b>ASK </b>` — 10px, letter-spacing .06em, matching
`.ref`), body text at the standard 12px note size below it. All three lines clamp to one line each by default
(`-webkit-line-clamp:1`) with a `… expand` / `– collapse` toggle per row, so a dense
section stays scannable and a reader who needs the full text gets it without leaving the
page. `EXPAND ALL` in the control bar (§10.4) toggles every row's clamp at once.

**Empty sections still get an IMPROVE control.** A section with zero rows renders
`— none —` plus a lone `(+)` button reusing the same action-trio wiring as every other
row (EXPLAIN and PROCEED present but hidden, since neither means anything on an empty
section) — so a facilitator can still open a field and say what should go there, instead
of an empty section being a dead end.

**A persistently empty section can be retired instead of shown `— none —` forever.**
Next to that lone `(+)`, an empty section's row also carries a `RETIRE` ghost control.
Pressing it stages `RETIRE <section>` on the next CREATE PROMPT rather than mutating
anything client-side (the dashboard still never writes canon directly, per §5). On the
next canon write, Claude adds the section's key to `meta.retiredSections` (an array of
section keys, e.g. `["risks","budget"]`) — a tracker instance checks this array beside the
existing absent/empty distinction (§3.4) as a third state: **absent** (never had the
section) is omitted silently; **empty** (`[]`) shows `— none —`; **retired** (empty AND
listed in `meta.retiredSections`) is omitted exactly like absent, but is a deliberate,
logged decision rather than the section never having existed. Un-retiring is the same
path in reverse — remove the key from `meta.retiredSections` on a future sync — never a
client-side toggle, so retiring a section is always a canon-visible, auditable act.

**The header purpose block.** Immediately below the title/eyebrow and above the
how-this-works panel (§10.3), an optional three-column block states what this specific
dashboard is for, driven by three `meta` fields:

| field | answers |
|---|---|
| `trackerFunction` | what this dashboard tracks, one to two sentences |
| `trackerPurpose` | why that matters — what question it lets the reader answer |
| `trackerOutcome` | the objective — what "done" or "working" looks like for this line |

Each column hides independently when its field is empty, and the whole block hides when
all three are empty — an older `EMBEDDED` seed or a tracker JSON that predates this field
renders exactly as it did before. This is a per-dashboard description, authored once when
the dashboard is built and revised only when what it tracks genuinely changes — not
regenerated content, and not a substitute for the tracker's own `sourceLabel`/`eyebrow`.

---

## 4. Sections, in order

1. Header · 2. Metric strip · 3. How-this-works panel · 4. Sticky control bar ·
5. Prompt output · 6. Portfolio Roster · 7. People & Allocation · 8. Module grid
(legend above) · 9. Queues (Proofs, Gates, Decisions) · 10. Open Issues · 11. Defect &
Task Register · 12. Risk Register · 13. Budget & Cost · 14. Timeline & Milestones ·
15. Next Actions · 16. Feedback & Suggestions · 17. Update Log

Drop sections with no data; never reorder what remains.

Insertion record, so the order is auditable rather than folklore: §4e Feedback was the
first one-time insertion (v3.1); §4f Portfolio Roster and §4g People & Allocation the
second (v3.2), placed before Module Grid because a portfolio is overview-level and
overview precedes per-line detail; §4h Defect & Task Register the third (v3.3), placed
directly after Open Issues because a defect is an issue with a reproduction and a ticket
number, and the two are read together. Once shipped, an insertion becomes part of the
fixed order like everything else — "never reorder" governs from here forward, not
retroactively.

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

**Track something new (v3.6).** Below the last row, a `+ NEW` control opens a small guided
form rather than a single freeform box — the point being that "track something new" is an
under-specified ask until the reader says what, where the number/status will come from, and
what "done" or "measured" means for it. Three fields, all required before the row can be
added: **what to track** (free text — becomes the row's `text`), **source** (free text —
where this data comes from, e.g. "sprint retro", "Alex in chat", "commit log"), **measured
by** — a fixed choice, not free text, one of `milestone` / `budget` / `risk` /
`brainstorming` / `code review` / `design review`. The completed form does not write a row
to canon directly (§5's rule holds here too) — it stages a `NEW FEEDBACK` line in the next
CREATE PROMPT, and Claude appends the real row (with a fresh `ref`) to `feedback` on the
next write. `note` on the resulting row records the measurement type so a reader scanning
the tracker later can see why the row exists without re-asking.

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

### 4h. Defect & Task Register — where numbered tickets live

**Issue = a condition. Defect = a numbered, reproducible ticket against a specific
version.** I8 "the shipping build was never synced" is an issue. "#183 table notes
disappear when a Crisis is triggered, seen in v0.20" is a defect. Filing the second as
the first loses the reproduction and the version; filing the first as the second invents
a ticket number for something nobody can close.

Before this section existed, a walkthrough that produced thirteen numbered tickets had
nowhere in the tracker to put them, so they lived in whatever tool the session happened to
use and stayed invisible to the dashboard. That is the gap this closes.

**Fields**: `ref` (T1, T2… — tracker-native, unique programme-wide) · `externalRef` (the
id in the system that actually holds the ticket — `#183`, `PROJ-412`, or blank if this
tracker is the only home) · `title` (one line, what's wrong) · `severity`
(`High`/`Med`/`Low`, the §2 vocabulary, no fourth word) · `mark` · `targetRef` (the module
name or M/I/D ref it hits, blank if unattributed) · `foundIn` (the subject version it was
observed in — the same version vocabulary as §3.6) · `fixedIn` (the version it was fixed
in, blank while open) · `note` (reproduction, or what's blocking).

**Mark** aliases the fixed marks the same way severity and §4f status do:
`~ OPEN` (pending, the default) · `✓ FIXED` (pass) · `■ BLOCKED` (blocked) ·
`✕ WONTFIX` (fail) · `– N/A` (na, e.g. not reproducible). Evidence-derived and read-only
like everything except §4e's chip — `✓ FIXED` means a verified fix in a stated version,
not a claim that someone believes it was addressed.

**`foundIn` is what makes this section honest**, and it interlocks with §3.6: a defect
found in a version *later* than `meta.evidenceBaseline` is evidence the baseline has moved
and the module marks are provisional. A register full of `foundIn: v0.20` rows on a
tracker baselined at `v0.6` is the mismatch banner arguing for itself. A `✓ FIXED` row
whose `fixedIn` is newer than `evidenceBaseline` is degraded by §3.6 like any other pass.

**Ref prefixes — one registry, programme-wide.** Refs are unique across every tracker in
the programme, not just within a section, so a prompt line reading `I8 ✓` is unambiguous
about which register it came from:

| prefix | register |
|---|---|
| `M` | Milestones (§4d) |
| `B` | Budget lines (§4c) |
| `R` | Risks (§4b) |
| `I` | Issues (§4, Open Issues) |
| `D` | Decisions (queues) |
| `AP` | Asset proofs (queues) |
| `PG` | Platform / Compliance Lines (queues) |
| `S` | Suggested activities (queues) |
| `Q` | Open questions |
| `E` | Epics and registered enhancements |
| `T` | Defects and tasks (§4h) |
| `F` | Feedback rows (§4e) |
| `P` | Portfolio projects (§4f) |

Two collisions are real, observed in a running programme, and named here rather than
quietly resolved:

- **`P` is also used for build phases** (`P3`, `P7`) by projects that adopted phase
  numbering before a portfolio view existed. A tracker that needs both must prefix
  portfolio projects `PR1`, `PR2` and say so in `meta`. Do not silently renumber the
  phases — they are cited in changelogs and decision entries that cannot be edited.
- **`E` covers both registered digital enhancements and backlog epics** in at least one
  real programme. They are different things sharing a letter. Keep the ranges apart
  (`E1`–`E9` enhancements, `E10`+ epics) or split to `EP` for epics, and record which
  convention the programme picked.

Neither is worth a migration on its own. Both are worth writing down, because the failure
mode is a prompt line that two registers both think is theirs.

### 4i. Next Actions — priority and pruning (v3.6)

**Fields**: `n` (row number, not a programme-wide ref — Next Actions is a per-tracker
scratch list, not a permanent register) · `action` (or the ISSUE·PROBLEM·ASK triple, §3.7,
for anything with real context to carry) · `owner` · `priority` (optional — `High`/`Med`/
`Low`, the same three words as §4e's, no fourth priority word) · `hold` (optional boolean)
· `done` (optional boolean).

**Priority chip.** When `priority` is set, render it exactly like a severity chip
(`✕ HIGH`/`~ MED`/`– LOW`, §2, subject to the same `compactChips` opt-in). Omitted
`priority` renders no chip at all — not every action needs one ranked.

**`hold` is a status, not a fourth priority word.** A row can be `priority:"High", hold:true`
— still the most important thing on the list, just deliberately not being worked right now.
Render `hold:true` as a separate `■ HOLD` badge (the `blocked` mark) beside the priority
chip rather than inventing a `priority:"Hold"` value, which would be exactly the
"no fourth priority vocabulary" violation §4e already rules out. A held row still counts
in the section's total; it is paused, not gone.

**`done` rows are pruned, not displayed struck-through.** The moment a Next Action is
marked done, it drops out of the rendered list entirely on the next regeneration — Next
Actions is a to-do list, not an audit trail, and a growing tail of completed rows defeats
the point of a scratch list a facilitator scans in seconds. The completion itself still
gets a `log` entry (§3.5's "every change adds a log entry" rule is not waived here); the
row's disappearance from Next Actions is how "handled" is communicated on this page, the
log is where it is proven.

---

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

**The emitted prompt is exactly the block above — nothing else gets prepended.** In
particular: no restated EXPLAIN/PROCEED/IMPROVE legend and no "refs only, re-read the full
text from canon" disclaimer. Both were tried on the Facilitator Hub build and cut in v3.6
— the how-this-works panel (§10.3) already teaches the trio once, on the page, and
repeating it inside the copied prompt just spends the paste target's space restating
something the reader already saw seconds earlier. The prompt is refs, choices and typed
directions — nothing framing them.

The revision number matters: it tells Claude which version of the source the user was
looking at, so a write can be refused or re-based if the source moved on.

The dashboard never mutates canon — the pasted prompt is the only channel that reaches canon,
and the how-this-works panel says so on every dashboard.

**Second channel, v3.7 — the queue (Mode D only).** Where the project runs a hosted replica
(§3.2D), the dashboard may POST to the Worker's `/api/queue`: the tray's SEND TO CLI,
and the §4e track-something-new form on every pane. This does not weaken the rule above. A
queue row is a **request**, sitting in its own table with a `status` of `ready` → `in_review`
→ `needs_review`; canon changes only when someone works that request through the §5 write
path. Two constraints follow, both load-bearing:

- **The paste never goes away.** The queue needs a Worker, and a `file://` copy cannot reach
  one. COPY TRAY TEXT is the fallback whenever the POST fails, and the failure message must
  say so rather than leaving the user stranded.
- **The queue is drained by a CLI session, not by a daemon (v3.12).** The owner's decision of
  2026-08-04 sends everything the dashboard queues to a **Claude Code CLI session** rather than
  to an unattended scheduled job. So the v3.11 sentence — "nothing consumes the queue on its
  own; there is no daemon watching the table" — remains **true of unattended processes**, and
  is restated here rather than deleted, because an earlier draft of v3.12 removed it and that
  draft was wrong.
- **What did change is that the consumer may now write canon.** A CLI session draining the
  queue edits **the tracker JSON on Drive** — the §5 write path — and re-runs the sync. Writing
  D1 directly and treating that as canon remains forbidden (`d1-replica.md`).
- **A human is present for every write.** This is the material safety property and it is worth
  naming: the queue is worked in an interactive session where the owner can see, question and
  stop what is being changed. An unattended hourly consumer with the same powers was specified
  and then rejected. Do not reintroduce one without re-deciding this in the log.
- **The delay IS the review window — do not engineer it away.** Earlier drafts of this section
  treated the gap between SEND and apply as an awkwardness to be honest about. It is the
  opposite: because nothing drains automatically, a request sent by mistake can be recalled
  before it touches canon. The owner may ask a session to **drain and verify** (report only),
  **drain and apply**, or **drain and delete**. An unattended consumer would have applied the
  mistake before anyone saw it, and that — not throughput — is what was bought by removing it.
- **The UI still says "queued", never "sent" or "saved".** The session runs when the owner
  starts it, not on the click, so nothing a reader types appears in the data until then. A
  surface that implies immediacy is lying about a delay the reader cannot see.

**Multi-dashboard prompts route through task-orchestrator.** A pasted sync prompt that
resolves into work against more than one dashboard or tracker in the same pass — a
full-suite REFRESH BUILD, a CANON SYNC that cascades stale flags across several trackers,
or any studio-wide regeneration — is standard-inclusion territory for task-orchestrator
(`project-skill-studio` SKILL.md Phase 4), not a serial loop over each dashboard. A prompt
scoped to one dashboard's own rows executes directly as before; orchestration is for when
the paste fans out.

**Write path.** Claude edits `DESIGN_TRACKER.json` (bump `meta.revision`, set
`meta.generatedAt`, append a `log` entry), uploads it to the canon folder, and tells the
user what changed. The HTML is only re-issued when the SHELL changes — a data change needs
no new HTML at all. That is the point of the split.

---

## 6. Colour schemes — exact values

`Navy` is the default; RESET returns to it. Each scheme is a complete token set:

```js
'Navy':          { bg:'#EDF1F7', panel:'#F9FBFD', ink:'#0E1E3F', headerBg:'#0E1E3F', headerFg:'#EDF1F7',
                   muted:'#5B6B8C', line:'#D7DEEA', zebra:'#F3F6FA', accent:'#2C5BA8', onAccent:'#FFFFFF',
                   accentText:'#2C5BA8', body:'#324066', field:'#FFFFFF', tested:'#D7E1F0', testedFg:'#0E1E3F' }
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

| mark | Navy | Canon v6 | Slate | Dark | Mono |
|---|---|---|---|---|---|
| pass | #1E6B47 / #E3F0E7 | #1E7A45 / #E4F2E9 | #1F6B45 / #E1EFE7 | #4CC38A / #17301F | #111111 / #E6E6E4 |
| fail | #B23A2E / #F9E5E2 | #B3261E / #FBE6E4 | #B4482F / #F9E7E2 | #F2665B / #331A19 | #111111 / #CFCFCD |
| pending | #9A6B12 / #F5EEDD | #A97605 / #F8EED6 | #9A6B12 / #F6EEDD | #E0A93A / #332714 | #6E6E6E / #EDEDEB |
| blocked | #0E1E3F / #E3E7F0 | #141414 / #E8E4DA | #1B2227 / #E4E7E9 | #C3C8CD / #2A2F35 | #111111 / #C2C2C0 |
| na | #8A93AC / #EEF1F7 | #9A8F75 / #F1EADA | #8D969B / #EEF1F2 | #6B7178 / #22272D | #9A9A98 / #F4F4F2 |

On Navy accent TEXT is `#2C5BA8`, matching accent — verified AA on both bg and panel. On
Canon v6 accent TEXT is `#A8843C`, not `#C9A961` — gold on cream fails contrast (I3).

---

## 7. Type — one table, every element, px only

This is the complete inventory. If an element is not listed, it is
`400 12px/1.45 Helvetica Neue,Helvetica,Arial,sans-serif`. Nothing on the page may use a
size that does not appear in this table.

| element | exact declaration |
|---|---|
| dashboard title | `700 27px/1.15 IBM Plex Mono,monospace` + `letter-spacing:-.01em` |
| metric number | `700 26px/1 IBM Plex Mono,monospace` + `letter-spacing:-.01em` |
| section title | `700 15px/1.2 IBM Plex Mono,monospace` |
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

**v3.8 (2026-08-03): the display serif is gone.** Titles, metric figures and section heads are
set in **IBM Plex Mono**, the face already carrying the chrome. Two families now, not three, and
the Libre Baskerville request drops out of the page entirely. Georgia/serif remains only as a
fallback in files not yet re-issued. Two things this changes and one it does not:

- **Request `700`.** Plex Mono was being loaded at `400;500;600`, so a bold title was
  synthesised by the browser rather than drawn. The font URL now asks for `700`.
- **Pull the tracking in** by `-.01em` at 26–27px. Mono is wide, and at display sizes its
  default tracking reads loose beside 12px body text.
- **Sizes do not move.** 27/26/15 are still 27/26/15 — this is a face change, not a scale
  change, and §11's audit is unaffected.

So the whole page uses exactly six sizes: **27, 26, 15** (display sizes, mono), **14/15/13**
(control and chip glyphs only), **12** (everything with words in it), **10** (small-caps
chrome). There is no 11px, no 11.5px, no 13px text, no `rem`.

Rules
- **px only.** No `rem`, no `em`, no `%` font sizes.
- **Every `font:` shorthand MUST end with a family** — including the one-off cases above.
  A family-less shorthand is invalid CSS and silently renders at 16px. This has been the
  single biggest cause of drift; when in doubt write `font-size` + `font-family`
  separately rather than the shorthand.
- **Two families only** (v3.8 — was three). Body prose:
  `Helvetica Neue,Helvetica,Arial,sans-serif`. Everything else — ids, labels, chips,
  buttons **and the display sizes** (title, metric figures, section heads):
  `IBM Plex Mono,monospace`.
- Weight vocabulary: 400 body, 500 meta, 600 labels/chips/titles-in-rows, 700 buttons and
  display titles. No 300, no 800.
- Load: `https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600;700&display=swap`
  **The `700` is load-bearing.** Without it the browser synthesises every bold title
  instead of drawing it — which is exactly what shipped before v3.8.

---

## 8. EXAMPLE line roster — replace with the host project's

The rows below come from the project this shell was designed on. Keep the SHAPE (title,
source JSON, what a row means, six check labels, which sections matter) and substitute
your own lines.

### 8.1 Swap-in recommendations per skill

| skill | title | source JSON | a row is | `meta.checkNames` | sections that matter |
|---|---|---|---|---|---|
| proj-online-dev-tracker | Digital Dev Tracker | ONLINE_DEV_TRACKER.json | an app module | TYP · UNI · GLD · MUL · SEC · PII | all (reference build) |
| proj-design-tracker | Programme Tracker | DESIGN_TRACKER.json | a delivery line | CANON · DRAFT · REVIEW · QA · PRINT · SHIP | metrics, queues, risks, budget, milestones |
| proj-card-design | Card Deck Tracker | content-source.py v6 | a card set | DATA · ART · TYPE · PROOF · WEBP · CANON | grid, proofs, issues |
| proj-manual-design | Manual Registry | manual registry v6 | a manual / cheatsheet / supplement | COPY · LAYOUT · RULES QA · VERSION · PDF · REGISTERED | grid, decisions, milestones |
| proj-box-design | Packaging Tracker | v6 brand system | a packaging part | COPY · ART · DIELINE · BLEED · PROOF · CANON | grid, proofs, budget |
| proj-print-production | Print Pack Tracker | print_ready_deck_v6 | an artefact heading to the printer | BLEED · TRIM · COLOUR · FONTS · RENDER · PACKAGED | grid, issues, budget, milestones |
| proj-game-publishing | Publishing Tracker | publisher brief | a publisher / channel / proof round | TEMPLATE · UPLOAD · PROOF · APPROVAL · FULFIL · CONTRACT | grid, decisions, budget, milestones |
| proj-game-marketing | Commercial Tracker | pricing model v1 | a channel or collateral piece | POSITION · COPY · ASSET · PRICE · LIVE · MEASURED | grid, budget, milestones |
| proj-client-engagement | Engagement Tracker | engagement record | a booked or proposed engagement | SCOPED · QUOTED · BOOKED · PREPPED · DELIVERED · REPORTED | grid, milestones, budget, risks |
| proj-workshop-design | Workshop Build Tracker | facilitator-guide v1.2 | a workshop module or framework pack | DESIGN · TIMING · MATERIALS · MAPPING · PILOTED · SIGNED OFF | grid, decisions, milestones |
| proj-playtest | Playtest Tracker | playtest log | a session | PLANNED · RUN · CAPTURED · ANALYSED · FED BACK · CLOSED | grid, issues, milestones |
| proj-balance-tuning | Balance Tracker | scoring-source v3.0 | a tuning question | SIM · EVIDENCE · RECO · REVIEWED · DECIDED · APPLIED | grid, decisions, risks |
| proj-rules-qa | Rules QA Tracker | canon rules set | a consistency sweep area | CARDS · MANUALS · CHEATSHEETS · SCORING · PACKS · DIGITAL | grid, issues, milestones |
| proj-expansion-design | Expansion Tracker | base 65-card canon | an expansion pack | SCOPE · MAPPING · CARDS · FACILITATION · QA · RELEASED | grid, decisions, budget |
| proj-platform-compliance | Compliance Line Tracker | live platform policies | a platform | POLICY READ · MANIFEST · A11Y · PRIVACY · TEST · SUBMITTED | gates, issues, risks, milestones |
| proj-teams-app-dev | (uses the online-dev tracker) | — | — | — | — |
| proj-hosting-ops | Hosting Tracker | deployment plan | an environment or pipeline stage | IAC · BUILD · DEPLOY · MONITOR · BACKUP · COST | grid, risks, budget (planning only) |
| proj-mobile-dev | Mobile Tracker | GATED — awaiting Q10 | a mobile surface | — | milestones + risks only |
| proj-collab-integrations | Surface Tracker | integration brief | a collaboration surface | SPEC · AUTH · BOT · PRIVACY · TEST · SHIPPED | grid, gates, risks |

Fewer than six checks is fine — drop columns rather than invent gates nobody runs. Refs
stay unique programme-wide — the full prefix registry, and the two known collisions, are
in §4h. Gated skills show the gate, not a build grid pretending work is underway.
proj-design-tracker's rows are the other trackers.

The `source JSON` column names one file per delivery line (§3.1). A source label naming a
source *folder* or a build zip — `05_TEAMS_APP_v0.6_SOURCE` and the like — is the old
pre-v3.0 habit and goes stale the moment that build is superseded; name the tracker file,
and put the build version in `meta.evidenceBaseline` where §3.6 can act on it.

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
    <div style="font:600 10px/1 IBM Plex Mono,monospace;letter-spacing:0.18em;color:var(--accentText)">Example Project · ONLINE DEV</div>
    <div style="font:700 27px/1.15 IBM Plex Mono,monospace;letter-spacing:-0.01em">Digital Dev Tracker</div>
  </div>
  <div style="font:400 10px/1.5 IBM Plex Mono,monospace;text-align:right;color:var(--muted)">source v0.6<br>baselined 2026-07-25</div>
</div>
```

### 10.2 Metric strip
Grid `repeat(auto-fit,minmax(120px,1fr))`, gap 10px, margin-top 18px.
Card: panel + 1px line + radius 4px, `padding:12px 12px 11px`, column flex, gap 4px.
Number `700 26px/1 IBM Plex Mono,monospace;letter-spacing:-0.01em`; label `500 10px/1.3 IBM Plex Mono,monospace; letter-spacing:0.1em; color:var(--muted)`.

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
Five buttons, one per scheme: `height:32px;padding:0 9px;border-radius:3px;border:1.5px solid var(--ink);font:600 10px/1 IBM Plex Mono,monospace;letter-spacing:0.06em`,
transparent → ink-filled when active. Each shows three 9px circles (headerBg, accent, bg)
overlapping by `margin-left:-3px`, then the label NAVY / CANON / SLATE / DARK / MONO, in that
order. The order is fixed and does not follow the default — NAVY leads the row whichever
scheme is current (v3.10 made Canon v6 the default again without reordering the switcher).
**A `<select>` is not an acceptable substitute.**

### 10.6 Status chip — the one visual that must never drift
```html
<div title="Golden files: PEND"
     style="display:flex;align-items:center;justify-content:center;gap:3px;min-height:24px;
            white-space:nowrap;border-radius:3px;font:600 12px/1 IBM Plex Mono,monospace;
            letter-spacing:0.02em;background:var(--tint);color:var(--mark)">
  <span style="font-size:13px">~</span>PEND
</div>
```
`min-height:24px` (not `height`) plus `white-space:nowrap` is mandatory: §4e permits long
domain-word aliases (`UNDECIDED`, `NOT INTERESTED`) with no length bound, and a fixed-height
chip with no nowrap rule clips them mid-word (`NOT INTERESTE` over a stray `D`). The floor
stays 24px; the chip grows only if a longer alias needs it. Legend chips are identical with `padding:0 9px` and gap 4px. Build-state badges:
`height:24px;padding:0 8px;border-radius:2px;font:600 12px/1 IBM Plex Mono,monospace;
letter-spacing:0.02em` with the badge colours of §6.

### 10.7 Action buttons — 30px circles, always three on an actionable row

**One exception, v3.7: the §4e form row carries a single `+`.** The trio is a *choice about
an existing row* — explain it, proceed with it, improve it. The track-something-new row has
no row to choose about; it is a form, and its `+` is a submit. Rendering `!` and `✓` beside
it would offer two controls that cannot mean anything, which is worse than the asymmetry.

The geometry does not change: same 30px circle, same 2px ink border, same outline-by-default,
and it sits in the same `.acts` cluster at the row's right edge so it reads as one family.
What it does not do is carry selected state — a submit either fires or reports why it did
not, so there is no fill to invert and nothing for `state.choices` to remember. Everything
below applies to the trio on actionable rows.
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
**A legend only ever attaches directly beneath the `sechead` of the section it explains —
Module Grid's is the one legend this spec defines, and no other section renders a floating
status-vocabulary key with no section title above it.** A section that wants to remind the
reader what its own domain words mean (Portfolio Roster's `ON TRACK`/`AT RISK`/…, for
instance) states that in the section's own `secmeta` strap or inline per-row, not as a
second detached legend block — one legend, one owning header, no orphans.

**Filter by state (v3.6).** Beside the legend, two dropdowns: filter by BUILD STATE badge
(`ALL` / `INTEGRATED` / `TESTED` / `BUILDING` / `PROTOTYPE`, populated from whatever
badges actually appear in `modules`) and filter by check state (`ALL` / `PASS` / `FAIL` /
`PEND` / `BLOCK` / `N/A`, matching against any of the six check columns on a row — a row
passes the filter if ANY of its six checks equals the selected state). The two filters
compose (AND); clearing either returns to `ALL`. Filtering is client-side over the already-
loaded `modules` array — it never triggers a re-fetch — and the metric strip counts (§4,
top of page) stay computed over the FULL unfiltered set, so filtering the grid never makes
the header metrics look wrong.

**A grid with no check data for this instance says why, instead of rendering blank
cells.** When `meta.checksNote` is set (a tracker instance whose Module Grid is a
cross-line synthesis rather than a real build-check report, e.g. a programme-level rollup),
render it as a single line directly under the grid's header row, in the note-text style,
before the first data row: *what this grid actually shows, and what would need to run to
populate real TYP/UNI/GLD/MUL/SEC/PII data instead.* Absent `meta.checksNote` changes
nothing — this is additive, not a new required field.

### 10.9 Section heading (every section below the grid)
```html
<div style="display:flex;align-items:baseline;gap:12px;margin:30px 0 10px">
  <div style="font:700 15px/1.2 IBM Plex Mono,monospace">Risk Register</div>
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
| Next Actions | `34px 1fr 88px 104px 116px` | n · action · priority chip (+ `HOLD` badge if held) · owner · actions — `done` rows are pruned, not rendered (§4i) |
| Feedback & Suggestions | `52px 1fr 108px 92px 96px 116px` | ref · text (raisedBy + targetRef stacked beneath, muted mono) · mark chip (clickable — see §4e) · owner · priority+timeline stacked · actions |
| Portfolio Roster | `52px 1fr 128px 76px 76px 1fr` | ref · name · status chip · people count · tasks count · thisWeek |
| People & Allocation | `1fr 96px 76px 1fr` | name (repeat rows for multi-project people) · projectRef · tasks · note |
| Update Log | `186px 1fr` | `border-left:2px solid var(--accent)`, `background:var(--zebra)`, gap 2px between entries |

All of these sit inside the standard panel container, rows separated by
`border-top:1px solid var(--line)`, padding `11–12px 14px`.

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
- [ ] all table text measures 12px; chrome labels 10px; titles 27/15/26px **mono**; no 11px,
      no 11.5px, no 13px text (13/14/15px exist only as control and chip glyphs)
- [ ] status marks show glyph + word + tint, 24px tall, radius 3px — no bare glyphs
- [ ] action buttons are 30px circles with 2px borders, three per actionable row, outline
      until selected, then ink-filled — the §4e form row is the one exception (§10.7): a
      single `+` submit, same circle, no selected state
- [ ] tapping a row control inverts it to a solid ink fill; tapping it again clears it;
      selecting another moves the fill (only one selected per row) — verified on touch,
      with no hover involved
- [ ] selection survives a re-render and the marked-count matches what is filled on screen
- [ ] key panel shows all six controls with the exact circle fills of §10.3 (EXPLAIN pale
      with accent ring, PROCEED ink-filled, IMPROVE accent-filled)
- [ ] scheme switcher is five swatch buttons, not a `<select>`
- [ ] containers radius 4px, chips/buttons 3px, badges 2px; no 8px radii
- [ ] no borders on individual cells; rows separated by one 1px line
- [ ] module grid columns `104/92/351/1fr/104`, min-width 848px, no sideways scroll at 900px
- [ ] Navy is the default scheme (v3.11, reverting v3.10) — used when no scheme is set,
      on first load, and after RESET; the NAVY switcher button renders active on open, and
      the `:root` block carries Navy's literal values so first paint never flashes another
      scheme. Whichever scheme is default, `:root` must mirror it
- [ ] table rows separate on `--rule`, not `--line`; `--rule` exists in all five schemes
- [ ] every section is a `<details>`; empty ones and the update log start closed, the rest
      open; the row count is on the summary and stays legible while shut
- [ ] within a tracker: populated sections, module grid, People, empty sections, update log
- [ ] each empty section offers a `+`; each tracker opens with four equal stat blocks
- [ ] "rows" excludes the update log EVERYWHERE it is counted — nav tab badge, overview
      column and per-tracker stat block must agree. The log is history, not tracked work,
      and a page showing 31 in one place and 25 in another is describing two different
      things with one word
- [ ] IMPROVE opens a multi-line dialog, not `window.prompt()`; every `+` on the page ends
      in the tray and nothing but SEND TO CLI transmits
- [ ] People is present wherever any row has an owner: on the PEOPLE tab and on each
      tracker. It was ALSO on the Overview until v3.12 gave it a tab — the Overview copy
      could only count trackers already fetched, so it carried a "covers N of M lines
      opened so far" caveat that the tab does not need. Two answers to one question, one
      of them conditionally wrong, is worse than one answer
- [ ] selecting a name filters every tracker behind a visible banner
- [ ] IMPROVE field spans the full row width and survives a re-render with its text intact
- [ ] print preview: controls hidden, every mark still readable in greyscale

**Programme hub only (§14):**
- [ ] the tabs render in the §14.1 order, and the order does not follow the default tab
- [ ] a pooled tab renders ONE table carrying Project and Tracker columns, not one per tracker
- [ ] a `Details` cell with a full triple renders four labelled lines; one with a flat string
      renders a single note line, not four `undefined` lines
- [ ] ADMIN is a ghost bar button, not a §10.7 circle, and does not bind the row-action handler
- [ ] ADMIN reports "queued", never "saved", and the tracker's title does not change on screen
      until the next sync
- [ ] a locked, retired or archived line appears on DONE and nowhere on the Overview
- [ ] an orphan finding carries the source that found it (2.a / 2.b / 2.c)
- [ ] a 2.c finding renders as a decision requiring an answer, not as a note
- [ ] every mark advanced by an automated pass carries a `log` entry naming the evidence used
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
- [ ] `meta.evidenceBaseline`, `meta.subjectVersion` and `meta.baselinedAt` are all
      present; a tracker whose subject is itself sets baseline and subject equal rather
      than omitting them
- [ ] with `evidenceBaseline` ≠ `subjectVersion`, the `~ PROVISIONAL` banner renders, the
      stamp carries the chip, and every `pass` mark degrades to the pending tint with the
      `*` suffix — verify by editing one field and reloading, with no other change
- [ ] the degrade rule leaves `pending`/`blocked`/`fail`/`na` marks visually untouched, and
      advances nothing
- [ ] Defect rows render with `externalRef`, `targetRef` and `fixedIn` blank without layout
      breakage; an empty `defects` array omits the section per §3.4
- [ ] every ref in the file matches the §4h prefix registry, and no two registers in the
      programme issue the same ref
- [ ] a row whose triple field is a flat string renders as a single note line, not three
      `undefined` lines (§3.7 flat-note fallback)
- [ ] a row whose triple field is an object renders all three labels plus the expand toggle
- [ ] both row shapes render correctly in the same section without layout divergence
- [ ] the longest status alias in use renders on one line at the narrowest column it appears
      in — no mid-word wrap or clip (§10.6 `white-space:nowrap`)
- [ ] a row with a missing severity/status/rating value renders `? UNDEF` grey, never the
      literal string "undefined" and never a blank cell
- [ ] a `resolution:"partial"` row renders `[~ PARTIAL]` beside, not instead of, its
      severity/rating chip
- [ ] the emitted CREATE PROMPT text contains no EXPLAIN/PROCEED/IMPROVE legend and no
      "refs only" disclaimer — compare byte-for-byte against the §5 block
- [ ] Module Grid's BUILD STATE and check-state filters compose correctly and the header
      metric strip stays computed over the unfiltered set while the grid is filtered
- [ ] a section listed in `meta.retiredSections` is omitted exactly like an absent section,
      not shown as `— none —`
- [ ] a Next Action with `done:true` does not render; one with `hold:true` shows the
      `■ HOLD` badge beside its priority chip if it has one
- [ ] Feedback & Suggestions' `+ NEW` control requires all three fields (what/source/
      measured by) before it stages a row, and `measured by` is the fixed six-value choice,
      never free text

---

## 14. The programme hub — a fourth surface

`dashboard-set.md` documents three surfaces: skill-builder, facilitator, resources. The
**programme hub** is a fourth. It is pooled across every project and answers one question
the other three cannot: *what is true across all lines at once.* It gets its own section
because its tab grammar is not §4's and not §10's — scattering it through those would
tangle a multi-line surface with rules written for a single-line tracker.

Protect HQ is the reference implementation.

### 14.1 Tab set and fixed order

After `OVERVIEW`, in this order and no other:

```
OVERVIEW · DECISIONS · RISK · PEOPLE · PROJECTS · ORPHANED · DONE
```

**The order is fixed and does not follow which tab is default**, exactly as §10.5 fixes the
scheme-switcher order independently of the default scheme. A reader navigates by position;
an order that reshuffles itself around state is an order they cannot learn.

**RESOURCES became PEOPLE the same day (2026-08-04, owner).** RESOURCES pooled the `person`
kind, and no tracker in the estate has ever carried a `person` row — it was an empty tab, the
same fault BUDGET was removed for hours earlier and missed here because it sat between two
tabs that were being built. The data was never absent, only stored elsewhere: every row
carries an owner. **PEOPLE is therefore DERIVED, not pooled** — there is no kind to gather —
which makes it the fullest cut on the hub rather than the emptiest. It has two states: a
roster answering "who is carrying what", and, with a name selected, the §14.2 pooled table of
that person's rows across every line. It also reports how many rows name **nobody**, which is
the number worth reducing.

**BUDGET was specified here and removed the same day (2026-08-04, owner).** One tracker of
nine carried any `budget_line` rows, so the tab was empty for the whole estate bar one line,
and `budget_line` left `ALWAYS_SECTIONS` with it — an EMPTY Budget section on eight lines
claimed "nobody has filled this in" about lines that were never going to have a budget. The
kind stays in `SECTION_ORDER`, so a tracker that carries budget rows still renders them.
**Removing a pooled tab is not the same as hiding the data.** A hub should not carry a cut
that is empty almost everywhere: a tab that is nearly always blank teaches the reader to stop
opening it, which is how the one line that does have a budget stops being seen.

`PROJECTS` is the synthetic container tab (v3.9): not a destination, active whenever the
selected tab is a project key, and the thing the per-project level hangs from.

### 14.2 The pooled single table

A pooled tab renders **one table across all trackers**, with columns exactly:

```
Project | Tracker | Ref | Mark | Details | Owner | actions
```

`Details` renders the §3.7 triple. Where a row has no triple it renders the flat note it
always was — a partial triple is worse than a plain sentence (§3.7), and four `undefined`
lines are worse than either.

This **replaces** the per-tracker grouping used up to v3.11, where a pooled view emitted one
table per tracker with the tracker's name as the heading. Grouping answered "what does this
line carry"; the hub's question is "where is this across everything", and that needs the
project and tracker as *columns you can scan*, not headings you scroll between.

Applies to **pooled tabs only**. Per-project sections keep their own row grids (§10.10). Do
not widen the per-project section renderer to serve both: the columns differ, and one
function serving two column sets is how a change to one silently breaks the other.

### 14.3 DECISIONS

Pools kinds `decision` **and** `decision_required`, summarised per project. The two belong
on one surface because the question is the same — what has been settled, and what is waiting
on someone — and separating them hides the second behind the first.

### 14.4 ORPHANED

Work that exists but is not tracked. **A tracker is orphaned when it has no
`meta.trackerFunction`, no `meta.trackerPurpose`, and no row carries an owner** — all three,
because any one alone catches lines that are merely incomplete rather than unowned.

Three scan sources, and a finding **must carry the source that found it**, so a reader can
tell a missing tracker from a missing repo:

- **2.a — orphaned projects.** A tracker meeting the test above.
- **2.b — git repos with no tracker.** A live repo whose Drive project has no tracker JSON.
- **2.c — local items not in git.** Work on disk under no version control at all.

A **2.c finding becomes a `decision_required` row**, phrased as a choice — *"No repo sync —
keep it local, or sync it"* — never a silent note. The point of surfacing untracked work is
to force the decision, and a note nobody must answer is not a decision.

### 14.5 DONE

Lifecycle `locked` + `retired` + archived, together, on one tab.

This **reverses commit `2011e55`**, which deliberately put locked and retired lines on the
Overview so that setting work down never looked like losing it. That reasoning still holds —
they are **reported, never deleted, and restorable** — but the Overview is the "what needs
attention" surface, and finished work sitting in it competes with work that is live. DONE
keeps the guarantee and moves the location.

A locked, retired or archived line appears on DONE and **nowhere** on the Overview.

### 14.6 ADMIN

The surface for editing tracker metadata: `title`, `trackerFunction`, `trackerPurpose`,
`trackerOutcome`, `lifecycle`, and the registry's `project` binding.

**ADMIN is not a §10.7 action circle.** It is a ghost bar button beside the tracker stats,
the same family as `ARCHIVE`. v3.11 records exactly what happens when the circle family is
over-bound: `.act` is *geometry* worn by three different controls, a bare `.act` selector
bound the row-action handler to all of them, and the track-more `+` fired twice and queued a
row with no `ref` and no `action`. Do not put a fourth control into that family.

**ADMIN writes to the queue only.** It does not touch the replica and it does not touch
canon. The dialog reports **"queued"** — never "saved" — and the tracker's title does not
change on screen until the next sync. Changes are picked up by the next **Claude Code CLI
session**, so a UI implying immediacy would be describing a write that has not happened.

> **Named alternative, considered and not built:** replica-immediate writes, following the
> `/api/archive` precedent, where the change lands in D1 at once *and* queues a row so canon
> catches up. It is recorded here so the next reader knows it was a choice rather than an
> oversight.

### 14.7 The refresh scan

The Overview's refresh does two things: re-fetches live data for the reader, **and** queues a
`REFRESH SCAN` job for the next CLI session.

That session may change **tracker metadata only** — the tracker JSON on Drive, via the §5 write
path, followed by a re-sync. It may **never** change application code, the Worker, or Access
configuration. The boundary is enforced by this spec and by the owner reading the session, not
by a tool allowlist; that is a weaker guarantee than a machine-enforced one and is written down
as such. What makes it tolerable is that the session is interactive — the owner sees each write
as it is proposed, which an unattended job would not have offered.

What a scan must report: what it changed and why, per tracker; what it found and did not
change; and every mark it advanced together with the evidence used (§2). A scan that reports
only successes is indistinguishable from a scan that did nothing.

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

**Hosting is a decision the owner makes, not a default.** A studio run emits three
surfaces (`dashboard-set.md`) and asks per surface whether to host. Hosting exposes the
page's contents to whoever holds the link and opens the §5 write-back channel — still
manual, still prompted, still explicitly approved before any write, but newly available.
Ask, record the answer as a logged decision, and take "no" as complete.

---

## 13. Facilitator and Resources — interactive pooled views

Two of the three surfaces in `dashboard-set.md` — Facilitator and Resources — are
**pooled derived views**: they render tracker data gathered across every line for a
specific audience, and author nothing of their own back into a source tracker directly.

That used to mean read-only. v3.3 and earlier exempted both surfaces from the action
trio, CREATE PROMPT and the scheme switcher, on the reasoning that a surface with no
write-back loop had no need for the machinery that serves one. **This was reversed in
v3.4** after real use showed the opposite: the moment someone marks ten rows pooled from
every project line and hands them back as one compiled prompt is precisely a facilitator
or resourcing review, not a single-line tracker session. A read-only briefing card removed
the one action that made opening it mid-meeting worthwhile.

**Carried, same as the shell**: the action trio (§10.7), CREATE PROMPT and
the prompt protocol (§5), REFRESH DATA (§10.4), the scheme switcher (§10.5), the sticky
control bar (§10.4). **Not carried**: REFRESH BUILD and CANON SYNC — both are
single-tracker build/canon actions with no meaning against a view pooling several
trackers at once; a pooled REFRESH DATA line covers re-reading every source tracker
the surface pools from instead (v1.11.2, found live-testing the CRA reference build --
REFRESH DATA had simply never been added to the pooled shell at all).

**Added, specific to a pooled surface, not present on a single-line tracker**:

- **A click-to-scope index** — one row per tracker (Facilitator) or per project line
  (Resources), each showing its own rollup counts, computed at render. Clicking a row
  filters every section below to that scope; clicking the same row again clears it.
- **Independent dropdown filters** — by tracker/program and by owner/person — plus a
  free-text search box, all three composable with the index scope and with each other.
- Sections below the index reuse the exact row/triple/action-trio machinery of §4 and
  §10.7-10.10 — a pooled view is still built from the same components, just fed rows
  gathered from more than one source tracker instead of one.

`references/facilitator-hub-reference.html` is the canonical shell for both surfaces —
copy it, the same way `dashboard-reference.html` is copied for a single-line tracker.
`docs/samples/resource-tracker/resource-tracker_v2.html` is the Resources instance of it;
`resource-tracker_v1.html` is kept for history and is superseded — it predates the
index/filter pattern and should not be copied for a new build.

**Binding, without exception, same as every other surface**: the status vocabulary and
glyph+word+tint rule (§2); evidence discipline and derived-never-stored (§3.5); the
freshness stamp and evidence baseline (§3.4, §3.6), including saying `Not live-synced` in
words when the surface is a snapshot; and the print rules — a facilitator surface is
printed or held on a second screen more often than any other page this spec produces.

A pooled view may scope and filter its data differently from a single-line tracker. It
may not use a simpler standard of truth, and — as of v3.4 — it does not drop the controls
either. The honesty rules were always the non-negotiable half of the old rule; dropping
the controls turned out to be the wrong way to protect them.
