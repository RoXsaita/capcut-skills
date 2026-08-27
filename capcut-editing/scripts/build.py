import json, os, uuid, copy, shutil
D=os.path.expanduser("~/Movies/CapCut/User Data/Projects/com.lveditor.draft")
P=f"{D}/Grok Build"
# Legacy one-off. The media constants below came from the single take this was
# written for; nothing here ships with sample media. Point them at your own files:
#   CAPCUT_CAM=... CAPCUT_BROLL=... CAPCUT_SCRATCH=... python <script>.py
CAM = os.environ.get("CAPCUT_CAM", "")          # talking-head source
GROK = os.environ.get("CAPCUT_BROLL", "")       # screen-recording B-roll source
SFXDIR=os.path.expanduser("~/Library/Containers/com.lemon.lvoverseas/Data/Movies/CapCut/User Data/Cache/music")
U=lambda: str(uuid.uuid4()).upper()
us=lambda s: int(round(s*1_000_000))

d=json.load(open(f"{P}/draft_info.json"))
M=d["materials"]
src=json.load(open(f"{D}/IKEA Refund/draft_info.json"))   # template donor

# ---------- template helpers ----------
VID_T={k:v for k,v in src["materials"]["videos"][0].items()}
AUD_T={k:v for k,v in src["materials"]["audios"][0].items()}
def donor(bucket):
    return copy.deepcopy(src["materials"][bucket][0])

def add_video_material(path,w,h,dur_s,has_audio=True,name=None):
    m=copy.deepcopy(VID_T); m.update(
        id=U(), local_material_id=U(), path=path, media_path="", duration=us(dur_s),
        width=w, height=h, has_audio=has_audio, type="video",
        material_name=name or os.path.basename(path), material_id="", 
        reverse_path="", intensifies_path="", reverse_intensifies_path="",
        intensifies_audio_path="", cartoon_path="", crop_scale=1.0)
    M["videos"].append(m); return m["id"]

def add_audio_material(path,dur_s,name):
    m=copy.deepcopy(AUD_T); m.update(id=U(), path=path, duration=us(dur_s), name=name, type="sound")
    M["audios"].append(m); return m["id"]

def refs_for(kind, speed=1.0):
    """create the extra_material_refs bundle a segment needs"""
    out=[]
    sp=donor("speeds"); sp.update(id=U(), speed=speed, mode=0, curve_speed=None)
    M.setdefault("speeds",[]).append(sp); out.append(sp["id"])
    ph=donor("placeholder_infos"); ph["id"]=U(); M.setdefault("placeholder_infos",[]).append(ph); out.append(ph["id"])
    if kind=="video":
        cv=donor("canvases"); cv["id"]=U(); M.setdefault("canvases",[]).append(cv); out.append(cv["id"])
        an={"id":U(),"type":"sticker_animation","animations":[],"multi_language_current":"none"}
        M.setdefault("material_animations",[]).append(an); out.append(an["id"])
    sc=donor("sound_channel_mappings"); sc["id"]=U(); M.setdefault("sound_channel_mappings",[]).append(sc); out.append(sc["id"])
    if kind=="video":
        mc=donor("material_colors"); mc["id"]=U(); M.setdefault("material_colors",[]).append(mc); out.append(mc["id"])
    else:
        ld=donor("loudnesses"); ld["id"]=U(); M.setdefault("loudnesses",[]).append(ld); out.append(ld["id"])
    vs=donor("vocal_separations"); vs["id"]=U(); M.setdefault("vocal_separations",[]).append(vs); out.append(vs["id"])
    return out

SEG_V=copy.deepcopy(src["tracks"][1]["segments"][1])
SEG_A=copy.deepcopy(src["tracks"][11]["segments"][0])

