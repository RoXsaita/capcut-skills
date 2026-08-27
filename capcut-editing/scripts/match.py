import glob, os, re, json, subprocess
# Legacy one-off. The media constants below came from the single take this was
# written for; nothing here ships with sample media. Point them at your own files:
#   CAPCUT_CAM=... CAPCUT_BROLL=... CAPCUT_SCRATCH=... python <script>.py
S = os.environ.get("CAPCUT_SCRATCH", os.path.expanduser("~/.cache/capcut-scratch"))
GROK = os.environ.get("CAPCUT_BROLL", "")       # screen-recording B-roll source

def load_index():
    idx={}
    for f in glob.glob(f"{S}/ocrtxt/o_*.txt"):
        sec=int(os.path.basename(f)[2:7])-1
        idx[sec]=open(f,errors="ignore").read().lower()
    return idx

def spans(idx, keys, min_dur=2, forbid=()):
    """seconds where ALL keys appear and no forbidden term does"""
    ok=sorted(s for s,t in idx.items()
              if all(k.lower() in t for k in keys) and not any(f.lower() in t for f in forbid))
    if not ok: return []
    out=[];cur=[ok[0]]
    for s in ok[1:]:
        if s-cur[-1]<=2: cur.append(s)
        else: out.append(cur); cur=[s]
    out.append(cur)
    return [(c[0],c[-1],c[-1]-c[0]+1) for c in out if c[-1]-c[0]+1>=min_dur]

def roi_for(sec, keys):
    """TSV pass on one frame -> y centre of the matched text, in 2652-space"""
    f=f"{S}/ocrframes/o_{sec+1:05d}.jpg"
    r=subprocess.run(["tesseract",f,"stdout","--psm","6","-l","eng","tsv"],
                     capture_output=True,text=True)
    ys=[]
    for line in r.stdout.splitlines()[1:]:
        p=line.split("\t")
        if len(p)<12: continue
        txt=p[11].strip().lower()
        if not txt: continue
        toks={w for k in keys for w in k.lower().split()}
        if any(t in txt or txt in t for t in toks if len(t)>3):
            ys.append(int(p[7])+int(p[9])//2)
    if not ys: return None
    scale=2652/810.0                       # OCR frames are 810 wide
    c=sum(ys)/len(ys)*scale
    return max(0,min(int(c-480), 2652-960)), len(ys)
