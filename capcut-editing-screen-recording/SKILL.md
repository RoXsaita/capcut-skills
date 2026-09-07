---
name: capcut-editing-screen-recording
description: >
  Select, time and place screen-recording B-roll in a CapCut video. Use when matching spoken
  sentences to on-screen events, building or querying an index of a long screen recording, or
  choosing crops and zooms. Use `capcutctl find` for OCR/transcript search, then inspect
  source frames to verify actions and results; automatic semantic alignment is not implemented. Read the
  capcut-editing hub first; for what `capcutctl` already automates, read capcut-cli.
---

# Screen recording — B-roll

Read `capcut-editing` (the hub) first.

The live search path is `capcutctl find` (OCR + transcript). An instrumented
recorder (`rl2`) exists in a separate private repo and is **not** part of this
toolkit; do not tell the user to clone or install it. For ordinary screen
recordings, index with `find` and place B-roll with `capcutctl add` / `layout`.
`add` persists the take's `trace.ndjson` beside the draft; `polish` maps
`click` / `typing_burst` onto the chopped B-roll as mouse-click and typing SFX.

## The premise

His words:

> **Every single sentence I say must be matched to the exact thing happening on screen.**

If he says "I tapped Grok Build," the frame must be the moment he taps Grok Build — ideally with a
punch-in zoom keyframed onto that element. Not approximately.

The strategy that follows from that: **do not build a vision system that understands 31 minutes of
pixels.** Make the recording emit an interaction trace, use a cheap model-free change signal to
fill the gaps, and spend model calls only on discriminating between a handful of candidates.

## Status

| Phase | What it is | State |
|---|---|---|
| 1 | `rl2` — instrumented capture: one clock, event packets, change signal, guided markers | **built** (v2.1). Timing/pixels solid. Two core modes: **whole screen** (usual) and **one window at full visible**. Acceptance take (10 named clicks + scroll + type + guided) still unrun |
| 2 | Event compiler — trace + video into a queryable session DB, four levels L0–L3 | not built |
| 3 | The editing skill — obligation contracts, global alignment, zoom synthesis, verification | not built |

This table describes the recorder roadmap, not a gate on ordinary video editing.
Use the current `find`, `layout` and `keyframe` commands with inspected frames.
Semantic sentence-to-event alignment still requires judgement; do not claim OCR
hits prove that an action happened.

## Build each shot from evidence

Use the existing compact shot list in `capcut-cli`; keep the exact narration phrase,
source file/range, timeline range and inspected evidence together.

- **Verify the verb.** For a click or change, inspect before/action/after frames or a short
  source playback. A labelled button alone proves neither a click nor a successful result.
  If the evidence is missing, find another take or flag the claim as unverified.
- **Separate waiting, action and result.** Trim or accelerate idle loading; keep the useful
  interaction readable and give its result a stable hold. Play that hold at phone size to
  judge its length. `pace --auto` only infers source gaps. If a source span includes both
  waiting and useful action, place them as separate shots first; apply per-clip
  `pace --at … --speed …` to the waiting shot and recheck the action/result timing.
- **Choose one focus.** Write what the viewer should notice. Crop/zoom to an inspected
  rectangle and leave caption space; use a highlight only if it makes that target clearer.
  Avoid simultaneous competing callouts, zooms and transitions. A stable shot is valid.
- **Check the assembled timing.** Verify the action/result against the spoken phrase after
  trimming or changing speed. Recheck rest, peak and return when adding camera movement.

## Why it was hard before the recorder

The voice side has three indexes and word-level precision. The screen side had a 1 fps OCR text
dump over a 31-minute (1,862 s) recording. That asymmetry *was* the problem:

- Content windows can be **4 seconds inside 31 minutes**.
- Keyword search silently over-matches. Searching `gold`+`wave` returned the chat text
  *describing* the game, not gameplay. `wave` also hit "wave progression" in a prompt; `imagine`
  hit a nav tab.
- OCR gives text, not **events**. It cannot tell you where a tap landed, so zoom coordinates have
  no source.
- Nothing degraded gracefully with length.

`rl2` attacks all four at the capture stage, which is cheaper than attacking them at the edit
stage. See `references/recorder.md`.

## Standing rule: the recording goes in whole

Every B-roll clip is imported at its **full capture resolution**, from a path that will still
exist next week. Crop, pan, zoom, trim and speed are CapCut properties — `layout broll --row`,
`layout screen`, `add --src/--dur`, `keyframe`, `pace` — not ffmpeg filters applied on the way
in. The AI Video Editor B-roll was cropped 1920×1080 → 1080×960 in a session scratchpad and
imported flat; the picture was right and nothing could be changed afterwards, which is the one
outcome this whole toolkit exists to avoid. `add` refuses it now (`PREFRAMED_MEDIA`,
`EPHEMERAL_MEDIA`). See the `capcut-editing` hub, rule 3, for the full translation table.

## Standing rule: never full-frame B-roll over his face

Tried and rejected outright:

> *"you used the screen recording as a cover, which I don't like and it's weird to edit."*

B-roll shares the frame with him via a layout preset (circle inset, or split screen) — it does not
replace him. See the `capcut-editing-talking-head` skill, `references/layouts.md`.

Historical note: an older project (`reference A`) used a **different** `Split` mask config —
`centerX 0.0435, centerY 0.4969`, with the screen on top and the face on the bottom — versus the
locked preset's `centerX -0.0046, centerY 0.5415`. The locked values come from a scene he
positioned by hand and are authoritative; the older ones are recorded only so nobody assumes the
split can go only one way. Neither was verified by rendering.

## Still open

1. **Shot-specific framing** — `layout broll --row` places a tall source in the TOP half;
   the locked face occupies the bottom. Inspect the chosen centre row and source window.
   `layout screen` handles framed window recordings.
2. **Sentence → moment binding** for unguided footage. Guided mode makes this a verification
   problem; footage recorded without it still needs the Phase 2 aligner.
3. **Automatic semantic zoom selection** remains manual. `keyframe --focus` now
   computes native position/scale from an inspected source rectangle; see `capcut-cli`.

## Files

| File | Use it for |
|---|---|
| `references/recorder.md` | `rl2` — running it, the trace schema, what is measured vs assumed |
| `references/roadmap.md` | Phase 2 and 3 design: contracts, alignment, zooms, verification |
| `references/indexing.md` | The older OCR index, keyword discipline, ROI selection |
| `references/recording-upgrades.md` | Capture hygiene; the original Recording Layout.app |

## Privacy — hard constraint

Log **that** a key was pressed and **when**, never **which**. Content would capture passwords.
Inspect recordings for personal content (notification shades, DMs) and exclude or flag it
before placement. Whole-screen capture can include notifications even with a privacy-aware
trace logger. The historical recorder notes describe trace restrictions, not a guarantee
that arbitrary video pixels are private.
