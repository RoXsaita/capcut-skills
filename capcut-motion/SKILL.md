---
name: capcut-motion
description: >
  Motion design for a CapCut short, with taste instead of templates: every video keeps the
  creator's brand (read from their capcutctl profile, never from this skill), flexes by the
  style for its video type, and gets one visual idea of its own, checked against a log so
  consecutive videos never look the same. Covers overlay graphics and full-frame scenes
  (`capcutctl mograph`: hook slams, openers, transitions, reveals, name cards), drawn B-roll the
  CLI cannot draw (the Remotion kit, rendered with alpha and placed `--generated`), the shot list
  from the transcript, the taste rules and AI-slop tells, and the still-frame QA. Use for any
  graphic, motion, intro/outro, kinetic type or transition in a CapCut edit, for "make it look
  premium / like a motion designer did it", for a motion reel, or when a graphic reads as
  generated. The edit itself is capcut-editing.
---

# CapCut motion

A template makes every video look the same; no system makes every video look like a stranger's.
This skill runs between them with three layers, and it holds **none** of the brand itself:

| Layer | What it fixes | Where it lives | Changes |
|---|---|---|---|
| **Brand** | Colour roles, font, the rules every video keeps, what was rejected | profile `brand`, `tokens` | Rarely, by the creator |
| **Style** | Pace, what leads (text, capture, number, name), where the accent goes, camera, sound | profile `styles.NAME` | Per video type |
| **Idea** | The one visual motif this video is built on | invented here, per video; logged | Every video |

The brand makes a video recognisable, the style makes it right for its type, and the idea
keeps it from being boring. The profile is the creator's file, outside every repository:
`~/.config/capcutctl/profile.json` merged over the CLI's shipped neutral defaults. Nothing
personal goes in this skill.

## 0. Read the profile first

```bash
capcutctl profile where      # is there a user layer? which file?
capcutctl profile            # the merged profile: read brand, tokens.color, tokens.font, styles
```

- **A user layer exists:** use it as written. Don't restate its values from memory. Read them.
- **No user layer:** the creator has no brand on this machine yet. Ask once: set one up now
  (`capcutctl profile init`, then fill `brand`, `tokens.color` and `styles` in with them), harvest
  it from their drafts (`capcutctl harvest --profile FILE`), or go ahead on the neutral defaults and
  say so in the hand-off. Never invent a brand, and never borrow another creator's.
- When the creator states a lasting preference ("my accent is…", "never do X again"), offer to
  write it into **their profile** (`brand.rules` / `brand.avoid` / a style). Something that only
  applies to one project goes in `capcutctl notes`. Neither kind of preference goes in this skill.

## 1. Pick the style

Read the signed-off transcript (`capcutctl scenes --project NAME --transcript`) and pick the
profile style whose `use` fits the video. Say which one and why in one line; the creator can
overrule. Put it in `edit.json` as `"style": "NAME"`. `build` and `gate --style` then hold the
graphics to that style's `pace`. The rest of the style (`feel`, `lead`, `accent`, `camera`,
`sound`) steers the beats you choose. When no style fits, pick the closest and say what does
not fit. If the creator makes this kind of video often, offer to add a style to their profile.

## 2. Read the log, then find the idea

```bash
tail -n 5 "$(capcutctl profile where | node -pe 'JSON.parse(require("fs").readFileSync(0)).userDir')/motion-log.jsonl"
```

The log is the creator's too: one JSON line per finished video, in their user dir (format
below). A missing file means no history. Start one.

**The idea** is one visual motif taken from *this* video's subject that the beats are built
from. It is not a scene name. Write it in one sentence before any shot list. Ways to find one:

- **An object the video is about**, as a shape: the dishwasher's rack becomes the grid the
  numbers sit in; a vacuum's path becomes the line a list travels along.
- **A gesture from the capture**: the cursor's click becomes the hit every graphic lands on; a
  terminal's caret becomes the cut.
- **The structure of the argument**: a before/after becomes two-ups throughout; a ranking becomes
  a block climbing.
- **A word the video keeps saying**: it becomes the recurring super that changes each time.

Then check it against the log. The rules below are what keep the videos from repeating while
the brand stays the same:

- The idea is not the same as any of the last 3 videos' ideas.
- The opening beat's archetype differs from the last video's opener.
- Across the last 5 videos, no archetype opens more than twice.
- Inside a video, no two adjacent beats share an archetype, and none appears three times.

## 3. The shot list, then build

