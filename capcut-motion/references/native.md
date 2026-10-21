# The native engine — `capcutctl mograph`

The CLI renders two kinds of motion graphic itself, with real motion blur, grain and synced
sound, in the profile's colours and font, and places them as `--generated` clips. Anything this
engine can express stays here: it re-renders when the profile changes and `build` re-anchors it
on a recut. A drawn B-roll insert is a scene too: fork the nearest one with
`presentation: "overlay"`. The Remotion kit ([remotion.md](remotion.md)) is a last resort, for
what the catalog truly cannot express, and only when the profile's `brand.avoid` does not name it.

The catalog below is a **vocabulary, not a menu.** The video's idea and its style decide what a
beat becomes (see the skill); the catalog is where you start building it. When the idea needs a
move the catalog does not have, that is a new scene or a new param — see *A new design*.

## Two kinds of motion graphic

| | **Template** (`mograph list`) | **Scene** (`mograph scenes`) |
|---|---|---|
| What it is | A small overlay over the picture, cropped to its box | The whole 1080×1920 frame for 1–3 s |
| For | A keyword, a number, a callout, the CTA, a brand chip | The opener, the one hook claim, a breather between sections, a reveal, the sign-off |
| Anchored | Leads its word by the profile's lead frames | Starts **on** its word, because it is a cut |
| Sound | A paired cue from the SFX library | Its own synthesised sound, inside the clip |
| How many | Every 5–8 s (profile `density`) | At most one per ~15 s of talking head, and never more than three in a video |

Most edits need templates on the face and **the style's `maxScenes`** at most: the hook, one
break or reveal, and the sign-off. Count them by hand (nothing enforces it); the house seam-wipe
chapter transitions and the auto follow ending do not count. More than that turns a video into a motion reel. If the request
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
| Chapter change, the house transition | `seam-wipe` | `text?` (1–3 word label on a brand slab), `beats?` (default 3) | the seam on both sides. **Bare** (`beats` 1, no label): start at cut − 0.2 s, so the cut lands under the open band. **Labelled**: start at cut − (beats × 0.5 − 0.35) s at 120 bpm, which is cut − 0.9 at `beats` 2.5 and cut − 1.15 at the default 3, so the label and the cover sit on the outgoing shot and the incoming proof shows by cut + 0.35. It scales with `tokens.scene.bpm`. Never cut − 0.2 with a label. In `edit.json` that is `at`/`offset`; on `mograph add` it is `--at` |
| The layout frame travelling between boxed shots | `frame-travel` | `keys` ([{at, to: [x,y,w,h] / "seam" / "full" / "none", frames?}]), `beats`, `stroke?`, `radius?` | not via `build`: render with `--samples 16`, `add --track layout-frame --layer top --generated --volume 0 --desc layout:frame-travel` (over the face, below the mograph and caption lanes); arrivals on the cut, leaves 2 frames before it |
| A spoken list of output formats | `format-morph` | `labels`, `actions`, `hero`, `presentation`, `imageData` | full: the seam on both sides; overlay: footage → footage |
| A reference-to-personal-result brief | `claude-brief` | `text`, `then`, `presentation` | full: the seam on both sides; overlay: footage → footage |
| Sign-off | `dot-signature` | `name`, `role`, `footer`, `hold` | the end |

`presentation: "overlay"` is transparent and bounded to x70–930 / y230–600, so the footage stays
in view around it; the default `"full"` opens and closes on the seam. `imageData` is a PNG/JPEG
base64 data URI (the captured result). Use each of these two scenes once per video at most.

**Layering a clip you `add` yourself** (frame-travel, a Remotion render): a new `--track` lands
under the face by default. `--layer top` puts it over the face, below the mograph and caption
lanes. Reusing a track that sits on the other side of the face refuses with `TRACK_PLACEMENT`;
name a new track. An `add` result with `underPrincipal: true` means a full-frame face hides the
clip, so run `capcutctl layout auto`. Do not run `layout auto` over a full-frame alpha graphic.

Text follows the profile's languages. `word-slam`, `particle-word` and `dot-signature` lay Arabic out by word,
right to left, with punctuation on the reading end. Keep copy to **1–3 words** per line and
**five words at most** in a caption. The scene wraps and fits, but short is what reads at speed.

## Workflow in an edit

1. **Mark the moments** in the signed-off cut: the hook claim (inside the first 3 s), at most
   one break or reveal in the middle, and the sign-off. Never cover the proof. When the screen
   recording shows the result, the picture is the result, not a scene.
