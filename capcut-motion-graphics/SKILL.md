---
name: capcut-motion-graphics
description: >
  Design and build the cinematic graphic beats that every short-form CapCut video gets —
  chosen from what the video says, not bolted on. A procedure from the cut transcript to a
  shot list (tag each beat, budget 3–6, pick the slot and the one accent), a scene
  vocabulary of ten archetypes (Big Word, Collage ring, Block climb, Prop drama, Number,
  Two-up, Word ticker, Callout on capture; brand marks and end cards stay native), the
  rulebook (palette, type limits, spacing, timing, 25 named easing curves, the AI-slop tells),
  a Remotion kit with three worked scenes, a still-render gate, and the alpha render →
  `capcutctl add --generated` → `qa` hand-off. Use for any graphic in a CapCut edit, for
  "make my videos look premium", or when a graphic reads as generated. The edit itself is the
  capcut-editing hub; this skill is the drawn picture.
---

# CapCut motion graphics — the drawn half of the frame

`capcutctl` cuts footage. It cannot draw: CapCut's format has no HTML, no shader, no
arbitrary geometry, and inventing effect structures is forbidden (see `capcut-cli`). So every
graphic is **rendered outside, then placed** with `capcutctl add --generated`. This skill is
about deciding *which* graphics a video earns, and making each one worth placing.

**The graphics pass is part of finishing every video.** It runs after the A-roll is signed off
and the layouts are set, before `polish`. A short with no graphic beats is unfinished unless
the user said so. `references/shotlist.md` is the procedure; `references/scenes.md` is what a
beat can become.

## Why graphics read as "AI"

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
| Default palette | indigo-on-navy, green check marks, gradients | near-achromatic; one accent per piece, taken from the subject |

If a still shows any of these, the shot is not done. Do not add motion to fix a layout
problem: "one flourish per beat; treat a busy scene as a layout problem".

## Files

| File | Use it for |
|---|---|
| `references/shotlist.md` | **Start here.** Transcript → tagged beats → budget → slot → accent → the shot list table |
| `references/scenes.md` | The ten archetypes: the beat each serves, picture, move, slot, pitfalls; which stay native |
| `references/rulebook.md` | Palette, type scale with copy limits, spacing, layout forms, timing, cuts, captions, sound |
| `references/easings.md` | Every curve in the kit, named for its intent, and how to pair them across a cut |
| `references/anatomy.md` | How the 32-second reference video is built, as measured: one timeline, one scalar per shot, hand-overs, deterministic scatter |
| `kit/README.md` | The Remotion kit: what each file is and how to install it |
| `kit/easing.ts` | The curves as `Easing.bezier()` — copy into the project, never retype numbers |
| `kit/timing.ts` | The house beat in integer ms: enter 400, exit 200, stagger 100, lap 4f, sound lead 4f, `CHAR_MS` 39 |
| `kit/motion.ts` | `progress`, `run`, `track` (eased keyframes), `handOver`, `staggerDelay`, `seed`/`span`, `cycle` |
| `kit/fonts.ts` | Inter and Anton loaded at render time (`@remotion/google-fonts`), so every machine draws the same type |
| `kit/Stage.tsx` | A plain stage: no glow, no grid; optional camera transform; `transparent` for alpha |
| `kit/Typed.tsx` | Text typed on the `WRITE` curve with a 120ms caret |
| `kit/examples/BigWord.tsx` | Big Word: one capital word too wide for the frame, struck letter by letter, pulled off left |
| `kit/examples/Collage.tsx` | Collage ring: 8–12 real stills unwinding round a shimmering label; clamps to either slot |
| `kit/examples/Terminal.tsx` | Block climb: a process seen running, typed on `WRITE`, the block climbing on `GLIDE` |
| `kit/scripts/stills.sh` | Render the frames you will inspect |
| `kit/scripts/render-alpha.sh` | ProRes 4444 with alpha, then the `capcutctl add --generated` line |

## The workflow

1. **Shot list from the transcript** (`references/shotlist.md`). `capcutctl scenes --project NAME --transcript`,
   read the whole script as a viewer, tag each beat (`CLAIM`, `NUMBER`, `LIST`, `PROCESS`,
   `COMPARE`, `OBJECT`, `ALL`, `POINT`, `NAME`, `CTA`, `PLAIN`), keep 3–6 graphic beats with
   one in the first 3s, choose the slot (top half by default) and the one accent, and write the
   table: time, words, tag, archetype, copy within its limit, real material, camera, sound
   cue. **Show it to the user before building.**
2. **Pick the archetype's recipe** (`references/scenes.md`). Three are in the kit as code; the
   rest are recipes precise enough to build in an hour. One object, one move, one idea per shot.
   Brand marks and end cards are native `capcutctl logo` / `endcard`, never a render.