def mkseg(kind, mat_id, src_start, tgt_start, tgt_dur, speed=1.0,
          volume=1.0, scale=1.0, ty=0.0, tri=0, kf=None):
    s=copy.deepcopy(SEG_V if kind=="video" else SEG_A)
    s.update(id=U(), material_id=mat_id, speed=speed, volume=volume,
             last_nonzero_volume=volume if volume>0 else 1.0,
             source_timerange={"start":us(src_start),"duration":us(tgt_dur*speed)},
             target_timerange={"start":us(tgt_start),"duration":us(tgt_dur)},
             extra_material_refs=refs_for(kind,speed),
             render_index=tri*100, track_render_index=tri,
             common_keyframes=[], keyframe_refs=[], group_id="")
    if kind=="video":
        s["clip"]={"scale":{"x":scale,"y":scale},"rotation":0.0,
                   "transform":{"x":0.0,"y":ty},
                   "flip":{"vertical":False,"horizontal":False},"alpha":1.0}
        if kf:  # (from_scale, to_scale) punch-in
            f,t=kf
            s["common_keyframes"]=[{
                "id":U(),"material_id":"","property_type":pt,
                "keyframe_list":[
                  {"id":U(),"curveType":"Line","time_offset":0,
                   "left_control":{"x":0.0,"y":0.0},"right_control":{"x":0.0,"y":0.0},
                   "values":[f],"string_value":"","graphID":""},
                  {"id":U(),"curveType":"Line","time_offset":us(tgt_dur),
                   "left_control":{"x":0.0,"y":0.0},"right_control":{"x":0.0,"y":0.0},
                   "values":[t],"string_value":"","graphID":""}]}
                for pt in ("KFTypeScaleX","KFTypeScaleY")]
    else:
        s["clip"]=None
    return s

def mktrack(kind, segs, flag=0):
    return {"id":U(),"type":kind,"flag":flag,"attribute":0,"name":"","is_default_name":True,
            "segments":segs}
print("helpers ready")

# ---------------- TIMELINE ----------------
CAM_ID  = add_video_material(CAM, 1440,2560, 232.366667, True,  "E32F9DC9 (cam take2)")
GROK_ID = add_video_material(GROK,1080,2652, 1861.611156, True, "Screen_Recording_Grok")

SFX={n:(f"{SFXDIR}/{h}.mp3",dur) for n,h,dur in [
 ("impact","07d7ecbf820c0a668adb491c04cf76fb",6.47),
 ("coin","2f1afdadff2934e4a5f43260d37b53fc",0.77),
 ("click","c651fe9e2c689a98afbbf03e114e6891",0.30),
 ("kbd","6048e7c00aed1a1b57c23518d0a86afd",0.50),
 ("pop","a0f3cad66351f21dd6456c0719135cb2",0.37),
 ("click2","d91f21d1c2b6ec21cf77a8d7185bdb47",0.20),
 ("shutter","c41a3fa1aa68fd2608e32f915792151a",0.60),
 ("enter","4cd0c7ee14c07e29164fd10df012a008",0.97),
 ("typing","51c6842d59d720932576a5a89797840e",60.33),
 ("clock","14567402c4be0b62e096b036a117ad65",4.07),
 ("select","769d41a88cecf6d6a0f24828a1996180",1.07)]}
SFX_ID={n:add_audio_material(p,dur,n) for n,(p,dur) in SFX.items()}

# beat = (vo_start, vo_end)  from cam TAKE 2
BEATS=[(121.20,129.40),(129.40,133.94),(135.88,142.74),(147.26,155.58),
       (155.58,162.94),(162.94,168.12),(168.12,174.96),(174.96,179.58),
       (183.86,189.68),(192.04,197.04),(213.88,222.48),(226.94,231.10)]

