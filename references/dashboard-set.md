# The dashboard set — three surfaces, one source

A studio run emits **three dashboards, not one**. They are three audiences reading the
same trackers, not three copies of the data: every surface derives from the per-line
tracker JSONs described in `tracker-schema.md`, and none of them is a source of truth.

| # | Surface | Answers | Read by |
|---|---|---|---|
| 1 | **Skill builder** (skills-creation) | what skills exist, which are stale, what installs next | whoever maintains the studio |
| 2 | **Facilitator** | how do I run the thing right now, and what's broken today | whoever is operating the project live |
| 3 | **Resources** | what exists, what state is it in, where does it live | anyone orienting on the project |

Build them in that order. The Skill builder is the one that tracks the studio's own growth,
so it exists before the surfaces that describe the work.

## 1. Skill builder — the existing behaviour

The standard tracker shell, built to `DASHBOARD_SPEC.md` in full: live fetch, the module
grid, the EXPLAIN/PROCEED/IMPROVE trio, CREATE PROMPT, the four schemes. Its rows are the
studio's own skills — roster, class, install state, and a staleness verdict per skill.

Nothing about this surface changes with this feature. It is listed here because a set of
three needs all three named in one place.

Its most valuable column is the staleness verdict, and it is only honest if it is derived:
a skill is stale when it asserts something canon has since changed, and the note says which
claim and which canon fact. "Looks fine" is not a verdict.

## 2. Facilitator — the live-operation surface

**What it is for**: someone is running the project *right now* — a workshop, a session, a
production run — and needs the operating rules and today's known breakage in front of them.
It is a briefing card, not a tracker.

Contents, all derived:

- **The operating sequence** — rounds, phases, stages, whatever the project's live run
  actually is, in order, with what happens at each step.
- **Quick reference** for the rules that get asked mid-session: scoring, thresholds,
  win/loss conditions, the ones people look up rather than remember.
- **Exception reference** — the non-standard events the operator can trigger, and what each
  does.
- **Actions available to the operator**, listed plainly.
- **Known issues, filtered live from the defect register** (`DASHBOARD_SPEC.md` §4h): open
  defects whose `foundIn` is the current `subjectVersion`, each with its ref, so an operator
  hitting one mid-session can name it rather than improvise. This panel is the reason the
  defect register and this dashboard shipped together — a numbered ticket nobody can see
  during the session it affects may as well not exist.

**It states its own staleness.** A facilitator surface is read under time pressure by
someone who cannot check whether it is current, so it carries a plain stamp — the subject
version it describes, the date, and whether it is live or a snapshot — and says
`Not live-synced` in words when it is a snapshot. This is not optional politeness; an
operating reference that is silently a week old is worse than none.

## 3. Resources — the orientation surface

**What it is for**: someone needs to know what this project consists of and where things
are. New collaborator, returning owner, anyone deciding what to pick up.

Contents, all derived:

- **What exists, by line**, with each item's version and state — locked, draft, in progress,
  cancelled.
- **Version skew, called out** — anything trailing what it should track gets a visible mark
  and how far behind it is. This is the same instinct as `§3.6`'s evidence baseline, applied
  to deliverables rather than marks.
- **The tracker and dashboard inventory** — every tracker, what it covers, and any that are
  retired, so nobody opens a superseded one and believes it.
- **Open decisions** awaiting the owner, with their D refs.
- **Where canon lives** — the canon root, the memory tiers (`memory-tiers.md`), and which
  file to read first in a new session.

The last point is what makes this surface worth building: it is the one page that answers
"where do I start" without a conversation.

## Conformance — pooled, interactive, and still bound by the honesty rules

The Facilitator and Resources surfaces are **pooled derived views** (`DASHBOARD_SPEC.md`
§13): every row is gathered from another tracker rather than authored here, but that does
not make the surface read-only. As of spec v3.4, both carry the full interactive
machinery — this reverses the original "exempt from controls" rule below, kept here with
the reason it changed rather than silently dropped:

