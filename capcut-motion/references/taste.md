# Taste — what makes motion read as designed

This is what separates a motion designer's work from generated motion, whatever the brand.
Hold every beat to it, native or Remotion, and every change to a scene. The numbers assume the profile's 30 fps and 120 BPM (one beat is
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

- `ink` and `paper`, plus two or three roles per scene, all from the profile. The accent goes
  to one thing.
- Type is big and short: 1–3 words per line, and captions of five words at most. One family
  (the profile face), plus mono for technical micro-type.
- At most the style's `pace.maxScenes` full-frame scenes in a video (never more than three).
  A scene never covers the proof on screen.

## 7. Sound is picture

- Every hit has a cue and every cue has a hit: slams thud, grid lines click, reveals ring and
  dives whoosh up into an impact.
- Cues come from the scene's `cues()` on the same clock as the picture, and are synthesised,
  so they cannot drift or go missing.

## The tells: why a graphic reads as "AI"

A viewer cannot name it, but they see it in one frame. Measured against a reference launch
video that was written entirely as code (4,170 lines for 32 seconds), and against the
previous house Remotion B-roll, the tells are always the same:

| Tell | What it looks like | The rule it breaks |
|---|---|---|
| Decoration for structure | glow, grid, gradient, vignette, coloured card, window chrome, `box-shadow` bloom | structure comes from scale, weight, spacing and luminance only |
| Linear motion | `interpolate()` with no `easing`, constant-rate typewriter | never linear unless the movement is mechanical |
| Slides | an element fades in, sits still, fades out | one camera move per shot; something is always moving |
| Springs on everything | Remotion `spring()` pop on every logo and card | curves are chosen for intent and named for it |
| Identical repeats | three cards with the same pop, same glow decay, same delay step | stagger from a meaningful origin; vary per item, deterministically |
| Butted cuts | shot A ends, shot B starts | shots lap by 4 frames; the leaver is still moving when the arriver is in |
| Sub-pixel drift | a 65px push over 175 frames (0.37 px/f) | a move under 1 px/frame stutters; move further, shorter, or on another channel |
| Copy shrunk to fit | a 50-glyph answer at a smaller size | rewrite copy over its limit; never shrink the type |
| Default palette | a stock palette instead of the brand, green check marks, gradients | the profile's roles only; one accent per piece |

If a still shows any of these, the shot is not done. Do not add motion to fix a layout
problem: "one flourish per beat; treat a busy scene as a layout problem".
