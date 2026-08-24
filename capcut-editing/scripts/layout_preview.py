import subprocess, os, sys
CAM=os.path.expanduser("~/Downloads/E32F9DC9-C213-4EAD-B7D2-C4F61FC731C8.mp4")
SCR=os.path.expanduser("~/Downloads/Screen_Recording_20260822_095151_Grok.mp4")
W,H=1080,1920
# CapCut: scale 1.0 == FIT whole clip inside canvas; transform in half-canvas units.
def fit(sw,sh,s=1.0):
    k=min(W/sw,H/sh)*s
    return round(sw*k), round(sh*k)

def render(out, scene, cam_t, scr_t, scr_scale, scr_ty, ysign):
    if scene=="circle":
        cw,ch=fit(1440,2560,0.19)                    # endcard avatar scale, verbatim
        d=round(ch*0.5618)                           # Circle mask height -> diameter
        cx=round(W/2 + (-0.5559524128804151)*(W/2))
        cy=round(H/2 + ysign*0.6442708333333333*(H/2))
        sw,sh=fit(1080,2652,scr_scale)
        fc=(f"[1:v]scale={sw}:{sh},crop={W}:{H}:{(sw-W)//2}:{max(0,min(sh-H,int((sh-H)/2+scr_ty)))}[bg];"
            f"[0:v]scale={cw}:{ch},crop={d}:{d}:{(cw-d)//2}:{(ch-d)//2 - round(0.0433*ch)}[c];"
            f"[c]format=rgba,geq=r='r(X,Y)':a='if(lte((X-{d//2})*(X-{d//2})+(Y-{d//2})*(Y-{d//2}),{(d//2)**2}),255,0)'[cc];"
            f"[bg][cc]overlay={cx-d//2}:{cy-d//2}[o1];"
            f"[o1]drawbox=x={cx-round(d*1.25)//2}:y={cy-round(d*1.25)//2}:w={round(d*1.25)}:h={round(d*1.25)}:color=white@0.9:t=7[v]")
    else:  # split
        sw,sh=fit(1080,2652,scr_scale)
        camy = round(H/2 + ysign*(-0.5208333333333334)*(H/2))
        line = camy + round(0.5415114961139896*(H/2))
        fc=(f"[1:v]scale={sw}:{sh},crop={W}:{H}:{(sw-W)//2}:{max(0,min(sh-H,int((sh-H)/2+scr_ty)))}[bg];"
            f"[0:v]scale={W}:{H}[cam];"
            f"[bg][cam]overlay=0:{camy-H//2}:enable=1[o];"
            f"[1:v]scale={sw}:{sh},crop={W}:{H-line}:{(sw-W)//2}:{max(0,min(sh-(H-line),int((sh-H)/2+scr_ty)))}[bot];"
            f"[o][bot]overlay=0:{line}[o2];"
            f"[o2]drawbox=x=0:y={line-4}:w={W}:h=8:color=0x6C5CE7@0.95:t=fill[v]")
    subprocess.run(["ffmpeg","-v","error","-y","-ss",str(cam_t),"-i",CAM,"-ss",str(scr_t),"-i",SCR,
        "-filter_complex",fc,"-map","[v]","-frames:v","1",out],check=True)

# scene 1 = circle preset, both y-sign conventions
render("p_circle_ydown.png","circle",125.0,1772.5,1.3811,0,+1)
render("p_circle_yup.png",  "circle",125.0,1772.5,1.3811,0,-1)
# scene 3 = split preset, both y-sign conventions
render("p_split_ydown.png","split",150.0,66.0,1.3811,0,+1)
render("p_split_yup.png",  "split",150.0,66.0,1.3811,0,-1)
for a,b,o,t in [("p_circle_ydown.png","p_circle_yup.png","cmp_circle.png","CIRCLE  y+=down  |  y+=up"),
                ("p_split_ydown.png","p_split_yup.png","cmp_split.png","SPLIT  y+=down  |  y+=up")]:
    subprocess.run(["ffmpeg","-v","error","-y","-i",a,"-i",b,"-filter_complex",
      f"[0]scale=340:-1,drawtext=text='y+ = DOWN':x=6:y=6:fontsize=22:fontcolor=yellow:box=1:boxcolor=black@0.6[l];"
      f"[1]scale=340:-1,drawtext=text='y+ = UP':x=6:y=6:fontsize=22:fontcolor=yellow:box=1:boxcolor=black@0.6[r];"
      f"[l][r]hstack",o],check=True)
print("ok")
