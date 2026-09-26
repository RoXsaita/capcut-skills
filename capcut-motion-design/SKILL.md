---
name: capcut-motion-design
description: >
  Motion design for his videos: full-frame scenes (opener, hook slam, textless transition,
  particle reveal, style-frame stinger, name card) and the overlay graphics that sit on the
  face, all rendered by `capcutctl mograph` with real motion blur, grain and synced sound, and
  placed in the CapCut project. Use for any request for motion graphics, B-roll motion design, transitions,
  an intro/outro, kinetic typography, "make it look like a motion designer did it", a
  showreel, or a standalone motion clip. Catalog first; a new design follows the promotion bar
  so the library never turns into slop.
---

# CapCut motion design

Generated motion graphics usually read as slop for four reasons. The motion is borrowed from
presets (fades, generic slides). Nothing shares a system: every piece has its own colours,
fonts and timing. Transitions have no reason to happen. And nobody looks at frames before
shipping. This skill covers all four with one engine, one catalog, one grammar and one QA loop.

## Two kinds of motion graphic

| | **Template** (`mograph list`) | **Scene** (`mograph scenes`) |
|---|---|---|
| What it is | A small overlay over the picture, cropped to its box | The whole 1080×1920 frame for 1–3 s |
| For | A keyword, a number, a callout, the CTA, a brand chip | The opener, the one hook claim, a breather between sections, a reveal, the sign-off |
| Anchored | Leads its word by the profile's lead frames | Starts **on** its word, because it is a cut |
| Sound | A paired cue from the SFX library | Its own synthesised sound, inside the clip |
| How many | Every 5–8 s (profile `density`) | At most one per ~15 s of talking head, and never more than three in a video |

Most edits need templates on the face and **two or three scenes**: the hook, one break or
reveal, and the sign-off. More than that turns a video into a motion reel. If the request
is a motion reel, see *Standalone motion pieces* below.

## The catalog

```bash
capcutctl mograph scenes          # id, params, length in beats, hand-off, when to use it
capcutctl mograph list            # the overlay templates
```

| Job | Scene | Params that matter | Chains into |
|---|---|---|---|
| Opener, section break | `ignition` | `to` (the colour it lands on), `label` | `word-slam` with `bg` = the same role |
| The one claim | `word-slam` | `text`, `then`, `caption`, `bg`, `to` (`"footage"` = dive into the next shot) | a shot, or `shape-grid` via `to: "paper"` |
| Textless breather | `shape-grid` | `ball` | `particle-word` with `from: "dots"` |
| Reveal a name, tool or number | `particle-word` | `text`, `caption`, `from`, `exit` | `style-stinger`, a hard cut |
| Energy, montage beat | `style-stinger` | `count` 4/8, `word`, `words`, `looks` | hard cuts either side |
| Sign-off | `dot-signature` | `name`, `role`, `footer`, `hold` | the end |

Text is Arabic-first: `word-slam`, `particle-word` and `dot-signature` lay Arabic out by word,
right to left, with punctuation on the reading end. Keep copy to **1–3 words** per line and
**five words at most** in a caption. The scene wraps and fits, but short is what reads at speed.

## Workflow in an edit

1. **Mark the moments** in the signed-off cut: the hook claim (inside the first 3 s), at most
   one break or reveal in the middle, and the sign-off. Never cover the proof. When the screen
   recording shows the result, the picture is the result, not a scene.
2. **Pick from the catalog and write params only.** Check the chain column: a scene's
   `handoff.out` should equal the next scene's `in`, or it should end on `"footage"` or a
   hard cut.
3. **Preview before placing**, and look at the sheet (see QA below):

   ```bash
   capcutctl mograph scene-preview --scene word-slam --params '{"text":"صُنع بالكود","then":"بأمر واحد","to":"footage"}' --out /tmp/slam.png
   ```