The original rule exempted both surfaces from the action trio, CREATE PROMPT and the
prompt protocol, the four-scheme switcher, and the sticky control bar, reasoning that a
surface with no write-back loop had no need for the machinery that serves one. Real use
showed the opposite: marking rows pooled from every line and compiling them into one
CREATE PROMPT hand-off is exactly what a facilitator or resourcing review is *for* — the
single action that makes opening either surface mid-meeting worth it. A briefing card that
cannot mark anything is a worse fit for that moment than the standard tracker shell it was
meant to simplify.

**Carried, same as the shell**: the action trio, CREATE PROMPT and the prompt protocol
(§5), the scheme switcher, the sticky control bar.

**Added, specific to a pooled surface**: a click-to-scope index (one row per tracker or
per project line; click to filter every section below to it, click again to clear),
independent dropdown filters (by tracker/program, by owner/person), and free-text search —
all composable. `references/facilitator-hub-reference.html` is the canonical shell for
both surfaces.

**Not exempt from anything, and these were never negotiable:**

- **Status vocabulary** (§2) — glyph, word and tint travel together; the word is what
  survives greyscale and colour-blindness. A red dot on a facilitator page is a defect.
- **Evidence discipline** (§3.5) — no note means no claim; nothing reads `pass` on intent.
- **Derived, never stored** (§3.5) — counts and totals computed from the tracker, never
  typed. A hand-typed "19 open bugs" is wrong the day after it is written.
- **The freshness stamp and the evidence baseline** (§3.4, §3.6) — including the explicit
  snapshot wording above.
- **Print rules** (§10) — the facilitator surface in particular is often printed or held on
  a second screen, and must stay legible in greyscale.

A pooled surface that scopes and filters its data differently from a single-line tracker
is still a conformant derived view. One that drops the honesty rules is a poster, whether
or not it has buttons on it — the controls were never the part actually protecting the
reader.

## Regeneration

All three are regenerated from the trackers, never hand-edited. Editing a dashboard to
correct a fact is the failure this whole discipline exists to prevent: fix the tracker,
re-emit the set. When only one surface's data has changed, re-emit that one — the set is
three files, not one bundle.

## Hosting as live artifacts — ask, never assume

**After the set is built, ask the owner whether they want these hosted as live artifacts.
Do not host by default, and do not skip the question.**

Delivered as files, the three dashboards are inert: they open locally, they show what the
tracker said when they were emitted, and nothing they contain can act.

Hosted as live artifacts, three things become true that were not true before, and each is
a real consequence rather than a feature bullet:

1. **The page is reachable by whoever holds the link.** Its contents — issue text, defect
   notes, budget lines, people rows — leave the owner's own storage. Some of that is
   ordinarily private, and a facilitator surface listing today's breakage is not always
   something a project wants circulated.
2. **The page becomes an action channel.** The write-back path (§5) means marks made in the
   page compile into a prompt that changes canon when pasted. That path is deliberately
   manual: the owner prompts, reviews the compiled block, and explicitly agrees before
   anything is written. Hosting does not make it automatic, and nothing in this spec ever
   writes to canon without that step — but the channel now exists where it did not, and
   the owner should be choosing it knowingly.
3. **It has to be maintained.** A hosted page that stops being re-emitted is a stale page
   with a URL, which travels further and is trusted more than a stale file on a disk.

Ask as a selection prompt, per surface if the answer differs — a project may well want
Resources shared and Facilitator kept local:

> Host these as live artifacts? **(a)** all three, **(b)** name which ones, **(c)** no —
> deliver as files. Live means: reachable by link, and the sync path becomes available
> (you still prompt and approve every write). Files are inert and local.

Record the answer as a logged decision, with the date and which surfaces it covered. It is
a scope and disclosure choice, and the next session should not have to re-ask or guess.

If the answer is yes, `DASHBOARD_SPEC.md` §12 governs *how* — the regular-artifact path,
not a Cowork live artifact, unless the owner explicitly wants Cowork's connector-refresh
behaviour and accepts losing website embedding for it.

If the answer is no, say plainly what was delivered instead and where the files are. "No"
is a complete answer and does not need a follow-up pitch.
