# Tracker schema — one JSON per delivery line

**There is no single `PROJECT_TRACKER.json`.** A studio keeps **one tracker JSON per
delivery line**, named for the line, living at the canon root — `DESIGN_TRACKER.json`,
`ONLINE_DEV_TRACKER.json`, `PRINT_TRACKER.json`. This matches `DASHBOARD_SPEC.md` §3.1,
which has said one-file-per-line since v3.0, and it is what the pattern's own reference
programme actually runs.

The JSON is the single truth for its line; any dashboard HTML is a view over it that holds
no status data of its own.

*Retired in v1.9.0: the earlier single-file `PROJECT_TRACKER.json` schema, with its
`items[]` / `depends_on` / `lines[]` / `backlog[]` fields and automatic staleness
propagation. Nothing in production ever used them. What real trackers use instead is an
issue and risk register (below) plus the evidence-baseline rule — a mark goes provisional
because the thing it describes moved, which is the failure that actually happens, rather
than because a dependency edge was declared up front.*

## Two shapes, both real

Which one a line uses depends on whether its rows are *build units* or *programme state*.

### A — Line tracker (dashboard source)

Feeds a dashboard directly, so its row arrays are **positional** and identical across
lines — the shell renders any of them without modification. The authority for this shape
is `DASHBOARD_SPEC.md` §3.3; it is summarised, not redefined, here:

```jsonc
{
  "meta": {
    "line": "online-dev",
    "title": "Digital Dev Tracker",
    "eyebrow": "PROJECT NAME · LINE",           // optional strap above the title
    "sourceLabel": "ONLINE_DEV_TRACKER.json",   // name the tracker file, not a build folder
    "checkNames": ["…", "…", "…", "…", "…", "…"],
    "checkAbbr":  ["TYP","UNI","GLD","MUL","SEC","PII"],  // optional; exactly 6 if present
    "currency": "AUD",
    "revision": 4,                              // increments on every write
    "generatedAt": "<ISO 8601>",
    "maintainer": "Claude",
    "evidenceBaseline": "v0.6",                 // version the marks were derived FROM
    "subjectVersion": "v0.20",                  // version shipping NOW
    "baselinedAt": "YYYY-MM-DD"
  },
  "modules":     [[name, builtAgainst, badge, [6 status keys], evidenceNote], …],
  "proofs":      [[ref, name, badge, note], …],
  "gates":       [[ref, name, badge, note], …],
  "decisions":   [[ref, title, "OPEN", note], …],
  "issues":      [[ref, "High"|"Med"|"Low", note], …],
  "defects":     [[ref, externalRef, title, severity, mark, targetRef, foundIn, fixedIn, note], …],
  "risks":       [[ref, "High"|"Med"|"Low", title, cause, control], …],
  "budget":      [[ref, lineItem, budget, spent, note], …],
  "milestones":  [[ref, "YYYY-MM-DD", title, "done"|"next"|"pending"|"blocked", note], …],
  "nextActions": [[n, action, owner], …],
  "feedback":    [[ref, raisedBy, text, targetRef, mark, owner, priority, timeline, note], …],
  "projects":    [[ref, name, status, people, tasks, thisWeek], …],
  "people":      [[name, projectRef, tasks, note], …],
  "log":         [[when, what], …]
}
```

Absent arrays omit their section; empty arrays render `— none —`. A second line needs a
new JSON file, never a new HTML file.

### B — Programme tracker (object-keyed)

The design/programme line's rows are *the other lines*, so it carries structure a build
grid has no column for. It is object-keyed rather than positional, and its dashboard
renders the queues it actually has rather than pretending to the module grid:

