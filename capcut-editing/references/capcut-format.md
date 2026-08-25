## Quantise to whole frames using frame-position differences

Timings are integer microseconds and a frame at 30 fps is 33333.33 µs, so `round(frames * 1e6/30)`
per segment accumulates 1 µs errors that read as overlapping segments. Derive each duration as the
**difference of two absolute frame positions**, never by rounding the duration on its own:

```python
us  = lambda f: int(round(f*1e6/30))
dur = us(t+n) - us(t)          # correct: end lands exactly on the next start
# NOT: dur = us(n)             # drifts by 1us and trips the overlap check
```
# CapCut project format

Reverse-engineered and verified working (a built project opened correctly in CapCut).
Undocumented and version-specific — **always back up before writing.**
## Paths

```
~/Movies/CapCut/User Data/Projects/com.lveditor.draft/
  root_meta_info.json          # the draft registry CapCut reads at launch
  <Project Name>/
    draft_info.json            # THE TIMELINE — this is what you edit
    draft_meta_info.json       # per-project media registry + draft_id/name/paths
    draft_cover.jpg
```

SFX cache (reusable, already downloaded):
`~/Library/Containers/com.lemon.lvoverseas/Data/Movies/CapCut/User Data/Cache/music/<md5>.mp3`
## draft_info.json shape

```
duration        # microseconds, int
canvas_config   # {ratio:"9:16", width:1080, height:1920}
fps             # 30.0
materials       # {videos:[], audios:[], speeds:[], canvases:[], common_mask:[], ...}
tracks          # [{id, type:"video"|"audio"|"text", flag, segments:[...]}]
```

**All times are integer microseconds.** Track order = render order; later tracks draw on top.
## Segment anatomy

```python
{
 "id": UUID,
 "material_id": <id in materials.videos/audios>,
 "source_timerange": {"start": us, "duration": us},   # position in the SOURCE file
 "target_timerange": {"start": us, "duration": us},   # position on the TIMELINE
 "speed": 1.0,
 "volume": 1.0,
 "clip": {"scale":{"x","y"}, "rotation", "transform":{"x","y"}, "flip", "alpha"},
 "extra_material_refs": [ ... ],                      # REQUIRED, see below
 "common_keyframes": [ ... ],
 "track_render_index": <track index>,
}
```

### The invariant that matters

```
source_timerange.duration == target_timerange.duration * speed
```

Violate it and speed ramps corrupt. Validate this on every segment before saving.

### extra_material_refs

Every segment needs a bundle of side-materials, each a real entry in `materials` with a unique id.
Missing refs = broken project.

- **video**: `speeds`, `placeholder_infos`, `canvases`, `material_animations`,
  `sound_channel_mappings`, `material_colors`, `vocal_separations`
- **audio**: `speeds`, `placeholder_infos`, `sound_channel_mappings`, `loudnesses`,
  `vocal_separations`

Easiest correct approach: deep-copy a donor entry from an existing working project, then replace
its `id`. See `scripts/build.py` (`refs_for`).
## Keyframes (punch-in / pan)

```python
{"id":UUID, "material_id":"", "property_type":"KFTypeScaleX",
 "keyframe_list":[{"id":UUID,"curveType":"Line","time_offset":0,
                   "left_control":{"x":0,"y":0},"right_control":{"x":0,"y":0},
                   "values":[1.0],"string_value":"","graphID":""}, ...]}
```

`time_offset` is microseconds **relative to the segment start**. Property types seen in the
user's own projects: `KFTypePositionX`, `KFTypePositionY`, `KFTypeScaleX`, `KFTypeScaleY`,
`KFTypeRotation`. For a punch-in, animate ScaleX **and** ScaleY together.
## Masks (split-screen)

A `common_mask` entry referenced from `extra_material_refs`. The user's split-screen uses the
built-in **`Split`** line mask — the exact config is `presets/layouts.json` and `capcutctl layout split-screen` applies it.
## Validation before saving

1. every `material_id` and every `extra_material_refs` id exists in `materials`
2. no overlapping `target_timerange` within a track
3. the speed invariant above
4. drop tracks with zero segments (CapCut carries empty ones through duplication)
## Registration (getting CapCut to see a new project)

1. `cp -R "Preset 3" "New Project"` — duplicating a real project is far safer than building
   `draft_meta_info.json` from nothing.
2. Update `draft_meta_info.json`: new `draft_id` (UUID), `draft_name`, `draft_fold_path`,
   `tm_draft_create/modified`, and append source media to the `type: 0` bucket in `draft_materials`.
3. Add an entry to `root_meta_info.json` → `all_draft_store`:
   `{draft_cover, draft_fold_path, draft_id, draft_json_file, draft_name, tm_draft_create, tm_duration}`

### CapCut must be closed for step 3

CapCut **rewrites `root_meta_info.json` when it quits**, erasing your entry. Writing the project
folder while it runs is fine; registering is not.

Good pattern — poll for exit, then register, so the user doesn't have to come back:

