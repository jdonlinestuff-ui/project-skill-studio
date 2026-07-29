# Changelog

All notable changes to this skill are documented here.

## [1.14.0] - 2026-07-29

Made task-orchestrator a standard inclusion for Phase 4 (the dashboard-set
generation phase), not just a general standing dependency -- per the owner's
explicit instruction, tied to the CREATE PROMPT protocol specifically.

**Added**
- `SKILL.md` Phase 4: new paragraph stating that building/refreshing the
  dashboard set (three core surfaces, or more once a studio outgrows one line
  per tracker -- this project runs eight) is independent, same-shell,
  different-DATA work per dashboard, and routes through task-orchestrator by
  default rather than a serial per-dashboard loop. Any CREATE PROMPT sync that
  lands work against more than one dashboard/tracker in the same pass, and any
  full-suite rebuild, is in scope -- subject to the shared-write rule added to
  task-orchestrator's own Step 2 (v1.13.0 of that skill): parallel reads of one
  source tracker are fine, but writes back to the same tracker from two
  dashboard rebuilds must be sequenced or merged, never dispatched independently.
- `references/DASHBOARD_SPEC.md` §5 (Controls and the prompt protocol): new
  paragraph cross-referencing the same rule -- a pasted sync prompt that fans out
  across multiple dashboards/trackers routes through task-orchestrator; a prompt
  scoped to one dashboard's own rows executes directly as before.

**Fixed (found while editing Phase 4)**
- `SKILL.md` Phase 4's own non-negotiables recap still said "Four schemes" and
  cited `DASHBOARD_SPEC.md (v3.4)" -- both stale since v1.13.0 added the Navy
  scheme and bumped the spec to v3.5. Corrected to five schemes (Navy default)
  and v3.5.

## [1.13.0] - 2026-07-29

Added a fifth colour scheme, Navy, and made it the new default scheme across
every dashboard surface, per the owner's explicit instruction. Canon v6 stays
available as a named scheme -- it is no longer what a dashboard opens to.

**Added**
- Navy token set (`['navy','NAVY','#0E1E3F','#2C5BA8','#EDF1F7']` in the JS
  `SCHEMES` array; full CSS custom-property block in `:root`) in both
  `references/dashboard-reference.html` and `references/facilitator-hub-reference.html`.
- `references/DASHBOARD_SPEC.md` bumped to v3.5: Navy's exact token set and mark
  tints added to §6, "four schemes" references in §1/§10.5/§11 updated to five,
  default-scheme checklist item repointed from Canon v6 to Navy, version-history
  table gained a v3.5 row.
- `references/dashboard-set.md`: both "four schemes"/"four-scheme switcher"
  mentions updated to five, Skill builder section notes Navy is now the default.

**Changed**
- `references/dashboard-reference.html` / `references/facilitator-hub-reference.html`:
  the CSS `:root` block (previously Canon v6's unconditional default) now holds
  Navy's token set; Canon v6's former `:root` values moved into an explicit
  `[data-scheme="canon"]` block alongside Slate/Dark/Mono. JS `SCHEMES` array now
  leads with `navy`. `state.scheme` default, `setScheme()`'s no-attribute
  special-case, and `resetAll()`'s reset target all changed from `'canon'` to
  `'navy'`. `dashboard-reference.html`'s footer line changed from "Canon v6
  scheme" to "Navy default scheme".

**Not changed**
- Slate/Dark/Mono token sets and the mark-tint values for pass/fail/pending/
  blocked/na on every existing scheme -- pixel-identical to v1.12.0.
- The scheme-switcher control geometry, swatch-button markup, and the
  five-button (was four-button) row itself -- only the array order and default
  selection changed, not the control.

## [1.12.0] - 2026-07-28

Formalised `task-orchestrator` from a soft "consider checking" reference into a
concrete, checked dependency, per the owner's explicit instruction to integrate
it into the studio.

**Added**
- `references/canon-first-workflow.md`: new "task-orchestrator integration"
  section naming concrete trigger points where this studio itself should route
  through task-orchestrator (Phase 3 multi-skill authoring, Phase 4 multi-surface
  dashboard builds, maintenance sweeps touching multiple generated skills, and a
  generated skill's own DRAFT step when it repeats a subtask across many items).
- `references/generated-skill-template.md`: new `## Dependencies` block in the
  generated-skill template, declaring task-orchestrator explicitly instead of
  leaving it implied by the canon-first-workflow reference alone.
- `references/intake.md`: Tools section now asks Phase 0 to confirm
  task-orchestrator is installed, flagging its absence as an open question
  rather than silently generating skills that reference a missing dependency.
- `SKILL.md`: Phase 0 intake table gets a Dependencies row; Phase 2 roster
  rules clarify that task-orchestrator is a standing dependency, not a roster
  candidate — distinct from (and composable with) a project's own class
  orchestrator skill, which routes between that project's own skills rather
  than handling arbitrary bundled/repeated work.
- `README.md`: `task-orchestrator` added to Requires, alongside `skill-creator`.

**Changed**
- `references/skill-baseline.md` checklist point 2 cross-references the new
  Dependencies block — a skill whose DRAFT step repeats a subtask across many
  items and doesn't declare task-orchestrator as a dependency now fails this
  checklist point explicitly, rather than the check being implicit.

No dashboard shell, prompt protocol, or tracker schema changed in this release
— this is a workflow/documentation integration only.

## [1.11.2] - 2026-07-28

Four more bugs found live-testing the reference programme's (CRA) dashboards, on top of
1.11.1's triple()/chip fixes (different bugs, same day, different session).

