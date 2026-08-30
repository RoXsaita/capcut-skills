---
name: capcut-cli
description: >
  What the `capcutctl` command line tool can already do to a local CapCut project, so you use it
  instead of hand-writing draft_info.json. Covers creating a project, the three locked layouts
  (split-screen, circle, background), scene listing, the transactional safety model, and the
  invariants that make a project unopenable. Read this BEFORE editing any CapCut JSON by hand.
  For the format itself, the user's style and project state, read the capcut-editing hub.
---

# capcutctl — what already exists

`capcutctl` is the CLI in the companion repo
(`https://github.com/RoXsaita/capcut-editor-cli`). Install with `npm link`
from that clone, or run `node bin/capcutctl.mjs`. See its README → *Style —
ask once* before the first write: bundled house style, harvest the user's
own drafts, or `--blank`.

**Do not hand-write `draft_info.json` for anything below.** It is already solved, tested, and
transactional. Hand-editing loses the snapshot, the root/timeline pairing and the mirror sync.

## On a machine you have not used before — `preflight`

```bash
capcutctl preflight        # deps, overlay artwork, SFX palette, drafts folder; exit 1 if unusable
```

Run it before blaming an edit. What is and is not portable:

| | |
|---|---|
| **Bundled, always works** | The indigo bar and white ring the layouts need ship in the package's `assets/`. `new --blank` needs no local draft either — it builds from `presets/blank-draft.json`. |
| **Per-machine, degrades** | The SFX and transition palette is CapCut's own effect/music cache, minted where the sound was downloaded. `polish` **skips** any sound that is not present and lists it in `unavailableSfx` — it does not fail, and it does not write a dead reference. A missing CapCut resource is a `MISSING_CAPCUT_RESOURCE` warning, never an error, because CapCut re-downloads its own effects and masks. |
| **Required** | `ffmpeg` / `ffprobe` on PATH. A missing one now says so (`MISSING_DEPENDENCY`) instead of `spawnSync ENOENT`. |

Bring your own instead of re-downloading someone else's: `CAPCUTCTL_ASSET_DIR` for overlay
artwork (searched before the bundle) and `CAPCUTCTL_PRESET_DIR` for your own
`sfx.json` / `brands.json` / `layouts.json` (falls back to the bundled preset per file).

**If `polish` reports `unavailableSfx`, say so in the hand-off.** The edit is real; the sound
design is not there yet, and the user needs to know which is which.

## Commands

