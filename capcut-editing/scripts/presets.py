import json, os, copy, uuid
P = os.path.expanduser("~/Movies/CapCut/User Data/Projects/com.lveditor.draft/grok-build-claude")
d = json.load(open(os.path.join(P,"draft_info.json")))
U = lambda: str(uuid.uuid4()).upper()
byid = {}
for k,v in d['materials'].items():
    if isinstance(v,list):
        for m in v:
            if isinstance(m,dict) and 'id' in m: byid[m['id']] = (k,m)

T   = d['tracks']
cam = T[1]['segments']
A, B, C1 = cam[0], cam[1], cam[2]

def mask_of(seg):
    for r in seg.get('extra_material_refs',[]):
        if r in byid and byid[r][0]=='common_mask': return byid[r][1]
    return None

# ---- the three references, read from what already works ------------------
AVATAR   = T[4]['segments'][0]                                   # endcard circular head
WCIRCLE  = T[6]['segments'][0]                                   # endcard white circle frame
FRAME2   = [s for s in T[5]['segments'] if s['target_timerange']['start'] < 20e6][0]  # your scene-2 purple frame
M_AVATAR, M_WCIRCLE, M_SPLIT = mask_of(AVATAR), mask_of(WCIRCLE), mask_of(B)
assert M_AVATAR and M_WCIRCLE and M_SPLIT

def clone_mask(src):
    m = copy.deepcopy(src); m['id'] = U()
    d['materials']['common_mask'].append(m); return m['id']

def clone_refs(seg):
    """fresh copies of a donor segment's side-materials, so nothing is shared"""
    out = []
    for r in seg.get('extra_material_refs',[]):
        if r not in byid: continue
        bucket, m = byid[r]
        if bucket == 'common_mask': continue          # caller supplies the mask
        nm = copy.deepcopy(m); nm['id'] = U()
        d['materials'][bucket].append(nm); out.append(nm['id'])
    return out

def apply_geo(seg, ref, mask_src):
    """copy scale/transform verbatim from a reference segment, attach a private mask"""
    seg['clip'] = copy.deepcopy(ref['clip'])
    seg['uniform_scale'] = copy.deepcopy(ref.get('uniform_scale'))
    seg['extra_material_refs'] = [r for r in seg['extra_material_refs']
                                  if not (r in byid and byid[r][0]=='common_mask')]
    seg['extra_material_refs'].append(clone_mask(mask_src))

def new_seg(donor, start, dur, ri, tri, clip_ref, mask_src, desc):
    s = copy.deepcopy(donor)
    s['id'] = U()
    s['target_timerange'] = {"start": start, "duration": dur}
    s['clip'] = copy.deepcopy(clip_ref['clip'])
    s['uniform_scale'] = copy.deepcopy(clip_ref.get('uniform_scale'))
    s['render_index'], s['track_render_index'] = ri, tri
    s['common_keyframes'], s['keyframe_refs'] = [], []
    s['desc'] = desc
    s['extra_material_refs'] = clone_refs(donor)
    if mask_src: s['extra_material_refs'].append(clone_mask(mask_src))
    return s

# ================= SCENE 1  ->  preset CIRCLE =============================
apply_geo(A, AVATAR, M_AVATAR)
T[6]['segments'].append(new_seg(WCIRCLE, A['target_timerange']['start'],
    A['target_timerange']['duration'], 4, 6, WCIRCLE, M_WCIRCLE, "scene1 white circle frame"))

# ================= SCENE 3  ->  preset SPLIT (match scene 2) ==============
apply_geo(C1, B, M_SPLIT)
T[5]['segments'].append(new_seg(FRAME2, C1['target_timerange']['start'],
    C1['target_timerange']['duration'], 3, 5, FRAME2, None, "scene3 purple frame"))

for t in T: t['segments'].sort(key=lambda s: s['target_timerange']['start'])

# ---- validate -----------------------------------------------------------
ids = {m['id'] for v in d['materials'].values() if isinstance(v,list)
              for m in v if isinstance(m,dict) and 'id' in m}
seen, errs = {}, []
for t in T:
    for s in t['segments']:
        if s['material_id'] not in ids: errs.append("missing material")
        for r in s['extra_material_refs']:
            if r not in ids: errs.append("missing ref "+r[:8])
            seen[r] = seen.get(r,0)+1
    e=sorted((x['target_timerange']['start'], x['target_timerange']['start']+x['target_timerange']['duration']) for x in t['segments'])
    for (s1,e1),(s2,e2) in zip(e,e[1:]):
        if s2 < e1: errs.append("overlap")
shared = [r for r,c in seen.items() if c>1]
if shared: errs.append(f"{len(shared)} side-materials shared between segments")
assert not errs, errs

d['duration'] = max(s['target_timerange']['start']+s['target_timerange']['duration']
                    for t in T for s in t['segments'])
json.dump(d, open(os.path.join(P,"draft_info.PENDING.json"),"w"), ensure_ascii=False)

for lbl,s in [("scene1 cam A",A),("scene2 cam B (yours)",B),("scene3 cam C1",C1)]:
    m=mask_of(s); c=s['clip']
    print(f"{lbl:22} scale=({c['scale']['x']:.4f},{c['scale']['y']:.4f}) "
          f"tf=({c['transform']['x']:.4f},{c['transform']['y']:.4f}) mask={m['name'] if m else None}")
print()
for lbl,s in [("scene1 white circle",T[6]['segments'][0]),("scene3 purple frame",[x for x in T[5]['segments'] if x.get('desc')=='scene3 purple frame'][0])]:
    c=s['clip']
    print(f"{lbl:22} scale=({c['scale']['x']:.4f},{c['scale']['y']:.4f}) "
          f"tf=({c['transform']['x']:.4f},{c['transform']['y']:.4f}) "
          f"tl {s['target_timerange']['start']/1e6:.2f}->{(s['target_timerange']['start']+s['target_timerange']['duration'])/1e6:.2f}")
print("\nvalidation: clean | duration", d['duration']/1e6)