1. **Shot list** ([shotlist.md](references/shotlist.md)): tag the beats, budget 3–6 graphic beats
   (the style's `pace` sets the spacing, `maxScenes` caps the full-frame scenes), choose the
   slot, and build each beat **from the idea** using the archetypes in
   [scenes.md](references/scenes.md) as vocabulary. Add columns for the idea and the colour role
   each beat uses. **Show it to the creator before building.**
2. **Native first** ([native.md](references/native.md)): overlay templates and full-frame
   scenes rendered by `capcutctl mograph` in the profile's colours and font, declared in
   `edit.json` beside the style, then `capcutctl build` and `capcutctl gate`. When the idea needs
   a move the catalog lacks, extend the library ([native-authoring.md](references/native-authoring.md)).
   Don't write a one-off.
3. **Remotion for the rest** ([remotion.md](references/remotion.md)): collages of real frames, a
   process climbing, captures built into two-ups. Sync the profile into the project first
   (`kit/scripts/sync-profile.sh`) so the render and the native graphics share one brand.
4. **Brand marks and the end card stay native** (`capcutctl logo`, `capcutctl endcard`).

## 4. Look before you ship

Nobody can watch the clip in real time here, so stills are the review: `mograph scene-preview`
/ `mograph preview` sheets for native pieces, `kit/scripts/stills.sh` for Remotion, then
`capcutctl qa` on the composite. On every frame, check:

- **The tells** in [taste.md](references/taste.md): no decoration standing in for structure,
  no linear entrances, no slides, no butted cuts, no sub-pixel drift, no copy shrunk to fit.
- **The brand**: every colour is a profile role. The accent is on one element in the shot.
  The type is the profile's family. Nothing in `brand.avoid` appears.
- **The style**: what leads is what the style says leads.
- **The idea**: someone who saw only the stills could say what the motif is.

Report colours by hex and role (for example "`#3D3D3D` brand fill"), not by colour name.

## 5. Log it

When the creator accepts the video, append one line to the log:

```json
{"date":"2026-09-27","project":"NAME","style":"product","idea":"the rack is the grid every number sits in","opener":"Number","archetypes":["Number","Two-up","Block climb","Big Word"],"accentOn":"the verdict number","verdict":"accepted","note":""}
```

If the creator rejects the idea, log it with `"verdict":"rejected"` and the reason. Rejected
ideas count toward the last-3 rule too.

## Non-negotiables

- **No brand in this skill or in any repository.** Colours, font, name, rules and styles are
  read from the profile, every time.
- **Colours are roles.** `brand` fills a block behind text. `accent` marks one element per shot,
  never a title or a large fill.
- **One family**, the profile's, plus its mono. Every move is on a named curve
  ([easings.md](references/easings.md)). Opacity resolves before movement.
- **Every graphic serves a spoken beat.** It starts on its word and is gone when the idea is.
- **Real material over illustration, illustration over stock.** Captured UI is shown, not
  redrawn.
- **Deterministic renders.** The still you approved is the frame you ship.
- **Anything CapCut can express stays native**, so the creator can still touch it.

## Files

| File | Use it for |
|---|---|
| `references/shotlist.md` | Transcript → tagged beats → budget → slot → the shot list table |
| `references/scenes.md` | The archetypes (Big Word, Collage ring, Block climb, Prop drama, Number, Two-up, Word ticker, Callout on capture): what beat each serves, picture, move, pitfalls |
| `references/taste.md` | The motion grammar and the AI-slop tells, with numbers |
| `references/rulebook.md` | Colour roles, type scale and copy limits, spacing, layout forms, timing, cuts |
| `references/easings.md` | Every curve, named for its intent, and how to pair them across a cut |
| `references/native.md` | `capcutctl mograph`: templates vs scenes, the catalog, `edit.json`, standalone reels, QA |
| `references/native-authoring.md` | Adding a param, forking a scene, the promotion checklist |
| `references/remotion.md` | When to use the kit, and its steps from shot to `add --generated` |
| `references/anatomy.md` | How a 32-second reference video is built, as measured |
| `kit/README.md` | The Remotion kit: files, install, `sync-profile.sh` |
| `kit/theme.ts` | The profile's roles, font and type scale, read from the synced `profile.json` |
| `kit/fonts.ts` | Loads the profile's font files |
| `kit/easing.ts` | The curves as `Easing.bezier()`. Import them, never retype |
| `kit/timing.ts` | The beat in integer ms: enter 400, exit 200, stagger 100, lap 4f, sound lead 4f |
| `kit/motion.ts` | `progress`, `run`, `track`, `handOver`, `staggerDelay`, `seed`/`span`, `cycle` |
| `kit/Stage.tsx` | A plain stage with an optional camera and a `transparent` mode for alpha |
| `kit/Typed.tsx` | Text typed on the `WRITE` curve with a caret |
| `kit/examples/BigWord.tsx` | Big Word, as code |
| `kit/examples/Collage.tsx` | Collage ring, as code |
| `kit/examples/Terminal.tsx` | Block climb, as code |
| `kit/scripts/sync-profile.sh` | The profile and its fonts into a Remotion project |
| `kit/scripts/stills.sh` | Render the frames you will inspect |
| `kit/scripts/render-alpha.sh` | ProRes 4444 with alpha, then the `capcutctl add --generated` line |

## What this skill does not do

It does not pick the story, the cut or the B-roll moment (`capcut-editing`). It does not add
captions. It does not decide the brand: the creator does, in their profile. Colour parity between
a Remotion still and CapCut's render is not claimed; inspect the composite with `capcutctl qa`.