**Fixed — CREATE PROMPT restated the full triple on pooled views
(`references/facilitator-hub-reference.html`)**
- `buildPrompt()` on Facilitator/Resources was writing every marked row's full
  `Issue:`/`Problem:`/`What is needed:` (or `Note:` on Resources) text into the compiled
  prompt, on top of the ref, tracker, owner, and choice. That's pure restatement — Claude
  already has the full text from canon when the prompt is pasted back. Trimmed to ref +
  label + tracker + owner + choice + the reader's own typed extra direction, matching the
  single-line shell's `id + choice + detail` convention. A one-line note in the prompt
  header now says explicitly that refs are on purpose, not accidental omission.

**Fixed — REFRESH DATA was missing entirely on Facilitator/Resources**
- The pooled shell carried CREATE PROMPT, RESET, and the scheme switcher (per 1.11.0) but
  never got a REFRESH DATA control — not broken, just never added. Added, wired the same
  way as the single-line shell's EMBEDDED-only case: sets a flag, re-renders, and CREATE
  PROMPT adds a `REFRESH DATA: re-read both source trackers fresh...` line when it's on.
  `dashboard-set.md`/`README.md`/`SKILL.md` updated: REFRESH DATA now named explicitly
  among what a pooled view carries; REFRESH BUILD and CANON SYNC stay shell-only, since
  both are single-tracker build/canon actions with no meaning against a pooled,
  multi-tracker view.

**Fixed — REFRESH DATA gave no visible confirmation on the single-line shell
(`references/dashboard-reference.html`)**
- `loadData()` always reset the button to its default text and stripped its `accent-on`
  class once the (EMBEDDED-only, no-op) refresh finished — including when
  `state.dataRefresh` was still `true`. REFRESH BUILD and CANON SYNC use `toggleFlag()`,
  which sets the `on` class from state and leaves it there; REFRESH DATA used a bespoke
  path that always cleared it. Click it, see a one-second "REFRESHING…" flash, and the
  button lands back exactly as it looked before — nothing on screen shows the click
  registered, even though `state.dataRefresh` was armed underneath and CREATE PROMPT
  would correctly include the REFRESH DATA line. Reported against the Digital Dev and
  Hosting trackers specifically, but the bug was in the shared shell — every single-line
  tracker had it. Fixed: the button now stays highlighted with a `✓` for as long as the
  flag is armed, cleared only by RESET.

**Fixed — "rev null" in the CREATE PROMPT header (`references/dashboard-reference.html`)**
- The stamp and prompt-header revision logic checked `mt.revision !== undefined`, which is
  `true` for an explicit `null` (the value every dashboard without a real revision number
  actually has) — so "viewing SNAPSHOT rev null" rendered on any tracker that doesn't carry
  a revision. Changed to `!= null`, which correctly treats both `undefined` and `null` as
  "no revision to show."

**Reconciliation note**: this patch was authored in a session that didn't know about
1.11.1 landing concurrently in another session on the same repo. Both patches touch
`dashboard-reference.html` and `facilitator-hub-reference.html`; 1.11.2 was rebased onto
1.11.1's actual committed content (not the pre-1.11.1 copy this session started from) so
neither patch's fixes were lost. Flagging the process gap, not just the fix: two sessions
editing the same reference files with no shared lock is exactly the kind of drift this
skill's own canon discipline exists to catch elsewhere — worth a coordination convention
(e.g. checking git log before a reference-file edit round) rather than relying on luck.

## [1.11.1] - 2026-07-29

**Fixed — found while regenerating the wiki screenshots, not part of the ask**
- `triple()` in `dashboard-reference.html` had no flat-note path, so any row whose
  triple field is a plain string rendered `ISSUE undefined / PROBLEM undefined /
  NEEDED undefined`. That is every row in the shipped `EMBEDDED` seed, across seven
  sections, and every row of any real tracker not yet authored as triples — which
  spec §3.7 explicitly permits and expects. Next Actions additionally lost its title
  text, since its third field *is* the action text. `triple()` now accepts either a
  triple object or a flat string and falls back to a single note line; the six call
  sites pass the field rather than three properties of it. Risk Register's positional
  three-string form is unchanged. Verified with both shapes rendering in one section.
- The Feedback interest chip wrapped mid-word (`NOT INTERESTE` / `D`): `.mk` was fixed
  at `height:24px` with no `white-space` rule, while §4e permits long domain-word
  aliases. Now `min-height:24px` + `white-space:nowrap`, which keeps the §10.6 floor
  and makes §10.6 and §4e compatible. `DASHBOARD_SPEC.md` §10.6 updated to carry the
  rule, so it isn't re-fixed per project.
- `facilitator-hub-reference.html` carries the same chip fix plus a guard at the top of
  its own `triple()`, falling back to `note`/`short` so a flat pooled row degrades to a
  readable line instead of three blanks.
- Four conformance items added (§11) for the flat-note path, the mixed-shape case, and
  the longest-alias case.

## [1.11.0] - 2026-07-28

Two changes, both driven by a real build on the reference programme (CRA): the
Facilitator/Resources exemption from 1.10.0 is reversed, and the ISSUE·PROBLEM·NEEDED row
triple used throughout that build's dashboards is now documented as the standard.

**Reversed — Facilitator and Resources are interactive again (`DASHBOARD_SPEC.md` §13,
`dashboard-set.md`)**
- 1.10.0 made both surfaces read-only, exempt from the action trio, CREATE PROMPT, and the
  scheme switcher, reasoning that a surface with no write-back loop had no need for the
  machinery that serves one.