```python
while subprocess.run(["pgrep","-x","CapCut"],capture_output=True).returncode==0:
    time.sleep(2)
time.sleep(4)   # let CapCut finish its own write
```
## Shifting a preset outro to the end

Add `delta = new_content_end - old_outro_start` to `target_timerange.start` of every existing
segment, then recompute `duration` as the max end across all tracks.
## CapCut keeps a second copy of the timeline — write BOTH or your edit silently reverts

This cost a full rebuild. The project folder contains:

```
<Project>/
  draft_info.json                       # what you naturally edit
  template-2.tmp                        # byte-identical mirror
  Timelines/project.json                # timeline registry
  Timelines/<timeline-uuid>/
    draft_info.json                     # <-- CapCut RESTORES FROM THIS ON OPEN
    draft_info.json.bak
    template-2.tmp
```

Editing only the top-level `draft_info.json` while CapCut is closed **looks like it worked** — the
file on disk is correct. But the next time CapCut opens the project it reads
`Timelines/<uuid>/draft_info.json` and writes it back over the top-level file. The edit is gone,
with no error and no prompt.

**Always write every copy:**

```python
targets = [f"{P}/draft_info.json", f"{P}/template-2.tmp"]
for tdir in glob.glob(f"{P}/Timelines/*/"):
    for f in ("draft_info.json", "draft_info.json.bak", "template-2.tmp"):
        if os.path.exists(tdir+f): targets.append(tdir+f)
for t in targets: open(t,"w").write(blob)
```

Verify afterwards with `md5 -q` across all of them — they must match.

### The timeline UUIDs are NOT per-project

`Timelines/project.json` carries an `id` and `main_timeline_id` that are **identical across every
project in the folder** (verified against CapCut's own duplicates: `0411` and `0411-copy` share
both). Only `draft_meta_info.json` → `draft_id` is unique. So when duplicating a project folder,
regenerate `draft_id` and leave the timeline UUIDs alone.
## Duplicating a project into a new one

```
cp -R "<Source>" "<New Name>"
cd "<New Name>"
rm -f .locked draft_info.json.bak *.BACKUP.json     # stray locks and backups
```

then in `draft_meta_info.json` set: new `draft_id` (UUID), `draft_name`, `draft_fold_path`,
`tm_draft_create`, `tm_draft_modified`, `tm_duration`. Everything else — including
`draft_root_path` and the whole `draft_materials` bin — carries over correctly.

Finally append to `root_meta_info.json` → `all_draft_store`, easiest by deep-copying the source
project's entry and overriding `draft_fold_path`, `draft_id`, `draft_name`, `tm_draft_create`,
`tm_duration` (and `draft_cover` / `draft_json_file` if the entry has them).

**CapCut must be fully quit for that last step** — it rewrites `root_meta_info.json` on exit.
Closing the project back to the home screen is not enough.

## Clip geometry — the exact model (measured, 2026-08-24)

Verified against `capcut-editor-cli/presets/suheil-vertical.json` to within 1px on the
card avatar (`205x364` predicted vs `205x364` recorded, left 137.2 vs 138).

```
k0        = min(W/sw, H/sh)          # scale 1.0 == FIT whole source inside canvas
displayed = (sw*k0*scale.x, sh*k0*scale.y)
centre    = (W/2 + tx*(W/2),  H/2 - ty*(H/2))
```

**`transform` is in half-canvas units and `y` is positive UP.** On 1080x1920, `ty=+0.5`
puts the clip centre at y=480 (upper half), `ty=-0.5` at y=1440.

Consequences worth remembering:

- To fill exactly half the canvas with a `1080x900` source: `scale = 960/900 = 1.06667`,
  `transform.y = +0.5` (top half). It bleeds to 1152 wide and the canvas crops it.
- A frame PNG whose artwork is centred in its own 1080x1920 canvas stays concentric with
  anything sharing its `transform`. Aligning a frame to its content is usually a
  one-value fix, not a resize.
- `crop` lives on the **material**, not the segment. Segments carry `crop: null`.

## Starting a video

`capcutctl new --project NAME --media FILE --scenes 0:6@122.4,6:12,12:18` clones
**Preset 3**, slides its endcard to sit right after the new scenes, registers the draft
so CapCut lists it, and prints `contentTrack` — the track your scenes landed on, which
the layout commands need. `--blank` for an empty timeline.

New scenes never inherit the template's mask/effect/animation materials. Preset 3's
backdrop segment carries a Blur; cloning it wholesale blurs every scene in the project.

## The three layouts are a command, not a judgement call

`capcutctl layout split-screen | circle | background` writes the exact measured
geometry from `presets/layouts.json` (captured from `grok-build-claude`). Do not
hand-compute these numbers again — and do not invent new ones.