```bash
capcutctl cut VIDEO [--keep …] [--project NAME]      # talking-head cleanup (see below)
capcutctl qa  --project NAME --times 3,9,15 --sheet  # composite real frames + contact sheet
capcutctl find "agent running" --media F --shows --strip   # when is it on screen
capcutctl find "قروك بيلد"     --media F --says            # when was it said
capcutctl close                                      # quit CapCut, wait for it to exit
capcutctl rm --project NAME                          # to .recycle_bin, registry cleaned

capcutctl preflight                                  # will this machine work? deps, assets, SFX
capcutctl projects                                   # list drafts
capcutctl scenes   --project NAME [--name SUBSTR] [--transcript]  # time, track, desc, media, source
capcutctl inspect  --project NAME                    # tracks, canvas, active timeline
capcutctl doctor   --project NAME                    # read-only integrity report

capcutctl new --project NAME [--media FILE] [--scenes 0:6@122.4,6:12,12:18]
capcutctl layout split-screen --project NAME --at SECONDS --track N
capcutctl layout circle       --project NAME --at SECONDS --track N
capcutctl layout broll        --project NAME --at S --track N --row ROW [--scale S]
capcutctl layout background   --project NAME
capcutctl layout list

capcutctl apply    --project NAME --spec FILE [--dry-run]   # arbitrary edits, v1 spec
capcutctl snapshot --project NAME --label WHY
capcutctl history  --project NAME
capcutctl restore  --project NAME --snapshot NAME
capcutctl sync     --project NAME                    # repair mirror drift + collapse duplicate material ids

capcutctl add      --project NAME --media FILE --at S --dur S --track NAME|N
                   [--src S] [--cover IN-OUT] [--volume 0] [--desc TEXT] [--no-localize]
capcutctl replace-media --project NAME --file FILE --at S --track NAME [--retime] [--no-localize]
capcutctl localize --project NAME          # copy outside videos into the draft (fixes Link media)
capcutctl trim     --project NAME --at S --track NAME --src IN-OUT
capcutctl shift    --project NAME --at S --track NAME --by SECONDS
capcutctl remove   --project NAME --at S --track NAME
capcutctl volume   --project NAME --at S --track NAME --level 0
capcutctl fade     --project NAME --at S --track NAME [--in 0.08] [--out 0.12]
capcutctl keyframe --project NAME --at S --track NAME [--to 2.4] [--hold 1.6] [--plan]
capcutctl preview  --project NAME --out preview.mp4 [--fps 6]
capcutctl diff     --project NAME --snapshot NAME | --against NAME
capcutctl harvest  [--projects A,B] [--out FILE] [--plan]

capcutctl timeline --project NAME [--width 64]          # ASCII stacked timeline
capcutctl finish   --project NAME [--plan] [--music] [--polish] [--regen]
capcutctl music    --project NAME [--plan] [--regen] [--volume 0.08]
capcutctl polish   --project NAME [--motivated]         # --motivated = picture changes only
```

Everything that writes takes `--dry-run`.

## Cleaning the talking head

```bash
capcutctl cut VIDEO.mp4 --lang ar                       # -> numbered review table
capcutctl cut VIDEO.mp4 --keep 0,2,3,6-10 --project NAME  # -> built project
```

One command, run twice. The first pass transcribes (mlx `large-v3-turbo`), builds the acoustic
energy index, splits beats on dead air, snaps every boundary to a real onset/trough, detects
takes and repeated lines, and prints a table with a copy-paste command for the second pass.
~10s for a 107s source, cached in `~/Downloads/.video-index` afterwards.

The second pass applies the selection, **auto-repairs** every seam fault the linter can compute
(an OUT on a rising envelope slides to the trough; dead air at an IN slides to the onset), packs
the timeline with no gaps, and refuses to build while findings remain (`--force` overrides).

The agent decides only: which take, which instance of a repeated line, what is a false start,
and the running order. Everything else is arithmetic.

**Non-negotiable:** boundaries come from `onset_after()` and `trough()`, never from a Whisper
timestamp — Whisper's word starts are contiguous-filled and lie by up to ~0.7s. Enforced in code.

## Layout is a rule, not a judgement — `layout auto`

```bash
capcutctl layout audit --project NAME          # what each clip is vs what it should be
capcutctl layout auto  --project NAME [--plan] # make it so
```

**If moving picture covers the moment from a lower track, he is sharing the frame:
split-screen. If nothing does, he is alone in it: full face.** That is the whole rule, and
it reproduces grok-build-final's hand-made choices **18 out of 18** — sixteen split-screen
beats and two full-face ones, zero disagreements. Layout plates (PNG/GIF bars and rings) do
not count as B-roll.

The open is not a judgement either. The first seconds must have B-roll — proof on screen,
sharing the frame. A 5s+ full-face start is a cold-open; `finish` reports it. Put the result
on the timeline at t=0, then `layout auto` will split it.

There is now a third layout, `full-face`: scale 1.0, transform 0, **no mask** — and applying
it also removes the seam bar the split screen left behind, which a mask-only change would
strand on screen.

## Verification — `qa --expect`

```bash
capcutctl qa --project NAME --times 18.6 --ocr                  # what is actually on screen
capcutctl qa --project NAME --times 18.6 --expect "18.6=Read file|Thinking for"
```