- Building the reference programme's actual Facilitator Hub and Resource Tracker showed
  the opposite: marking rows pooled from every line and compiling them into one CREATE
  PROMPT hand-off is exactly what a facilitator or resourcing review is for. A read-only
  briefing card removed the one action that made opening either surface mid-meeting worth
  it.
- Both surfaces now carry the action trio, CREATE PROMPT, and the scheme switcher, same as
  the shell — plus something the shell doesn't need: a click-to-scope index (one row per
  tracker or per project line; click to filter every section below to it) and independent
  dropdown filters (by tracker/program, by owner/person) composable with free-text search.
- The honesty rules that were never exempt — status vocabulary, evidence discipline,
  derived-never-stored, freshness stamp, evidence baseline, print rules — are unchanged;
  they were the actual point of the 1.10.0 rule, the controls were just the wrong lever.
- New reference build: `references/facilitator-hub-reference.html`, the canonical shell
  for both surfaces, alongside the existing `dashboard-reference.html` for single-line
  trackers.
- New sample: `docs/samples/resource-tracker/resource-tracker_v2.html` (and matching
  `.json`) built on the new shell. `resource-tracker_v1.html` is kept for history and
  marked superseded — it predates the index/filter pattern.

**Added — the ISSUE·PROBLEM·NEEDED row triple (`DASHBOARD_SPEC.md` §3.7)**
- Any row a reader has to act on — Decisions, Open Issues, Next Actions, and anything
  pooled onto Facilitator/Resources from them — may now be authored as three fields
  (`issue`, `problem`, `needed`) instead of one flat `note`. A flat note conflates three
  different questions a facilitator needs answered separately: what is this, why does it
  matter, what has to happen next.
- Each line clamps to one row by default with a per-row `… expand` / `– collapse` toggle;
  `EXPAND ALL` in the control bar toggles every row at once. This is an authoring step,
  not a splitting heuristic — a row missing any of the three fields stays a flat `note`
  rather than shipping a padded or guessed triple.
- Empty sections keep a lone `(+)` IMPROVE button, reusing the standard action-trio wiring
  with EXPLAIN/PROCEED present but hidden, so a facilitator can still direct what belongs
  in an empty section instead of hitting a dead end.
- `references/dashboard-reference.html` updated to match: the triple format is now the
  default row renderer for the sections above, replacing the flat-note-only version.

**Added — the header Function/Purpose/Objective block (`DASHBOARD_SPEC.md` §3.7)**
- Three optional `meta` fields — `trackerFunction`, `trackerPurpose`, `trackerOutcome` —
  render as a three-column block below the title/eyebrow and above the how-this-works
  panel, stating what a specific dashboard tracks, why, and what "done" looks like for
  that line.
- Each column hides independently when empty; the whole block hides when all three are
  empty, so older `EMBEDDED` seeds and pre-1.11.0 tracker JSON render unchanged.

**Changed**
- `SKILL.md` Phase 4 and the references list updated to the reversed pooled-view rule and
  the new `facilitator-hub-reference.html` file.
- `README.md` sample-dashboards section and file tree updated to match.

## [1.10.0] - 2026-07-27

A standard run now emits **three dashboards, not one**, and asks before hosting any of
them. Generalised from the reference programme, which had already built exactly this set
by hand — a skills-creation dashboard plus separate Facilitator and Resources surfaces —
and retired its earlier per-line dashboards in the process.

**Added — the dashboard set (`references/dashboard-set.md`)**
- **Skill builder** (existing behaviour, unchanged): the full tracker shell, rows are the
  studio's own skills — roster, class, install state, staleness verdict.
- **Facilitator**: the live-operation briefing. Operating sequence, the rules people look
  up mid-session, exception reference, actions available to the operator, and **today's
  open defects filtered from the §4h register** at the current `subjectVersion`. This
  panel is why the defect register and this surface ship together — a numbered ticket
  nobody can see during the session it affects may as well not exist.
- **Resources**: orientation. What exists by line with versions and state, version skew
  called out, the tracker and dashboard inventory including retired ones, open decisions,
  and where canon and the memory tiers live. The one page that answers "where do I start".
- Build order is Skill builder → Facilitator → Resources: the surface that tracks the
  studio's own growth exists before the ones describing the work.
- All three regenerate from the trackers. Editing a dashboard to correct a fact is the
  failure the whole discipline exists to prevent — fix the tracker, re-emit.

**Added — derived views (`DASHBOARD_SPEC.md` §13)**
- Facilitator and Resources are read-only derived views, **exempt** from the machinery
  that serves the write-back loop: the action trio, CREATE PROMPT and the prompt protocol,
  the scheme switcher, the sticky control bar, the module-grid geometry.
- **Binding without exception**: status vocabulary and the glyph+word+tint rule, evidence
  discipline, derived-never-stored, the freshness stamp and evidence baseline — including
  saying `Not live-synced` in words when the surface is a snapshot — and the print rules,
  since a facilitator surface is printed or held on a second screen more than any other
  page this spec produces.
- Stated plainly: dropping the controls makes it a briefing card; dropping the honesty
  rules makes it a poster.

**Added — the live-artifact consent step**
- Hosting is now an explicit question asked after the set is built, **per surface** (a
  project may well want Resources shared and Facilitator kept local), with the answer
  recorded as a logged decision.
- The question states the three consequences rather than selling the feature: the page
  becomes reachable by whoever holds the link and its contents leave the owner's storage;
  the §5 write-back channel opens — still manual, still prompted, still explicitly
  approved before any write, but newly available where it was not; and a hosted page that
  stops being re-emitted is a stale page with a URL, which travels further and is trusted
  more than a stale file on a disk.