| | subject | companion |
|---|---|---|
| `split-screen` | `scale 1.0`, `transform.y -0.5208333333333334`, `Split`/line mask `centerY 0.5415114961139896` `rotation 180` → fills the BOTTOM half from y=960 | indigo bar, `scale (1.8272246516061672, 0.7521039538453399)`, `transform.y -0.6036269430051813` |
| `circle` | `scale 0.19`, `transform (-0.5559524128804151, 0.6442708333333333)`, `Circle` mask `height 0.5618028307506959` `centerY -0.04329882358536104` | white ring, `scale 0.2728009828009824`, `transform (-0.5559524128804151, 0.6328125)`, **plus its own circle mask** |
| `background` | — | blurred copy of the subject, `scale 1.12`, `alpha 0.72`, `Blur` effect, on a track BELOW |

```bash
capcutctl scenes  --project NAME                       # what each scene currently is
capcutctl layout split-screen --project NAME --at 1.5 --track 8
capcutctl layout background   --project NAME           # auto-finds circle+ring scenes
```

The white ring carries a circle mask of its own. `grok-build-gpt`'s hand-built rings
do not, which is why they sit ~5px off their avatars; re-running `layout circle`
repairs that.

## Mask coordinates

`centerX`/`centerY` are **half-clip** units with y positive UP — the same convention as
`transform`. `width`/`height` are **full-clip fractions** (circle x-diameter = `width*w`).
Mixing these up puts the split seam at y=420 instead of y=960.

## Z-order: unresolved, so make it moot

`render_index` (lower = further back) and track order disagree in `grok-build-gpt`:
track 3 is a 72%-alpha blurred face with `render_index 18`, the highest. Under
render_index ordering it covers the whole frame; under track ordering the project looks
correct — and the correct look is what the user sees. `track_render_index` only mirrors
track position, so it does not discriminate.

**Do not rely on either model.** Keep `render_index` monotonic with track order so both
resolve identically. Check it before shipping a project you did not build.

## The layer stack — measured from `Hermes-agent`

`Hermes-agent` is the reference: it contains every layout (split screen, circle inset,
full face) and the user calls it the masterpiece of the set. Its stack, verified against
the JSON and against the CapCut timeline he screenshotted:

| track | content | note |
|---|---|---|
| 0 | main — **always empty** | he calls it "the cover" and never uses it |
| 1 | blurred backdrop (the face again, under an effect) | furthest back |
| 2 | screen-recording B-roll | `attribute: 1` (muted) |
| 3 | indigo rect **when it frames the screen recording** | circle-inset scenes only |
| 4 | **the talking head — carries every transition** | gapless, spans the timeline |
| 5 | plates on top: indigo rect in split scenes, white circle ring in circle scenes | absolute front |

**Higher track index renders in front, and the CapCut UI draws the highest index as the
top row.** This resolves the ambiguity in the section above for real projects: track order
is the model that matches what he sees.

The indigo rect appears at two different heights because it does two different jobs:

- framing the **screen recording** (circle-inset scenes) → *below* the face, `s=(1.05, 0.75) t=(0, 0)`
- framing the **talking head** (split-screen scenes) → *above* the face, `s=(1.4777, 0.7211) t=(-0.0710, -0.5725)`

His words: *"the purple cover usually sits at the absolute top … however, in case the scene
is the [circle] talking head, then the purple cover sits in the middle on top of the screen
recording, but under the talking head."* Both halves check out against the JSON.

## Transitions belong to one track

All **9** of Hermes-agent's transitions sit on track 4, the talking head. None sit anywhere
else, and none are orphaned. Two rules follow, and `capcutctl polish` now enforces both:

1. **One layer.** A transition affects the composite from its own layer down. Split across
   layers, each wipe fires alone while the others cut straight through it — a B-roll that
   dissolves under a face that jumps.
2. **A clip on both sides.** A transition on a segment with nothing after it on its own
   track is *silently discarded by CapCut on load*. The project is correct on disk and
   wrong the moment it opens. This cost a payoff cue in `grok-build-final` — 15 written,
   14 survived — and was invisible until the transitions were counted after a re-save.

Hermes achieves (2) by slicing the face at every visible cut **even where the face content
runs straight through**: five of its segments 0.00–8.80 are the same file at the same
geometry, cut only so the transitions have boundaries to live on. `polish` reproduces this
(`sliced` in its result) and the cut is frame-continuous, so nothing moves in the picture.

`doctor` checks: `TRANSITION_ORPHANED` (error), `TRANSITION_OFF_PRINCIPAL` (warn),
`TRANSITION_BELOW_TOP` (warn — a higher track of *moving picture* cutting bare through the
wipe; plates and PNG frames swapping with the layout are expected and exempt).

## Rendered-pixel QA

`capcutctl qa` composites any timeline frame outside CapCut and prints each
segment's on-canvas rect. `capcutctl doctor` validates structure only — it passed clean
on a split that was 900/1020 instead of 960/960 and on a frame 47px off its content.
Numbers first, then look at the frame.

```bash
capcutctl qa --project grok-build-gpt --times 1.5,6,41.5 --guide 960 --out qa/
```