2. **Build the beat the idea asks for.** When a catalog scene does it, params are enough;
   when it nearly does, add the param. Check the chain column: a scene's `handoff.out` should
   equal the next scene's `in`, or it should end on `"footage"` or a hard cut.
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
       { "scene": "dot-signature", "at": 41.5, "params": { "name": "BRAND_NAME", "role": "BRAND_ROLE" } }
     ] }
   ```

   ```bash
   capcutctl build --project NAME --edit edit.json --dry-run
   capcutctl build --project NAME --edit edit.json
   ```

   One scene without a plan: `capcutctl mograph add --project NAME --scene word-slam --params JSON --say WORDS --dry-run`.
   With `--scene`, `--say` starts the scene **on** the word; a template still leads it.
5. **The gate** treats a scene as full-frame by design and as carrying its own sound. It still
   counts the scene for crowding and spacing. `mograph-import` stays a WARN until the Mac
   import checklist in the CLI's `docs/mograph.md` passes. Name that WARN in the hand-off.

## Renders, rerender and refusals

- **Files.** A render is `mograph/<id>-<fingerprint>.mov` (or `.png`), written as `.partial`
  and then renamed, so a draft never points at a half-written file. Older renders are kept. The
  cache is `mograph/.render`. The fingerprint covers the template or scene file, the runtime,
  the params and the profile's tokens, safe zones and canvas. A template's also covers the bytes
  of any local file its params name, so replacing an image at the same path re-renders.
- **`mograph rerender`** keeps the graphic where it sits on the timeline now (a ripple or a hand
  move in CapCut included; the output says `moved: {from, to}` when that differs from the
  render), and keeps its sidecar `sfx` and `allowUnsafe`. `--no-sfx` and `--allow-unsafe`
  override them: `capcutctl mograph rerender --project NAME --id ID --params JSON --no-sfx`.
- **Refusals.** `CAPCUT_RUNNING` comes before anything renders (quit CapCut first).
  `MOGRAPH_CANVAS`: the draft's canvas is not the profile's canvas (a landscape draft, say); use a
  profile whose canvas matches. `MOGRAPH_SAFE_ZONE`: a template's readable text sits in a
  platform-UI zone; it refuses before encoding and names a `suggestCenter`. Put that in
  `params.center` and render again.

## Standalone motion pieces (a reel, an ad, a showreel)

Chain scenes whose hand-offs match, render each one as mp4, and join them:

`BRAND_NAME` is the profile's `brand.name`; read it, never type a person's name from memory.

```bash
capcutctl mograph scene-render --scene ignition      --params '{"to":"hot"}' --out 01.mp4 --format mp4
capcutctl mograph scene-render --scene word-slam     --params '{"text":"صُنع بالكود","bg":"hot","to":"paper"}' --out 02.mp4 --format mp4
capcutctl mograph scene-render --scene shape-grid    --params '{}' --out 03.mp4 --format mp4
capcutctl mograph scene-render --scene particle-word --params '{"text":"Opus 5.5","from":"dots"}' --out 04.mp4 --format mp4
capcutctl mograph scene-render --scene dot-signature --params '{"name":"BRAND_NAME"}' --out 05.mp4 --format mp4
```

```bash
ls 0*.mp4 | sed "s/^/file '/; s/$/'/" > list.txt && ffmpeg -f concat -safe 0 -i list.txt -c copy reel.mp4
```

When the catalog does not have the piece the brief needs, that is a new scene. Follow the
next section. Do not write an ad-hoc HTML/Remotion/After Effects-style one-off beside the
library: it will not share the palette, the beat grid, the blur, the sound or the tests, and
that mismatch is exactly what reads as slop.

## A new design

Read [native-authoring.md](native-authoring.md) and hold
[taste.md](taste.md). In short, in this order:

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

- A placed `seam-wipe`: sample `capcutctl qa --times` every 0.3 s across [at, at + length].
- `scene-preview` gives 8 motion-blurred frames with the platform-UI zones outlined, and it
  lists unsafe text. `--times` puts frames on the hits (every half beat) and on the first and
  last frame.
- On each frame, check that there is one thing to look at, that the text reads, and that
  Arabic letters join with punctuation on the reading end. Check that the last frame is
  exactly the next scene's first, and that nothing important sits in a zone outline.
- `scene-render` refuses unsafe readable text (`SCENE_SAFE_ZONE`). Fix the copy; do not
  reach for `--allow-unsafe`. A template's equivalent is `MOGRAPH_SAFE_ZONE`: move it to its
  `suggestCenter` (as `params.center`) or shorten the copy.
- Sound can't be heard here. Every scene declares `cues`, and its level is normalised to
  -6 dBFS peak, so it sits under the voice and the project's loudness pass finishes it. Say
  in the hand-off that the mix was checked by numbers, not by ear.