Exit 0 if every phrase is on the rendered frame, **exit 1** if any is missing — so it can
gate a build. `doctor` validates structure and cannot see the picture; `qa` drew the picture
but needed a human to read it. This closes the loop: the composited frame the viewer will
actually see is read back and checked against what the edit claims is on it.

This is the only check that would have caught the sidebar-vs-file-list mistake, where the
JSON was valid, the geometry was right, and the frame simply showed the wrong thing.

OCR is Apple's Vision framework via a small Swift helper — `pyobjc` and `pytesseract` are
both absent on a stock machine, and this is the engine the OS itself uses, so it reads UI
text well. Build it once:

```bash
swiftc -O -o tools/vision/ocr tools/vision/ocr.swift
```

## The signature — `wrap`, `logo`, `endcard`, `zoom`

```bash
capcutctl brands                                       # what is known, and which need a PNG
capcutctl wrap    --project NAME --words TRANSCRIPT.json [--text Follow] [--plan]
capcutctl logo    --project NAME --at 8.25 --brand grok [--scale 0.36] [--hold 2.5] [--pos x,y]
capcutctl endcard --project NAME [--text Follow] [--at S]
capcutctl zoom    --project NAME --auto | --at S[,S...] [--to 1.15] [--hold 1.6]
```

`wrap` is the "final touches" pass: brand logos keyed to the moment he says the name, the
Follow/CTA card **on the talking head**, and a push-in on every talking-head scene. `--plan`
shows it without writing. `--words` wants a Whisper transcript (`segments[].words`), not
`.aroll.json`. Omit it and wrap looks in `~/Downloads/.video-index/<stem>.whisper-*.json`
(written by `cut`).

**Follow is not the leftover.** New projects clone Preset 3 and **park** its clips 30s after
the talking head — a parts bin for copying attributes, not the video's ending. Do not delete
them. `wrap` / `endcard` / `music` time themselves to the talking-head end (`contentEnd`),
never to draft duration (which includes the leftover). Putting Follow on the preset clips is
the bug.

**Brand logos.** Measured across 11 projects: scale `0.01 → 0.20–0.57` over **0.07–0.17s**,
held ~2.5s, with `"Pop!" "Pon!" Pitch height` **0.1s ahead** of the picture. Each brand pops
**once**, when he introduces it — never on later mentions.

**The endcard.** Starts at **93–98% of the talking head** (default 96% of `contentEnd`, not of
draft duration), scale `0.01 → 1.4–3.4` over **0.07–0.20s**, with `Culin…` **coincident**, not
leading. Text varies by video — `Follow`, `نشر`, `دليل`, `CV` — so it is a parameter, defaulting
to `Follow`.

**The talking-head push-in.** `1.0 → 1.15` over **0.23s**, hold 1.6s, release. That is 25 of
43 measured face push-ins at 1.15 and 11 more at 1.2; median ramp 0.23s. Much subtler than
a B-roll punch, which goes to 2.0–4.5. `--auto` finds the scenes: a principal-track clip
carrying **no mask** is him alone in frame; a Split or Circle mask means he is sharing it.

### The piece that makes it work: source time → timeline time

The transcript is of the **raw take**; the timeline is a recut of it with dead air removed
and clips sped up. "Put a logo where he says Grok" is meaningless until those are joined.
`sourceToTimeline()` builds the map from the principal track's paired ranges — exact, not
estimated — and `detectBrands` takes the first mention **that survives the cut**, because
the earliest one is usually in a take that was thrown away.

Whisper transliterates inconsistently — جروك and قروك in the same file — so aliases are
compared after folding Arabic letters that differ only by dots or hamza.

### Logo assets

`presets/brands.json` maps a brand to its spoken aliases and a **transparent raster**.
CapCut will not place an SVG, and `qlmanage` (the only rasteriser on a stock Mac) composites
onto opaque white, so `tools/rasterize.py` keys the white back out and reports what survived
— under 0.5% ink means a white-on-white logo, over 60% means a block, not a glyph.