4. **Declare the scenes in `edit.json`**, beside `graphics`, and build:

   ```json
   { "version": 1,
     "graphics": [ { "template": "number-pop", "say": "تسعين", "params": { "value": 90, "suffix": "%" } } ],
     "scenes": [
       { "scene": "word-slam", "say": "بالكود", "params": { "text": "صُنع بالكود", "then": "بأمر واحد", "to": "footage" } },
       { "scene": "dot-signature", "at": 41.5, "params": { "name": "سهيل", "role": "صانع محتوى" } }
     ] }
   ```

   ```bash
   capcutctl build --project NAME --edit edit.json --dry-run
   capcutctl build --project NAME --edit edit.json
   ```

   One scene without a plan: `capcutctl mograph add --project NAME --scene word-slam --params JSON --say WORDS --dry-run`.
5. **The gate** treats a scene as full-frame by design and as carrying its own sound. It still
   counts the scene for crowding and spacing. `mograph-import` stays a WARN until the Mac
   import checklist in the CLI's `docs/mograph.md` passes. Name that WARN in the hand-off.

## Standalone motion pieces (a reel, an ad, a showreel)

Chain scenes whose hand-offs match, render each one as mp4, and join them:

```bash
capcutctl mograph scene-render --scene ignition      --params '{"to":"hot"}' --out 01.mp4 --format mp4
capcutctl mograph scene-render --scene word-slam     --params '{"text":"صُنع بالكود","bg":"hot","to":"paper"}' --out 02.mp4 --format mp4
capcutctl mograph scene-render --scene shape-grid    --params '{}' --out 03.mp4 --format mp4
capcutctl mograph scene-render --scene particle-word --params '{"text":"Opus 5.5","from":"dots"}' --out 04.mp4 --format mp4
capcutctl mograph scene-render --scene dot-signature --params '{"name":"سهيل"}' --out 05.mp4 --format mp4
```

```bash
ls 0*.mp4 | sed "s/^/file '/; s/$/'/" > list.txt && ffmpeg -f concat -safe 0 -i list.txt -c copy reel.mp4
```

When the catalog does not have the piece the brief needs, that is a new scene. Follow the
next section. Do not write an ad-hoc HTML/Remotion/After Effects-style one-off beside the
library: it will not share the palette, the beat grid, the blur, the sound or the tests, and
that mismatch is exactly what reads as slop.

## A new design

Read [references/authoring.md](references/authoring.md) and hold
[references/grammar.md](references/grammar.md). In short, in this order:

1. An existing scene does the job: **params only.**
2. A param would do it: **add the param** to that scene (a variant), with its header and test case.
3. A new job, or a clearly different motion idea: **fork the closest scene** and rewrite only
   the choreography. The kit already has the maths, palette roles, type, camera, blur, grain
   and sound.
4. **Promote** only what clears the checklist: documented header, roles only, half-beat
   length, declared hand-off, a cue on every hit, readable text through `K.text`, a test
   case, and a preview sheet that someone looked at.

Colour and copy are always params. A scene with this video's words baked in, or the same idea
in a new colour, does not go in the library.

## QA: look before you ship

Nobody on this machine can watch the clip in real time, so the frames are the review:

- `scene-preview` gives 8 motion-blurred frames with the platform-UI zones outlined, and it
  lists unsafe text. `--times` puts frames on the hits (every half beat) and on the first and
  last frame.
- On each frame, check that there is one thing to look at, that the text reads, and that
  Arabic letters join with punctuation on the reading end. Check that the last frame is
  exactly the next scene's first, and that nothing important sits in a zone outline.
- `scene-render` refuses unsafe readable text (`SCENE_SAFE_ZONE`). Fix the copy; do not
  reach for `--allow-unsafe`.
- Sound can't be heard here. Every scene declares `cues`, and its level is normalised to
  -6 dBFS peak, so it sits under the voice and the project's loudness pass finishes it. Say
  in the hand-off that the mix was checked by numbers, not by ear.

## Files

| File | Use it for |
|---|---|
| `references/grammar.md` | The motion grammar: what makes motion read as designed rather than generated, with numbers |
| `references/authoring.md` | Writing, forking and promoting a scene: anatomy, the kit, the checklist |
