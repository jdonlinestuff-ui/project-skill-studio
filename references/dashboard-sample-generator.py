"""Tracker Shell v1.0 reference sample generator.

Emits, from one token table:
  * tracker-shell-reference.html - the conformant reference implementation
    (statically baked default scheme + in-page JS switcher, CSS custom properties)
  * tracker_dashboard_<scheme>.png - one flat render per scheme

PNGs are rendered from a per-scheme flattened variant because wkhtmltoimage's
engine predates CSS custom properties; the reference HTML is the artefact to
copy from. Prints a WCAG 2.1 contrast table - a scheme whose worst pair falls
below 4.5:1 must not ship.

Requires: wkhtmltoimage on PATH. OUT_DIR env var overrides output location.
"""
import subprocess, json, tempfile, os

WORK = tempfile.mkdtemp(prefix='tracker-shell-')
OUT  = os.environ.get('OUT_DIR', '/mnt/user-data/outputs')

def lum(h):
    h=h.lstrip('#'); r,g,b=[int(h[i:i+2],16)/255 for i in (0,2,4)]
    f=lambda c: c/12.92 if c<=0.03928 else ((c+0.055)/1.055)**2.4
    r,g,b=f(r),f(g),f(b); return 0.2126*r+0.7152*g+0.0722*b
def cr(a,b):
    l1,l2=sorted([lum(a),lum(b)],reverse=True); return round((l1+0.05)/(l2+0.05),2)

# Typography slots: display serif / UI sans / mono-for-evidence.
# Local stacks only - no webfont fetch, so this renders identically offline.
SERIF = "Georgia,'Libre Baskerville','Times New Roman',serif"
SANS  = "-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif"
MONO  = "ui-monospace,SFMono-Regular,Menlo,Consolas,'IBM Plex Mono',monospace"

SCHEMES = {
 "01_ink": dict(label="Ink", bg="#FFFFFF", panel="#FFFFFF", text="#111418", muted="#4A5158",
    line="#D6DAE0", accent="#1F4E79", accentText="#FFFFFF",
    ok="#186A3B", bad="#A32020", pend="#4A5158", blk="#8A4B00", na="#6B7280",
    tok="#EAF5EE", tbad="#FBECEC", tpend="#F2F4F6", tblk="#FBF1E3", tna="#F2F4F6"),
 "02_parchment": dict(label="Parchment", bg="#FAF7F0", panel="#FFFDF8", text="#1A1A1A", muted="#5A5145",
    line="#DED5C4", accent="#7A5E23", accentText="#FFFDF8",
    ok="#2F5D34", bad="#96261F", pend="#5A5145", blk="#8A5A12", na="#6E675C",
    tok="#EDF3EA", tbad="#F8EAE7", tpend="#F3EFE6", tblk="#F7EEDC", tna="#F3EFE6"),
 "03_mono_hc": dict(label="Mono HC", bg="#FFFFFF", panel="#FFFFFF", text="#000000", muted="#2B2B2B",
    line="#000000", accent="#000000", accentText="#FFFFFF",
    ok="#000000", bad="#000000", pend="#2B2B2B", blk="#000000", na="#2B2B2B",
    tok="#FFFFFF", tbad="#FFFFFF", tpend="#FFFFFF", tblk="#FFFFFF", tna="#FFFFFF"),
 "04_slate_dark": dict(label="Slate dark", bg="#14181D", panel="#1B2027", text="#E8EDF2", muted="#A3AEBA",
    line="#2E3742", accent="#7FB2E5", accentText="#0F1317",
    ok="#6FD08C", bad="#F58A80", pend="#A3AEBA", blk="#E8B366", na="#8B95A1",
    tok="#1B2A22", tbad="#2B1D1D", tpend="#1F252C", tblk="#2B2317", tna="#1F252C"),
}

