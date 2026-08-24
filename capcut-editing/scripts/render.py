import subprocess, os, json, sys
S="/private/tmp/claude-501/-Users-roxsa/0832a1d1-cbc4-4d25-a86b-4bbad0c63b60/scratchpad"
CAM="/Users/roxsa/Downloads/E32F9DC9-C213-4EAD-B7D2-C4F61FC731C8.mp4"
GROK="/Users/roxsa/Downloads/Screen_Recording_20260822_095151_Grok.mp4"
CAM_Y=640          # verified good face framing
W,H=1080,1920; HALF=960

def shot(i,s,out):
    """s: dict(dur, layout, cam, grok, gspeed, roi)"""
    d=s["dur"]; lay=s["layout"]
    if lay=="full_cam":
        cmd=["ffmpeg","-v","error","-ss",str(s["cam"]),"-i",CAM,"-t",str(d),
             "-vf",f"scale={W}:{H},fps=30,setsar=1","-an"]
    elif lay=="full_screen":
        sp=s.get("gspeed",1.0)
        cmd=["ffmpeg","-v","error","-ss",str(s["grok"]),"-i",GROK,"-t",str(d*sp),
             "-vf",f"crop={W}:{H}:0:{min(s['roi'],2652-H)},setpts=PTS/{sp},fps=30,setsar=1","-an"]
    else:  # split : grok top, cam bottom
        sp=s.get("gspeed",1.0)
        cmd=["ffmpeg","-v","error",
             "-ss",str(s["grok"]),"-i",GROK,
             "-ss",str(s["cam"]),"-i",CAM,
             "-filter_complex",
             f"[0:v]crop={W}:{HALF}:0:{s['roi']},setpts=PTS/{sp},fps=30,setsar=1[top];"
             f"[1:v]scale={W}:{H},crop={W}:{HALF}:0:{CAM_Y},fps=30,setsar=1[bot];"
             f"[top][bot]vstack=inputs=2[v]",
             "-map","[v]","-t",str(d),"-an"]
    cmd+=["-c:v","libx264","-preset","ultrafast","-crf","20","-pix_fmt","yuv420p",out,"-y"]
    r=subprocess.run(cmd,capture_output=True,text=True)
    if r.returncode: print("ERR",i,r.stderr[-300:]); return False
    return True

def render(shots, name, vo_start, vo_dur):
    os.makedirs(f"{S}/shots",exist_ok=True)
    files=[]
    for i,s in enumerate(shots):
        f=f"{S}/shots/{name}_{i:02d}.mp4"
        if shot(i,s,f): files.append(f)
    lst=f"{S}/shots/{name}.txt"
    open(lst,"w").write("\n".join(f"file '{f}'" for f in files))
    subprocess.run(["ffmpeg","-v","error","-f","concat","-safe","0","-i",lst,
                    "-c","copy",f"{S}/shots/{name}_mute.mp4","-y"],check=True)
    # VO from cam
    parts=[]
    for j,(a,b) in enumerate(vo_start):
        f=f"{S}/shots/{name}_vo{j}.m4a"
        subprocess.run(["ffmpeg","-v","error","-ss",str(a),"-i",CAM,"-t",str(b),
                        "-vn","-ac","2","-ar","48000","-c:a","aac",f,"-y"],check=True)
        parts.append(f)
    vl=f"{S}/shots/{name}_vo.txt"; open(vl,"w").write("\n".join(f"file '{x}'" for x in parts))
    subprocess.run(["ffmpeg","-v","error","-f","concat","-safe","0","-i",vl,"-c","copy",
                    f"{S}/shots/{name}_vo.m4a","-y"],check=True)
    subprocess.run(["ffmpeg","-v","error","-i",f"{S}/shots/{name}_mute.mp4",
                    "-i",f"{S}/shots/{name}_vo.m4a","-c:v","copy","-c:a","aac","-shortest",
                    f"{S}/{name}.mp4","-y"],check=True)
    print(f"rendered {S}/{name}.mp4  ({len(files)} shots)")
