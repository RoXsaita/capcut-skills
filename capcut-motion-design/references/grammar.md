# The motion grammar

This is what separates a motion designer's work from generated motion. Hold every scene to
it, and every change to a scene. The numbers assume the profile's 30 fps and 120 BPM (one beat is
0.5 s, or 15 frames).

## 1. Every transition is motivated

The last thing on screen becomes the first thing of the next moment:

- a dot winds up and snaps into a line (`ignition`);
- a full stop becomes the camera's dive into the next shot (`word-slam`);
- a grid collapses into dots and the dots become particles (`shape-grid` → `particle-word`);
- the opening dot returns as the name card's full stop (`dot-signature`).

A crossfade, a push with nothing carried across, or a flash that hides a cut are not
transitions. Every scene declares `handoff: { in, out }`, and a chain matches them.

## 2. Anticipation → action → follow-through

- **Wind-up** before a move: squash against the direction of travel for 4–8 frames before
  the release.
- **Overshoot** after arrival: springs (`K.spring(t, 2.0–2.6 Hz, damping 0.4–0.5)`) or
  `E.outBack`, with 3–8% past the target, then settle.
- **Contact** squashes (`K.wobble`) and speed stretches along the direction of travel,
  keeping the volume (x shrinks as y grows).

## 3. Spacing, not speed

- Entrances use expo or spring. Exits are faster than entrances. Linear is for counters and
  scrolling only.
- Staggers are 2–4 frames (0.05–0.06 s) in **reading order**. Arabic staggers by word, never
  by letter (joined forms break), with `K.dir` so punctuation lands on the reading end.
- Nothing idles. There's no ambient wiggle and no loop: each move has a start, a hit and a
  settle.

## 4. The beat is the grid

- A scene is a whole number of half beats long. Hits land on beats. A transition finishes
  on the **last frame**, so the next scene's first frame is the downbeat.
- One idea per beat. If two things want the same beat, one of them waits a beat or goes.

## 5. Depth without gimmicks

- A slow camera push (2–3% over the scene), camera shake only on impacts, and parallax
  between layers.
- Motion blur comes from the runtime (a 180° shutter), and film grain and vignette come from
  the profile.
- **Slop tells, never used:** drop shadows on everything, bevels, lens flares, glow as
  decoration, gradient text as a default, emoji, stock "tech" HUDs with no meaning, a
  particle burst with nothing forming.

## 6. Restraint

- `ink` and `paper`, plus two or three roles per scene. The accent goes to one thing.
- Type is big and short: 1–3 words per line, and captions of five words at most. One family
  (the profile face), plus mono for technical micro-type.
- At most three scenes in a talking-head video. A scene never covers the proof on screen.

## 7. Sound is picture

- Every hit has a cue and every cue has a hit: slams thud, grid lines click, reveals ring and
  dives whoosh up into an impact.
- Cues come from the scene's `cues()` on the same clock as the picture, and are synthesised,
  so they cannot drift or go missing.