# b-roll: beat_idx -> [(grok_src, tgt_offset_in_beat, tgt_dur, speed, punch_in)]
BROLL={
 0:[(1772.0,0.00,2.50,1.0,None)],
 1:[(0.0,   0.50,1.50,2.0,None),(6.0,2.00,2.00,1.5,None)],
 2:[(46.0,  0.75,5.00,1.0,(1.0,1.18))],
 3:[(64.0,  0.70,4.00,1.0,(1.0,1.15)),(80.0,4.70,3.00,1.5,None)],
 4:[(84.0,  0.60,6.50,1.4,(1.0,1.12))],
 5:[(404.0, 0.70,4.00,1.0,(1.0,1.25))],
 6:[(395.0, 0.55,3.50,1.0,None),(535.0,4.05,2.50,2.0,None)],
 7:[(600.0, 0.50,1.50,100.0,None),(1700.0,2.00,1.50,1.5,None),(1760.0,3.50,1.10,1.0,None)],
 8:[(1808.0,0.60,5.00,1.6,None)],
 9:[(1773.0,0.55,3.50,1.0,None)],
 10:[(70.0, 0.75,3.00,1.0,(1.0,1.15)),(1794.0,4.25,3.50,1.0,(1.0,1.15))],
 11:[],
}
# sfx: (name, absolute_target_time, duration)
SFXCUES=[]
def cue(n,t,dur=None): SFXCUES.append((n,t,dur or SFX[n][1]))

aroll=[]; broll=[]; t=0.0
for i,(vs,ve) in enumerate(BEATS):
    dur=ve-vs
    aroll.append(mkseg("video",CAM_ID,vs,t,dur,1.0,volume=1.0,scale=1.0,tri=0))
    for (gs,off,gd,sp,kf) in BROLL.get(i,[]):
        broll.append(mkseg("video",GROK_ID,gs,t+off,gd,sp,volume=0.0,scale=1.0,tri=1,kf=kf))
    t+=dur
CONTENT_END=t

cue("impact",0.0,2.4); cue("pop",2.45)
cue("click",8.70); cue("click",10.20)
cue("click",13.49); cue("select",15.60)
cue("kbd",20.30); cue("typing",20.80,2.6)
cue("click",28.52); cue("click",29.60); cue("click2",30.70); cue("click",31.80)
cue("pop",35.98)
cue("shutter",41.01); cue("shutter",44.51)
cue("clock",47.80,1.5); cue("coin",50.80)
cue("select",52.52)
cue("pop",63.49); cue("pop",66.99)
cue("pop",71.40)

sfx_segs=[[],[],[]]
for n,tt,dd in SFXCUES:
    lane=0 if n in("impact","clock","typing") else (1 if n in("click","click2","kbd") else 2)
    sfx_segs[lane].append(mkseg("audio",SFX_ID[n],0.0,tt,min(dd,SFX[n][1]),1.0,volume=1.0,tri=10+lane))

# ---- shift the Preset-3 outro to the absolute end ----
OLD_OUTRO_START=68.833333
delta=CONTENT_END-OLD_OUTRO_START
for tr in d["tracks"]:
    for s in tr.get("segments",[]):
        s["target_timerange"]["start"]+=us(delta)
        for k in s.get("common_keyframes",[]) or []: pass
NEW_DUR=max(s["target_timerange"]["start"]+s["target_timerange"]["duration"]
            for tr in d["tracks"] for s in tr.get("segments",[]))

# ---- assemble tracks: A-roll bottom, B-roll above, outro tracks on top, audio last ----
outro_tracks=d["tracks"]
d["tracks"]=[mktrack("video",aroll,0), mktrack("video",broll,2)] + outro_tracks + \
            [mktrack("audio",s,0) for s in sfx_segs if s]
for i,tr in enumerate(d["tracks"]):
    for s in tr["segments"]:
        s["track_render_index"]=i
d["duration"]=max(NEW_DUR, us(CONTENT_END))
d["name"]="Grok Build"

json.dump(d, open(f"{P}/draft_info.json","w"), ensure_ascii=False)
shutil.copy(f"{P}/draft_info.json", f"{P}/draft_info.json.bak")
print(f"content {CONTENT_END:.2f}s | outro shifted +{delta:.2f}s | total {d['duration']/1e6:.2f}s")
print(f"A-roll {len(aroll)} | B-roll {len(broll)} | SFX {sum(len(x) for x in sfx_segs)} | tracks {len(d['tracks'])}")
