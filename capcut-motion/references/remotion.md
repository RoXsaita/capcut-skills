# Remotion — for what the native engine cannot draw

`capcutctl mograph` covers overlay graphics and full-frame scenes ([native.md](native.md)). Use the
Remotion kit (`../kit/`) for a drawn piece those cannot express: a collage of real frames, a
process climbing, a big word pulled off the frame, a two-up built from captures. The result is
rendered, then placed with `capcutctl add --generated`; the edit around it stays native.

The kit has no brand of its own: `kit/scripts/sync-profile.sh` copies the creator's merged
profile and font files into the project, and `kit/theme.ts` reads only that.

## Which tool

| Piece | Tool |
|---|---|
| A talking-head video with drawn B-roll inserts (the normal case) | Remotion + this kit → `add --generated` → finish in CapCut |
| A graphics-heavy promo with a few seconds of face | Diffusion Studio (`dapi mount` a TSX composition; MPL-2.0, `brew install --cask diffusionstudio/tap/editor`), render, then `add --generated` if it must end in CapCut |
| A camera move on real footage | `capcutctl keyframe` / `punch` / `zoom` — native, eased, editable in CapCut; not a render |
| A brand mark or a text line that earned the beat | `capcutctl logo` or `capcutctl motion` — default orbit-glow (Blur underlay plus the recipe). Not a render, and not a word dropped on a face that did not ask for it |

The last two rows matter: anything CapCut can express natively should stay native so the user
can still touch it. Render only what CapCut cannot draw.

## Steps

1. **Shot list from the transcript** ([shotlist.md](shotlist.md)). `capcutctl scenes --project NAME --transcript`,
   read the whole script as a viewer, tag each beat (`CLAIM`, `NUMBER`, `LIST`, `PROCESS`,
   `COMPARE`, `OBJECT`, `ALL`, `POINT`, `NAME`, `CTA`, `PLAIN`), keep 3–6 graphic beats with
   one in the first 3s, choose the slot (top half by default) and the one accent, and write the
   table: time, words, tag, archetype, copy within its limit, real material, camera, sound
   cue. **Show it to the user before building.**
2. **Pick the archetype's recipe** ([scenes.md](scenes.md)). Three are in the kit as code; the
   rest are recipes precise enough to build in an hour. One object, one move, one idea per shot.
   Brand marks and end cards are native `capcutctl logo` / `endcard`, never a render.
3. **Copy the kit** into the Remotion project as `src/motion/` and run
   `kit/scripts/sync-profile.sh PROJECT_DIR` (see `kit/README.md`), so it draws in the creator's
   brand. Do not
   retype curve numbers or timing constants into a component — import them, so the whole
   video shares one beat. Load fonts through `kit/fonts.ts`.
4. **Write the shot as a schedule, not as frames.** Put the content in a table (rows, words,
   marks), derive every time from it in ms, and let one camera track and one progress scalar
   per shot drive the rest. The three examples are the shape; every one takes its size from
   the composition, so it renders in the 1080×960 slot and full frame alike.
5. **Stills first.** `kit/scripts/stills.sh src/index.ts SHOT qa/SHOT 6 20 45 70`, then look
   at every frame against the tells in [taste.md](taste.md). A wrong still is cheaper than a wrong render,
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
