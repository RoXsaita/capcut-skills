---
name: capcut-editing-screen-recording
description: >
  Select, time and place screen-recording B-roll in a CapCut video. Use when matching spoken
  sentences to on-screen events, building or querying an index of a long screen recording, or
  choosing crops and zooms. Use `capcutctl find` for OCR/transcript search. THE EDITING HALF
  IS STILL UNSOLVED — read the status table below before promising precision. Read the
  capcut-editing hub first; for what `capcutctl` already automates, read capcut-cli.
---

# Screen recording — B-roll

Read `capcut-editing` (the hub) first.

The live search path is `capcutctl find` (OCR + transcript). An instrumented
recorder (`rl2`) exists in a separate private repo and is **not** part of this
toolkit; do not tell the user to clone or install it. For ordinary screen
recordings, index with `find` and place B-roll with `capcutctl add` / `layout`.

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

Build order is a gate, not a preference: **do not start Phase 3 until a real recording
round-trips through Phase 2.** Every confident-but-wrong result in the one full build came from
guessing at this layer.

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

## Standing rule: never full-frame B-roll over his face

Tried and rejected outright:

> *"you used the screen recording as a cover, which I don't like and it's weird to edit."*

B-roll shares the frame with him via a layout preset (circle inset, or split screen) — it does not
replace him. See the `capcut-editing-talking-head` skill, `references/layouts.md`.

Historical note: an older project (`IKEA Refund`) used a **different** `Split` mask config —
`centerX 0.0435, centerY 0.4969`, with the screen on top and the face on the bottom — versus the
locked preset's `centerX -0.0046, centerY 0.5415`. The locked values come from a scene he
positioned by hand and are authoritative; the older ones are recorded only so nobody assumes the
split can go only one way. Neither was verified by rendering.

## Still open

1. **The SPLIT preset's bottom half** — the face geometry is locked; what scale/position the
   recording takes below the split line was never determined.
2. **Sentence → moment binding** for unguided footage. Guided mode makes this a verification
   problem; footage recorded without it still needs the Phase 2 aligner.
3. **Zoom/keyframe synthesis** — designed in `references/roadmap.md`, not built.

## Files

| File | Use it for |
|---|---|
| `references/recorder.md` | `rl2` — running it, the trace schema, what is measured vs assumed |
| `references/roadmap.md` | Phase 2 and 3 design: contracts, alignment, zooms, verification |
| `references/indexing.md` | The older OCR index, keyword discipline, ROI selection |
| `references/recording-upgrades.md` | Capture hygiene; the original Recording Layout.app |

## Privacy — hard constraint

Log **that** a key was pressed and **when**, never **which**. Content would capture passwords.
Personal content (notification shades, DMs) is excluded by default and flagged, never silently
included. In `rl2` this is enforced in code, not by convention — see `references/recorder.md`.
