# Hosted tracker replica — D1 behind a Worker

Added 2026-08-02. Companion to `DASHBOARD_SPEC.md` §3.2 (load modes) and
`tracker-schema.md` (the JSON shapes). Read those first; this describes one
additional way a dashboard can reach its data, and what a studio must do to
keep that path honest.

## The one rule that does not change

**The tracker JSON on disk is still the source of truth.** D1 is a read
replica. If the two disagree, the JSON wins and the replica is wrong — re-sync
it, never hand-edit the database to match. A dashboard reading from D1 is still
a VIEW over the tracker, one hop further away.

This exists because a local file cannot be read from a phone, and because
`file://` blocks `fetch()` outright, so a dashboard opened by double-clicking
silently falls back to its `EMBEDDED` snapshot. A hosted replica fixes both
without moving authority off the canon file.

## What NOT to do with it

- **Do not make D1 canonical.** That breaks §3.1 and turns the Drive files into
  derived artifacts. It needs its own logged decision and a spec rewrite; it is
  not a thing to drift into.
- **Do not build a write-back path** from the database to the JSON. The write
  path is unchanged: Claude edits the tracker file, per §5's CREATE PROMPT
  protocol. A replica that accepts writes is a second source of truth wearing a
  disguise.

  **This rule survives v3.12, and the automated dispatcher does not breach it —
  read this before "fixing" anything.** From v3.12 a scheduled consumer drains the
  queue and may change canon. It does so by editing **the tracker JSON on Drive**
  and re-running the sync. That is the §5 write path executed on a schedule
  instead of by hand; the direction of travel is still Drive → D1, and D1 is still
  derived. What remains forbidden is the other direction: writing D1 and treating
  that as the record. Stated plainly because the next reader will see an automated
  process with write access and reach for the wrong correction — the danger is not
  that it writes, it is *where* it writes.

  The one narrow exception predates this and is unchanged: `archived` /
  `archived_at` are **replica state, not canon** (§14.5), which is why the
  `trackers` upsert is `ON CONFLICT DO UPDATE` and deliberately not
  `INSERT OR REPLACE` — replace would rewrite the whole row and un-archive every
  line the owner had archived.
- **Do not let a project's dashboard read D1 while its tracker is edited by
  hand and never re-synced.** A stale replica reporting confidently is exactly
  the failure `generatedAt` and §3.6 exist to catch.

## Schema — two tables

```sql
CREATE TABLE trackers (
  id TEXT PRIMARY KEY,        -- '<project>.<line>', lower_snake: 'abgi.discovery'
  project TEXT NOT NULL,
  line TEXT,
  shape TEXT NOT NULL,        -- 'A' line | 'B' programme | 'C' narrative
  title TEXT,
  source_path TEXT NOT NULL,  -- pointer to the canon file; never a copy of it
  revision INTEGER,
  generated_at TEXT,
  evidence_baseline TEXT,
  subject_version TEXT,
  payload TEXT NOT NULL,      -- the ENTIRE original JSON, verbatim
  synced_at TEXT NOT NULL
);

CREATE TABLE rows_ (
  tracker_id TEXT NOT NULL,
  ref TEXT NOT NULL,
  kind TEXT NOT NULL,         -- issue | risk | module | decision | next_action | …
  status TEXT,                -- the §2 five, plus 'undef'
  severity TEXT,              -- High | Med | Low
  text TEXT, owner TEXT, note TEXT,
  editable INTEGER NOT NULL,  -- 0 = DERIVED, 1 = EDITABLE (spec v4 §A.1/A.2)
  ord INTEGER,                -- position in the source array, so round-trips stay faithful
  extra TEXT,                 -- JSON for shape-specific fields
  PRIMARY KEY (tracker_id, ref)
);
```

**Both tables, not one, and both earn their place.** `payload` holds the whole
original file so any existing dashboard can be served its exact source
byte-identical — the six-check module grids, the ISSUE/PROBLEM/NEEDED triples,
everything — with no reshaping and therefore no risk to a dashboard that already
works. `rows_` is what makes a pooled surface possible at all: "every open High
across every project" is not a question a blob can answer.