```bash
python3 tools/rasterize.py ~/Downloads/Logos/grok.svg --out ~/Downloads/Logos/.raster/grok.png
```

## Pace — `pace`

```bash
capcutctl pace --project NAME                          # the plan (read-only, default)
capcutctl pace --project NAME --auto [--max 100] [--min-gap 5]
capcutctl pace --project NAME --at 16.57 --speed 8
capcutctl pace --project NAME --at 16.57 --cover 178.6-296.0
```

**Speed is arithmetic, not judgment.** The A-roll cut already fixes how long a B-roll slot
lasts, so the only free variable is how much source it consumes:

```
speed = source_duration / target_duration
```

`pace` never changes a clip's position or length on the timeline — only how much footage
it races through. Measured from his own projects:

| project | source | screen | compression | at 1× |
|---|---|---|---|---|
| IKEA Refund | 1317.6s | 66.8s | **19.7×** | 38% |
| Hermes-agent | 61.8s | 40.4s | 1.5× | 62% |
| grok-build-final *(before)* | 76.4s | 40.9s | 1.9× | **79%** |
| grok-build-final *(after `--auto`)* | — | — | **8.1×** | 42% |

79% at real time means the viewer watches a phone scroll at the speed it actually
scrolled. That is the single loudest "not premium" tell. IKEA crushes 260s of an agent
working into 2.6s at 100× and drops its final beat to 0.4×.

**What `--auto` does, and what it refuses to do.** For each B-roll clip it looks at how
much source is *skipped* before the next shot from the same file — matched by **path**, not
material id, because CapCut keeps many material records per file. A long skip is waiting;
it closes the gap so the footage plays through instead of cutting past it. It will not:

- touch the principal (talking-head) track — faces never ramp
- override a ramp that is already there (`speed ≠ 1.0`) — that was somebody's choice
- fire on a skip under `--min-gap` (default 5s) — a few seconds is an editorial cut
- exceed `--max` (default 100, his own ceiling) or run past the end of the source

Everything else is the plan table plus your judgment. `pace` with no flags prints it —
each clip's source window, current speed, skipped seconds, suggested speed, and `desc`.

**Zooms survive a speed change.** Keyframe `time_offset` is an *absolute source position*,
so a 0.2s punch-in at 10× would collapse to 0.02s — under one frame, reading as a jump.
`pace` rescales every offset by the same factor as the window, which holds each zoom's
**on-screen** duration constant. Verified: a clip taken 1× → 3.08× kept its 0.333s ramp.

## SFX and transitions — `polish`

```bash
capcutctl polish --project NAME [--lead 0.14] [--track N] [--no-transitions] [--motivated]
```

`--motivated` keeps a transition only when the **picture** changes (B-roll shot or layout class). An A-roll splice over the same screen is left as a hard cut. Use this on the finish pass. Without the flag, polish still fires on every visible cut.

**Clicks and typing come from the rl2 take, not from guessing at the picture.** `add` copies
`trace.ndjson` / `session.json` into `.capcutctl/rl2/<take>/` next to the localized
`screen.mp4`. `polish` then maps each `click` / `typing_burst` through the chopped B-roll
(`source` window → timeline, speed-aware). A moment that was cut out of the B-roll has no
cue — that is the index, not a bug. `in_capture: false` is the recorder's own UI and is
skipped. `--no-interactions` skips the pass. Today's traces are often thin (one click, no
typing); the mapping is what makes a richer take just work.

Puts a transition and its matching sound on those cuts, using the grammar measured
from Hermes-agent, Higgsfield Refund, Content System and IKEA Refund:

| pair | transition | sound |
|---|---|---|
| layout change | `Horizontal Triptych` | `Woosh` / `swish_whoosh` (5/5 in his projects) |
| jump inside a scene | `Flash` / `White Flash 2` / `Glitch Flash II` | `Decision / choice / click` (6/7) |
| the machine doing something | `Glitch` | `Glitch sound that matches the sound logo` (2/2) |

