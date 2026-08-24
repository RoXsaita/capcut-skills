#!/usr/bin/env python3
"""
capcut.py — one deterministic entry point for everything that was being hand-rolled.

    capcut spans    <proj>              print the live EDL (source in/out per clip)
    capcut lint     <proj>              energy-lint every seam in the live project
    capcut strip    <proj> [a] [b]      ASCII energy strip of the cut
    capcut preview  <proj> [out.mp4]    render the VO from the live spans
    capcut sheet    <proj> [out.png]    contact sheet of every cut frame
    capcut verify   <proj>              structural validation + all-copies md5 check
    capcut backup   <proj> [tag]        snapshot draft_info.json
    capcut fixstills <proj> [--wait]    repair stills whose source duration was
                                        inherited from a donor (CapCut truncates them)
    capcut write    <proj> <new.json> [--wait]
                                        THE ONLY WAY TO WRITE. Refuses while CapCut
                                        is running unless --wait (then it blocks —
                                        run that in the background). Writes every
                                        timeline copy, updates meta + registry,
                                        verifies md5, keeps a pre-write backup.
                                        Refuses outright if validation fails.

Project may be a name or a full path.
"""
import sys, os, json, glob, shutil, subprocess, hashlib, time

ROOT = os.path.expanduser("~/Movies/CapCut/User Data/Projects/com.lveditor.draft")
CAM  = os.path.expanduser("~/Downloads/E32F9DC9-C213-4EAD-B7D2-C4F61FC731C8.mp4")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def proj(name): return name if os.path.isdir(name) else os.path.join(ROOT, name)
def load(p):    return json.load(open(os.path.join(p, "draft_info.json")))

def copies(p):
    """every file CapCut treats as the timeline. Missing any one of these = silent revert."""
    out = [os.path.join(p,"draft_info.json"), os.path.join(p,"template-2.tmp")]
    for t in glob.glob(os.path.join(p,"Timelines","*/")):
        for f in ("draft_info.json","draft_info.json.bak","template-2.tmp"):
            if os.path.exists(t+f): out.append(t+f)
    return out

def vo_track(d):
    """the A-roll track: the overlay track with the most segments"""
    ov = [t for t in d['tracks'] if t.get('flag')==2 and t['segments']]
    return max(ov, key=lambda t: len(t['segments']))

def spans_of(d):
    segs = sorted(vo_track(d)['segments'], key=lambda s: s['target_timerange']['start'])
    out=[]
    for s in segs:
        sr=s['source_timerange']
        out.append((s.get('desc','').split(':')[0] or '?', sr['start']/1e6,
                    (sr['start']+sr['duration'])/1e6, s['target_timerange']['start']/1e6))
    return out

def validate(d):
    ids = {m['id'] for v in d['materials'].values() if isinstance(v,list)
                  for m in v if isinstance(m,dict) and 'id' in m}
    errs, seen = [], {}
    for t in d['tracks']:
        for s in t['segments']:
            if s['material_id'] not in ids: errs.append(f"missing material {s['material_id'][:8]}")
            for r in s.get('extra_material_refs',[]):
                if r not in ids: errs.append(f"missing ref {r[:8]}")
                seen[r] = seen.get(r,0)+1
            sr,tg = s['source_timerange'], s['target_timerange']
            if abs(sr['duration'] - tg['duration']*s['speed']) > 2000:
                errs.append(f"speed invariant broken: {s.get('desc','')[:24]}")
        e=sorted((x['target_timerange']['start'],
                  x['target_timerange']['start']+x['target_timerange']['duration']) for x in t['segments'])
        for (a1,b1),(a2,b2) in zip(e,e[1:]):
            if a2 < b1: errs.append(f"overlap in {t['type']} track ({(b1-a2)}us)")
    if any(t.get('flag')==0 and t['segments'] for t in d['tracks']):
        errs.append("RULE ZERO: main track is not empty")
    dup = [r for r,c in seen.items() if c>1]
    if dup: errs.append(f"{len(dup)} side-materials shared between segments")
    return errs

def md5(f): return hashlib.md5(open(f,'rb').read()).hexdigest()

# ---------------------------------------------------------------- commands
def cmd_spans(p):
    for lbl,a,b,tl in spans_of(load(p)):
        print(f"  {lbl:4} src {a:8.3f} -> {b:8.3f}  ({b-a:5.2f}s)   tl {tl:6.2f}")