**`(tracker_id, ref)` is the key, so refs only need to be unique per tracker.**
The existing per-line prefix registries already guarantee that. Do not
project-prefix refs to force global uniqueness — an earlier pooled design needed
that and it made every ref uglier for no gain here.

## Shape C — narrative canon

A line whose status lives as prose in `SESSION_STATE.md` with no tracker JSON
gets a `trackers` row with `shape='C'`, zero rows in `rows_`, and a small
payload recording where the prose lives and why there is no tracker:

```json
{"_shape":"C","_narrative":true,"_source":"<path>\\SESSION_STATE.md",
 "_why":"<why this line has no tracker>","_rows":"none by design"}
```

This is what lets a pooled surface list **every** line in the programme without
inventing rows for the ones that have none. A surface that derives its tabs from
the tracker table then covers the whole programme by construction, with nothing
hardcoded — add a tracker and the line appears, remove the last one and it goes.

## Load mode D — dashboard reads the replica

`DASHBOARD_SPEC.md` §3.2 gains a fourth mode alongside live fetch (A), Claude
re-issue (B), and the snapshot fallback (C):

**D — hosted replica.** `TRACKER_SOURCE` points at
`<worker>/api/tracker/<tracker-id>`, which returns the payload verbatim. Nothing
else in the dashboard changes: same parse, same render, same `EMBEDDED`
fallback. Prefer a relative path (`/api/tracker/…`) by serving the dashboard
from the same Worker — a hostname baked into every dashboard file is N things to
fix when it moves.

**A and C are still required.** Mode D is a better default source, not a
replacement for the discipline: the fetch can still fail, and when it does the
banner rules apply unchanged. The stamp must say which mode produced what is on
screen — a replica read is not a canon read, and the reader is entitled to know
which they are looking at.

## Sync — the part that actually decays

The replica is only worth having if it tracks the files. Cloudflare cannot read
a Drive folder, so the push comes from a machine holding both:

1. **Claude-in-the-loop (start here).** Whenever Claude edits a tracker it
   re-syncs in the same pass. No new infrastructure, and it fits the existing
   trust boundary rather than adding one — every tracker already declares
   `maintainer: Claude`, and §3.1 already says writes happen only through
   Claude. Gap: a hand-edit outside that path won't sync until Claude next
   touches the file.
2. **A sync script on demand or on a schedule.** Closes the hand-edit gap.
3. **File-watch automation.** Most moving parts, most to go wrong. Not worth it
   until 1 and 2 have proven the shape.

`synced_at` on every `trackers` row is what makes staleness visible. A surface
reading the replica should show it next to `generatedAt`, because they answer
different questions: when the file was last written, versus when the replica
last caught up.

## Extraction gotcha, learned the hard way

**Tracker sections mix positional-array and object-form rows in the same
array.** A loader that array-destructures every row will throw on the object
ones — this is a real, logged defect (CRA_Online issue I24, which records
dashboards breaking on exactly this), and a first pass at the D1 loader hit it
immediately.

Handle both forms. Normalising into `rows_` also fixes the class of bug
permanently for everything downstream, which is a quiet second reason the
normalised table earns its keep.

## Studio obligations

When a studio scaffolds trackers (Phase 1) or builds the dashboard set
(Phase 4), and the project has a hosted replica:

- register every tracker in `trackers`, including shape-C rows for lines that
  have only narrative canon — a line missing from the table is invisible to
  every pooled surface;
- keep `id` as `<project>.<line>` in lower_snake, consistently: a pooled table
  joins on it, and a hyphen where the rest of the set uses an underscore
  produces an orphan that silently joins to nothing;
- point new dashboards at mode D, and say so in the stamp;
- state the sync mechanism in the project's `SESSION_STATE.md`, so the next
  session knows whether the replica can be trusted.
