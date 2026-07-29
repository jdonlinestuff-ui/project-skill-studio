#!/usr/bin/env node
/*
 * pre-publish-privacy-guard — zero-dependency scanner
 *
 * Finds personal / confidential / secret data before it reaches a public repo.
 * It is deterministic tooling: it reports findings and PROPOSES obfuscations.
 * The human review gate (which findings to scrub) lives in SKILL.md, not here.
 *
 * Usage:
 *   node scan.mjs scan  [--all | --staged | --range A..B | <files...>] [--json] [--out F] [--config C] [--no-fail]
 *   node scan.mjs apply --select all|1,3,5  [--findings F] [--config C]
 *   node scan.mjs allow --select 1,3,5      [--findings F] [--config C]
 *
 * Exit codes (scan): 0 = clean, 1 = findings (so hooks/CI block), 2 = error.
 */
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { execSync } from 'node:child_process';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

const TEXT_EXT = new Set(['.md','.markdown','.txt','.html','.htm','.json','.jsonc','.js','.mjs','.cjs',
  '.ts','.tsx','.jsx','.py','.rb','.go','.rs','.java','.cs','.php','.sh','.bash','.yml','.yaml','.toml',
  '.ini','.cfg','.css','.scss','.svg','.xml','.csv','.env','.tsv','.sql','.gitignore','.gitattributes']);

function die(msg){ console.error('privacy-guard: ' + msg); process.exit(2); }

/* ---------- config ---------- */
function loadConfig(cliPath){
  const candidates = [
    cliPath,
    path.join(process.cwd(), '.privacy-guard', 'patterns.json'),
    path.join(process.cwd(), 'privacy-patterns.json'),
    path.join(__dirname, '..', 'assets', 'patterns.json'), // bundled default
  ].filter(Boolean);
  let found = null;
  for (const c of candidates){
    try { if (fs.existsSync(c)) { found = { cfg: JSON.parse(fs.readFileSync(c,'utf8')), path: c }; break; } }
    catch(e){ die('bad config ' + c + ': ' + e.message); }
  }
  if (!found) die('no patterns.json found (looked in .privacy-guard/, cwd, bundled default)');
  // Merge an optional local, GITIGNORED denylist so the sensitive vocabulary is never
  // committed to the (public) repo. Local hooks read it from disk; CI restores it from a secret.
  const localPath = path.join(path.dirname(found.path), 'denylist.local.json');
  if (fs.existsSync(localPath)){
    try {
      const loc = JSON.parse(fs.readFileSync(localPath,'utf8'));
      found.cfg.denylist  = [...(found.cfg.denylist||[]),  ...(loc.denylist||[])];
      found.cfg.allowlist = [...(found.cfg.allowlist||[]), ...(loc.allowlist||[])];
    } catch(e){ die('bad denylist.local.json: ' + e.message); }
  }
  return found;
}

/* ---------- file selection ---------- */
function git(args){ return execSync('git ' + args, { encoding:'utf8', stdio:['pipe','pipe','pipe'] }); }
function inGitRepo(){ try { git('rev-parse --is-inside-work-tree'); return true; } catch { return false; } }

