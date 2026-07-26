---
name: project-skill-studio
description: Bootstrap and maintain a complete Claude skill suite for ANY project — a generic "skill studio" that interviews the project, identifies its canonical sources of truth, designs a skill roster (canon skill + one build skill per active delivery line + studio-ops skills), authors and packages the .skill files, and installs the tracking discipline (SESSION_STATE.md, PROJECT_TRACKER.json, decision log, black-on-white HTML dashboard with Create-prompt sync). Use whenever the user wants to create a skill suite for a project, "skill up" a project, make their project repeatable/consistent, enforce canon compliance across sessions, add project trackers, or says things like "project skill studio", "build skills for this project", "make this project a studio", or wants to clone the pattern used on a previous project onto a new one.
---

# Project Skill Studio

A meta-skill that turns any project into a **skill studio**: a versioned suite of project-specific skills plus a tracking discipline, so work on the project is repeatable, canon-compliant, and resumable across sessions and across Claude instances.

This generalises a pattern proven on a real project (a card-game design studio that grew to 20+ skills across three classes). The pattern, not the project, is what this skill encodes.

## Core model

Every studio has four parts:

1. **Canon** — the project's locked sources of truth, held in one canonical location (Drive folder, git repo, or local folder), with `SESSION_STATE.md` and `PROJECT_TRACKER.json` at its root.
2. **Skill roster** — project-prefixed skills in three classes:
   - **Canon skill** (exactly one): the locked content/identity skill everything depends on — data sources, style system, naming, specs, "never invent" rules.
   - **Line skills** (one per *active* delivery line): build/production skills for each real workstream (e.g. print production, a Teams app, a marketing line). Never create a line skill for a platform that isn't in scope yet — that is scope drift.
   - **Studio-ops skills**: tracker, QA/review, playtesting/validation, client engagement — whatever cross-cutting operations the project actually runs.
   Large classes get an **orchestrator skill** that routes to the class members.
