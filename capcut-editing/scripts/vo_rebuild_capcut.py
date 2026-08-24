import json, os, sys, glob, shutil
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from vo_plan import spans

P = sys.argv[1]
US = lambda s: int(round(s*1e6))
src = os.path.join(P,"draft_info.json")
d = json.load(open(src))

main = [t for t in d['tracks'] if t['type']=='video' and t.get('flag')==0][0]
if len(main['segments']) == len(spans) and abs(d['duration']-76266733) < 1000:
    print("already rebuilt:", P); sys.exit(0)
donors = main['segments']
assert len(donors) >= len(spans), (len(donors), len(spans))

tl = 0.0; newsegs = []
for n,(sid,a,b,lbl) in enumerate(spans):
    s = donors[n]; dur = b-a
    s['source_timerange'] = {"start": US(a), "duration": US(dur)}
    s['target_timerange'] = {"start": US(tl), "duration": US(dur)}
    s['speed']=1.0; s['volume']=1.0
    s['clip']={"scale":{"x":1.0,"y":1.0},"rotation":0.0,"transform":{"x":0.0,"y":0.0},
               "flip":{"vertical":False,"horizontal":False},"alpha":1.0}
    s['common_keyframes']=[]; s['keyframe_refs']=[]
    s['render_index']=0; s['track_render_index']=0
    s['desc']=f"{sid}: {lbl[:60]}"
    newsegs.append(s); tl += dur
main['segments']=newsegs
VO_END = tl

keep=[]
for t in d['tracks']:
    if t is main: keep.append(t); continue
    if t['type']=='audio': continue
    if t['type']=='video' and len(t['segments'])>3: continue
    if not t['segments']: continue
    keep.append(t)
d['tracks']=keep

outro=[t for t in keep if t is not main]
old=min(s['target_timerange']['start'] for t in outro for s in t['segments'])
delta=US(VO_END)-old
for t in outro:
    for s in t['segments']: s['target_timerange']['start'] += delta

d['duration']=max(s['target_timerange']['start']+s['target_timerange']['duration']
                  for t in d['tracks'] for s in t['segments'])

used=set()
for t in d['tracks']:
    for s in t['segments']:
        used.add(s['material_id']); used.update(s.get('extra_material_refs',[]))
for k,v in list(d['materials'].items()):
    if isinstance(v,list) and v and isinstance(v[0],dict) and 'id' in v[0]:
        seen=set(); kept=[]
        for m in v:
            if m['id'] in used and m['id'] not in seen:
                seen.add(m['id']); kept.append(m)
        d['materials'][k]=kept

ids={m['id'] for v in d['materials'].values() if isinstance(v,list)
             for m in v if isinstance(m,dict) and 'id' in m}
errs=[]
for t in d['tracks']:
    for s in t['segments']:
        if s['material_id'] not in ids: errs.append("missing material")
        for r in s.get('extra_material_refs',[]):
            if r not in ids: errs.append("missing ref")
        sr,tr=s['source_timerange'],s['target_timerange']
        if abs(sr['duration']-tr['duration']*s['speed'])>2000: errs.append("speed invariant")
    e=sorted((x['target_timerange']['start'],x['target_timerange']['start']+x['target_timerange']['duration']) for x in t['segments'])
    for (s1,e1),(s2,e2) in zip(e,e[1:]):
        if s2<e1: errs.append("overlap")
assert not errs, errs

blob = json.dumps(d, ensure_ascii=False)
# CapCut restores from Timelines/<uuid>/draft_info.json on open -> write EVERY copy
targets = [os.path.join(P,"draft_info.json"), os.path.join(P,"template-2.tmp")]
for tdir in glob.glob(os.path.join(P,"Timelines","*/")):
    for f in ("draft_info.json","draft_info.json.bak","template-2.tmp"):
        fp=os.path.join(tdir,f)
        if os.path.exists(fp): targets.append(fp)
for t in targets:
    open(t,"w").write(blob)

m=os.path.join(P,"draft_meta_info.json")
mi=json.load(open(m)); mi['tm_duration']=d['duration']; json.dump(mi,open(m,'w'),ensure_ascii=False)

print(f"{os.path.basename(P)}: VO {VO_END:.3f}s, total {d['duration']/1e6:.3f}s, "
      f"tracks {[(t['type'],len(t['segments'])) for t in d['tracks']]}")
print("  wrote:", *[os.path.relpath(t,P) for t in targets], sep="\n    ")