function selectFiles(mode, rest){
  let files = [];
  if (rest.length) files = rest;
  else if (mode === 'staged') files = git('diff --cached --name-only --diff-filter=ACM').split('\n');
  else if (mode === 'range') files = git('diff --name-only --diff-filter=ACM ' + rest0Range).split('\n');
  else if (mode === 'all' && inGitRepo()) files = git('ls-files').split('\n');
  else { // walk cwd (non-git)
    const out = [];
    (function walk(d){ for (const e of fs.readdirSync(d,{withFileTypes:true})){
      if (e.name === '.git' || e.name === 'node_modules') continue;
      const p = path.join(d, e.name);
      if (e.isDirectory()) walk(p); else out.push(path.relative(process.cwd(), p));
    }})(process.cwd());
    files = out;
  }
  return files.map(f => f.trim()).filter(Boolean)
    .filter(f => !/(^|\/)\.privacy-guard\//.test(f.replace(/\\/g,'/'))) // never scan the guard's own config/scanner
    .filter(isTextFile);
}
let rest0Range = '';

function isTextFile(f){
  const ext = path.extname(f).toLowerCase();
  if (ext && !TEXT_EXT.has(ext)) return false;
  try {
    const buf = fs.readFileSync(f);
    if (buf.includes(0)) return false;            // null byte → binary
    if (buf.length > 3_000_000) return false;      // skip huge files
    return true;
  } catch { return false; }
}

/* ---------- allowlist ---------- */
function makeAllow(list){
  const exact = new Set(), regexes = [];
  for (const a of (list||[])){
    if (typeof a === 'string' && a.startsWith('re:')) { try { regexes.push(new RegExp(a.slice(3))); } catch{} }
    else exact.add(String(a));
  }
  return (text) => exact.has(text) || regexes.some(r => r.test(text));
}

/* ---------- scanning (line-based: bounds regex input, fast, exact offsets) ---------- */
const MAX_LINE = 5000; // cap regex work on pathological minified lines
function compileRules(cfg){
  return (cfg.rules||[]).map(r=>{
    let re; try { re = new RegExp(r.regex, (r.flags||'').includes('g') ? r.flags : (r.flags||'')+'g'); } catch { re = null; }
    return re && { r, re, allow: makeAllow(r.allow) };
  }).filter(Boolean);
}
function compileDenies(cfg){
  return (cfg.denylist||[]).filter(d=>d.term).map(d=>{
    const esc = d.term.replace(/[.*+?^${}()|[\]\\]/g,'\\$&');
    const pat = d.word ? '\\b' + esc + '\\b' : esc;
    let re; try { re = new RegExp(pat, d.caseSensitive ? 'g' : 'gi'); } catch { re = null; }
    return re && { d, re };
  }).filter(Boolean);
}
function scanFile(file, rules, denies, isAllowed){
  let content; try { content = fs.readFileSync(file,'utf8'); } catch { return []; }
  const hits = [];
  const lines = content.split('\n');
  let base = 0;
  for (let li = 0; li < lines.length; li++){
    const line = lines[li];
    const lineBase = base;
    base += line.length + 1; // + '\n'
    if (!line) continue;
    const target = line.length > MAX_LINE ? line.slice(0, MAX_LINE) : line;
    const ctx = line.length > 160 ? line.trim().slice(0,157)+'…' : line.trim();
    const push = (m, category, ruleId, replace) => {
      const text = m[0];
      hits.push({ file, line: li+1, col: m.index+1, start: lineBase+m.index, end: lineBase+m.index+text.length,
                  text, category, ruleId, replace, context: ctx });
    };
    for (const {r, re, allow} of rules){
      re.lastIndex = 0; let m;
      while ((m = re.exec(target)) !== null){
        if (!m[0]){ re.lastIndex++; continue; }
        if (isAllowed(m[0]) || allow(m[0])) continue;
        push(m, r.category||'confidential', r.id, r.replace ?? placeholderFor(r.category));
      }
    }
    for (const {d, re} of denies){
      re.lastIndex = 0; let m;
      while ((m = re.exec(target)) !== null){
        if (isAllowed(m[0])) continue;
        push(m, d.category||'confidential', d.id||('deny:'+d.term), d.replace ?? placeholderFor(d.category));
      }
    }
  }
  return hits;
}
function placeholderFor(cat){
  return ({ PII:'[REDACTED]', secret:'[REDACTED-SECRET]', 'local-path':'<PATH>', confidential:'[REDACTED]' })[cat] || '[REDACTED]';
}
// drop findings fully contained inside another finding in the same file (first rule wins)
function dedupe(hits){
  hits.sort((a,b)=> a.file.localeCompare(b.file) || a.start-b.start || (b.end-b.start)-(a.end-a.start));
  const kept = [];
  for (const h of hits){
    const prev = kept[kept.length-1];
    if (prev && prev.file===h.file && h.start < prev.end) continue; // overlap
    kept.push(h);
  }
  return kept;
}

/* ---------- rendering ---------- */
function table(findings){
  if (!findings.length) return 'No findings — clean.';
  const rows = findings.map((f,i)=>[String(i+1), f.category, f.file+':'+f.line, trunc(f.text,42), trunc(f.replace,22)]);
  const head = ['#','CATEGORY','LOCATION','MATCH','→ PROPOSED'];
  const w = head.map((h,c)=> Math.max(h.length, ...rows.map(r=>r[c].length)));
  const fmt = r => r.map((c,i)=> c.padEnd(w[i])).join('  ');
  return [fmt(head), w.map(x=>'-'.repeat(x)).join('  '), ...rows.map(fmt)].join('\n');
}
function trunc(s,n){ s=String(s).replace(/\s+/g,' '); return s.length>n ? s.slice(0,n-1)+'…' : s; }

/* ---------- apply / allow ---------- */
function parseSelect(sel, n){
  if (!sel) die('--select required (all | 1,3,5)');
  if (sel === 'all') return [...Array(n).keys()];
  return sel.split(',').map(s=>parseInt(s.trim(),10)-1).filter(i=>i>=0 && i<n);
}
function applyFindings(findings, idxs){
  const byFile = new Map();
  idxs.forEach(i => { const f=findings[i]; if(!byFile.has(f.file)) byFile.set(f.file,[]); byFile.get(f.file).push(f); });
  let changed = 0;
  for (const [file, fs2] of byFile){
    let content = fs.readFileSync(file,'utf8');
    fs2.sort((a,b)=> b.start - a.start); // right-to-left so offsets stay valid
    for (const f of fs2){
      if (content.slice(f.start, f.end) !== f.text) { console.error('  ! skipped '+file+':'+f.line+' (content moved; re-scan)'); continue; }
      content = content.slice(0,f.start) + f.replace + content.slice(f.end);
      changed++;
    }
    fs.writeFileSync(file, content);
  }
  return changed;
}
function addAllow(findings, idxs, cfgPath){
  const cfg = JSON.parse(fs.readFileSync(cfgPath,'utf8'));
  cfg.allowlist = cfg.allowlist || [];
  let added = 0;
  for (const i of idxs){ const t = findings[i].text; if (!cfg.allowlist.includes(t)){ cfg.allowlist.push(t); added++; } }
  fs.writeFileSync(cfgPath, JSON.stringify(cfg,null,2)+'\n');
  return added;
}

/* ---------- main ---------- */
const [,, cmd, ...args] = process.argv;
function opt(name){ const i=args.indexOf(name); return i>=0 ? args[i+1] : undefined; }
function flag(name){ return args.includes(name); }
const positional = args.filter((a,i)=> !a.startsWith('--') && !(i>0 && args[i-1].startsWith('--') && ['--config','--out','--select','--findings','--range'].includes(args[i-1])));

const { cfg, path: cfgPath } = loadConfig(opt('--config'));
const isAllowed = makeAllow(cfg.allowlist);

if (cmd === 'scan'){
  let mode = 'all';
  if (flag('--staged')) mode = 'staged';
  else if (opt('--range')) { mode = 'range'; rest0Range = opt('--range'); }
  const files = positional.length ? positional : selectFiles(mode, positional);
  const rules = compileRules(cfg), denies = compileDenies(cfg);
  let findings = [];
  for (const f of files) findings.push(...scanFile(f, rules, denies, isAllowed));
  findings = dedupe(findings);
  const out = opt('--out');
  if (out) fs.writeFileSync(out, JSON.stringify(findings,null,2));
  if (flag('--json')) process.stdout.write(JSON.stringify(findings,null,2)+'\n');
  else { console.log(table(findings)); console.log('\n'+findings.length+' finding(s). config: '+path.relative(process.cwd(),cfgPath)); }
  process.exit(findings.length && !flag('--no-fail') ? 1 : 0);
}
else if (cmd === 'apply' || cmd === 'allow'){
  const ffile = opt('--findings') || '.privacy-guard/findings.json';
  if (!fs.existsSync(ffile)) die('findings file not found: '+ffile+' (run `scan --out '+ffile+'` first)');
  const findings = JSON.parse(fs.readFileSync(ffile,'utf8'));
  const idxs = parseSelect(opt('--select'), findings.length);
  if (cmd === 'apply'){ const n = applyFindings(findings, idxs); console.log('privacy-guard: obfuscated '+n+' finding(s). Re-run scan to confirm.'); }
  else { const n = addAllow(findings, idxs, cfgPath); console.log('privacy-guard: added '+n+' entry(ies) to allowlist in '+path.relative(process.cwd(),cfgPath)); }
}
else {
  console.log('usage: node scan.mjs scan|apply|allow  (see header of this file)');
  process.exit(cmd ? 2 : 0);
}
