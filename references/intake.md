# Intake — Project Profile

Goal: fill the profile with minimum owner burden. Order of evidence:
1. Current conversation + project files
2. Connected tools (Drive search, repo listing) — look for existing SESSION_STATE.md, trackers, canonical folders
3. Past-chat search (conversation_search) for prior conventions
4. Only then: ask the owner, using selection prompts (2–4 options each), max ~3 questions per turn

## Question set

**Identity**
- Project name; short prefix for skill names (2–4 letters, lowercase, e.g. `cra-`)
- Sole owner or team? (Team → consider plugin packaging later; sole owner → .skill files only)

**Canon**
- Where does canon live? (Drive folder / git repo / local folder / "nowhere yet — create it")
- What are the single sources of truth? (data files, style specs, scoring sheets, brand tokens)
- Which of these are LOCKED (never change silently) vs DESIGN-CONTROLLED (change via logged decision, with affected tracker rows re-marked and the decision id cited)?
- Does a second memory tier already exist — a coding agent's project-memory file, a condensed per-line state file? If so, what does each own, and which wins on a version-specific fact? (`memory-tiers.md`)
- What version vocabulary does each line's subject use (`v0.20`, `v6`, a date)? That becomes `evidenceBaseline` / `subjectVersion`.
- Any values that are documented assumptions, not confirmed? → these become the studio's open-questions list

**Lines**
- Which delivery lines are ACTIVE today? (physical product, web app, Teams/Slack app, publishing, marketing, client services…)
- Which are aspirational? → backlog with decision gates, not skills

**Ops**
- Tracker: always yes — one JSON per active delivery line, named for the line.
- Dashboards: the standard set is three (Skill builder, Facilitator, Resources — see `dashboard-set.md`). Confirm the set, and ask what the project's *live operation* actually is, since that's what the Facilitator surface describes (a workshop, a session, a production run, a release procedure — or none, in which case say so and drop it).
- Hosting: ask separately, after the set is built, per surface. Never assume — it exposes the pages by link and opens the write-back channel. Default is files.
- QA/review loop? Playtest/validation loop? Client engagement lifecycle? Tuning/balancing?

**Tools**
- Which connectors does the project use, and what quirks have been learned? Seed defaults for Google Drive if used:
  - `textContent` reliable to ~17 KB; `base64Content` truncates ~5 KB (unusable for binaries)
  - Binary delivery via present_files zips, not Drive upload
  - No delete tool — owner cleans stale files manually
  - Search folder contents with query `parentId = '<folder-id>'`
  - Check `canAddChildren` before uploading to a folder
  These are examples of the *kind* of constraint to capture; verify per project rather than assuming.

**Cadence**
- Owner's working style (terse/momentum vs discursive)? Default to the studio standard: selection prompts, no preamble, surgical fixes.
