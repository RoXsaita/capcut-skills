# From the transcript to a shot list

The graphics pass is part of finishing every video, not a favour for special ones. It runs
after the A-roll is signed off and the layouts are set, and before `polish`. Its input is the
cut transcript; its output is a shot list table; the shots are then built (`scenes.md`),
rendered, placed and inspected.

## 1. Read the beats

```bash
capcutctl scenes --project NAME --transcript
```

Read the *whole* surviving script once, as a viewer, before tagging anything. The graphic
beats are the sentences you would remember; the rest is the face talking, which is fine.

## 2. Tag each beat

One tag per beat, the strongest that applies:

| Tag | The sentence… | Archetype |
|---|---|---|
| `CLAIM` | says the one thing the video is about, in a word or two | Big Word |
| `NUMBER` | states a figure, count or multiplier | Number |
| `LIST` | names three to five things | Word ticker |
| `PROCESS` | describes steps happening or a tool running | Block climb |
| `COMPARE` | sets two things against each other | Two-up |
| `OBJECT` | does one thing to one thing (drop, press, send, publish) | Prop drama |
| `ALL` | refers to a body of material — everything watched, every draft, all comments | Collage ring |
| `POINT` | points at something in a recording — this, here, that line | Callout on capture |
| `NAME` | names a brand or tool for the first time | **native** `capcutctl logo` |
| `CTA` | asks for the follow, the comment, the link | **native** `capcutctl endcard` |
| `PLAIN` | none of the above | none — the face, or recorded B-roll |

Most beats are `PLAIN`. That is correct. A video where every sentence has a graphic is a slide
deck with a voiceover.

## 3. Budget

For a 30–60s short:

- **3–6 graphic beats**, no more. Fewer for a video that is mostly a recording.
- **One in the first 3 seconds.** The open must have picture on screen (`finish` reports a
  cold open); a graphic beat is a good way to make it.
- **One on the biggest claim**, and one on any number that matters.
- **Never the same archetype twice running**, and no archetype more than twice in a video.
  `polish` reports transition variety as a quality signal; hold graphics to the same standard.
- **Each ≤ 3s** unless it is a collage or a process, which may run to the sentence's end.
- The graphic starts **on the word**, not before it, and never after the word has passed. Use the
  word's timeline time from `scenes --transcript`, then `qa --times` on that frame to check the
  picture is up when the word is said.

## 4. Slot

| Situation | Slot | Then |
|---|---|---|
| The face keeps talking and the graphic proves the words | top half, 1080×960 | `layout auto` treats it as B-roll covering the moment → split-screen |
| The graphic *is* the moment (Big Word, a Number that lands) | full frame, 1080×1920, alpha | over the face; keep it off the head (`rulebook.md` safe area) |
| The point is in a recording | the recording, top half | draw only the callout; camera move is native `keyframe --focus` |

Full frame is the exception. If in doubt, top half.

## 5. The accent

One accent colour for the whole video, taken from the subject: the tool's UI colour, a colour in
the footage, the house indigo when the subject is `capcutctl` itself. Write it down before the
first shot. It goes on at most one element per shot, never on a title or a fill.

## 6. Write the table

Columns, one row per graphic beat:

| t (s) | spoken words | tag | archetype | copy (≤ limit) | material | camera | sound cue |
|---|---|---|---|---|---|---|---|
| 0.0–2.4 | "I watched every take" | ALL | Collage ring | *Watching footage* | 10 stills from the takes | ring turn | picture change → polish |
| 8.1–9.5 | "eighteen out of eighteen" | NUMBER | Number | *18 / 18* + *scenes matched* | — | drift | picture change |
| … | | | | | | | |

**Copy** is checked against the role's limit (`kit/theme.ts` → `TYPE`); over it, rewrite.
**Material** is real — frames from his footage (`ffmpeg -ss T -i FILE -frames:v 1`), his
screenshots, his numbers — or it is a drawn prop; never stock. **Sound cue** is what `polish`
will key on, not something baked into the render.

Show the table to the user before building. A shot list is cheap; six renders are not.

## 7. Build, look, render, place

For each row:

```bash
kit/scripts/stills.sh src/index.ts SHOT qa/SHOT 6 20 45 70         # look first
kit/scripts/render-alpha.sh src/index.ts SHOT /durable/path/SHOT.mov [--opaque]
capcutctl add --project NAME --media /durable/path/SHOT.mov --at T --dur D \
  --track broll --volume 0 --generated --desc SHOT
```

Then the composite, at the word and at the shot's peak:

```bash
capcutctl qa --project NAME --times T,T+1
capcutctl layout auto --project NAME            # the face shares the frame where a graphic covers it
```

## 8. The variety check

Before `polish`, list the archetypes in order. If any two adjacent are the same, or one appears
three times, change one. Then `capcutctl finish` and `polish --motivated` as usual; the graphic's
picture changes are its cues.

## What this pass is not

It is not permission to skip recorded B-roll. A real screen recording of the thing happening
beats any graphic of it. Graphics carry the beats a recording *cannot*: the claim, the number,
the list, the "all of it", the object that does not exist on screen.
