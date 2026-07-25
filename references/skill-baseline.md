# Skill baseline — mandatory in every generated skill

Two blocks and one checklist. Every skill the studio authors carries them, and
the studio enforces them on its own growth: a skill missing any element **fails
creation review**, and the tracker raises it as an issue rather than letting it
install.

## 1. The work loop

`DRAFT → VERIFY → PROOF → REVISE → REGISTER`

No one-shot deliverables on anything canon-affecting.

- **DRAFT** — produce the smallest reviewable unit (one module, one content
  slice, one page set, one model, one gate report). Not the whole artefact.
- **VERIFY** — run this skill's own checks: canon diff, counts and ranges,
  tests or golden files, style gate, or a live rule fetch, whichever the skill
  defines. The skill states its checks explicitly; "looks right" is not a check.
- **PROOF** — owner review for content, visual, and commercial outputs, via the
  dashboard trio, numbered feedback, or a rendered proof. Outputs that are
  purely machine-verifiable (passing tests, format conversions) may skip
  straight to REGISTER.
- **REVISE** — surgical fixes to the findings only. Never rebuild the whole
  artefact for a local fix; this is the modular rule applied to everything.
- **REGISTER** — the canon write-back: tracker, decision log, version
  registration.

The loop repeats until gates pass **and**, where acceptance is required, the
owner has explicitly accepted. It exits nowhere else.

## 2. MCP-first

Use connected tools before manual workarounds:

- the canon store's own connector for every canon read and write
- vendor documentation tools for that vendor's platform facts
- web search/fetch for anything that must be live-verified — policies, standard
  editions, prices, platform rules

If a needed capability has no connected tool, search the connector registry and
surface connect options to the owner. Never hand-roll an integration, and never
answer from memory on a fact that a connected tool could verify.

## 3. New-skill baseline checklist

Any new skill — from a gap scan, an owner request, or a dashboard install
prompt — ships with all five:

1. **Frontmatter** with a pushy description and an argument-hint, so it is
   slash-command ready and actually triggers.
2. **Canon consistency & write-back** section: what it reads before, which style
   or format gate it passes, what it writes after, with concrete IDs or paths.
3. **Work loop & MCP use** section (§1 and §2 above).
4. **Dashboard integration**: its outputs raise decision cards or suggested
   activities carrying the EXPLAIN/PROCEED/IMPROVE trio, and it registers itself
   in the tracker's `skills` list on install.
5. **An explicit tunable vs locked boundary**, and where it gates, whether it
   *reports* or *fixes*. A skill that could silently change a locked value is
   not finished.

## 4. Install boundary

Claude cannot install a skill into the owner's account. A `REINSTALL` status is
therefore an instruction to Claude to **re-present the packaged skill file** so
the owner can tap Save — not a state Claude can clear itself. Never mark a skill
installed on the owner's behalf.