3. **Copy the kit** into the Remotion project as `src/motion/` (see `kit/README.md`). Do not
   retype curve numbers or timing constants into a component — import them, so the whole
   video shares one beat. Load fonts through `kit/fonts.ts`.
4. **Write the shot as a schedule, not as frames.** Put the content in a table (rows, words,
   marks), derive every time from it in ms, and let one camera track and one progress scalar
   per shot drive the rest. The three examples are the shape; every one takes its size from
   the composition, so it renders in the 1080×960 slot and full frame alike.
5. **Stills first.** `kit/scripts/stills.sh src/index.ts SHOT qa/SHOT 6 20 45 70`, then look
   at every frame against the tells table above. A wrong still is cheaper than a wrong render,
   and a still is exact: the kit has no wall clock and no `Math.random`.
6. **Render** with `kit/scripts/render-alpha.sh` (`--opaque` when the graphic fills its slot,
   alpha when it lies over footage). Keep the output somewhere durable; `add` refuses `/tmp`.
7. **Place and inspect the composite**, not the movie:

```bash
capcutctl add --project NAME --media /path/renders/SHOT.mov --at 16.3 --dur 5.8 \
  --track broll --volume 0 --generated --desc SHOT
capcutctl qa --project NAME --times 16.3,19,22
```

   `--generated` records that there is no editable original to relink; without it the origin
   contract refuses the file. `qa` sees the composited frame CapCut will show, keyframes
   resolved, which the Remotion still cannot. Then `capcutctl layout auto` so the face shares
   the frame wherever a graphic covers it.

8. **Variety, then sound.** List the archetypes in order; no two adjacent the same, none three
   times. Sound belongs to `polish`, not to the render: the graphic's picture changes are the
   cues; `capcutctl polish` puts the transition and its sound 4 frames ahead of them. Do not
   bake SFX into the movie.

## Rules that are not negotiable

- **Achromatic by default.** `#000` / `#161616` / `#F8F8F8` / `#A4A4A4`. One accent per piece,
  on at most one element per shot, taken from the subject. Never on a title or a large fill.
- **One family plus its mono.** Inter or Geist; the stack falls back to the system sans. No
  display fonts, no italic.
- **Every move on a named curve** from `kit/easing.ts`, chosen for what the motion *is*. A new
  curve is added with the sentence that says what it is for, or it is not added.
- **Opacity resolves before movement** (300ms then 400ms), so a line is readable before it
  settles. A support element leads its body by 3 frames and rises 8px, no more.
- **One camera move per shot, and shots are handed over**, not cut: leaver on `EXIT`, arriver
  on `CAM_IN`, lapping 4 frames.
- **Deterministic.** A scatter comes out of `seed(i, salt)`, never `Math.random()`; a count is
  `cycle()` off the frame, never a CSS animation. The still you approved is the frame you ship.
- **Copy has a limit** per role (`kit/theme.ts` → `TYPE`). Over it, rewrite. The example throws
  at build time on over-length copy; keep that habit.
- **No chrome.** No window frames, traffic lights, cards with borders, drop shadows, or glows
  unless the subject *is* that window and it is captured, not drawn.
- **Real UI is captured, not reconstructed.** Show the recording (`capcut-editing-screen-recording`);
  draw only what does not exist on screen — labels, marks, the one number.
- **Real material over illustration, illustration over stock.** A collage is of *his* frames;
  a number is *his* number; a prop is drawn flat when the object does not exist on screen.
- **The graphic serves a spoken beat.** It starts on the word and is gone when the idea is. A
  graphic nobody said is decoration.

## When to use which tool

| Piece | Tool |
|---|---|
| A talking-head video with drawn B-roll inserts (the normal case) | Remotion + this kit → `add --generated` → finish in CapCut |
| A graphics-heavy promo with a few seconds of face | Diffusion Studio (`dapi mount` a TSX composition; MPL-2.0, `brew install --cask diffusionstudio/tap/editor`), render, then `add --generated` if it must end in CapCut |
| A camera move on real footage | `capcutctl keyframe` / `punch` / `zoom` — native, eased, editable in CapCut; not a render |
| A brand mark popping on its name | `capcutctl logo` — the harvested glow reveal; not a render |

The last two rows matter: anything CapCut can express natively should stay native so the user
can still touch it. Render only what CapCut cannot draw.

## What this skill does not do

It does not pick the story, the cut or the B-roll moment (`capcut-editing-talking-head`,
`capcut-editing-screen-recording`). It does not add captions. It does not promise Inter is
installed — check `fc-list | grep -i inter` or accept the system fallback and say so in the
hand-off. Slider-exact colour parity between the Remotion still and CapCut's render is not
claimed; inspect the composite with `capcutctl qa`.