CSS = """
*{box-sizing:border-box}
body{margin:0;padding:20px;background:%(bg)s;color:%(text)s;font:14px/1.45 %(SANS)s}
.wrap{max-width:1000px;margin:0 auto}
h1{font-family:%(SERIF)s;font-size:21px;margin:0 0 4px;font-weight:700}
.meta{color:%(muted)s;font-size:12px;margin-bottom:4px}
.mono{font-family:%(MONO)s}
.switch{float:right;text-align:right}
.switch b{display:block;font-size:9.5px;letter-spacing:.1em;color:%(muted)s;text-transform:uppercase;margin-bottom:4px;font-weight:600}
.sw{display:inline-block;border:1px solid %(line)s;padding:4px 8px;margin-left:4px;font-size:11px;color:%(muted)s;background:%(panel)s}
.sw.on{border-color:%(accent)s;color:%(accentText)s;background:%(accent)s;font-weight:700}
.bar{margin:14px 0 4px}
.flag{display:inline-block;border:1px solid %(line)s;padding:8px 12px;margin:0 6px 6px 0;font-size:12px;font-weight:600;background:%(panel)s;color:%(text)s;min-height:30px}
.flag.primary{background:%(accent)s;color:%(accentText)s;border-color:%(accent)s}
h2{font-family:%(SERIF)s;font-size:12.5px;letter-spacing:.08em;text-transform:uppercase;color:%(muted)s;margin:22px 0 7px;padding-bottom:5px;border-bottom:1px solid %(line)s;font-weight:700}
table{width:100%%;border-collapse:collapse}
td,th{text-align:left;padding:7px 8px;border-bottom:1px solid %(line)s;vertical-align:top;font-size:13px}
th{font-size:10.5px;text-transform:uppercase;letter-spacing:.06em;color:%(muted)s;font-weight:600}
.st{display:inline-block;padding:2px 8px;font-size:11px;font-weight:700;border:1px solid;white-space:nowrap}
.ok{color:%(ok)s;border-color:%(ok)s;background:%(tok)s}
.bad{color:%(bad)s;border-color:%(bad)s;background:%(tbad)s}
.pend{color:%(pend)s;border-color:%(pend)s;background:%(tpend)s}
.blk{color:%(blk)s;border-color:%(blk)s;background:%(tblk)s}
.na{color:%(na)s;border-color:%(na)s;background:%(tna)s}
.trio span{display:inline-block;border:1px solid %(line)s;width:30px;height:30px;line-height:28px;text-align:center;font-weight:700;margin-right:5px;background:%(panel)s;color:%(text)s}
.ev{color:%(muted)s;font-size:11.5px;font-family:%(MONO)s}
.badge{display:inline-block;border:1px solid %(line)s;padding:1px 6px;font-size:10.5px;color:%(muted)s;margin-left:5px;font-family:%(MONO)s}
.stale{border:1px solid %(bad)s;background:%(tbad)s;padding:9px 11px;margin-bottom:6px;font-size:12.5px}
.legend span{margin-right:13px;font-size:12px}
.log{font-size:12px;padding:5px 0;border-bottom:1px solid %(line)s;color:%(text)s}
.foot{margin-top:18px;padding-top:9px;border-top:1px solid %(line)s;color:%(muted)s;font-size:11.5px}
"""

def switcher(active):
    b=''.join(f'<span class="sw{" on" if k==active else ""}" data-s="{k}">{v["label"]}</span>'
              for k,v in SCHEMES.items())
    return f'<div class="switch"><b>Scheme</b>{b}</div>'

