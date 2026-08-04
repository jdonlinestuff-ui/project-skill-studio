#!/usr/bin/env node
/**
 * Generate the distributable spec copies from canon.
 *
 * Canon lives on Drive and is written with the real client vocabulary, because a
 * spec full of "Example Project" is harder to read and harder to keep true. This
 * repo is PUBLIC, so it carries a scrubbed derivative instead.
 *
 * That derivative used to be maintained by hand, which is why it drifted seven
 * versions behind (v3.5 against canon's v3.12): anything skilled up from it built
 * a dashboard with no --rule token, no <details> sections and the wrong default
 * scheme. Hand-maintenance was the problem, not the scrub — the mapping has been
 * decided and stable for weeks. So the copy is generated.
 *
 *   node tools/scrub-canon.mjs            # write references/
 *   node tools/scrub-canon.mjs --check    # exit 1 if references/ is stale
 *
 * The mapping is .privacy-guard/denylist.local.json, which is GITIGNORED and must
 * stay that way — it is the list of real terms, so publishing it would defeat the
 * scrub it drives.
 */
import { readFileSync, writeFileSync, existsSync } from "node:fs";
import { join, dirname } from "node:path";
import { fileURLToPath } from "node:url";

const ROOT = join(dirname(fileURLToPath(import.meta.url)), "..");
const CANON = process.env.PROTECT_SPEC || "G:\\My Drive\\Protect\\dashboards\\_spec";
const FILES = ["DASHBOARD_SPEC.md", "tracker-schema.md", "dashboard-set.md", "d1-replica.md"];

const denyPath = join(ROOT, ".privacy-guard", "denylist.local.json");
if (!existsSync(denyPath)) {
  console.error(`FATAL no denylist at ${denyPath}\n` +
    "  Refusing to generate: without the mapping this would copy canon verbatim\n" +
    "  into a public repo, which is exactly what the scrub exists to prevent.");
  process.exit(1);
}
const { denylist } = JSON.parse(readFileSync(denyPath, "utf8"));
if (!Array.isArray(denylist) || !denylist.length) {
  console.error("FATAL denylist is empty — refusing to generate.");
  process.exit(1);
}

const esc = (s) => s.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
// Longest term first, so a two-word term is not half-eaten by a shorter rule
// that matches inside it. (No example here on purpose: this file is public, and
// the guard rightly blocked an earlier draft that used a real term to explain
// how real terms get removed.)
const rules = [...denylist].sort((a, b) => b.term.length - a.term.length).map((d) => ({
  ...d,
  re: new RegExp(d.word ? `\\b${esc(d.term)}\\b` : esc(d.term), d.caseSensitive ? "g" : "gi"),
}));

const check = process.argv.includes("--check");
let stale = 0, total = 0;

for (const f of FILES) {
  const src = join(CANON, f);
  if (!existsSync(src)) { console.error(`  MISSING in canon: ${f}`); process.exitCode = 1; continue; }
  let text = readFileSync(src, "utf8");
  const hits = [];
  for (const r of rules) {
    const n = (text.match(r.re) || []).length;
    if (n) { hits.push(`${r.term}->${r.replace} x${n}`); total += n; }
    text = text.replace(r.re, r.replace);
  }
  const dest = join(ROOT, "references", f);
  const prev = existsSync(dest) ? readFileSync(dest, "utf8") : null;
  const changed = prev !== text;
  if (check) {
    if (changed) { console.error(`  STALE  ${f}`); stale++; }
    else console.log(`  ok     ${f}`);
  } else {
    if (changed) writeFileSync(dest, text, "utf8");
    console.log(`  ${changed ? "wrote " : "same  "} ${f}  ${hits.length ? "(" + hits.join(", ") + ")" : "(no terms found)"}`);
  }
}

if (check && stale) {
  console.error(`\n${stale} file(s) stale — run: node tools/scrub-canon.mjs`);
  process.exit(1);
}
if (!check) console.log(`\n${total} replacement(s) applied across ${FILES.length} file(s).`);