- Files are the default. "No" is a complete answer and gets no follow-up pitch.
- `DASHBOARD_SPEC.md` §12 continues to govern *how* to host if the answer is yes.

**Changed**
- `SKILL.md` Phase 4 rewritten from "tracker dashboard (optional but standard)" to the
  three-surface set plus the hosting ask; core model, frontmatter description and the
  references list updated to match.
- `intake.md` now asks what the project's *live operation* actually is, since that is what
  the Facilitator surface describes — and says to drop that surface, explicitly, for a
  project that has no live operation rather than inventing one.

## [1.9.0] - 2026-07-26

Reconciliation release. The pattern was checked against the reference programme it was
generalised from — two real trackers, the real dashboard shell, the real memory files —
and the docs were corrected to match what that programme actually runs. Where the repo and
production disagreed, production was treated as the validated party.

**Changed — one tracker per delivery line**
- Retired the single `PROJECT_TRACKER.json` mandate. A studio keeps **one tracker JSON per
  delivery line** (`DESIGN_TRACKER.json`, `ONLINE_DEV_TRACKER.json`, …), which is what
  `DASHBOARD_SPEC.md` §3.1 has specified since v3.0 and what the reference programme has
  always done. `SKILL.md`, `tracker-schema.md` and `generated-skill-template.md` said
  otherwise and now don't; the spec needed no change.
- `tracker-schema.md` rewritten against the two shapes actually in production: the
  **line tracker** (positional arrays, feeds the dashboard directly) and the **programme
  tracker** (object-keyed — `canon_versions`, `pipeline`, `assets`, `teams_app`,
  `open_questions`, `decisions_required`, `suggested_activities`, `expansions`,
  `digital{}`, `digital_enhancements`, `backlog_epics`, `superseded_skills`).
- Retired with it: `items[]`, `depends_on`, `lines[]`, `backlog[]` and automatic staleness
  propagation. Nothing ever used them. Working rule 2 now describes what real trackers do
  — a decision names what it invalidates and affected rows are re-marked deliberately, by
  someone who looked at them, rather than by a declared dependency cascade.
- `suite_version` is recorded once, in the programme tracker, not per line.

**Added — evidence baseline (`DASHBOARD_SPEC.md` §3.6)**
- `meta.evidenceBaseline` / `meta.subjectVersion` / `meta.baselinedAt`: the version the
  marks were derived from, the version now shipping, and when the baseline was last taken.
- The degrade rule: on mismatch, a `~ PROVISIONAL` banner renders, the stamp carries the
  chip alongside any `~ STALE`, and every `pass` in the Module Grid degrades to the pending
  tint with a `*` suffix and a footnote naming both versions. `pending`/`blocked`/`fail`/`na`
  are untouched — degrading applies only to claims of success — and the rule never advances
  a mark or guesses what the newer version does.
- This closes the gap that made a stale dashboard invisible: `generatedAt` measures when the
  file was written, not whether what it says is still true, so a tracker rewritten this
  morning about a build from three versions ago reads green on every existing signal. New
  working rule 10 states the same thing for generated skills.

**Added — Defect & Task Register (`DASHBOARD_SPEC.md` §4h)**
- Numbered, reproducible tickets now have a home in the tracker instead of living in
  whatever tool the session happened to use and staying invisible to the dashboard.
  Fields: `ref` · `externalRef` (the id in the system that actually holds the ticket) ·
  `title` · `severity` · `mark` (`~ OPEN` / `✓ FIXED` / `■ BLOCKED` / `✕ WONTFIX` / `– N/A`,
  aliasing the fixed marks as §4e and §4f already do) · `targetRef` · `foundIn` · `fixedIn` ·
  `note`.
- `foundIn` interlocks with §3.6: defects found in a version later than `evidenceBaseline`
  are evidence the baseline has moved, and a `✓ FIXED` row is degraded like any other pass.
- **Issue vs defect stated plainly**: an issue is a condition ("the build was never synced"),
  a defect is a numbered ticket against a version ("#183 notes disappear on Crisis, v0.20").
- **One programme-wide ref-prefix registry**: M · B · R · I · D · AP · PG · S · Q · E · T ·
  F · P. Two real collisions are documented rather than silently resolved — `P` is also used
  for build phases by projects that numbered phases before a portfolio view existed, and `E`
  covers both registered enhancements and backlog epics. Both get a stated convention
  instead of a migration that would break refs already cited in changelogs.
- Section order 16 → 17, inserted after Open Issues; the insertion record in §4 now names
  all three one-time insertions and why each landed where it did.

**Added — memory tiers (`references/memory-tiers.md`)**
- Documents the second and third memory tier that real projects grow — a coding agent's
  project-memory file (conventionally `CLAUDE.md`) and a condensed per-line state file
  (e.g. `PROJECT_STATE.md`) — instead of pretending `SESSION_STATE.md` is always alone.
  One tier stays the default; a tier is added when a real second reader exists.
- **Precedence rule**: for version-specific facts, the most version-specific file wins
  (tier 3 → 1 → 2); for locked facts the order inverts and the locked-architecture tier
  wins, with any state file contradicting it reporting a drift rather than a change.
  Session open still reads `SESSION_STATE.md` first — it holds the next step.
- Four rules that keep tiers honest: every tier names the others and states the precedence
  rule; knowingly-superseded content carries a supersession header above it; no tier
  duplicates another's owned fact; one copy of each tier file.
