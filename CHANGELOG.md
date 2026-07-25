# Changelog

All notable changes to this skill are documented here.

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
