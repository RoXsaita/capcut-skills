---
name: capcut-editing-talking-head
description: >
  Cut and lay out the talking-head (A-roll) half of a CapCut video. Use when trimming a face
  recording to its best take, removing duplicate lines, fillers, stutters and dead space, placing
  frame-accurate cut points, or applying one of the three locked layout presets (circle + white
  frame / full frame / split screen + purple frame). Covers Whisper + audio-energy indexing and
  the seam linter. Read the capcut-editing hub first for the format and the safe write path.
---

# Talking head — cutting and layout

The A-roll half. **This part is solved**: the procedure here produced a cut the user reviewed as
*"just fucking perfect ... literally no mistakes."* Follow it rather than improvising.

Read `capcut-editing` (the hub) first — it owns the CapCut format, the write path and rule zero.

## Do not do this by hand — `aroll` does it

`aroll index MEDIA --lang ar` then `aroll cut MEDIA.aroll.json --keep … --project NAME`
implements steps 1–10 of the locked procedure deterministically: transcription, the energy index,
dead-air removal, take and duplicate detection, acoustic boundary snapping, auto-repair of every
computable seam fault, frame quantisation and the CapCut write. It self-tests (`aroll selftest`).

The procedure below is still the reference for **why**, and for the judgement calls the tool
deliberately leaves to you: which take, which instance of a repeated line, what is a false start,
and the running order. Read `references/procedure.md` before overriding anything.

## The one idea that matters

Whisper is **semantic** and its timings lie (word starts are contiguous-filled, off by up to
~0.7 s). The audio energy index is **acoustic** and sample-true but knows no meaning.

> Whisper decides *which words*. The energy index decides *exactly where*.

Every seam defect came from trusting Whisper alone.

## Files

| File | Use it for |
|---|---|
| `references/procedure.md` | **The 13-step locked cut procedure** — start here — plus known weaknesses |
| `references/indexing.md` | The indexes, the seam linter, take/beat selection, verification |
| `references/layouts.md` | The three layout presets as copy-paste numbers, geometry conventions |

Scripts live in the hub: `~/.claude/skills/capcut-editing/scripts/`
(`audio_index.py` for the energy index and linter, `capcut.py lint|strip|preview|sheet`).

## Non-negotiables

- Boundaries come from `onset_after()` and `trough()`, never from a Whisper timestamp.
- `capcut.py lint` must return **zero findings** before you render.
- Re-transcribe the render and check it reads as one coherent script.
- Contact-sheet every cut frame and confirm head size and position hold across each pair.
- Layout numbers are **copied verbatim from a reference segment, never recomputed**.