3. **Trackers** — `SESSION_STATE.md` (where are we, what's next), `PROJECT_TRACKER.json` (item status), decision log folder, and optionally an HTML dashboard.
4. **Working rules** — canon discipline, decision logging, staleness propagation, proof gates. Baked into every generated skill, not documented separately.

## Workflow

### Phase 0 — Intake

Before writing anything, establish the project profile. Extract as much as possible from the current conversation, project files, connected tools (search Drive/repos for existing canon), and past-chat search. Only then ask the user — and ask via short selection prompts, not open-ended discussion. Read `references/intake.md` for the full question set. The minimum profile:

| Field | Example |
|---|---|
| Project name + skill prefix | "Cyber Risk Assessment" → `cra-` |
| Canon root location + IDs | Drive folder ID / repo URL / local path |
| Single sources of truth | e.g. one data file all content flows from; a locked style spec |
| Locked vs design-controlled | What may never change silently vs what changes via logged decision |
| Active delivery lines | e.g. physical print, Teams app — only lines that are real today |
| Studio-ops needed | tracker (always), QA, playtest/validation, client engagement, tuning |
| Tool constraints | connector quirks discovered on this project (upload limits, no-delete, permission checks) |
| Open questions | anything unconfirmed — these get flagged in skills, never invented |

If the user says "same as my last project" or references an existing studio, search past conversations and Drive for that studio's conventions and carry them over explicitly, listing what was inherited.

### Phase 1 — Scaffold the canon root

Create (or verify) at the canon root:
- `SESSION_STATE.md` — from `references/session-state-template.md`
- `PROJECT_TRACKER.json` — from `references/tracker-schema.md`
- A decision-log folder (dated markdown entries)

If a tracker already exists, adopt it — never create a parallel one.

### Phase 2 — Design the roster

Propose the roster as a table (skill name, class, scope, build order) and confirm via a selection prompt. Rules:
- One canon skill. It is built **first** and every other skill references it by name.
- The tracker skill is built **second** (or first task of a new class) — tracking exists before the work it tracks.
- Line skills only for active lines. Speculative platforms go in the tracker backlog with a decision gate, not the roster.
- Reuse before writing: check installed plugin/public skills (engineering:*, design:*, docx/pptx/xlsx/pdf, frontend-design). Generated skills should *call* those, not duplicate them. Write new skills only for genuine gaps.

### Phase 3 — Author the skills

Use the **skill-creator** skill's authoring and packaging machinery (read its SKILL.md; package with `package_skill.py`). Every generated skill follows `references/generated-skill-template.md` and must embed:

1. **Canon block** — the project's sources of truth, IDs/paths, locked values, and the rule: *content flows from the canonical source through the pipeline; never hand-type, never duplicate, never invent. Unconfirmed values are flagged as open questions back to the owner.*
2. **Session loop** — open: read `SESSION_STATE.md` → resume next phase without preamble. Close (`/consolidate` or session end): log decisions to the decision-log folder → update `SESSION_STATE.md` and tracker.
3. **Tool constraints block** — the project's discovered connector quirks, phrased defensively: *if the tool isn't connected, ask the owner to reconnect rather than proceeding from memory.*
4. **Working rules** — from `references/working-rules.md`: modular design (re-author and test one module, never whole-package rebuilds), proof gates on visual output (owner approves proofs before build continues), staleness propagation (a changed decision flags downstream items stale in the tracker), leverage-existing-skills-first, local-first prototyping for code lines.
5. **Decision gates** — anything the owner controls (e.g. deck composition, scope changes) changes only via a logged decision, which auto-flags dependents.

Every generated skill additionally carries the **work loop**
(`DRAFT → VERIFY → PROOF → REVISE → REGISTER`), the **MCP-first rule**, and an
explicit **tunable vs locked** boundary — all specified in
`references/skill-baseline.md`, which also holds the five-point checklist a new
skill must satisfy before packaging. The studio enforces this on its own growth:
a skill missing any point fails creation review and the tracker raises it as an
issue. Claude cannot install skills — a `REINSTALL` status means re-present the
packaged file for the owner to save.

Keep each generated SKILL.md under ~500 lines; push bulk detail into that skill's own `references/`.

### Phase 4 — Tracker dashboard (optional but standard)

Build it to **`references/DASHBOARD_SPEC.md` (v3.0)** — that file is the authority.
Copy `references/dashboard-reference.html`, point `TRACKER_SOURCE` at the line's
JSON, replace the `EMBEDDED` seed. Copying the reference is faster and far more
accurate than building from the spec text.

**A dashboard is a VIEW over a source, never a copy.** The HTML holds no status
data. It fetches the JSON at run time and renders whatever it finds — because the
moment a status is typed into markup it starts lying and nobody can tell how stale
it is. Three load modes (spec §3.2): live fetch with `{cache:'no-store'}` by
default; Claude re-issue for anything structural, since a browser fetch can only
re-render what the JSON already says; and an `EMBEDDED` snapshot that keeps the
file usable offline and **must announce itself** with a full-width banner and a
`SNAPSHOT` stamp. Never render snapshot data as if it were live.

The non-negotiables — these are what drift:

- **px sizes only, and every `font:` shorthand ends with a family.** A family-less
  shorthand is invalid CSS and silently renders at 16px; it is the single biggest
  cause of drift. Six sizes total, 12px for anything containing words.
- **Status marks** `✓ PASS` / `~ PEND` / `✕ FAIL` / `■ BLOCK` / `– N/A` as glyph +
  word + tint, 24px tall. The word is what survives greyscale and colour-blindness.
- **Badge axis = build state** (`INTEGRATED / TESTED / BUILDING / PROTOTYPE`, plus
  `PROPOSED / OPEN` for queues), separate from the checks. A row can read TESTED
  while its checks say PEND — that is the point of splitting them.
- **Six checks** on build lines: `TYP UNI GLD MUL SEC PII`.
- **Action buttons**: 30px circles, three per actionable row — `!` EXPLAIN,
  `✓` PROCEED, `+` IMPROVE. Selected inverts to a solid ink fill; one selection
  per row; tapping again clears. IMPROVE opens a full-width field.
- **Five bar flags**: CREATE PROMPT (the single sync action), RESET, REFRESH
  BUILD, CANON SYNC, ↻ REFRESH DATA. Never a separate Save/Export.
- **Four schemes** as swatch buttons, never a `<select>`; selection in state, not
  the DOM. Radii 4/3/2/50%, never 8px.
- **Freshness is visible**: stamp states both fetch time and `meta.generatedAt`
  with revision; `generatedAt` over 7 days adds a `~ STALE` chip, over 30 days
  escalates to the banner.
- **Evidence discipline**: `pending` is the default and no note means no claim.
  Never mark `pass` on code review, intent, or "it should work".
- **Derived, never stored**: metric counts, totals and percentages computed at
  render. Absent array omits its section; empty array renders `— none —`, so the
  reader can tell empty from missing.
- **Print is a first-class output** — controls carry `noprint`, and the page must
  paginate cleanly and stay legible in greyscale.
- One file, no dependencies: inline CSS and script, no build step, opens from
  `file://`, a Drive preview, or an artefact viewer.

### Phase 5 — Package, version, deliver

- Package every skill as `.skill` via skill-creator's `package_skill.py`; deliver with `present_files` so the Save-skill button appears.
- The suite carries a single version number recorded in `PROJECT_TRACKER.json` (`suite_version`). Any skill change bumps the suite version and marks changed skills `reinstall` in the tracker.
- Sync source markdown of the skills to the canon root if the project uses Drive/repo storage (respect tool constraints — bundle large files as zips for chat delivery when uploads are unreliable).
- Log a decision-log entry: roster built, versions, open questions.

## Maintaining an existing studio

- **Add a skill**: confirm class, check reuse, author per Phase 3, bump suite version, mark `reinstall`.
- **Revise a skill**: preserve its name, copy to a writable location, edit, repackage, bump version.
- **New delivery line**: goes through a logged decision first; then a line skill (and, if the class is new, its tracker task first).
- **Retire/park**: mark parked in tracker with the gating decision; don't delete the skill file from canon.

## Interaction style

Match the studio owner's cadence: terse, momentum-focused, selection prompts over open questions, surgical fixes over rebuilds, no investigation preamble. When the owner opens with "what is my next step" or `/consolidate`, that is the session loop — execute it.

## References

- `references/intake.md` — full intake question set + selection-prompt phrasing
- `references/session-state-template.md` — SESSION_STATE.md template
- `references/tracker-schema.md` — PROJECT_TRACKER.json schema
- `references/generated-skill-template.md` — skeleton every generated skill follows
- `references/skill-baseline.md` — work loop, MCP-first rule, five-point new-skill checklist, install boundary
- `references/working-rules.md` — the generic working-rule set embedded in generated skills
- `references/DASHBOARD_SPEC.md` — **the dashboard authority** (v3.0): data contract and load modes, status marks, controls and prompt protocol, colour schemes, full type inventory, literal CSS/markup recipes, conformance checklist
- `references/dashboard-reference.html` — the working live-fetch build: copy this, don't build from prose
- `references/dashboard-standard.md` — pointer + record of what v3.0 changed from the superseded static-bake rules
- `references/dashboard-sample-generator.py` — regenerates the four scheme mockups and prints the WCAG contrast table
