---
name: project-skill-studio
description: Bootstrap and maintain a complete Claude skill suite for ANY project — a generic "skill studio" that interviews the project, identifies its canonical sources of truth, designs a skill roster (canon skill + one build skill per active delivery line + studio-ops skills), authors and packages the .skill files, and installs the tracking discipline (SESSION_STATE.md, one tracker JSON per delivery line, decision log, and a set of three dashboards — skills-creation, facilitator and resources — with Create-prompt sync and an explicit ask before anything is hosted as a live artifact). Use whenever the user wants to create a skill suite for a project, "skill up" a project, make their project repeatable/consistent, enforce canon compliance across sessions, add project trackers, or says things like "project skill studio", "build skills for this project", "make this project a studio", or wants to clone the pattern used on a previous project onto a new one.
---

# Project Skill Studio

A meta-skill that turns any project into a **skill studio**: a versioned suite of project-specific skills plus a tracking discipline, so work on the project is repeatable, canon-compliant, and resumable across sessions and across Claude instances.

This generalises a pattern proven on a real project (a card-game design studio that grew to 20+ skills across three classes). The pattern, not the project, is what this skill encodes.

## Core model

Every studio has four parts:

1. **Canon** — the project's locked sources of truth, held in one canonical location (Drive folder, git repo, or local folder), with `SESSION_STATE.md` and one tracker JSON per delivery line at its root.
2. **Skill roster** — project-prefixed skills in three classes:
   - **Canon skill** (exactly one): the locked content/identity skill everything depends on — data sources, style system, naming, specs, "never invent" rules.
   - **Line skills** (one per *active* delivery line): build/production skills for each real workstream (e.g. print production, a Teams app, a marketing line). Never create a line skill for a platform that isn't in scope yet — that is scope drift.
   - **Studio-ops skills**: tracker, QA/review, playtesting/validation, client engagement — whatever cross-cutting operations the project actually runs.
   Large classes get an **orchestrator skill** that routes to the class members.
