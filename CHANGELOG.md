# Changelog

All notable changes to this skill are documented here.

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
