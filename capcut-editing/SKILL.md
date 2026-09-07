---
name: capcut-editing
description: >
  Edit real video projects with capcutctl, preserving native CapCut properties so the user finishes in the
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
| **capcut-cli** | **`capcutctl` — what is already automated: create a project, the locked layouts, scene listing, snapshots. Check here BEFORE hand-writing JSON.** |
| **capcut-editing** (this one) | The format, the safe write path, his style, pitfalls, project state |
| **capcut-editing-talking-head** | Cutting the face: deterministic mechanics, semantic keep/order review, escalation diagnostics, and the 3 layout presets |
| **capcut-editing-screen-recording** | B-roll: OCR index, ROI, content matching, `capcutctl find`. **Semantic matching requires inspected source evidence.** |

**Colour lives in `capcut-cli` (`grade`).** Preserve source colour by default.
Scopes help diagnose exposure; whole-frame RGB averages do not establish correct
skin colour or justify changing UI whites. Use explicit correction and compare in
CapCut. The native Adjust material structure must not be hand-written.

## The four rules

**0. Overlays only.** His main track is **always empty**. He calls the main track "the cover" and
never uses it — every clip goes on an overlay track (`flag=2`). Confirm against `Preset 3`
(main track `n=0`). See `references/style.md`.

**1. Doctor-gated handoff.** Build the editable project, run `capcutctl doctor`, and when it is
error-free, tell the user the project is available in CapCut. For B-roll, layouts, crops, and
finish work, render/composite representative frames with `qa` because `doctor` cannot see the
picture. Full preview renders, contact sheets, and render re-transcription are targeted
diagnostics when playback or lint identifies a risk; they are not mandatory before every
ordinary A-roll build. See `references/preview-loop.md`.

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
capcutctl cut VIDEO --keep 0,2-9 --order 0,2,3,4,5,6,7,8,9 --dry-run
capcutctl cut VIDEO --keep 0,2-9 --order 0,2,3,4,5,6,7,8,9 --project NAME
capcutctl add --project NAME --media FILE --at S --dur S --track broll
capcutctl layout auto|split-screen|circle|background --project NAME
capcutctl polish|pace|wrap --project NAME
capcutctl grade    --project NAME [--measure] [--apply]   # colour: preserve unless explicitly corrected
capcutctl timeline|finish|music --project NAME   # last pass: ASCII, scorecard, generated bed
capcutctl scenes|inspect|doctor --project NAME
capcutctl qa --project NAME --times 3,9,15       # composite real frames
capcutctl snapshot|history|restore --project NAME
```

`--track` is a name or an index. Read `capcut-cli` before reaching for `apply --spec`.

Transactional project edits are snapshotted, applied to the root draft and the active timeline as separate
documents, staged, re-parsed, atomically renamed, doctored, and rolled back on failure. It
refuses to run while CapCut is open.

**Never hand-roll a project writer, and never hand-write `draft_info.json`.** If `capcutctl`
cannot express the edit, extend it — the layouts got built exactly that way, by capturing a
verified structure out of a real project instead of inventing one.

### Retired scripts

The legacy Python helpers were removed: their writers bypassed transactions and their
indexes/previews had diverged from the CLI. Use `capcutctl cut`, `find`, `qa` and `preview`.
For implementation details, inspect the maintained `tools/` and `src/` in the CLI repository.
See [the migration map](scripts/README.md).

## Workflow

1. **Cut the A-roll** — `capcutctl cut VIDEO`, read the full script, then dry-run and build with
   `--keep` plus `--order` when the story differs from source order. Use safe inward
   `--trim-beat` only for a justified edge. Face stays **1×**. Before handoff, read back the
   current script with the existing `capcutctl scenes --project NAME --track CONTENT_TRACK
   --transcript`; compare its timeline-order `says` rows with the raw word-level transcript and
   remove accidental repeats, false starts, and filler by recutting the A-roll. This is an audit
   feed, not proof: overlapping transcript segments can repeat words at clip boundaries. Re-run
   it after any user tweak, then run `capcutctl doctor`; when it is error-free, tell the user the
   project is available in CapCut. See `capcut-editing-talking-head`.
2. **Stop and get the cut signed off.** Hand off the project and wait for the user to confirm
   the keep list. Do not start B-roll, layouts, or finish until then. The face is the timeline's
   clock; everything else hangs off it.
3. **Give the scenes their looks** — `capcutctl layout …`. The first picture is proof
   (split-screen or circle + 80% recording). Bind each narration phrase to an inspected
   action/result using the [screen-recording skill](../capcut-editing-screen-recording/SKILL.md).
   Compress waiting, keep actions legible, and hold results until they can be understood.
   Pick one focus per shot; a zoom or highlight must point to that focus. `finish` checks
   opening coverage; it cannot verify that the picture proves the words.
4. **Look at frames** — `capcutctl qa`. `doctor` validates structure and cannot see the picture;
   two real defects passed it clean.
5. **Check colour** — measure if a source looks wrong, then make a small explicit
   correction with `grade --set`. Default `grade` leaves sources unchanged. Compare
   before/after in CapCut; the proxy's slider model is approximate. Preserve screen
   recordings unless a specific capture defect needs correction.
6. **Finish** — run `finish` and review the proposed seams before applying polish.
   A picture change is eligible for a transition; a clean cut is still a valid choice.
   Choose music from the story: mood, energy arc, texture and pacing. Pass that brief with `music --prompt`
   or use a suitable local track with `music --file`. Avoid a generic tech-demo bed.
   Balance the voice first, then the bed and SFX underneath it. Picture stays locked;
   speech is never recut to a beat. See `references/finish.md` for mixing and selected seams.
7. **Watch the finished edit** — check changed frames with `qa`, then play the current
   project in CapCut at normal speed, with sound, at phone size. Check proof readability,
   cut syllables, music/SFX balance and native effects. Inspect the actual export too.
   A proxy or a clean `doctor` result cannot replace this playback check. If native playback
   is unavailable, report it as pending instead of claiming the edit passed.
8. **`capcutctl doctor`** must be error-free before you hand it over.

Work **one section at a time** and check end-to-end. He asked for this explicitly.

## Reference files

| File | Use it for |
|---|---|
| `references/capcut-format.md` | draft_info.json schema, segments, masks, keyframes, the multi-copy write, registration |
| `references/style.md` | Rule zero, his measured signature, SFX palette |
| `references/finish.md` | Last pass: motivated seams, ASCII timeline, generated beat-aligned bed |
| `references/preview-loop.md` | Bounded frame/proxy checks and final native playback |
| `references/pitfalls.md` | Concrete traps already hit. Read before starting. |
| `references/project-state.md` | How to inspect current sources, timeline state and local caches |

`scripts/README.md` maps retired helpers to the maintained CLI commands.