**The sound leads the picture by 0.14s** — measured median across 20 paired cuts, not invented.
(Re-measured 2026-08-26 on 22 seams: **0.133s = exactly 4 frames at 30fps**, with the sound
starting when the transition starts. 0.14 is within a fifth of a frame; either is right.)
Volume 1.0, transitions 0.20–0.33s. Never the same pair twice running.

**Callouts click.** Every rectangle / arrow / circle highlight (the GIFs, not the indigo seam bar) gets `Enter / click / select` — alternating the two variants — coincident with the picture. `polish` writes these as `polish:callout`.

**Cashier is not a scene transition.** Coin/cashier is a success accent, not the last-cut pair.

**Sweeps alternate.** A layout change gets a sweep, but `sweep` and `sweepL` take turns. They used
to be exempt from never-twice-running, so a video whose every scene changes layout got the
identical `Horizontal Triptych` + `Woosh` on every cut — **18 of 24 seams** in
`GrokBuild-20260825`. Identical seams are the loudest tell that a machine made the edit; his own
hand-cut projects keep any one transition under ~45% (Hermes-agent 4/9, Higgsfield 2/6).
`polish` now reports this as `variety: {cuts, distinct, top, topShare, lopsided}` — read it,
it is a quality signal, not an error.

**Every transition goes on the principal track** — the one gapless video track that spans the
timeline, which is the talking head. That is where all 9 of Hermes-agent's transitions sit and
none sit anywhere else. `polish` finds it automatically (`--track N` overrides) and **slices it
at every cut that lacks a boundary**, frame-continuously, so the transition has a clip on both
sides. Without a clip after it, CapCut silently drops the transition on load: the file is right
on disk and wrong in the app. See `capcut-editing/references/capcut-format.md` for the full
layer stack.

`polish` owns the transitions: it clears and rebuilds all of them, because CapCut strips any
marker it could use to recognise its own. Pass `keepExisting` in a spec to protect hand-made
ones. Otherwise re-running is idempotent — same timeline, same result.

## Finish — `timeline` / `finish` / `music`

```bash
capcutctl timeline --project NAME
capcutctl finish   --project NAME              # ASCII + scorecard (read-only)
capcutctl polish   --project NAME --motivated
capcutctl finish   --project NAME --music      # Lyria bed, beat-offset to picture changes
```

The last pass. `timeline` is a one-screen dump of stacked tracks (the view that makes
same-screen Flashes obvious). `finish --music` generates an instrumental via Gemini Lyria 3
Pro (`GEMINI_API_KEY` in `cli/.env`, gitignored), caches it at `.capcutctl/music.mp3`, and
places it at ~0.08 with fades. Beats are detected with ffmpeg PCM; the clip is shifted so
downbeats land on **picture changes**. The talking head is never recut. See
`capcut-editing/references/finish.md`.

## B-roll framing — `layout broll`

```bash
capcutctl layout broll --project NAME --at 35 --track 4 --row 2336
```

Frames a B-roll clip in the TOP half of a split screen on a chosen **source row**, and cuts it
at the seam. It computes the transform and the mask line, refuses a scale that would leave
background at the sides, and clamps the window inside the frame so it can never run off the edge.
Omit `--scale` for exact 1:1 full width — anything larger crops the sides, which on a phone UI
cuts text.

## Finding the moment

```bash
capcutctl find "agent running" --media screen.mp4 --shows --strip   # on screen, + frames
capcutctl find "publish"       --media cam.mp4    --says --context  # spoken, word-level
```

`--shows` searches the OCR index, `--says` the Whisper transcript. Runs are collapsed and
reported from their first *stable* second.

**`--strip` is not optional in practice.** OCR matches text it cannot tell is occluded or
scrolled off. A search for "read file" reported a run starting at 168s; at 168s the sidebar
drawer is open over it and the file list does not actually appear until 176s. The B-roll sat on
the wrong content until the frames were checked. Look before you cut.