- `session-state-template.md` reconciled with the sections a real one carries — canonical
  sources (one file per line, with ids and connector quirks), decisions awaiting owner,
  an issues register with severity, housekeeping for superseded files. The unused "Stale
  items" section is gone.

**Fixed — spec defects found during the reconciliation**
- Version label: the file was titled v3.0 while §4 cited "v3.2". Now titled **v3.3**, with
  a version-history table stating what v3.0/3.1/3.2/3.3 each changed, so no section has to
  guess again.
- Duplicate `## 5. Controls and the prompt protocol` heading removed (it appeared twice,
  consecutively).
- §12 Delivery physically preceded §11 Conformance. Conformance now comes first, matching
  its numbering and the actual order of work — check before ship, then ship.
- §3.3's documented payload omitted four fields the reference build reads or ships:
  `checkAbbr`, `eyebrow`, `baselinedAt`, `maintainer`. All four are now documented.
- §8.1's example row cited `05_TEAMS_APP_v0.6_SOURCE` — a build folder three versions stale.
  Example rows and both reference builds now name the tracker file; a new note explains why
  a `sourceLabel` naming a build folder is the pre-v3.0 habit and where the build version
  belongs instead (`meta.evidenceBaseline`, where §3.6 can act on it).
- Six conformance-checklist items added for the baseline pair, the degrade rule, defect-row
  rendering and ref-prefix uniqueness.

## [1.8.0] - 2026-07-26

New tracker archetype: **Resource Tracker** — portfolio-level status across every project, not one line's build detail. Same shell, same file, no parallel system: two new optional sections, populated by a different JSON shape, everything else absent per the existing omission rule.

**Added**
- `DASHBOARD_SPEC.md` §4f Portfolio Roster: one row per project — status (aliasing the fixed marks with domain words: `✓ ON TRACK` / `~ AT RISK` / `■ BLOCKED` / `✕ CANCELLED` / `– NOT STARTED`, same pattern as severity and the feedback interest mark), a people count, a task count, and `thisWeek` — one line, expected to be replaced weekly, not accumulated.
- §4g People & Allocation: one row per person **per project** — someone on three projects gets three rows, never one hand-summed row. Every total is computed at render by summing rows for that name/project; nothing is ever stored as a total.
- **The derive-if-roster-exists rule**: if People & Allocation has rows for a project, that project's people/task counts in the Portfolio Roster are DERIVED from them at render and marked `calc`; if no roster exists for that project, the counts are recorded directly on the project's own row instead. A tracker instance picks one mode per project, never both — verified by building an instance with three projects in derived mode and a fourth in recorded mode side by side, and confirming the sums are arithmetically correct and the `calc` badge appears only where it should.
- Section order grows from 14 to 16: Portfolio Roster and People & Allocation inserted before Module Grid — overview before per-line detail. Second one-time insertion after §4e; the spec says explicitly this is not a precedent for reordering anything else.
- `docs/samples/resource-tracker/`: a full worked example (4 projects, 6 people rows, both derive-modes demonstrated on different projects) as JSON + a working HTML instance + three real screenshots.

## [1.7.2] - 2026-07-26

**Added**
- `DASHBOARD_SPEC.md` §4e: the Feedback & Suggestions section is also usable for lightweight sprint planning, with no schema or code change — `timeline` was already free text with zero date parsing anywhere in the reference (checked before writing this, not assumed), so a row can hold `"Sprint 14"` there exactly as it holds a date elsewhere.
- Two things named as deliberately staying separate, not merged for convenience: `priority` stays priority, not size — sizing belongs in `note` or a documented project-specific field, never folded into `priority`; and the interest `mark` stays a stakeholder's reaction, not a planner's sprint commitment, since those are often different decisions by different people at different times.
- Explicitly out of scope, named rather than silently added: capacity/velocity math, burndown, a dedicated Sprint view. That's Budget-sized additional work, not a quiet extension of Feedback rows — a project that needs it gets its own section and its own decision.
- Example seed row F2 updated to demonstrate the pattern (owner, priority, and a sprint label together) rather than just describing it; screenshots regenerated and the render verified by reading the actual DOM text, not by eye.

## [1.7.1] - 2026-07-26

**Added**
- `docs/samples/shoot.py` + `docs/samples/screenshots/`: real Playwright screenshots of the actual `references/dashboard-reference.html`, in all four real schemes (Canon/Slate/Dark/Mono), showing the new §4e Feedback & Suggestions section plus one full-page render.
- `docs/wiki/Tracker-Shell-Samples.md`, ready to paste into the GitHub wiki.

**Removed**
- The v1.3.1 SVG mockup generator (`docs/samples/generate-mockups.py`, `tracker-*.svg`). It was a separate hand-coded renderer with its own scheme names — Ink / Parchment / Mono print / Dark console — that had already drifted from the reference build's real four schemes (Canon / Slate / Dark / Mono) by the time §4e shipped, and it predated the Feedback section entirely. Screenshotting the real file removes the second system to keep in sync. Files kept as `.superseded` in this working copy rather than deleted outright, so the retirement is visible in the diff.

## [1.7.0] - 2026-07-26

Checked live before writing anything: "Cowork live artifact" and "embeddable on a website" are two different, non-overlapping features, not two names for the same thing.