def cmd_lint(p):
    from audio_index import AudioIndex, lint
    idx = AudioIndex.build_or_load(CAM)
    f = lint(idx, [(l,a,b) for l,a,b,_ in spans_of(load(p))])
    print("\n".join("  "+x for x in f) if f else "  CLEAN — 0 findings")

def cmd_strip(p, a=None, b=None):
    from audio_index import AudioIndex
    wav = render_vo(p, None, audio_only=True)
    idx = AudioIndex.from_wav(wav, 50)
    a,b = float(a or 0), float(b or len(idx.db)*idx.bin)
    cuts = {}
    t=0.0
    for lbl,x,y,_ in spans_of(load(p)):
        t += y-x; cuts[round(t/0.05)] = lbl
    W=100
    for row in range(int(a/0.05), int(b/0.05), W):
        line="".join('|' if i in cuts else
                     ('#' if idx.db[i]>-28 else ('o' if idx.db[i]>-45 else '.'))
                     for i in range(row, min(row+W, len(idx.db))))
        print(f"{row*0.05:6.1f}s {line}")

def render_vo(p, out, audio_only=False):
    sp = spans_of(load(p))
    cache = os.path.expanduser("~/Movies/GrokBuild-wip/vo")
    os.makedirs(cache, exist_ok=True)
    out = out or os.path.join(cache, "cli_preview." + ("wav" if audio_only else "mp4"))
    fv,fa,vl,al = [],[],[],[]
    for n,(_,a,b,_) in enumerate(sp):
        fa.append(f"[0:a]atrim=start={a}:end={b},asetpts=PTS-STARTPTS[a{n}]"); al.append(f"[a{n}]")
        if not audio_only:
            fv.append(f"[0:v]trim=start={a}:end={b},setpts=PTS-STARTPTS,scale=608:1080,fps=30,setsar=1[v{n}]")
            vl.append(f"[v{n}]")
    if audio_only:
        fc=";".join(fa)+";"+"".join(al)+f"concat=n={len(sp)}:v=0:a=1[a]"
        cmd=["ffmpeg","-v","error","-y","-i",CAM,"-filter_complex",fc,"-map","[a]","-ac","1","-ar","16000",out]
    else:
        fc=";".join(fv+fa)+";"+"".join(v+a for v,a in zip(vl,al))+f"concat=n={len(sp)}:v=1:a=1[v][a]"
        cmd=["ffmpeg","-v","error","-y","-i",CAM,"-filter_complex",fc,"-map","[v]","-map","[a]",
             "-c:v","libx264","-crf","30","-preset","veryfast","-pix_fmt","yuv420p","-c:a","aac",out]
    subprocess.run(cmd, check=True)
    return out

def cmd_preview(p, out=None):
    f = render_vo(p, out)
    print(f"  {f}  ({os.path.getsize(f)/1e6:.1f} MB)")

def cmd_sheet(p, out=None):
    sp = spans_of(load(p)); mp4 = render_vo(p, None)
    out = out or os.path.expanduser("~/Movies/GrokBuild-wip/vo/cli_sheet.png")
    tmp = os.path.join(os.path.dirname(out), "_sheet"); shutil.rmtree(tmp, ignore_errors=True); os.makedirs(tmp)
    t=0.0; marks=[]
    for lbl,a,b,_ in sp:
        marks.append((lbl,"in",t)); t+=b-a; marks.append((lbl,"out",t-0.05))
    for n,(lbl,k,tt) in enumerate(marks):
        subprocess.run(["ffmpeg","-v","error","-ss",str(max(0,tt)),"-i",mp4,"-frames:v","1","-vf",
            f"scale=200:-1,drawtext=text='{lbl}-{k}':x=4:y=4:fontsize=18:fontcolor=yellow:box=1:boxcolor=black@0.6",
            "-y",f"{tmp}/{n:02d}.png"],check=True)
    cols=5; rows=(len(marks)+cols-1)//cols
    subprocess.run(["ffmpeg","-v","error","-y","-pattern_type","glob","-i",f"{tmp}/*.png",
        "-filter_complex",f"tile={cols}x{rows}:padding=4:color=0x202020","-frames:v","1",out],check=True)
    print(f"  {out}")

