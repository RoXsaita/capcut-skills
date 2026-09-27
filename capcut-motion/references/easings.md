# Easings — every curve in the kit, and why

A curve is chosen for what the motion *is*, and named for it. `kit/easing.ts` is the source of
truth; this page is the index. Never retype a bezier into a component — import the name.

## The six anchors (mirrored pairs)

| Name | Bezier | Use for |
|---|---|---|
| `SNAPPY_OUT` | `0, 0.6, 0.4, 1` | energetic entrances that settle softly |
| `SNAPPY_IN` | `0.6, 0, 1, 0.4` | wind-ups that exit at full speed |
| `EXPO_OUT` | `0, 1, 0, 1` | dramatic reveals, scale pops, counters |
| `EXPO_IN` | `1, 0, 1, 0` | anticipation into a hard exit or cut |
| `OUT_IN` | `0, 0.7, 1, 0.3` | motion carried across a cut — a whip |
| `IN_OUT` | `0.7, 0, 0.3, 1` | A-to-B moves at rest on both ends |

**Across a cut, alternate them** so objects are at their highest velocity at the moment of the
cut: an *in* curve to animate out, then an *out* curve for the reveal.

## Arriving and leaving

| Name | Bezier | What it is |
|---|---|---|
| `ENTER` | `0.2, 0.75, 0.34, 0.94` | arriving: three quarters of the travel in the first fifth |
| `EXIT` | `1, 0.02, 0.54, 0.42` | leaving: holds, then all of it at once |
| `SETTLE` | `0.25, 0.4, 0.35, 1` | a long arrival, motion spent evenly |
| `LAND` | `0.16, 1, 0.3, 1` | coming to rest: fast in, nearly all of it spent slowing |
| `GLIDE` | `0.66, 0.004, 0.376, 1.001` | Apple's sheet settle: away at speed, then a long even landing |
| `DIVE` | `0.86, 0.005, 0.999, 0.177` | the way out: barely leaving, then all at once — a thing let go |
| `STAND` | `0.5, 0, 0.3, 1` | a letter or glyph standing up over a few frames |
| `DEPART` | `0.55, 0, 0.85, 0.55` | a hand withdrawing: gathers from rest |

`ENTER` is too fast to be *seen* over three or four frames — that is what `STAND` is for.

## Writing and reaching

| Name | Bezier | What it is |
|---|---|---|
| `WRITE` | `0.3, 0, 0.75, 0.55` | typing: leaves rest and keeps gathering, quickest at the last key |
| `FOLLOW` | `0.45, 0, 0.55, 1` | soft and symmetric, quick through the middle |
| `AIM` | `0.32, 0.04, 0.3, 1` | a reach: one throw, quickest a third in, then homing |
| `TURN` | `0.737, 0.195, 0.927, 0.549` | a quarter turn, gathering, quickest as it lands |

## Marks and cards

| Name | Bezier | What it is |
|---|---|---|
| `STAMP` | `0, 0.626, 0.369, 0.993` | a mark set down: full speed in, seated in the first third |
| `UNVEIL` | `0, 0.36, 0.469, 0.993` | stepping aside to reveal, softer than STAMP |
| `ALIGHT` | `0, 0.816, 0.135, 1.001` | a card's arrival: nearly all the travel in the first frames |
| `DWINDLE` | `0, 0.986, 1, 0.371` | a card's whole stay on one curve: shrink at the cut, drift, close |
| `COLLAPSE` | `0.001, 0.725, 0.238, 0.99` | collapsing onto its own frame, one long landing |
| `WIND` | `0.35, 0.45, 0.85, 0.28` | a whole shot's rotation: quick, slow, quickest; monotone |

## The camera

Shots leave on the move they were already making and the next arrives at the speed the last one
left at, so a hand-over reads as one swing.

| Name | Bezier | What it is |
|---|---|---|
| `CAM_IN` | `0.161, 0.708, 0.562, 0.916` | bringing a shot on: in at speed, the rest is settle |
| `PANEL_IN` | `0, 0.544, 0.414, 0.994` | a panel's arrival: full speed, then one long even settle |
| `PULL` | `0.378, 0.226, 0.817, 0.634` | eased in from a still frame, gathering, easing off as it carries the subject out |
| `SWEEP` | `0.705, 0.076, 0.965, 0.818` | a whole camera in one move: near the subject's own rate, then the run-off |
| `CLIMB` | `0.512, 0.203, 1, 0.788` | at rest while there is room, then gathering — quickest as it takes the block off |

`SMOOTH` is a smoothstep for a value that must leave *and* arrive at a standstill — an unwinding
that ends at any pace reads as a second animation.

## Using them

```ts
import {progress, run, track} from './motion';
import {GLIDE, ENTER, SETTLE} from './easing';

const o = progress(frame, at, frames(300), ENTER);              // opacity first…
const y = run(frame, at, frames(400), SETTLE, 8, 0);            // …then an 8px settle
const cam = track(frame, [{at: 0, value: 0}, {at: 12, value: -64, ease: GLIDE}]);
```

`track()` eases each segment with the *destination* key's curve: a key describes how the value
arrives at it.

## In CapCut

`capcutctl keyframe`, `punch`, `zoom` and `logo` write the harvested `FreeCurveInOut` shape by
default. This vocabulary does not yet exist there as `--ease NAME`; until it does, native camera
moves are eased once and rendered graphics carry the rest of the vocabulary.
