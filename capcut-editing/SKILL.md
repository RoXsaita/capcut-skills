---
name: capcut-editing
description: >
  Edit real video projects by writing CapCut's project JSON directly, so the user finishes in the
  CapCut UI he actually likes. THE HUB — start here for any CapCut editing request. Covers why
  this exists, the non-negotiable rules, the draft_info.json schema, the user's measured style,
  pitfalls, and current project state. The write path itself is `capcutctl` — read capcut-cli
  before touching JSON. For cutting the talking head use capcut-editing-talking-head; for
  screen-recording B-roll use capcut-editing-screen-recording.
---

# CapCut Editing — hub

Programmatic video editing that hands off cleanly to a human.

## First: install, then ask which style

If `capcutctl` is not on PATH, clone and `npm link` [capcut-editor-cli](https://github.com/RoXsaita/capcut-editor-cli) (see its `SETUP.md`). It needs Node 20+ and **ffmpeg**.

Then run `capcutctl preflight` once. It reports the dependencies, the bundled overlay artwork,
the SFX palette and the drafts folder, and names the fix for anything missing. The layouts work
on any machine; the SFX palette is CapCut's per-machine cache, so `polish` may report
`unavailableSfx` and place no sound — that is a degraded edit, not a broken one, and it belongs
in the hand-off. See `capcut-cli`.

Then **ask the user, once, before writing a project**:

1. **Keep the bundled house style** (Suheil / suheilai) — `style.md`, `presets/layouts.json`, `polish` / `pace` / `wrap` as documented. Default if they already edit this way.
2. **Harvest their own CapCut edits** — `capcutctl harvest`, then treat *their* drafts as the style source. Do not apply the bundled seam formula or branded endcard unasked.
3. **Build their own style** — `capcutctl new --blank` (or `--from` a draft they name). Skip `polish` / `wrap` until they say what they want.

Do not silently apply option 1 to a stranger.

## Why this exists

The deliverable is a *CapCut project*, not a rendered file. Code-render tools
(HyperFrames, Remotion) cannot hand the edit back to CapCut's UI. CapCut stores
projects as plain JSON on disk, which is what `capcutctl` writes.

## The family

| Skill | Use it for |
|---|---|
| **capcut-cli** | **`capcutctl` — what is already automated: create a project, the three locked layouts, scene listing, snapshots. Check here BEFORE hand-writing JSON.** |
| **capcut-editing** (this one) | The format, the safe write path, his style, pitfalls, project state |
| **capcut-editing-talking-head** | Cutting the face: the 3 indexes, seam linting, the locked cut procedure, the 3 layout presets |
| **capcut-editing-screen-recording** | B-roll: OCR index, ROI, content matching, `capcutctl find`. **The editing half is still unsolved — read its status table first.** |

## The four rules

**0. Overlays only.** His main track is **always empty**. He calls the main track "the cover" and
never uses it — every clip goes on an overlay track (`flag=2`). Confirm against `Preset 3`
(main track `n=0`). See `references/style.md`.

**1. Never build blind.** The first attempt failed ("quality is like 1/100") because 83 seconds of
timeline were written from arithmetic and handed over without a single frame being looked at.
Render an ffmpeg preview → **look at the frames** → fix → repeat → only then write CapCut.
See `references/preview-loop.md`.

**2. Edit quality == index quality.** Every cut you cannot verify is a guess, and guesses are
where the errors were. Never derive geometry either — render it and compare against a frame you
know is right.

**3. Every edit happens INSIDE CapCut.** His words, after the AI Video Editor video:

> *"the videos were cropped outside of CapCut… I cannot edit it after. I have to re-figure out
> where the fuck is the video."*

The deliverable is a project he finishes by hand. That only holds if every decision is still a
CapCut property he can drag. Anything you flatten into the pixels before import is a decision
he can no longer take back, and `doctor` cannot see it, because the picture is *correct* — it
is just frozen. **ffmpeg renders previews. It never produces media that goes into the project.**

| Tempting ffmpeg pass | What it costs him | The CapCut-native verb |
|---|---|---|
| `crop=` to the split-screen half | Cannot reframe, re-zoom, or move the scene to another layout — those rows are gone | `capcutctl layout broll --row PIXEL_ROW` (writes `clip.scale` + `clip.transform` + the seam mask) |
| `crop=` a landscape/window capture | Same, plus the measured window treatment is lost | `capcutctl layout screen --media FULL.mp4` |
| `-ss`/`-t` to cut a subclip | He can only extend inside the window you chose | `add --src S --dur S` — the segment's `source_timerange` on the whole file |
| `setpts=`/`atempo=` for speed | Speed stops being a slider | `add --cover IN-OUT`, or `capcutctl pace` |
| `zoompan` for a punch-in | A camera move he cannot retime | `capcutctl keyframe --to 2.4 --hold 1.6` |
| `concat` a montage | One clip where there were eight | one `add` per shot |

Import the **full-frame original**, from a path that still exists next week. `add` and
`replace-media` now enforce this: media exactly half the canvas is refused as `PREFRAMED_MEDIA`,
and a source in `/tmp` or a session scratchpad is refused as `EPHEMERAL_MEDIA` — that is how the
last project lost the trail back to its screen recordings for good. `--generated` is the honest
escape for a Remotion/AE render with no editable original; `--derived-from ORIGINAL` records the
source when pre-processing really was unavoidable. `capcutctl doctor` reports both faults on
projects built before the contract existed.

## The CLI — the only sanctioned way to write

**`capcutctl`.** Read `capcut-cli` for the full surface. The short version:

```bash
capcutctl cut VIDEO --lang ar                    # A-roll: index, review table
capcutctl cut VIDEO --keep 0,2-9 --project NAME  # A-roll: build the project
capcutctl add --project NAME --media FILE --at S --dur S --track broll
capcutctl layout auto|split-screen|circle|background --project NAME
capcutctl polish|pace|wrap --project NAME
capcutctl timeline|finish|music --project NAME   # last pass: ASCII, scorecard, generated bed
capcutctl scenes|inspect|doctor --project NAME
capcutctl qa --project NAME --times 3,9,15       # composite real frames
capcutctl snapshot|history|restore --project NAME
```

`--track` is a name or an index. Read `capcut-cli` before reaching for `apply --spec`.

Every write is snapshotted, applied to the root draft and the active timeline as separate
documents, staged, re-parsed, atomically renamed, doctored, and rolled back on failure. It
refuses to run while CapCut is open.

**Never hand-roll a project writer, and never hand-write `draft_info.json`.** If `capcutctl`
cannot express the edit, extend it — the layouts got built exactly that way, by capturing a
verified structure out of a real project instead of inventing one.

### Legacy scripts

`scripts/` still holds the one-off tools this grew out of (`capcut.py`, `build.py`, `render.py`,
`to_overlays.py`, the `vo_*` pair, …). They predate `capcutctl` and are kept for reference and
for the few things it does not do yet. `scripts/audio_index.py` is still live — `capcut.py`
imports it. Prefer `capcutctl` for anything it covers.

## Workflow

1. **Cut the A-roll** — `capcutctl cut VIDEO`, review the table, re-run with `--keep`.
   Face stays **1×**. See `capcut-editing-talking-head`.
2. **Stop and get the cut signed off.** He watches the talking head in CapCut and confirms
   the keep list. Do not start B-roll, layouts, or finish until he has. The face is the
   timeline's clock; everything else hangs off it.
3. **Give the scenes their looks** — `capcutctl layout …`. The first picture is proof
   (split-screen or circle + 80% recording), not a 5s+ full-face talking-head. `finish`
   reports a cold-open if you miss this.
4. **Look at frames** — `capcutctl qa`. `doctor` validates structure and cannot see the picture;
   two real defects passed it clean.
5. **Finish** — `capcutctl finish --project NAME`, then `polish --motivated` and `finish --music`.
   Picture-locked first. Music is generated to the picture; speech is never recut to a beat.
   Captions stay outside CapCut. See `references/finish.md`.
6. **Look at the finished frames** — those last-pass writes change the picture. Run
   `capcutctl timeline`, then `capcutctl qa` at the new seams / music-in / CTA, then a mute
   watch. `doctor` cannot see transition, track-slice, or music-placement defects.
7. **`capcutctl doctor`** must be error-free before you hand it over.

Work **one section at a time** and check end-to-end. He asked for this explicitly.

## Reference files

| File | Use it for |
|---|---|
| `references/capcut-format.md` | draft_info.json schema, segments, masks, keyframes, the multi-copy write, registration |
| `references/style.md` | Rule zero, his measured signature, SFX palette |
| `references/finish.md` | Last pass: motivated seams, ASCII timeline, generated beat-aligned bed |
| `references/preview-loop.md` | Full-motion ffmpeg preview and contact sheets (frame checks are `capcutctl qa`) |
| `references/pitfalls.md` | Concrete traps already hit. Read before starting. |
| `references/project-state.md` | Sources, the signed-off VO EDL, what is done and what is not |

`scripts/` — legacy one-offs, see `scripts/README.md`. The live tooling is `capcutctl`.
