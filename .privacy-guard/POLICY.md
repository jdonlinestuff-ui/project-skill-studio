# Privacy policy for this public repo

This repo is public. Anything committed is permanent — cloned, cached, and indexed within
minutes, and unrecoverable after the fact. The `privacy-guard` scan (local hooks + the CI
workflow) enforces the rules below; the CI check is the one that must pass before anything is
trusted as safe to publish.

## Rules

1. **No personal data.** No real names, emails, usernames, or anything that identifies a person
   — in content, sample data, commit messages, or notes.
2. **No confidential vocabulary.** No real project, programme, client, or product names; no canon
   filenames or internal identifiers. These live in `.privacy-guard/patterns.json` → `denylist`;
   keep it current for this repo.
3. **No secrets.** No API keys, tokens, or private keys — ever. Use environment variables and a
   secrets manager.
4. **No absolute local paths.** No `C:\Users\…`, `/Users/…`, `/home/…` machine paths.
5. **Sample and demo data must be synthetic.** This is where leaks happen: real canon gets pasted
   into "sample" trackers or reference-build `EMBEDDED` snapshots. Demo data uses neutral,
   invented values — never a copy of real production data.

## When the scan flags something

Run the `pre-publish-privacy-guard` **scrub** workflow: it shows a numbered table and you choose
what to obfuscate, what's genuinely fine (allowlisted), or cancel. A legitimately-public match
(a placeholder, a deliberate origin mention) goes in the `allowlist`; everything else gets a
synthetic replacement before it's committed.

## Adding a rule

Edit `.privacy-guard/patterns.json` — `denylist` for a literal term (with a sensible synthetic
`replace`), `rules` for a regex pattern. See the skill's `references/obfuscation.md`.
