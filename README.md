# project-skill-studio

A meta-skill for Claude that turns any project into a **skill studio**: a versioned suite of project-specific skills plus a tracking discipline, so work on a project is repeatable, canon-compliant, and resumable across sessions.

Generalised from a real production pattern (a card-game design studio that grew to 20+ skills across three classes). The pattern, not any one project, is what's encoded here.

## What it does

Point it at a project and it will:

- **Interview** the project (pulling from chat context, connected tools, and past sessions first — asking you only what it can't find)
- **Design a skill roster**: one canon skill (locked sources of truth), one build skill per *active* delivery line, plus studio-ops skills (tracker, QA, etc.) — never speculative skills for platforms that aren't real yet
- **Author and package** each skill as a `.skill` file, using Anthropic's `skill-creator`
- **Scaffold trackers**: `SESSION_STATE.md`, `PROJECT_TRACKER.json`, a decision log, and (optionally) a plain black-and-white sync dashboard
- **Bake in working rules** into every generated skill: canon discipline, decision logging with staleness propagation, modular re-authoring instead of rebuilds, proof gates on visual output, defensive tool-connection checks

## Install

### Claude.ai
Settings → Capabilities → Skills → Upload → select `project-skill-studio.skill` (built via `skill-creator`'s `package_skill.py`, or download the release asset from this repo).

### Claude Code
Copy this folder into your skills directory:
```bash
cp -r project-skill-studio ~/.claude/skills/
# or, for a single repo:
cp -r project-skill-studio /path/to/repo/.claude/skills/
```

Follows the open [Agent Skills](https://www.anthropic.com/news/skills) format — portable to any tool that adopts the standard.

## Use

Just describe your project and ask for a skill studio:

> "Run project skill studio on my [project name] — [one-line description]."

It will interview you (short selection prompts, not an essay), propose a roster for your confirmation, then build and package the suite.

If you already have a studio pattern from another project, say so — it will search for and carry over conventions explicitly rather than starting from scratch.

## Structure

```
project-skill-studio/
├── SKILL.md                              # main workflow
└── references/
    ├── intake.md                         # intake question set
    ├── session-state-template.md         # SESSION_STATE.md template
    ├── tracker-schema.md                 # PROJECT_TRACKER.json schema
    ├── generated-skill-template.md       # skeleton every generated skill follows
    ├── working-rules.md                  # working-rule set embedded in generated skills
    └── dashboard-standard.md             # dashboard spec + interaction standard
```

## Requires

- Anthropic's `skill-creator` skill (for authoring/packaging test cases and `.skill` files) — install it alongside this one.

## License

[CC0-1.0](LICENSE) — public domain dedication. Use it, fork it, adapt it, no attribution required.

## Changelog

See [CHANGELOG.md](CHANGELOG.md).
