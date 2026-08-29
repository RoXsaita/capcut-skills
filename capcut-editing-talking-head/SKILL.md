---
name: capcut-editing-talking-head
description: >
  Cut the talking-head (A-roll) half of a CapCut video and give each scene a layout. One
  command does the mechanical work — transcribe, energy-sync, strip dead air, snap every
  boundary, lint and repair the seams, build the project. Use when trimming a face recording,
  removing duplicate lines, false starts and dead space, or applying the circle / full-frame /
  split-screen looks. Read the capcut-editing hub for the format and the write path.
---

# Talking head — one command, one review

```bash
capcutctl cut VIDEO.mp4 --lang ar
```

Transcribes (mlx large-v3-turbo), builds the acoustic energy index, splits beats on dead air,
snaps every boundary to a real onset/trough, detects takes and repeated lines, and prints a
numbered table. **~10s for a 107s source; cached after that.**

Read the table. Decide what to keep. Then:

```bash
capcutctl cut VIDEO.mp4 --keep 0,2,3,6-10,13-14,16-19,22 --project my-video
```

It applies your selection, auto-fixes every seam fault it can compute, packs the timeline with
no gaps, lints, and builds the CapCut project. It **refuses to build** if a seam is still bad.
That is the whole procedure. Two invocations, one command, ~2 minutes.

**Stop there.** Hand him the project and wait. Do not add B-roll, layouts, pace, polish, or
music until he has watched the talking-head cut and signed it off. Recutting the face after
B-roll is on the timeline desyncs every shot.

The face is **always 1×**. `pace` already refuses the principal track; `clip.trim` that
lengthens the source window without lengthening the target is a speed ramp — same crime.
To drop a line, re-run `cut --keep` (that changes *length*, still at 1×). To include a word
the energy snap dropped, also re-run `cut --keep` after fixing the keep list — never steal
the word by playing the clip faster.

Then give the signed-off scenes their looks — see `capcut-cli`:

```bash
capcutctl layout auto         --project my-video   # split where B-roll covers, full face else
capcutctl layout circle       --project my-video --at 12 --track content
capcutctl layout split-screen --project my-video --at 30 --track content
capcutctl layout background   --project my-video
capcutctl qa --project my-video --times 4,12,30 --guide 960 --out qa/
```

## What you decide, and nothing else

The tool proposes "last take, last instance of every repeat". That is a starting point, not an
answer. Yours are the calls a transcript cannot make:

- **which take** — he warms up as he goes, so the last is usually best
- **which instance of a repeated line** — his rule: *"generally the last cut of a specific thing
  is better."* Sanity-check that the last is also the most complete; it usually gains a word
- **false starts** — a short beat whose full version appears later. These often do *not* cluster
  as duplicates, because the complete version continues past the shared opening
- **near-duplicates the clustering missed** — different phrasings of one idea
- **running order**, if a beat lands badly

Everything else — timings, boundaries, dead air, frame quantisation, seam repair — is arithmetic.
Do not do it by hand and do not second-guess it without reading `references/procedure.md`.

## The one idea that matters

Whisper is **semantic** and its timings lie (word starts are contiguous-filled, off by up to
~0.7s). The energy index is **acoustic** and sample-true but knows no meaning.

> Whisper decides *which words*. The energy index decides *exactly where*.

Every seam defect in this project's history came from trusting Whisper alone. Boundaries come
from `onset_after()` and `trough()`. This is enforced in code; you cannot get it wrong by
accident any more.

## Files

| File | Use it for |
|---|---|
| `references/procedure.md` | Why each step exists, and the known-weak list — read before overriding |
| `references/indexing.md` | The indexes, the linter's calibration, take/beat selection |
| `references/layouts.md` | The three layouts as raw numbers (`capcutctl layout` applies them for you) |

## Still done by eye

Not yet automated, so still yours:

- **Loudness across seams** — two clips can differ by a few dB and the join is audible even with
  perfect timing.
- **Breaths** sit near −45 dB and read as silence. Usually keep at a sentence start, cut
  mid-phrase.
- **The video side of a seam.** `capcutctl qa` renders the frames; nothing yet checks head
  position holds across a cut.
- The lint margin is **one example wide** (0.28s good vs 0.35s bad). Flag any bad seam you hear
  by timecode — each one is a labelled negative worth keeping.
