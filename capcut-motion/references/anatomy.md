# Anatomy of a reference — a 32-second video written entirely as code

The Diffusion Studio launch video (MIT, `github.com/diffusionstudio/launch-video`) is the
measured reference for this skill: 450K+ views, "didn't touch the timeline once". What that
sentence hides is what makes it work.

## The numbers

| | |
|---|---|
| Duration | 32 s |
| Code | 4,170 lines across 8 scenes — **~130 lines per second** |
| Real footage | two files (`aroll.mp4`, `aroll-post.mp4`) |
| Everything else | SVG marks and ten PNG stills |
| Named easing curves | 25, each with a one-sentence justification |
| Springs | 0 |
| `Math.random` | 0 — every scatter is a hash of the index |
| Commits | 1 |

The lesson is the budget. A 5-second graphic on these rules is a few hundred decisions, not a
component and a fade. No skill file compresses that; the kit only makes each decision cheap.

## One timeline, seeked

Every scene is an `<html>` node — real HTML/CSS drawn into the canvas — driven by **one**
anime.js timeline built with `autoplay: false` and `seek`ed from the editor's playhead. Nothing
runs on the wall clock, so scrub, still and export are the same picture. Remotion gives this for
free (`useCurrentFrame`), which is why the kit has no timers and no CSS animations.

## One scalar per shot

The collage ("Watching footage") is ten frames on a tilted ellipse. One progress value `p` runs
the whole shot on one curve (`WIND`); every angle, size and z-order is `p` times a constant, so
nothing can be out of step. Distance `m` is a second scalar, deliberately separate, because it
scales sizes as well as the ring — "the one thing the winding must not do".

Per-frame variety comes from a hash seed, centred so the pile sits where it was put:

```js
d:    ((i + 1) / COUNT) * TAU + span(i, 1, -SCATTER, SCATTER),  // how far round it travels
s:    span(i, 3, 0.66, 1.24),                                   // its size
rate: span(i, 4, 0.95, 1.05),                                   // so the ring breathes, not a rigid wheel
tilt0: span(i, 7, -11, 11),                                     // lies off level in the pile, comes up square
```

A big frame sets off later than a small one (`LAG = 140ms × (s − S_LO)/(S_HI − S_LO)`) — a
property of the frame, not of its index, so the pile comes apart unevenly. The kit's `seed`,
`span` and `centered` are this pattern.

## Hand-overs, not cuts

The first three shots are handed over: the leaver accelerates out on `EXIT` in 450ms, the arriver
sets off 300ms in on `CAM_IN` and spends 500ms settling. Two views of the same command line at
different sizes are never both legible at once — one baton, not a shared frame. The kit's
`handOver()` is this; `LAP_F = 4` is the minimum overlap.

## Timing with reasons

Everything is an integer in ms with a sentence:

- `DARK = 160` — the frame is empty before the caret first lights
- `CHAR_DT = 39` — about a glyph a frame through the fast middle of `WRITE`
- `EAGER = 200` — output prints before the pan has settled, the way a real CLI answers before
  the scroll stops
- `LAP = 4 frames` — cuts are lapped rather than butted
- `OUT_O = 90, OUT_B = 130` — it leaves the way it came but in a third of the time: an entrance is
  watched, an exit is got out of the way of
- The label's shimmer is a `background-clip: text` gradient swept by a ramp read modulo, "a count
  read modulo cannot be wrong on any frame"

The kit's `timing.ts` keeps this form. Add a constant with its sentence or do not add it.

## Focus is the frame's, not the element's

The collage blurs in as *one* picture (`animations={[{type:'blur'}]}` on the node), while opacity
is staggered per frame — "one picture resolving, not ten and a line of type each resolving
separately", and under the blur "a pile assembling rather than a finished pile turned up". Two
channels, two owners, deliberately not the same thing twice.

## What it is not

It is not an agent auto-editing footage, and it is not a template. It is motion design written
in JSX by someone who knows what Apple's sheet-presentation curve is, hosted in an editor that
keeps every element editable. The same file would look identical exported from After Effects.
That is the standard; the kit exists so a shot on that standard costs an evening, not a week.
