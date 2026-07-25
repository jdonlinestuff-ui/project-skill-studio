# PROJECT_TRACKER.json schema

The JSON is the single truth; any dashboard HTML is a regenerated view of it.

```json
{
  "project": "string",
  "prefix": "string",
  "suite_version": "v1",
  "updated": "YYYY-MM-DD",
  "canon": {
    "root": "drive-folder-id | repo-url | path",
    "sources_of_truth": [{"name": "", "id_or_path": "", "locked": true}]
  },
  "skills": [
    {"name": "", "class": "canon|line|ops|orchestrator",
     "role": "one-line scope", "status": "installed|reinstall|draft|parked",
     "improve": "", "notes": ""}
  ],
  "lines": [
    {"name": "", "status": "active|parked|gated", "phase": "", "gate": "decision id if gated"}
  ],
  "items": [
    {"id": "", "line": "", "title": "", "status": "pending|in-progress|done|stale",
     "stale_reason": "", "depends_on": []}
  ],
  "backlog": [{"name": "", "prio": 1, "reason": ""}],
  "decisions": [{"id": "D1", "date": "", "summary": "", "flags_stale": ["item ids"]}],
  "open_questions": [{"id": "Q1", "question": "", "blocks": "", "assumption": ""}]
}
```

Staleness propagation: when a decision changes something design-controlled, every
item listing it in `depends_on` (directly or transitively) flips to `stale` with
`stale_reason` set to the decision id. Stale items surface at the top of the
dashboard and in SESSION_STATE.md until reworked.