**Added**
- `DASHBOARD_SPEC.md` §12, Delivery: ship the dashboard as a real artifact (single self-contained HTML), not a handed-over file — that's what unlocks Publish/Share and an embed code. A comparison table sets out what a Cowork live artifact actually is (Team/Enterprise-only sharing, Claude Desktop only, refreshed through Cowork's own connectors, versioned automatically) against a regular artifact (Publish on Free/Pro/Max or Share on Team/Enterprise, runs in any browser, genuine iframe embed code with an allowed-domains list).
- The explicit finding: **Cowork live artifacts do not support website embedding at all.** Sharing one produces an org-internal link that opens in Claude Desktop, not a browser embed. A request to "build it in Cowork so it can be embedded on a site" is not achievable as stated — the two halves point at different features — and the spec says so plainly rather than silently picking one interpretation.
- Guidance: default to the regular-artifact path, since this spec's `fetch(TRACKER_SOURCE)` model already produces exactly the single-file shape that path needs. A genuine Cowork live artifact requires building inside an actual Cowork session on Claude Desktop with connectors named up front — it cannot be produced by authoring a static file outside Cowork and calling it one, since the connector wiring and automatic versioning are Cowork's own infrastructure.
- `SKILL.md` Phase 4 gains a pointer to §12 so the distinction is discoverable without reading the whole spec.

## [1.6.0] - 2026-07-26

New tracked concept: **Feedback & Suggestions**, a facilitator-recorded capture surface for live reviews — not a multi-user voting system.

**Added**
- `DASHBOARD_SPEC.md` §4e: new fourteenth section, `feedback` array in the payload shape (§3.3), row grid in §10.10, two new conformance checklist items (§11). Placed after Next Actions, before Update Log.
- **No vote tally, by design.** A running count invites gaming and implies a rigour the dashboard can't back, since it never verifies who touched it. Instead: a single status — `~ UNDECIDED` (default) / `✓ INTERESTED` / `✕ NOT INTERESTED` — aliasing the existing pass/pending/fail marks with domain words, the same pattern the spec already uses for severity. This is the **one deliberately clickable chip** in the whole dashboard; every other chip is evidence-derived and read-only, and the spec says so explicitly rather than leaving the exception to be discovered by accident.
- `raisedBy` and `owner` are both optional free text — the section is built for a facilitator transcribing for a room as often as for named individual input.
- Export beyond the page (email, spreadsheet) is explicitly deferred, not silently built. `DASHBOARD_SPEC.md` §4e notes that Create Prompt's plain-text output already pastes into either without new code, and that a real one-click integration is its own decision requiring its own connector.
- Prompt grammar extended (§5): a feedback mark that changed from its row's own last-known value compiles as its own `F<n> mark:<interested|not-interested|undecided>` line, separate from the ordinary `!`/`✓`/`+` choice line — a row can carry both in the same prompt.
- Reference build: full render path for the new section, `cycleMark()` for the clickable chip, `FEEDBACK_WORD`/`FEEDBACK_CYCLE` tables, three example seed rows in `EMBEDDED` (one anonymous, one named, one already marked). Verified by running, not reading: offline snapshot, live fetch, and the mark-cycle → Create Prompt path all exercised under a DOM shim.

**Fixed — found while implementing, not part of the ask**
- `markEmpty()` had been defined during the v1.4.0 partial-payload fix but **never actually called anywhere** — an absent array rendered a bare section heading with nothing under it, meeting neither the "omit the section" nor the "— none —" requirement of spec §3.4. Wired it into `render()` for real, wrapped every section's heading+panel in a shared `<section id="sec-*">` so both hide together, and fixed the Queues container so each of its three sub-lists (proofs/gates/decisions) is independently omitted or shown-empty rather than the whole cluster moving as one block. Verified against three payload shapes: array absent (section hidden), array present-but-empty (`— none —`), array present-with-data (rows render) — for both the new section and the ten pre-existing ones.
- The fix that wired `applyEmptyStates()` into `render()` was itself written once and **silently failed to apply** on the first attempt — the anchor text it searched for had shifted earlier in the same edit session when `cycleMark()` was inserted, and that particular replace had no assertion to catch the non-match. Caught only by running the actual code rather than reading the diff; re-applied with an assertion.
- `DASHBOARD_SPEC.md`'s own §4 section-order list had said "13 sections" through v1.5.0's changelog description of it as "fourteen" — that description was wrong at the time it was written. It is only accurate now that §4e exists. Noted in the spec itself so the discrepancy doesn't look like an unexplained retcon.

## [1.5.0] - 2026-07-26

**Added**
- `references/canon-first-workflow.md`: mandatory sequence for any generation request (task, design, code, documentation) — search the connected canon store first, treat what's found as authoritative, never assume when canonical information exists. Six steps: search canonical assets, summarise, identify missing information, generate a plan, generate implementation tasks, produce the deliverable only after the plan is approved.
- Conflict rule: when canonical assets disagree, surface the conflict and cite both sources rather than inventing a resolution or silently picking one side.
- "Key skills to consider for every request": check `task-orchestrator` for bundled/repeated/multi-model work, and the project's own installed skills (canon + line/ops) before writing new logic — this studio is one of these for scaffolding and tracker duties, not a replacement for a project's own canon skill once built.
- Wired into `generated-skill-template.md` (new template section), `working-rules.md` (rule 12), `skill-baseline.md` (tied into the Canon consistency & write-back checklist point), and `SKILL.md` (Phase 3 embedding item 6).
- Explicitly reconciled against the existing work loop rather than left as a second, competing sequence: the six steps are the concrete canon-search instantiation of `DRAFT` (search → summarise → plan → tasks) and the `PROOF` gate (approval before producing); `VERIFY`/`REVISE`/`REGISTER` continue to apply once the deliverable exists. The mapping lives once, in `canon-first-workflow.md`, and every other reference point cites it rather than restating it.

## [1.4.0] - 2026-07-26