## Housekeeping

```bash
capcutctl close                 # quit CapCut and WAIT — writes are refused while it runs
capcutctl rm --project NAME     # move to .recycle_bin and drop the registry entry
```

`rm` is the recoverable version of what deleting by hand looks like: `rm -rf` plus a hand-edited
`root_meta_info.json`. It backs up the registry, moves rather than deletes, and prints the `mv`
that puts it back.

## Creating a project

`new` is a **literal duplicate of `Preset 3`** with the name changed — nothing cleverer. The
preset's own clips are **kept** (do not delete them — he copies attributes off them) and
**parked 30s after the talking head**, so they are not the video's ending. `--from NAME` for a
different template. `--blank` empties the timeline (and with `--media`, keeps only your new
scenes). `--canvas WIDTHxHEIGHT` and `--fps N` write through; they used to be accepted and
discarded.

`--scenes` is `START:END` on the timeline, `@SOURCE` for the media in-point, seconds throughout.
It prints **`contentTrack`** — the track index your scenes landed on. The layout commands need it.

## The three layouts

Exact measured geometry from `presets/layouts.json`, captured from `grok-build-claude`. Never
recompute these numbers, never invent new ones.

| | subject | companion |
|---|---|---|
| `split-screen` | fills the BOTTOM half from y=960; `Split`/line mask, `rotation 180` | indigo bar on the seam |
| `circle` | upper-left circular avatar (`transform.y = +0.669`, y up) | white ring (**which carries its own circle mask**, `y = +0.664`) |
| `background` | — | blurred copy of the subject, `scale 1.12`, `alpha 0.72`, on a track BELOW |

`background` auto-detects circle-scenes-with-a-ring and skips the cloned preset's endcard
(`.capcutctl/created.json` records its range); `--include-template` overrides.

Re-running a layout replaces the overlay covering that span rather than stacking duplicates.

## Invariants that bite

- **`draft_info.json`'s top-level `id` must equal the timeline id**, in the root draft AND the
  timeline copy. Get this wrong and the project passes every structural check and still will not
  open in CapCut. `doctor` reports it as `TIMELINE_ID_MISMATCH`.
- **Z-order is track order**, lower index further back. `render_index` is preserved but is not
  authoritative — keep it monotonic with track order so both models agree.
- **Every document has three mirrors** (`draft_info.json`, `.bak`, `template-2.tmp`) and a project
  has two document groups (root + active timeline). All must be written from one edit with the
  same generated ids, or they drift.
- **Writes are refused while CapCut is running** — it holds the draft in memory and clobbers you
  on its next autosave. Quit it first.
- Transform is in **half-canvas units, y positive UP**. Mask `centerX/centerY` are half-**clip**
  units, y up; mask `width/height` are full-clip fractions.

**A logo whose pixel size cannot be read is refused** (`LOGO_SIZE_UNKNOWN`). CapCut lays out from
the material's `width`/`height`, so falling back to the 1280×276 template renders any other logo
as a squashed strip — silently. `imageSize` reads PNG / JPEG / GIF / WebP headers and falls back
to `sips`; `brands.json` ships a `.webp`, so PNG-only was never enough.

**Errors print their details whatever shape they are.** `details` is an array of validation issues
for `VALIDATION_FAILED`, but a plain object for `ROLLED_BACK` (`{snapshot}`) and `CAPCUT_RUNNING`.
Iterating it blindly threw a `TypeError` that buried the real message under a stack trace — worst
on rollback, exactly when you need to be told which snapshot saved you.

**`--dry-run` works while CapCut is open.** A dry run writes nothing, so refusing it cost a
quit-and-relaunch just to see a plan. Only real writes still require CapCut closed.

## doctor cannot see the picture

It validates structure only. A split at 900/1020 instead of 960/960, and an indigo frame 47px off
its content, both passed `doctor` clean. For pixels:

