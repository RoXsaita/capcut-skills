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

## Why this exists

He rejects code-render tools (HyperFrames, Remotion) for this work — not because they can't
render, but because **he can't take over and finish the edit in a good UI**. He edits in CapCut.
So the deliverable is a *CapCut project*, not a rendered file. This works because CapCut stores
projects as plain JSON on disk.

## The family

| Skill | Use it for |
|---|---|
| **capcut-cli** | **`capcutctl` — what is already automated: create a project, the three locked layouts, scene listing, snapshots. Check here BEFORE hand-writing JSON.** |
| **capcut-editing** (this one) | The format, the safe write path, his style, pitfalls, project state |
| **capcut-editing-talking-head** | Cutting the face: the 3 indexes, seam linting, the locked cut procedure, the 3 layout presets |
| **capcut-editing-screen-recording** | B-roll: the `rl2` instrumented recorder (built), the OCR index, ROI, content matching. **The editing half is still unsolved — read its status table first.** |

## The three rules

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
   See `capcut-editing-talking-head`.
2. **Give the scenes their looks** — `capcutctl layout …`.
3. **Look at frames** — `capcutctl qa`. `doctor` validates structure and cannot see the picture;
   two real defects passed it clean.
4. **Finish** — `capcutctl finish --project NAME`, then `polish --motivated` and `finish --music`.
   Picture-locked first. Music is generated to the picture; speech is never recut to a beat.
   Captions stay outside CapCut. See `references/finish.md`.
5. **Look at the finished frames** — those last-pass writes change the picture. Run
   `capcutctl timeline`, then `capcutctl qa` at the new seams / music-in / CTA, then a mute
   watch. `doctor` cannot see transition, track-slice, or music-placement defects.
6. **`capcutctl doctor`** must be error-free before you hand it over.

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
