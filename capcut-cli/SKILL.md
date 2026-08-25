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

`capcutctl` is installed (`~/.local/bin/capcutctl`, source at
`~/Documents/Codex/2026-08-23/can-x20/outputs/capcut-editor-cli`, `npm link`ed).

**Do not hand-write `draft_info.json` for anything below.** It is already solved, tested, and
transactional. Hand-editing loses the snapshot, the root/timeline pairing and the mirror sync.

## Commands

```bash
capcutctl cut VIDEO [--keep …] [--project NAME]      # talking-head cleanup (see below)
capcutctl qa  --project NAME --times 3,9,15 --sheet  # composite real frames + contact sheet
capcutctl find "agent running" --media F --shows --strip   # when is it on screen
capcutctl find "قروك بيلد"     --media F --says            # when was it said
capcutctl close                                      # quit CapCut, wait for it to exit
capcutctl rm --project NAME                          # to .recycle_bin, registry cleaned

capcutctl projects                                   # list drafts
capcutctl scenes   --project NAME                    # every segment: time, track, style
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

## The signature — `wrap`, `logo`, `endcard`, `zoom`

```bash
capcutctl brands                                       # what is known, and which need a PNG
capcutctl wrap    --project NAME --words TRANSCRIPT.json [--text Follow] [--plan]
capcutctl logo    --project NAME --at 8.25 --brand grok [--scale 0.36] [--hold 2.5] [--pos x,y]
capcutctl endcard --project NAME [--text Follow] [--at S]
capcutctl zoom    --project NAME --auto | --at S[,S...] [--to 1.15] [--hold 1.6]
```

`wrap` is the "final touches" pass: brand logos keyed to the moment he says the name, the
closing card, and a push-in on every talking-head scene. `--plan` shows it without writing.

**Brand logos.** Measured across 11 projects: scale `0.01 → 0.20–0.57` over **0.07–0.17s**,
held ~2.5s, with `"Pop!" "Pon!" Pitch height` **0.1s ahead** of the picture. Each brand pops
**once**, when he introduces it — never on later mentions.

**The endcard.** Starts at **93–98% of duration** (default 96%), scale `0.01 → 1.4–3.4` over
**0.07–0.20s**, with `Culin…` **coincident**, not leading. Text varies by video — `Follow`,
`نشر`, `دليل`, `CV` — so it is a parameter, defaulting to `Follow`.

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
capcutctl polish --project NAME [--lead 0.14] [--track N] [--no-transitions]
```

Puts a transition and its matching sound on every visible cut, using the grammar measured
from Hermes-agent, Higgsfield Refund, Content System and IKEA Refund:

| pair | transition | sound |
|---|---|---|
| layout change | `Horizontal Triptych` | `Woosh` / `swish_whoosh` (5/5 in his projects) |
| jump inside a scene | `Flash` / `White Flash 2` / `Glitch Flash II` | `Decision / choice / click` (6/7) |
| the machine doing something | `Glitch` | `Glitch sound that matches the sound logo` (2/2) |
| the payoff, once, on the last cut | `Flash` | `Coin cashier shop item get 4` |

**The sound leads the picture by 0.14s** — measured median across 20 paired cuts, not invented.
Volume 1.0, transitions 0.20–0.33s. Never the same pair twice running.

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
branded endcard comes along and is slid to sit immediately after your scenes. `--from NAME` for a
different template, `--blank` to drop the template content.

`--scenes` is `START:END` on the timeline, `@SOURCE` for the media in-point, seconds throughout.
It prints **`contentTrack`** — the track index your scenes landed on. The layout commands need it.

## The three layouts

Exact measured geometry from `presets/layouts.json`, captured from `grok-build-claude`. Never
recompute these numbers, never invent new ones.

| | subject | companion |
|---|---|---|
| `split-screen` | fills the BOTTOM half from y=960; `Split`/line mask, `rotation 180` | indigo bar on the seam |
| `circle` | upper-left circular avatar | white ring (**which carries its own circle mask**) |
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

## doctor cannot see the picture

It validates structure only. A split at 900/1020 instead of 960/960, and an indigo frame 47px off
its content, both passed `doctor` clean. For pixels:

```bash
capcutctl qa --project NAME --times 3,9,15 --guide 960 --out qa/
```

It composites any frame outside CapCut and prints each segment's on-canvas rect. Check the numbers
first, then look at the frame.

## What it does NOT do

No transitions, speed ramps, keyframes, text, audio or SFX placement; no effect structures invented
from scratch; no zoom-to-bbox. For those, capture a verified template from a real CapCut project
first — that is how the three layouts were built.