```bash
capcutctl qa --project NAME --times 3,9,15 --guide 960 --out qa/
```

It composites any frame outside CapCut and prints each segment's on-canvas rect. Check the numbers
first, then look at the frame.

It also cannot see a frame that is correct but **frozen**. `MEDIA_PREFRAMED` and
`MEDIA_ORIGIN_LOST` are the two warnings for that: media whose framing was cropped in before
import, and media whose recorded original no longer exists. Neither is an error — they report
projects built before the origin contract, and the repair (relink the original, re-express the
framing with `layout broll --row`) is the human's call.

## Adding B-roll — `add` / `replace-media`

**The origin contract runs first.** Both verbs refuse media whose framing was baked in before
import, and media that came from a directory the human will not have next week:

| Code | What triggered it | The fix |
|---|---|---|
| `PREFRAMED_MEDIA` | The file is exactly half the canvas (1080×960 on a 1080×1920 project). Nothing records at that size — it is a crop. | Import the full-frame source, then `layout broll --row` / `layout screen`. |
| `EPHEMERAL_MEDIA` | The source path is under `/tmp`, `$TMPDIR`, or a `scratchpad/` directory. The bytes get copied in, but the recorded origin becomes a dead link. | Render/move it somewhere durable first. |
| `DERIVED_SOURCE_MISSING` / `_EPHEMERAL` | `--derived-from` named a file that does not exist, or one that is itself temporary. | Point it at the recording that survives. |

Escapes, both recorded in `media-map.json` and on the material:
`--generated` (a Remotion/AE render with no editable original — nothing to relink) and
`--derived-from ORIGINAL [--derived-offset S]` (you pre-processed anyway; the source stays
findable). Neither is a way to skip thinking: pre-framed B-roll is the one defect the user
called out by name, because it is the one he cannot repair in the UI.

Enforced by `add`, `replace-media`, `layout screen` and `new --media`. It is checked in the
*operation*, so an `apply --spec` carrying `clip.add` / `replace.media` / `layout.screen` obeys it
too. A project whose own directory is temporary is exempt from the ephemeral half — it cannot
outlive its own media.

Do **not** hand-write `material.clone` + `track.clone` + N `segment.clone` for B-roll. `add` is the verb:

```bash
capcutctl add --project NAME --media screen.mp4 \
  --at 16.3 --dur 8.2 --src 90 \
  --track broll --volume 0 --desc reading-files
```

