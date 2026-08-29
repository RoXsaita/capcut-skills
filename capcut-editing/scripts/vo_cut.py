import subprocess, os, sys
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from vo_plan import spans

SRC = os.environ.get("CAPCUT_CAM")
OUT = os.environ.get("CAPCUT_VO_OUT", os.path.expanduser("~/Movies/capcut-vo"))
if not SRC:
    sys.exit("Set CAPCUT_CAM to the talking-head file")
os.makedirs(OUT, exist_ok=True)

# one filter_complex, re-encode once, frame accurate. 1440x2560 is already 9:16 -> scale to 1080x1920.
fv, fa, vl, al = [], [], [], []
for n,(i,a,b,_) in enumerate(spans):
    fv.append(f"[0:v]trim=start={a}:end={b},setpts=PTS-STARTPTS,scale=1080:1920,fps=30,setsar=1[v{n}]")
    fa.append(f"[0:a]atrim=start={a}:end={b},asetpts=PTS-STARTPTS[a{n}]")
    vl.append(f"[v{n}]"); al.append(f"[a{n}]")
fc = ";".join(fv+fa) + ";" + "".join(v+a for v,a in zip(vl,al)) + f"concat=n={len(spans)}:v=1:a=1[v][a]"

cmd = ["ffmpeg","-v","error","-stats","-y","-i",SRC,"-filter_complex",fc,
       "-map","[v]","-map","[a]","-c:v","libx264","-preset","medium","-crf","18",
       "-pix_fmt","yuv420p","-c:a","aac","-b:a","192k",
       os.path.join(OUT,"VO_cut_master.mp4")]
subprocess.run(cmd, check=True)
print("done")
