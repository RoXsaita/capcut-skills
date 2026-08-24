# The preview loop

Render → look → fix → repeat. Only write CapCut once the preview is actually good.

> **For still frames, use `capcutctl qa --project NAME --times 3,9,15 --guide 960`.** It
> composites the real timeline outside CapCut and prints every segment's on-canvas rect, so the
> geometry is checked as numbers first. The ffmpeg renderer below is for **full-motion** preview
> — watching the cut play — which `qa` does not do.
## Why

The first build skipped this entirely and produced an unusable edit. Looking at frames catches,
in minutes, errors that are invisible in JSON: wrong crop, wrong moment, a shot drifting onto the
next screen, a black transition frame.
## Split-screen renderer

The user's layout is **screen on top, face on bottom** (see `style.md`). For a 1080×1920
canvas that is two 1080×960 halves.

```
[0:v] crop=1080:960:0:{roi}, setpts=PTS/{speed}, fps=30, setsar=1 [top]
[1:v] scale=1080:1920, crop=1080:960:0:{CAM_Y}, fps=30, setsar=1   [bot]
[top][bot] vstack=inputs=2 [v]
```

- `CAM_Y = 640` was verified as the best face framing for a 1440×2560 source (full face, eyes in
  upper third, shoulders in). y=200 and y=420 both leave too much headroom.
- Source-vs-target duration: **`source_duration = target_duration × speed`**. Same rule as CapCut.
- Render each shot to its own file, then `concat`. Simpler and more debuggable than one giant
  filter graph.

See `scripts/render.py`.
## Audio

Build VO by concatenating the kept beat spans (the timeline skips fumbles, so a single continuous
extract will **not** line up). Then mix SFX with `adelay` + `amix` + `alimiter`.

**Always include SFX in a preview you show the user.** A silent preview was shown once and the
user reasonably asked "where are the sounds" — they existed, but not in what he was handed.
## Verification contact sheets

The actual review step. Sample one frame per shot, label each with its timestamp, tile into a grid,
and look at it.

```python
d.rectangle([0,0,62,17],fill="red"); d.text((3,3),f"{t}s",fill="white")
```

Label everything — timestamps on frames, y-values on ROI candidates, beat numbers on crops.
Unlabeled grids are hard to act on.

Useful sheet types:
- **ROI candidates** — same frame at several crop offsets, with a y-ruler drawn on
- **Per-beat crops** — the chosen moment for every beat, to confirm content matches the VO line
- **End-to-end** — one frame per shot across the whole cut, to catch drift and pacing
## Delivering the preview

`SendUserFile` caps at **30 MiB**. A 75s 1080×1920 render was 83 MB. Downscale for delivery and
keep the full-res master on disk:

```bash
ffmpeg -i master.mp4 -vf scale=720:1280 -c:v libx264 -preset slow -crf 30 \
       -c:a aac -b:a 128k -movflags +faststart preview.mp4     # 83MB -> 4.6MB
```