Absorbs the owner's `status-dashboard` skill. **`references/DASHBOARD_SPEC.md` (v3.0) is now the dashboard authority** and supersedes the Tracker Shell v1.0 rules.

**Changed — a deliberate reversal**
- **Static bake is out; live fetch is in.** v1.0 mandated that dashboards bake their content into the HTML and render with JavaScript disabled. v3.0 inverts this: a dashboard is a **view over a JSON source**, fetched at run time with `{cache:'no-store'}`, because the moment a status is typed into markup it starts lying and nobody can tell how stale it is. Offline use is served by an `EMBEDDED` snapshot that must announce itself with a banner and a `SNAPSHOT` stamp — never by presenting baked data as current.
- Default surface is black on **cream**, not white.
- Type is pinned to **six px sizes**, and every `font:` shorthand must end with a family — a family-less shorthand is invalid CSS that silently renders at 16px, the single biggest cause of drift.
- `dashboard-standard.md` reduced to a pointer recording the supersession and the v1.0→v3.0 delta, so nobody builds from the retired rules.
- `tracker-shell-reference.html` **removed** — it was a plain-HTML approximation with no load layer, superseded by the real reference build.

**Fixed — the upstream reference was not spec-conformant**
- The shipped v7 reference had `const DATA={…}` baked in and **no** `TRACKER_SOURCE`, `fetch`, `EMBEDDED` or `SNAPSHOT` anywhere; `forceRefresh()` faked a refresh with a 700ms `setTimeout` and re-stamped without a network call. It violated rule #1 of the skill it shipped inside. Retrofitted to full §3.2 conformance: real fetch, `EMBEDDED` fallback, snapshot banner, honest stamp stating both fetch time and `meta.generatedAt` with revision, `~ STALE` chip past 7 days, banner past 30, and a real in-flight `↻ REFRESHING…` state.
- **Partial payloads crashed the reference.** Live fetch of any JSON missing a section threw `undefined.length` — a defect invisible while data was baked in, and a direct violation of §3.4. Added normalisation: an absent array omits its section, an empty array renders `— none —`, so render never sees undefined and the reader can tell empty from missing.
- **Check columns were hardcoded in markup.** `meta.checkNames` could not drive them, so a line with different checks rendered under another line's abbreviations. Now driven by `meta.checkAbbr` with a three-letter fallback derivation.
- The reference also hardcoded one project's CREATE PROMPT copy (source filename, check names, canon terminology); now derived from `meta`.
- `meta` now drives title, eyebrow, source label, check names and currency, so a second line needs a new JSON file rather than a new HTML file.
- The CREATE PROMPT block now names the revision being viewed, per §5, so a write can be re-based if the source moved on.
- Verified by execution, not inspection: syntax-checked, then all four load paths exercised under a DOM shim — offline snapshot, fresh live fetch, 7–30 day chip, and >30 day stale banner.
- Sample mockup footers said "swap the DATA block only", which taught the superseded model; now "live view over its JSON source · swap TRACKER_SOURCE, not the data".

**Known inconsistency, carried not hidden**
- The upstream skill body names the source constant `DASHBOARD_SOURCE`; spec §3.2 names it `TRACKER_SOURCE`. The reference defines `TRACKER_SOURCE` and aliases `DASHBOARD_SOURCE`, so either works. Pick one per project.

## [1.3.1] - 2026-07-25

**Added**
- `docs/samples/` — four sample dashboards as **SVG**, one per scheme, plus `generate-mockups.py`. SVG rather than PNG so the samples are text: they can be committed and diffed, stay crisp at any width, and render inline in the README.
- README gains a Sample dashboards section explaining what the mockups demonstrate — the two independent axes, evidence beside every claim, the trio, and the in-UI sync contract.
- The mockup generator asserts the AA threshold and refuses to emit a scheme whose worst pair falls below 4.5:1.

**Fixed**
- Dark console `N/A` mark lightened `#7E868D` → `#A3ACB4`; it measured 4.07:1 against its tint and would have shipped below the threshold the spec itself sets. Now 6.53.

## [1.3.0] - 2026-07-25

Spec reconciled against the source project's **actual** tracker shell, read from its canon store for the first time. Everything prior to this was reconstructed from prose descriptions; several details were wrong.

**Fixed**
- Status glyphs corrected: pending is `~` (tilde) not `◦`, blocked is `■` U+25A0 not `▲`. Labels are abbreviated PASS/FAIL/PEND/BLOCK/N-A so a mark fits a narrow grid cell.
- Check names corrected to six with three-letter headers: Typecheck `TYP`, Unit `UNI`, Golden files `GLD`, Multi-client `MUL`, Code security `SEC`, Privacy `PII`. v1.2.0 wrongly had REVIEW/PRIVACY.
- Badge axis is **build state** (`INTEGRATED / TESTED / BUILDING / PROTOTYPE`, plus `PROPOSED / OPEN` for queues), not versions and dependencies as previously described. A row may be TESTED while its checks still read PEND — separating the axes is the point.
- Section order replaced with the real fourteen-section inventory: metrics strip, action key, sticky bar, in-place prompt textarea, queues, risk register, budget with spend bars, milestone rail, next actions, update log.

**Added**
- The shell is data-driven — swap the DATA block only; layout, theming and interaction are shared.
- Print-safe rule: controls carry `noprint` and are hidden under `@media print`, so the same page prints as a status report.
- Trio buttons toggle (pressing again unmarks); IMPROVE reveals a per-row textarea appended to that item's prompt line.
- The sync contract is stated in the UI itself: Claude cannot see edits made in the page, so marks must be compiled via CREATE PROMPT and pasted back.
- Canonical copy-from sources recorded (shell + `support.js` + the two compiled standalone instances). This skill's `tracker-shell-reference.html` is documented as a plain-HTML approximation for projects with no component runtime; where they differ, the project's own shell wins.
- Numeric audit of the source project's default scheme, recording that `#A8843C` on cream measures 2.97 and still fails AA despite having been adopted as a contrast fix.

