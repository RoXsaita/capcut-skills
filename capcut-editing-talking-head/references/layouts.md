# The three layout presets (LOCKED)

> **Do not apply these by hand.** `capcutctl layout circle|split-screen|background` writes them.
> The machine-readable source of truth is `presets/layouts.json` in the capcutctl repo, measured
> verbatim from `grok-build-claude`. This file is the *record of what the numbers mean* — read it
> to understand or to verify, not to copy-paste.
>
> ```bash
> capcutctl layout circle       --project NAME --at 12 --track 7
> capcutctl layout split-screen --project NAME --at 30 --track 7
> capcutctl layout background   --project NAME      # blurred plate under circle scenes
> ```

Every scene uses exactly one of these. They describe **where the talking head goes** — B-roll is a
separate decision and is not part of the preset.

His method, verbatim: *"I copy the attributes of the circular small talking head, and just paste
it, then I copy the white frame, and it's like 99.9% of the times fits perfectly."* The numbers
are **copied, never recomputed** — which is precisely why they are now data in a file rather than
something an agent retypes.
## Preset 1 — CIRCLE (small head + white frame)

**Always put the white circle over it. Always.** The two are one unit; a circle without its frame
is wrong.

```python
# the cam segment
clip = {"scale": {"x": 0.19, "y": 0.19},
        "transform": {"x": -0.5559524128804151, "y": 0.6442708333333333}}
uniform_scale = {"on": True, "value": 1.0}
mask = {"name": "Circle", "resource_type": "circle", "config": {
        "width": 1.0032193406262426, "height": 0.5618028307506959,
        "centerX": 0.0, "centerY": -0.04329882358536104,
        "rotation": 0.0, "feather": 0.0, "expansion": 0.0,
        "roundCorner": 0.0, "invert": False, "aspectRatio": 1.0}}

# the white frame -- suheilai-circle-white-1080x1920.png, same timerange, render_index ABOVE the cam
clip = {"scale": {"x": 0.2728009828009824, "y": 0.2728009828009824},
        "transform": {"x": -0.5559524128804151, "y": 0.6328125}}
mask = {"name": "Circle", "resource_type": "circle", "config": {
        "width": 0.8681592039800995, "height": 0.48616915422885576,
        "centerX": 0.01608984799212853, "centerY": 0.0392156862745098, ...}}
```

Note the frame sits 0.0114 higher than the head — that offset is deliberate, keep it.
## Preset 2 — FULL

Nothing to do. `scale 1.0`, `transform (0,0)`, no mask. This is the default state of a clip.
## Preset 3 — SPLIT (head on top + purple frame)

```python
# the cam segment
clip = {"scale": {"x": 1.0, "y": 1.0}, "transform": {"x": 0.0, "y": -0.5208333333333334}}
mask = {"name": "Split", "resource_type": "line", "config": {
        "width": 0.28, "height": 0.0,
        "centerX": -0.004608294930875577, "centerY": 0.5415114961139896,
        "rotation": 180.0, "feather": 0.0, "expansion": 0.0,
        "roundCorner": 0.0, "invert": False, "aspectRatio": 1.0}}

# the purple frame -- suheilai-rect-indigo-1080x1920 (2).png, same timerange, render_index ABOVE cam
clip = {"scale": {"x": 1.8272246516061674, "y": 0.7521039538453399},
        "transform": {"x": 0.0, "y": -0.6036269430051813}}
uniform_scale = {"on": False, "value": 1.0}      # non-uniform -- do NOT force uniform
```

The split line position is **not derived here on purpose.** These values came from a scene the
user positioned by hand; copy them and let CapCut place the line. An attempt to compute it from
transform + mask arithmetic produced a confidently wrong answer.
## Geometry conventions (verified, not assumed)

- `scale: 1.0` means **fit the whole clip inside the canvas**, not fill. A 1080x2652 source in a
  1080x1920 canvas lands at 782x1920 with side bars.
- `transform` is in **half-canvas units**: `x * 540`, `y * 960` for a 1080x1920 canvas.
- **`y` positive = UP.** Verified by rendering the endcard both ways and matching against a
  reference frame the user supplied: `y = +0.6443` puts the circular head at the **top-left**,
  straddling the purple frame's corner. The opposite sign puts it bottom-left, which is wrong.
  (An earlier note here claimed DOWN, derived from split-line arithmetic. That derivation was
  wrong. Do not re-derive geometry — render it and look.)
- Mask `centerY` is relative to **half the clip height**, in the clip's own space.
- Mask configs transfer between clips of the same aspect ratio without change — the endcard's
  source is 1080x1920 and the cam is 1440x2560, both 9:16, which is why paste-in-place works.
## Applying a preset in code

Copy `clip` and `uniform_scale` wholesale from the reference segment, then attach a **private
copy** of the mask (new UUID). Never let two segments share one `common_mask` entry, or moving one
moves the other. See `scripts/presets.py`.
## The CIRCLE preset's full composition

A small circle is almost never alone. Its standard completion — the user: *"usually, when there's
a small circle, it's followed by an 80% screen recording"* — is four layers, and the Preset 3
endcard (around 1:00 in the timeline) is the canonical instance of it. Copy from there.

Bottom to top by `render_index`:

| # | Layer | scale | transform | uniform | notes |
|---|---|---|---|---|---|
| 1 | MacBook screen recording | `0.80` | `(0, 0)` | on | centred |
| 2 | purple frame `suheilai-rect-indigo-1080x1920 (2).png` | `(1.05, 0.75)` | `(0, 0)` | **off** | border around the recording |
| 3 | talking head, `Circle` mask | `0.19` | `(-0.5559524, 0.6442708)` | on | **top-left** |
| 4 | white circle frame, `Circle` mask | `0.2728010` | `(-0.5559524, 0.6328125)` | on | rides 0.0114 lower |

The circle deliberately **overlaps the frame's top-left corner** — it is not inset. See the user's
reference frame; this is the look.

Note the purple frame here is `(1.05, 0.75)`, which is **not** the SPLIT preset's frame
`(1.8272, 0.7521)`. Two different framings of the same PNG. Do not mix them up.

### Why the screen recording is always 0.80

He records with **Recording Layout**, which pins the capture to fixed bounds every time, so every
MacBook screen recording arrives at the same dimensions (the endcard's is 1440x1998). That is what
makes a single hard-coded scale safe across videos — there is no per-clip fitting to do. If a
recording ever arrives at different dimensions, it did not come from Recording Layout and the 0.80
does not transfer.
## Rendering a preview of these layouts

`scripts/layout_preview.py` composites a preset in ffmpeg so you can look before writing CapCut.
It approximates masks with `geq` alpha circles — good enough for position and size, not for
feather. **Always sanity-check a preview against a real frame** before trusting its geometry; the
sign-convention error above survived one preview precisely because nothing was compared to ground
truth.
