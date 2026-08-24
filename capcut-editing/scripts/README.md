# Scripts

## Start here: `capcut.py`

One deterministic entry point. Use it instead of hand-rolling a script — every command below
existed as ad-hoc code first, and each rewrite was a chance to drop a step.

```
capcut.py spans   <proj>              the live EDL
capcut.py lint    <proj>              energy-lint every seam
capcut.py strip   <proj> [a] [b]      ASCII energy map
capcut.py preview <proj> [out.mp4]    render the VO from live spans
capcut.py sheet   <proj> [out.png]    contact sheet of every cut frame
capcut.py verify  <proj>              structure + all-copies md5
capcut.py backup  <proj> [tag]
capcut.py write   <proj> <new.json> [--wait]
```

**`write` is the only sanctioned way to modify a project.** It validates first and refuses on
error, refuses while CapCut is running (unless `--wait`, which blocks — background it), writes
**every** timeline copy, updates meta + registry, keeps a pre-write backup, and md5-verifies.

`verify` checks rule zero (main track empty), material/ref integrity, track overlaps, the speed
invariant, and that no two segments share a side-material. It found a real bug the first time it
ran: two still segments whose `source_timerange` was inherited from a donor and no longer matched
their placed duration — CapCut would have truncated the frames mid-scene.

## Other runnable scripts

| File | What it does |
|---|---|
| `audio_index.py` | **The audio energy index + cut linter.** Self-contained, cached, no deps beyond stdlib+ffmpeg. `python3 audio_index.py <media> [a b]` prints an ASCII strip. Import `AudioIndex` / `lint`. |
| `vo_plan.py` | The signed-off VO cut as data: spans, labels, and what was dropped with the reason. `python3 vo_plan.py` prints the EDL. |
| `vo_cut.py` | Renders `vo_plan` spans to a single ffmpeg concat (video+audio, frame accurate). |
| `vo_rebuild_capcut.py` | Writes a VO cut into a CapCut project — retimes the cam track, drops B-roll/SFX, re-anchors the outro, prunes and de-dupes materials, writes **every** timeline copy. Takes the project path as argv[1]. |
| `to_overlays.py` | Moves everything off the main track onto overlay tracks (rule zero). Idempotent-ish; read before re-running. |
| `presets.py` | Applies the CIRCLE / SPLIT layout presets by copying `clip`+`uniform_scale` from a reference segment and attaching a **private** mask copy. The pattern to reuse. |
| `layout_preview.py` | ffmpeg composite of a layout so you can look before writing CapCut. Masks approximated with `geq` alpha — fine for position/size, not feather. |

## Reference implementations (paths point at a dead scratchpad — read, do not run)

| File | What it does |
|---|---|
| `match.py` | OCR index loader, `spans()` content search, `roi_for()` TSV ROI hint |
| `render.py` | ffmpeg split-screen preview renderer (`shot()` / `render()`) |
| `build.py` | CapCut writer from scratch — materials, `refs_for()` bundles, `mkseg()`, keyframes, outro shift |
| `full.py` | An EDL as data: beats → (vo span, b-roll shots) |
| `beats.py` | Beat → screen-content keyword spec |

Start from `build.py::refs_for` and `build.py::mkseg` — they encode the parts of the CapCut schema
that are easiest to get wrong.

## Order of use on a fresh video

```
audio_index.py  ->  vo_plan.py  ->  vo_cut.py  ->  (look / re-transcribe)
                ->  vo_rebuild_capcut.py  ->  to_overlays.py  ->  presets.py
```