```jsonc
{
  "updated": "YYYY-MM-DD",
  "suite_version": "v21",
  "canon_versions": { "<asset id>": "<version>", … },   // the locked set everything cites
  "pipeline": [{ "stage": 1, "name": "", "skill": "", "status": "done|active|blocked",
                 "built_against": {…}, "suggested_instruction": "" }],
  "assets":   [{ "id": "", "name": "", "version": "", "status": "locked|draft|in-progress|cancelled",
                 "built_against": {…}, "notes": "" }],
  "teams_app": [{ "phase": "P3", "name": "", "status": "done|partial|queued|blocked|removed",
                  "built_against": {…}, "note": "" }],   // rename per the project's build line
  "open_questions":      [{ "id": "Q1", "text": "", "status": "open|answered", "answer": "", "note": "" }],
  "decisions_required":  [{ "id": "D10", "title": "", "note": "", "choice": null,
                            "details": "", "raised": "", "resolved": "" }],
  "suggested_activities":[{ "id": "S1", "title": "", "why": "", "choice": null, "details": "" }],
  "issues":   [{ "id": "I8", "text": "", "severity": "high|med|low",
                 "status": "open|resolved", "note": "" }],
  "defects":  [{ "id": "T1", "external_ref": "#183", "title": "", "severity": "high|med|low",
                 "status": "open|fixed|blocked|wontfix", "target_ref": "",
                 "found_in": "", "fixed_in": "", "note": "" }],
  "expansions": [{ "pack_id": "", "name": "", "type": "", "version": "", "framework": "",
                   "framework_edition": "", "verified_date": "", "status": "", "built_against": {…} }],
  "digital_enhancements": [{ "id": "E1", "name": "", "added": "", "status": "registered|unregistered",
                             "detail": "", "decision": "D13" }],
  "backlog_epics": [{ "id": "E10", "name": "", "tier": "", "status": "", "note": "" }],
  "digital": { "app_version": "", "modules": [{ "name": "", "status": "",
                 "tests": { "typecheck": "", "unit": "", "golden": "", "multiclient": "" },
                 "review": { "code_security": "", "privacy_invariant": "" },
                 "built_against": {…}, "note": "" }],
               "module_list": [], "asset_proofs": [], "platform_targets": [] },
  "skills": [{ "name": "", "status": "installed|reinstall|draft|parked", "improve": "" }],
  "superseded_skills": [{ "name": "", "note": "why, and what replaced it" }],
  "decisions":    [{ "date": "", "by": "", "summary": "", "drive_ref": "" }],
  "next_actions": [{ "text": "", "owner": "", "priority": 1 }]
}
```

`built_against` is the spine: every asset, stage and module records which canon versions it
was built from, so a canon bump makes the gap computable instead of remembered.

**`digital.modules` mirrors, and does not own.** Where a programme tracker carries a
condensed copy of a build line's modules, the line's own tracker stays authoritative and
the mirror says so in a `phases_mirror_note`. Two files claiming the same fact is the drift
this whole discipline exists to prevent.

## Evidence baseline — required on both shapes

`evidenceBaseline` / `subjectVersion` / `baselinedAt` (shape A `meta`; shape B top level or
`digital.app_version` plus the same two companions). When baseline and subject differ,
every `pass` degrades to provisional and the dashboard says so — the full rule, including
what it must not do, is `DASHBOARD_SPEC.md` §3.6.

This is the mechanism that catches the common failure: a tracker rewritten today, about a
build three versions old, showing green on every freshness signal it has.

Record the mismatch as an issue as well as a banner. The banner is for whoever opens the
page; the issue is for whoever reads the source.

## Ref prefixes

One registry programme-wide — `M` milestones · `B` budget · `R` risks · `I` issues ·
`D` decisions · `AP` asset proofs · `PG` gates · `S` suggested activities · `Q` open
questions · `E` epics and enhancements · `T` defects · `F` feedback · `P` portfolio
projects. Two known collisions (`P` also used for build phases, `E` covering both
enhancements and epics) are documented in `DASHBOARD_SPEC.md` §4h; pick a convention and
record it rather than renumbering refs already cited in changelogs.

## Write discipline

- **One named file per line at canon root.** A second copy of the same name is how a
  superseded tracker gets read as canon.
- Cite the input file id in `meta.sourceLabel` (or the shape-B equivalent) so any write is
  traceable to what it was derived from.
- Bump `revision`, set `generatedAt`, append a `log` / `decisions` entry on every write.
- **Where the canon store has no delete tool, every write is an add, not a replace.** Hand
  back a delete URL with each write and name the superseded file and its size, so the owner
  can clean up. A dashboard pointed at a tracker *by file id* needs repointing on every
  revision, because the id changes — prefer a stable path or published link where the store
  offers one.
- Statuses change only when evidence changes. A rewrite that advances no mark is a normal,
  healthy outcome and the log should say so plainly.
