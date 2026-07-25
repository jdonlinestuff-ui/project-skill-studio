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

Keep each generated SKILL.md under ~500 lines; push bulk detail into that skill's own `references/`.

### Phase 4 — Tracker dashboard (optional but standard)

If the user wants a dashboard, follow `references/dashboard-standard.md`. Non-negotiables from the proven pattern:
- Plain **black-on-white, high-contrast** HTML. No brand theming on owner-facing dashboards.
- Items default to **pending**; untouched items need no action.
- Each actionable item carries the **EXPLAIN / PROCEED / IMPROVE** trio (no HOLD button — untouched = held).
- One single **Create prompt** button that compiles all marked edits into a ready-to-paste sync prompt for the next Claude session. Never separate Save/Export buttons that do the same thing.
- Code-line dashboards may add **REFRESH BUILD** (full clean pipeline) and **CANON SYNC** (diff build vs canon) actions.
- The dashboard is a static HTML artifact regenerated from `PROJECT_TRACKER.json` — the JSON is the truth, the HTML is a view.

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
- `references/working-rules.md` — the generic working-rule set embedded in generated skills
- `references/dashboard-standard.md` — dashboard spec + interaction standard
