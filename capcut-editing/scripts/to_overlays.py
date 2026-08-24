import json, os, glob, copy, uuid

P = os.path.expanduser("~/Movies/CapCut/User Data/Projects/com.lveditor.draft/grok-build-claude")
d = json.load(open(os.path.join(P,"draft_info.json")))
U = lambda: str(uuid.uuid4()).upper()

main  = [t for t in d['tracks'] if t['type']=='video' and t.get('flag')==0][0]
ovl   = [t for t in d['tracks'] if t is not main]
donor = ovl[0]

# the endcard base video is the ri=0 clip I wrongly pushed into main last round
vo_segs   = [s for s in main['segments'] if s.get('desc')]
endcard   = [s for s in main['segments'] if not s.get('desc')]
assert len(vo_segs)==9 and len(endcard)==1, (len(vo_segs), len(endcard))

def new_track(segs):
    t = copy.deepcopy(donor)
    t['id'] = U()
    t['segments'] = segs
    return t

# main track stays present but EMPTY -- exactly how Preset 3 is built
main['segments'] = []

vo_track = new_track(vo_segs)
for s in vo_segs:
    s['render_index'] = 2                    # behind everything; never overlaps the endcard anyway
ec_track = new_track(endcard)
endcard[0]['render_index'] = 45              # its original z-order in the preset

# rebuild track order: empty main, VO, then the preset's endcard stack in its original order
rest = sorted(ovl, key=lambda t: [45,36,43,20,46,47].index(t['segments'][0]['render_index']))
d['tracks'] = [main, vo_track, ec_track] + rest

for i,t in enumerate(d['tracks']):
    for s in t['segments']:
        s['track_render_index'] = i          # main=0, overlays 1..7

d['duration'] = max(s['target_timerange']['start']+s['target_timerange']['duration']
                    for t in d['tracks'] for s in t['segments'])

# ---- validate ----
ids = {m['id'] for v in d['materials'].values() if isinstance(v,list)
              for m in v if isinstance(m,dict) and 'id' in m}
errs=[]
seen_track_ids=set()
for t in d['tracks']:
    if t['id'] in seen_track_ids: errs.append("duplicate track id")
    seen_track_ids.add(t['id'])
    for s in t['segments']:
        if s['material_id'] not in ids: errs.append("missing material")
        for r in s.get('extra_material_refs',[]):
            if r not in ids: errs.append("missing ref")
        sr,tg=s['source_timerange'],s['target_timerange']
        if abs(sr['duration']-tg['duration']*s['speed'])>2000: errs.append("speed invariant")
    e=sorted((x['target_timerange']['start'],x['target_timerange']['start']+x['target_timerange']['duration']) for x in t['segments'])
    for (s1,e1),(s2,e2) in zip(e,e[1:]):
        if s2<e1: errs.append("overlap")
assert not errs, errs

json.dump(d, open(os.path.join(P,"draft_info.PENDING.json"),"w"), ensure_ascii=False)

mats={m['id']:(m.get('material_name') or m.get('path','').split('/')[-1][:30]) for m in d['materials']['videos']}
for i,t in enumerate(d['tracks']):
    tag = "MAIN (empty)" if t.get('flag')==0 else f"overlay tri={i}"
    print(f"[{i}] {tag}  n={len(t['segments'])}")
    for s in t['segments'][:3]:
        tr=s['target_timerange']
        print(f"      {tr['start']/1e6:6.3f}->{(tr['start']+tr['duration'])/1e6:6.3f} ri={s.get('render_index'):3} {mats.get(s['material_id'],'?')[:28]:30} {s.get('desc','endcard base')[:22]}")
    if len(t['segments'])>3: print(f"      ... +{len(t['segments'])-3} more")
print(f"\nduration {d['duration']/1e6:.3f}s   validation: clean")
