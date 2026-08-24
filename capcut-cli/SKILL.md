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
capcutctl layout background   --project NAME
capcutctl layout list

capcutctl apply    --project NAME --spec FILE [--dry-run]   # arbitrary edits, v1 spec
capcutctl snapshot --project NAME --label WHY
capcutctl history  --project NAME
capcutctl restore  --project NAME --snapshot NAME
capcutctl sync     --project NAME                    # repair mirror drift
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
