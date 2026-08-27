import sys,subprocess,os
# Legacy one-off. The media constants below came from the single take this was
# written for; nothing here ships with sample media. Point them at your own files:
#   CAPCUT_CAM=... CAPCUT_BROLL=... CAPCUT_SCRATCH=... python <script>.py
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from render import render, S
CAM = os.environ.get("CAPCUT_CAM", "")          # talking-head source
# (vo_start, vo_dur, [ (b_dur, grok_t, roi, speed, layout) ... ])
BEATS=[
 (121.20,8.20,[(2.00,1772.3,900,1.0,"full_screen"),(1.70,1774.3,900,0.8,"split"),(4.50,1758,200,1.0,"split")]),
 (129.40,4.54,[(1.50,0,420,2.0,"split"),(3.04,110,300,1.0,"split")]),
 (135.88,6.86,[(6.86,45,300,1.0,"split")]),
 (147.26,8.32,[(8.32,63,700,1.0,"split")]),
 (155.58,7.36,[(7.36,84,1150,1.0,"split")]),
 (162.94,5.18,[(5.18,518,1500,1.0,"split")]),
 (168.12,6.84,[(6.84,386,1350,1.0,"split")]),
 (174.96,4.62,[(1.50,600,320,100.0,"split"),(3.12,1759.5,200,1.0,"split")]),
 (183.86,5.82,[(5.82,1840,1233,1.2,"split")]),
 (192.04,5.00,[(5.00,1772.4,900,0.7,"split")]),
 (213.88,8.60,[(4.30,74,150,1.0,"split"),(4.30,1797,150,1.0,"split")]),
 (226.94,4.16,[(4.16,None,0,1.0,"full_cam")]),
]
shots=[];vo=[];t=0.0
for vs,vd,bs in BEATS:
    vo.append((vs,vd)); c=vs
    for (bd,gt,roi,sp,lay) in bs:
        d=dict(dur=bd,layout=lay,cam=c,roi=roi,gspeed=sp)
        if gt is not None: d["grok"]=gt
        shots.append(d); c+=bd; t+=bd
print(f"{len(shots)} shots, {t:.2f}s")
render(shots,"final",vo,t)