## [1.2.1] - 2026-07-25

**Added**
- `tracker-shell-reference.html`: the shipped reference dashboard implementation — statically-baked default scheme, working in-page scheme switcher, responsive collapse to single-column with 44px targets. Skills copy from this rather than rebuilding the shell.

**Fixed**
- Sample trackers rebuilt to full v1.2.0 conformance. The v1.1.0 samples predated the corrected spec and were missing the fixed section order (no Suggested activities or Change log sections), the typography slots, the scheme switcher, and 30px trio sizing; they also still showed the wrong RAISE ISSUE flag.
- Generator now emits both the reference HTML and the four PNGs from one token table, so a token change cannot leave them disagreeing.

## [1.2.0] - 2026-07-25

Review pass over the source project's full skill suite (21 skills, suite v25), generalising what had been added there since v1.1.0.

**Added**
- `skill-baseline.md`: the mandatory work loop `DRAFT → VERIFY → PROOF → REVISE → REGISTER` (smallest reviewable unit, named checks, owner proof for content/visual/commercial output, surgical revision only, canon write-back; exits only on gates passing plus explicit acceptance where required), the MCP-first rule (connected tools before manual workarounds; registry search rather than hand-rolled integrations or memory), the five-point new-skill checklist, and the install boundary (Claude cannot install skills; REINSTALL means re-present the file).
- Working rule 9, **source-sync invariant**: the canon store is authoritative only if the work actually landed there. Work done in another surface can leave canon several versions stale while looking current — verify version numbers against artefacts, and raise unsynced-source discoveries as issues.
- `generated-skill-template.md` gains a Work loop & MCP section and an explicit tunable-vs-locked block.
- Tracker Shell: fixed section order, three typography slots (display serif / UI sans / mono for evidence — mono on evidence makes a fabricated value visually obvious), in-page scheme switcher layered over the baked default, 30px trio controls with 44px touch targets.

**Fixed**
- Bar flags corrected to the source spec: `CREATE PROMPT · RESET · REFRESH BUILD · CANON SYNC · ↻ REFRESH DATA`. v1.1.0 wrongly listed RAISE ISSUE in place of RESET. Sample generator and PNGs regenerated to match.

## [1.1.0] - 2026-07-25

Incorporates the owner-authored **Tracker Shell spec v1.0**, generalised from the project it was developed on.

**Added**
- `dashboard-standard.md` rewritten as the Tracker Shell spec: fixed status vocabulary (pass/fail/pending/blocked/na as glyph + word + tint, never colour alone), badge axis separate from status, evidence discipline (absent evidence an item is pending, not pass), `TYPECHECK/UNIT/GOLDEN/MULTICLIENT/REVIEW/PRIVACY` check names for build lines.
- Mandatory static-bake rule: dashboards render fully with JavaScript disabled, mobile-first, 44px touch targets — a JS-dependent dashboard once rendered blank on a phone in real use.
- Four colour schemes with published tokens — Ink (default), Parchment, Mono HC, Slate dark — all verified to WCAG 2.1 AA numerically. Worst-case pair per scheme: 5.94 / 5.13 / 14.16 / 6.81.
- `dashboard-sample-generator.py`: renders all four schemes to PNG and prints the contrast table. Run after changing any token.
- Conformance is enforced at skill creation rather than retrofitted: a skill emitting a non-conforming dashboard fails creation review and the tracker flags it.

**Changed**
- Five bar flags now specified (CREATE PROMPT primary, REFRESH DATA, REFRESH BUILD, CANON SYNC, RAISE ISSUE); REFRESH BUILD and CANON SYNC are no longer code-line-only extras.
- **Revises v1.0's black-on-white-only rule.** v1.0 forbade any theming on owner-facing dashboards; v1.1.0 permits four verified schemes. Dashboards remain working tools — schemes vary contrast and warmth, not decoration, and carry no product branding.

## [1.0.0] - 2026-07-25

Initial release. Generalised from a project-specific ("CRA") skill designer into a project-agnostic studio bootstrapper.

**Added**
- Intake workflow: pulls project profile from conversation context, connected tools, and past sessions before asking the user anything; short selection-prompt questions only.
- Three-class skill roster model (canon / line / studio-ops) with an active-lines-only rule — no skills for speculative platforms.
- `generated-skill-template.md`: skeleton every authored skill follows, embedding canon rules, a session loop, tool-connection constraints, and working rules.
- `tracker-schema.md`: `PROJECT_TRACKER.json` schema with staleness propagation (a logged decision flags dependent items stale automatically).
- `session-state-template.md`: terse `SESSION_STATE.md` format for cross-session resume.
- `dashboard-standard.md`: locked interaction pattern — black-on-white styling, EXPLAIN/PROCEED/IMPROVE trio per item, single "Create prompt" sync button, REFRESH BUILD / CANON SYNC actions for code lines.
- `working-rules.md`: ten generic working rules (canon discipline, decision logging, modular design, proof gates, local-first prototyping, leverage-existing-skills-first, defensive tooling, surgical fixes, live research, no floating questions).

**Notes**
- No project-specific values are hard-coded anywhere in this skill.
- Requires Anthropic's `skill-creator` skill for authoring test cases and packaging `.skill` files.