- `--track broll` (name) creates/reuses that overlay (`flag=2`) **below** the talking head. Never `track.clone`.
- `--track N` (number) uses that index and **refuses to create** — inserting a track renumbers everything above it.
- **Never the main track (`flag=0`) — from any verb.** `remove` / `volume` / `trim` / `shift` / `fade` / `keyframe` all resolve through one gate (`resolveClip`), which refuses a flag=0 segment and makes the main track invisible to a bare `--at`. It filtered on track *type* only until 2026-08-26, so all six could edit the cover track.
- Overlap on that named overlay is refused by the op (`CLIP_OVERLAP`). Doctor's `TRACK_OVERLAP` is only a warning.
- Running past `doc.duration` slides the preset endcard and **rewrites** `.capcutctl/created.json` `preserved: {start,end}`. That window feeds `layout background` / scene filters — leaving it stale includes or drops the wrong scenes.
- Endcard sliding is measured from where the endcard **is now**, shared across every op in a spec and across both mirror documents. Two `add`s in one spec each push it once. A clip that already sits *inside* the window refuses (`INSIDE_ENDCARD`) rather than pushing it again — otherwise a 1ms nudge grew the project by 1ms, forever.
- Speed is `source/target`, written to the segment **and its speed material** — `pace` reads the material first, so a clip whose material still says 1× reads as un-ramped. `--cover IN-OUT` or `--src-dur` sets the source window (passing both is refused); otherwise 1×.
- `--src` defaults to **0**, the start of the media. It defaulted to `--at` until 2026-08-26, so `add --at 30` silently began 30s into the file.
- Prints the segment id, track name + index, and a `layout broll --at … --track NAME` reminder (name, not a stale N).
- **Copies the file into the draft** (`Resources/CapcutctlMedia/`, unique name from the parent folder so three `screen.mp4` takes don't collide). CapCut is sandboxed and cannot read Desktop/`rl2` folders it didn't pick itself — that's the "Link media" dialog. `--no-localize` keeps the original path. `capcutctl localize --project NAME` retrofits a draft that was written without the copy.

`replace-media` relinks the material (cloning it if shared) and **must not** go through `segment.clone` — that wipes `keyframe_refs` / `common_keyframes`. It refuses upfront rather than rolling back: a missing file, a selector matching more than one clip, or a current window longer than the new file (pass `--retime` to rebuild the window). `trim` refuses a window past the end of the media the same way.

```bash
capcutctl replace-media --project NAME --at 16.3 --track broll --file new.mp4 [--retime]
```

`--track` takes a **name or an index everywhere**, `layout` included — it was `Number()`-parsed there, so the `layout broll --track broll` line `add` prints resolved to `NaN` and matched nothing.

Nudge after the fact with `trim` / `shift` / `remove` / `volume` / `fade`. `shift` uses the same extend-or-refuse policy as `add`. `fade` clones a verified `audio_fade` extra (`fade_type`, `fade_in_duration`, `fade_out_duration`) harvested from Higgsfield/IKEA — it does not invent fields.

**`trim` on the talking head is a 1× window slip, or it is a mistake.** Speed is `source/target`. Lengthening the source and leaving the target puts the face above 1× — forbidden, same as `pace` touching the principal track. To drop a line or keep a word, recut with `cut --keep` so the clip's *length* changes and speed stays 1. See `capcut-editing-talking-head`.

## Scale punch — `keyframe`

Scale-only, cloned from logo `popKeyframes`. Offsets are **absolute source positions** (`source.start + ramp`), not 0. A clip added with `--src 90` that punched at offset 0 would clamp to a dead hold. Two keys that clamp to the same offset are refused (`KEYFRAME_CLAMPED`).

```bash
capcutctl keyframe --project NAME --at 43.2 --track broll --to 2.4 --hold 1.6
```

Position punches wait on a harvested `KFTypePositionX/Y` block. `capcutctl harvest` now walks
**all 88 drafts** and writes two: `positionScale` (a `Line` block from IKEA Refund) and
`positionScaleEased` (a real `FreeCurveInOut` block from Higgsfield Refund, with genuine
`left_control` / `right_control` bezier handles, covering PositionX + PositionY + ScaleX).
Copy one of those; do not invent the fields.

**Prefer the eased block.** 57 keyframe points across 10 of his projects use `FreeCurveInOut`;
a linear scale punch reads mechanical where an eased one reads like a camera. Note CapCut writes
`left_control`/`right_control` objects on `Line` points too, so their presence does not mean
eased — test `curveType === 'FreeCurveInOut'`.

## Watchable proxy — `preview` / `diff`

```bash
capcutctl preview --project NAME --out preview.mp4     # 6fps compositor stills + principal audio
capcutctl diff --project NAME --snapshot BEFORE        # what changed since a snapshot
capcutctl harvest                                      # catalogue transitions / SFX / masks / Line + eased Position+Scale blocks
```

`preview` reuses `qa`'s compositor (speed-aware source time). It is not CapCut's export. `harvest` is catalogue-only — there is no `--apply`.

## What it does NOT do

No captions (those stay outside CapCut), OTIO, HTTP CapCut APIs, or driving CapCut's UI to export. No inventing effect/filter/sticker/Position-keyframe structures — harvest a real one first (`capcutctl harvest`). Moment-finding for screen recordings is `capcutctl find`. Music beds are `finish --music`, not CapCut's stock library.