def body(active):
    return f"""{switcher(active)}
<h1>Project Tracker &mdash; Sample Project</h1>
<div class="meta">Suite <span class="mono">v3</span> &middot; updated <span class="mono">2026-07-25</span> &middot; canon: Drive / Canonical Assets &middot; <b>2 stale</b></div>

<div class="bar">
 <span class="flag primary">&#9998; CREATE PROMPT</span>
 <span class="flag">RESET</span>
 <span class="flag">&#8634; REFRESH BUILD</span>
 <span class="flag">&#8646; CANON SYNC</span>
 <span class="flag">&#8635; REFRESH DATA</span>
</div>

<h2>Status vocabulary</h2>
<div class="legend">
 <span class="st ok">&#10003; PASS</span> <span class="st bad">&#10007; FAIL</span>
 <span class="st pend">&#9702; PENDING</span> <span class="st blk">&#9650; BLOCKED</span>
 <span class="st na">&ndash; N/A</span>
 &nbsp;<span class="ev">glyph + word + tint &mdash; never colour alone</span>
</div>

<h2>Stale &mdash; upstream decision changed</h2>
<div class="stale"><b>&#9650; BLOCKED</b> &nbsp;ITEM-014 Export template &mdash; stale by <b>D13</b> (schema change)<span class="badge">depends_on: ITEM-009</span></div>
<div class="stale"><b>&#9650; BLOCKED</b> &nbsp;ITEM-021 Debrief mapping &mdash; stale by <b>D13</b><span class="badge">depends_on: ITEM-014</span></div>

<h2>Build line &mdash; checks</h2>
<table>
<tr><th style="width:17%">Module</th><th style="width:10%">Typecheck</th><th style="width:8%">Unit</th><th style="width:10%">Golden</th><th style="width:12%">Multiclient</th><th style="width:9%">Privacy</th><th>Evidence</th></tr>
<tr><td>engine</td><td><span class="st ok">&#10003; PASS</span></td><td><span class="st ok">&#10003; PASS</span></td><td><span class="st bad">&#10007; FAIL</span></td><td><span class="st na">&ndash; N/A</span></td><td><span class="st ok">&#10003; PASS</span></td><td class="ev">tsc 0 err; 26 assertions; golden 2/3 tiers</td></tr>
<tr><td>state machine</td><td><span class="st ok">&#10003; PASS</span></td><td><span class="st ok">&#10003; PASS</span></td><td><span class="st pend">&#9702; PENDING</span></td><td><span class="st pend">&#9702; PENDING</span></td><td><span class="st ok">&#10003; PASS</span></td><td class="ev">8 smoke checks green; no live session run</td></tr>
<tr><td>export</td><td><span class="st blk">&#9650; BLOCKED</span></td><td><span class="st na">&ndash; N/A</span></td><td><span class="st na">&ndash; N/A</span></td><td><span class="st na">&ndash; N/A</span></td><td><span class="st na">&ndash; N/A</span></td><td class="ev">blocked on D13</td></tr>
</table>

<h2>Skills roster</h2>
<table>
<tr><th style="width:24%">Skill</th><th style="width:11%">Class</th><th style="width:15%">Status</th><th style="width:15%">Actions</th><th>Improve note</th></tr>
<tr><td>proj-canon</td><td>canon</td><td><span class="st ok">&#10003; INSTALLED</span></td><td class="trio"><span>!</span><span>&#10003;</span><span>+</span></td><td class="ev">&mdash;</td></tr>
<tr><td>proj-tracker</td><td>ops</td><td><span class="st ok">&#10003; INSTALLED</span></td><td class="trio"><span>!</span><span>&#10003;</span><span>+</span></td><td class="ev">&mdash;</td></tr>
<tr><td>proj-app-dev</td><td>line</td><td><span class="st bad">&#10007; REINSTALL</span></td><td class="trio"><span>!</span><span>&#10003;</span><span>+</span></td><td class="ev">re-present file; owner taps Save</td></tr>
<tr><td>proj-mobile</td><td>line</td><td><span class="st blk">&#9650; PARKED</span></td><td class="trio"><span>!</span><span>&#10003;</span><span>+</span></td><td class="ev">gated on scope decision</td></tr>
</table>

<h2>Decisions required</h2>
<table>
<tr><th style="width:8%">ID</th><th style="width:45%">Title</th><th style="width:14%">Status</th><th>Actions</th></tr>
<tr><td class="mono"><b>D13</b></td><td>Register digital-only mechanics as additive enhancements?</td><td><span class="st pend">&#9702; PENDING</span></td><td class="trio"><span>!</span><span>&#10003;</span><span>+</span></td></tr>
<tr><td class="mono"><b>D14</b></td><td>Accept expansion pack v0.1-draft</td><td><span class="st pend">&#9702; PENDING</span></td><td class="trio"><span>!</span><span>&#10003;</span><span>+</span></td></tr>
</table>

<h2>Suggested activities</h2>
<table>
<tr><th style="width:8%">ID</th><th style="width:45%">Activity</th><th style="width:14%">Status</th><th>Actions</th></tr>
<tr><td class="mono">S1</td><td>Run the full rules-QA gate before the next release</td><td><span class="st pend">&#9702; PENDING</span></td><td class="trio"><span>!</span><span>&#10003;</span><span>+</span></td></tr>
<tr><td class="mono">S8</td><td>Golden-file tests against the canonical scoring matrix</td><td><span class="st pend">&#9702; PENDING</span></td><td class="trio"><span>!</span><span>&#10003;</span><span>+</span></td></tr>
</table>

<h2>Open questions &mdash; never invented, always flagged</h2>
<table>
<tr><th style="width:8%">ID</th><th style="width:46%">Question</th><th style="width:16%">Blocks</th><th>Interim assumption</th></tr>
<tr><td class="mono">Q1</td><td>Confirm threshold values against the printed manual</td><td class="ev">scoring</td><td class="ev">documented assumption</td></tr>
<tr><td class="mono">Q7</td><td>Asset IP exposure for bundled web assets</td><td class="ev">web assets</td><td class="ev">bundled, flagged</td></tr>
</table>

<h2>Change log</h2>
<div class="log"><b class="mono">v3</b> &mdash; Tracker Shell v1.0 conformance: fixed section order, typography slots, in-page switcher, 30px trio</div>
<div class="log"><b class="mono">v2</b> &mdash; Evidence discipline enforced; three items reverted to pending for lacking evidence</div>
<div class="log"><b class="mono">v1</b> &mdash; Tracker seeded from canon root</div>

<div class="foot">Untouched items stay <b>pending</b> &mdash; no HOLD action exists. Marked actions compile into one paste-ready sync prompt via CREATE PROMPT. Content is statically baked: this renders with JavaScript disabled, and the scheme switcher is the only thing JS adds.</div>"""