def cmd_verify(p):
    errs = validate(load(p))
    print("  structure:", "clean" if not errs else "\n   - "+"\n   - ".join(errs))
    # CapCut rewrites every one of these files while it has the project open,
    # and re-serialises .bak on its own schedule. Comparing them mid-session
    # reports a revert that is not happening. Only compare when it is closed,
    # and never hold the .bak to byte equality — it is CapCut's backup, not ours.
    if subprocess.run(["pgrep","-x","CapCut"],capture_output=True).returncode == 0:
        print("  timeline copies: CapCut is open — it rewrites these constantly, so a "
              "byte-comparison now means nothing. Re-run after quitting.")
        return
    live = [f for f in copies(p) if not f.endswith(".bak")]
    h = {md5(f) for f in live}
    print(f"  timeline copies: {len(live)} live files, {len(h)} distinct md5",
          "(consistent)" if len(h)==1 else "*** MISMATCH — CapCut will revert ***")

def cmd_backup(p, tag="manual"):
    dst = os.path.join(p, f"draft_info.BACKUP_{tag}.json")
    shutil.copy(os.path.join(p,"draft_info.json"), dst); print("  ", dst)

def cmd_fixstills(p, *a):
    """Stills whose source_timerange was inherited from a donor get truncated by CapCut.
    Read -> fix -> write, so it always acts on the CURRENT project, never a stale blob."""
    if subprocess.run(["pgrep","-x","CapCut"],capture_output=True).returncode == 0:
        if "--wait" not in a: print("  CapCut running; re-run with --wait in the background."); sys.exit(2)
        print("  waiting for CapCut to quit...")
        while subprocess.run(["pgrep","-x","CapCut"],capture_output=True).returncode == 0: time.sleep(2)
        time.sleep(4)
    d = load(p)
    mt = {m['id']: m.get('type') for m in d['materials']['videos']}
    n = 0
    for t in d['tracks']:
        for s in t['segments']:
            if mt.get(s['material_id']) == 'photo':
                td = s['target_timerange']['duration']
                if abs(s['source_timerange']['duration'] - td*s['speed']) > 2000:
                    print(f"   {s.get('desc','still')}: src {s['source_timerange']['duration']} -> {td}")
                    s['source_timerange'] = {'start': 0, 'duration': td}; n += 1
    if not n: print("  nothing to fix"); return
    tmp = os.path.join(p, "draft_info.FIXSTILLS.json")
    json.dump(d, open(tmp,'w'), ensure_ascii=False)
    cmd_write(p, tmp); os.remove(tmp)

def cmd_write(p, newjson, *a):
    d = json.load(open(newjson))
    errs = validate(d)
    if errs:
        print("  REFUSING TO WRITE:"); [print("   -",e) for e in errs]; sys.exit(1)
    if subprocess.run(["pgrep","-x","CapCut"],capture_output=True).returncode == 0:
        if "--wait" not in sys.argv:
            print("  CapCut is RUNNING. It rewrites the project on exit, so writing now would be\n"
                  "  silently reverted. Either quit CapCut and re-run, or re-run with --wait\n"
                  "  IN THE BACKGROUND (it blocks until CapCut quits).")
            sys.exit(2)
        print("  waiting for CapCut to quit...")
        while subprocess.run(["pgrep","-x","CapCut"],capture_output=True).returncode == 0:
            time.sleep(2)
        time.sleep(4)
    shutil.copy(os.path.join(p,"draft_info.json"), os.path.join(p,"draft_info.BACKUP_prewrite.json"))
    blob = json.dumps(d, ensure_ascii=False)
    for f in copies(p): open(f,"w").write(blob)
    m = os.path.join(p,"draft_meta_info.json")
    mi = json.load(open(m)); mi['tm_duration'] = d['duration']; json.dump(mi, open(m,'w'), ensure_ascii=False)
    rp = os.path.join(ROOT,"root_meta_info.json")
    r = json.load(open(rp)); name = os.path.basename(p.rstrip("/"))
    for e in r['all_draft_store']:
        if e['draft_name'] == name: e['tm_duration'] = d['duration']
    json.dump(r, open(rp,'w'), ensure_ascii=False)
    h = {md5(f) for f in copies(p)}
    print(f"  wrote {len(copies(p))} copies, {len(h)} distinct md5",
          "OK" if len(h)==1 else "*** MISMATCH ***", f"| duration {d['duration']/1e6:.3f}s")

if __name__ == "__main__":
    if len(sys.argv) < 3: print(__doc__); sys.exit(0)
    cmd, p, rest = sys.argv[1], proj(sys.argv[2]), sys.argv[3:]
    globals()[f"cmd_{cmd}"](p, *rest)