3. **Trackers** — `SESSION_STATE.md` (where are we, what's next), **one tracker JSON per delivery line** (`DESIGN_TRACKER.json`, `ONLINE_DEV_TRACKER.json`, …), a decision log folder, and **a set of three dashboards** over them (`dashboard-set.md`): Skill builder, Facilitator, Resources. Optionally a second memory tier (`memory-tiers.md`) where a coding agent reads a different file from the design sessions.
4. **Working rules** — canon discipline, decision logging, evidence baselines, proof gates. Baked into every generated skill, not documented separately.

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
- **One tracker JSON per active delivery line** — from `references/tracker-schema.md`,
  named for the line (`DESIGN_TRACKER.json`, `ONLINE_DEV_TRACKER.json`). There is no
  single combined project tracker; a second line means a second JSON file, and the
  dashboard shell renders any of them unchanged.
- A decision-log folder (dated markdown entries)
- If the project has a second memory tier — a coding agent's project-memory file, a
  condensed per-line state file — register it in `SESSION_STATE.md`'s canonical-sources
  table and apply the precedence rule in `references/memory-tiers.md`. Don't create one
  speculatively: one tier is the default.

If a tracker already exists, adopt it — never create a parallel one. If two copies of the
same tracker name exist, that is an issue to raise before writing anything, not a choice to
make quietly.

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
4. **Working rules** — from `references/working-rules.md`: modular design (re-author and test one module, never whole-package rebuilds), proof gates on visual output (owner approves proofs before build continues), evidence baselines (a tracker states which version its marks came from, and passing marks go provisional when the subject moves past it), leverage-existing-skills-first, local-first prototyping for code lines.
5. **Decision gates** — anything the owner controls (e.g. deck composition, scope changes) changes only via a logged decision, which auto-flags dependents.
6. **Canon-first request handling** — before generating any task, design, code, or documentation, search the connected canon store and treat what's found there as authoritative; never assume when canonical information exists. Full six-step sequence and the two skills to check first in `references/canon-first-workflow.md`.

Every generated skill additionally carries the **work loop**
(`DRAFT → VERIFY → PROOF → REVISE → REGISTER`), the **MCP-first rule**, and an
explicit **tunable vs locked** boundary — all specified in
`references/skill-baseline.md`, which also holds the five-point checklist a new
skill must satisfy before packaging. The studio enforces this on its own growth:
a skill missing any point fails creation review and the tracker raises it as an
issue. Claude cannot install skills — a `REINSTALL` status means re-present the
packaged file for the owner to save.

Keep each generated SKILL.md under ~500 lines; push bulk detail into that skill's own `references/`.

### Phase 4 — The dashboard set (three surfaces, standard)

A studio run emits **three dashboards, not one** — three audiences reading the same
trackers. `references/dashboard-set.md` is the authority on what each contains and how
the two pooled surfaces filter and scope; build in this order:

1. **Skill builder** (skills-creation) — the full tracker shell, rows are the studio's
   own skills: roster, class, install state, staleness verdict. Existing behaviour.
2. **Facilitator** — the live-operation briefing: operating sequence, the rules people
   look up mid-session, exception reference, actions available, and **today's open
   defects filtered from the register** (§4h) at the current `subjectVersion`.
3. **Resources** — orientation: what exists by line with versions and state, version
   skew called out, the tracker/dashboard inventory including retired ones, open
   decisions, and where canon and the memory tiers live.

Surfaces 2 and 3 are **pooled derived views** (spec §13) — every row is gathered from
another tracker rather than authored here — but as of spec v3.4 both are fully
interactive: the action trio, CREATE PROMPT, REFRESH DATA, and the scheme switcher all
carry over from the shell (REFRESH BUILD and CANON SYNC stay shell-only -- both are
single-tracker build/canon actions that don't generalise to a pooled, multi-tracker view),
plus a click-to-scope index and dropdown/search filtering unique to a pooled
surface (filter by tracker/program, by owner/person, or by text, all composable). Copy
`references/facilitator-hub-reference.html` for both — don't build either from prose. The
status vocabulary, evidence discipline, derived-never-stored, freshness stamp, evidence
baseline and print rules still bind without exception; those were never the part the
controls existed to protect. All three regenerate from the trackers; none is ever
hand-edited to fix a fact.

**Then ask about hosting — do not assume it.** Delivered as files the set is inert.
Hosted as live artifacts, the pages become reachable by whoever holds the link and the
§5 write-back channel opens: still manual, still prompted, still explicitly approved
before any write, but newly available. Ask per surface (a project may want Resources
shared and Facilitator local), record the answer as a logged decision, and treat "no"
as a complete answer. Full wording and rationale in `dashboard-set.md`.

Build the shell to **`references/DASHBOARD_SPEC.md` (v3.4)** — that file is the authority.
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
- **Evidence baseline** (spec §3.6) — the one that catches a dashboard freshness
  cannot. `meta.evidenceBaseline` records the version the marks came from,
  `meta.subjectVersion` the version now shipping. When they differ, a
  `~ PROVISIONAL` banner renders and every `pass` degrades to the pending tint
  with a `*`. A tracker rewritten this morning about a build from three versions
  ago is fresh by date and wrong in fact; without this pair, every signal on the
  page reads green.
- **Evidence discipline**: `pending` is the default and no note means no claim.
  Never mark `pass` on code review, intent, or "it should work".
- **Numbered defects have a home** (spec §4h): a Defect & Task Register, with
  `foundIn`/`fixedIn` versions and an `externalRef` for tickets that live in
  another system. An issue is a condition; a defect is a numbered, reproducible
  ticket against a stated version. Refs follow the one programme-wide prefix
  registry in §4h.
- **Derived, never stored**: metric counts, totals and percentages computed at
  render. Absent array omits its section; empty array renders `— none —`, so the
  reader can tell empty from missing.
- **Print is a first-class output** — controls carry `noprint`, and the page must
  paginate cleanly and stay legible in greyscale.
- One file, no dependencies: inline CSS and script, no build step, opens from
  `file://`, a Drive preview, or an artefact viewer.
- **Deliver it as a real artifact, not a handed-over file** — that's what makes Publish/
  Share and an embed code possible. `references/DASHBOARD_SPEC.md` §12 distinguishes this
  from a Cowork live artifact: Cowork's version pulls through its own connectors and is
  desktop-only, org-share-only, and **not web-embeddable at all** — the two are not
  interchangeable, and "build it in Cowork so it can be embedded on a site" isn't
  achievable as stated. Default to the regular-artifact path unless a request is
  explicitly asking for Cowork's connector-refresh behaviour in exchange for giving up
  website embedding.

### Phase 5 — Package, version, deliver

- Package every skill as `.skill` via skill-creator's `package_skill.py`; deliver with `present_files` so the Save-skill button appears.
- The suite carries a single version number recorded as `suite_version` in the programme tracker (the design/programme line's JSON — the one whose rows are the other lines). Any skill change bumps the suite version and marks changed skills `reinstall` there. One `suite_version` per studio, not one per line.
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
- `references/memory-tiers.md` — SESSION_STATE.md plus the optional second/third memory tier, and the precedence rule between them
- `references/tracker-schema.md` — the per-line tracker JSON schemas (line tracker and programme tracker), evidence-baseline fields, ref-prefix registry, write discipline
- `references/generated-skill-template.md` — skeleton every generated skill follows
- `references/skill-baseline.md` — work loop, MCP-first rule, five-point new-skill checklist, install boundary
- `references/canon-first-workflow.md` — the mandatory search-canon-first sequence for generation requests; task-orchestrator and the project's own skills as the two checks before acting
- `references/working-rules.md` — the generic working-rule set embedded in generated skills
- `references/dashboard-set.md` — the three surfaces a run emits (Skill builder, Facilitator, Resources), what each derives, the pooled-view conformance rules, and the live-artifact consent step
- `references/DASHBOARD_SPEC.md` — **the dashboard authority** (v3.4): data contract and load modes, evidence baseline, the ISSUE·PROBLEM·NEEDED row triple and header purpose block, status marks, defect register and ref-prefix registry, controls and prompt protocol, colour schemes, full type inventory, literal CSS/markup recipes, conformance checklist, pooled-view rules
- `references/dashboard-reference.html` — the working live-fetch build for a single-line tracker: copy this, don't build from prose
- `references/facilitator-hub-reference.html` — the working build for the Facilitator and Resources surfaces: click-to-scope index, dropdown/search filtering, same action trio and CREATE PROMPT as the shell
- `references/dashboard-standard.md` — pointer + record of what v3.0 changed from the superseded static-bake rules
- `references/dashboard-sample-generator.py` — regenerates the four scheme mockups and prints the WCAG contrast table