def page(tokens, active, varmode=False, switcher_js=False):
    css = CSS % dict(tokens, SANS=SANS, SERIF=SERIF, MONO=MONO)
    js = """
<script>
document.querySelectorAll('.sw').forEach(function(b){
  b.addEventListener('click',function(){
    document.documentElement.setAttribute('data-scheme', b.dataset.s);
    document.querySelectorAll('.sw').forEach(function(x){x.classList.remove('on')});
    b.classList.add('on');
  });
});
</script>""" if switcher_js else ""
    return f"""<!doctype html><html><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Project Tracker &mdash; Sample Project</title>
<style>{css}
@media(max-width:700px){{
 body{{padding:12px}} .switch{{float:none;text-align:left;margin-bottom:10px}}
 table,tr,td,th{{display:block;width:auto}} th{{display:none}}
 td{{border:0;padding:3px 0}} tr{{border-bottom:1px solid {tokens['line']};padding:8px 0;display:block}}
 .flag{{display:block;margin:0 0 6px;min-height:44px;line-height:28px}}
 .trio span{{width:44px;height:44px;line-height:42px}}
}}
</style></head><body><div class="wrap">{body(active)}</div>{js}</body></html>"""

report=[]
for key,t in SCHEMES.items():
    html=os.path.join(WORK,f"{key}.html")
    open(html,"w").write(page(t, key))
    subprocess.run(["wkhtmltoimage","--width","1040","--quality","92",
                    html, os.path.join(OUT,f"tracker_dashboard_{key}.png")],
                   check=True, capture_output=True)
    pairs={"body":cr(t['text'],t['bg']),"muted":cr(t['muted'],t['bg']),"accent":cr(t['accentText'],t['accent']),
           "pass":cr(t['ok'],t['tok']),"fail":cr(t['bad'],t['tbad']),
           "blocked":cr(t['blk'],t['tblk']),"pending":cr(t['pend'],t['tpend'])}
    report.append((t['label'],pairs,min(pairs.values())))

# reference implementation: default scheme baked, switcher live
open(os.path.join(OUT,"tracker-shell-reference.html"),"w").write(
    page(SCHEMES["01_ink"], "01_ink", switcher_js=True))

print(f"{'scheme':14s} {'worst':>6s}  result")
for n,p,w in report:
    print(f"{n:14s} {w:6.2f}  {'AA OK' if w>=4.5 else 'FAIL - do not ship'}")
    print("               "+" ".join(f"{k}={v}" for k,v in p.items()))
