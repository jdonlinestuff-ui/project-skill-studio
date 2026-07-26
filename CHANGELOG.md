# Changelog

All notable changes to this skill are documented here.

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
