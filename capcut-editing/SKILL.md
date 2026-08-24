---
name: capcut-editing
description: >
  Edit real video projects by writing CapCut's project JSON directly, so the user finishes in the
  CapCut UI he actually likes. THE HUB — start here for any CapCut editing request. Covers why
  this exists, the non-negotiable rules, the draft_info.json schema, the safe write path
  (scripts/capcut.py), the user's measured style, pitfalls, and current project state. For cutting
  the talking head use capcut-editing-talking-head; for screen-recording B-roll use
  capcut-editing-screen-recording.
---

# CapCut Editing — hub

Programmatic video editing that hands off cleanly to a human.

## Why this exists

He rejects code-render tools (HyperFrames, Remotion) for this work — not because they can't
render, but because **he can't take over and finish the edit in a good UI**. He edits in CapCut.
So the deliverable is a *CapCut project*, not a rendered file. This works because CapCut stores
projects as plain JSON on disk.

## The family

| Skill | Use it for |
|---|---|
| **capcut-cli** | **`capcutctl` — what is already automated: create a project, the three locked layouts, scene listing, snapshots. Check here BEFORE hand-writing JSON.** |
| **capcut-editing** (this one) | The format, the safe write path, his style, pitfalls, project state |
| **capcut-editing-talking-head** | Cutting the face: the 3 indexes, seam linting, the locked cut procedure, the 3 layout presets |
| **capcut-editing-screen-recording** | B-roll: the `rl2` instrumented recorder (built), the OCR index, ROI, content matching. **The editing half is still unsolved — read its status table first.** |

## The three rules

**0. Overlays only.** His main track is **always empty**. He calls the main track "the cover" and
never uses it — every clip goes on an overlay track (`flag=2`). Confirm against `Preset 3`
(main track `n=0`). See `references/style.md`.

**1. Never build blind.** The first attempt failed ("quality is like 1/100") because 83 seconds of
timeline were written from arithmetic and handed over without a single frame being looked at.
Render an ffmpeg preview → **look at the frames** → fix → repeat → only then write CapCut.
See `references/preview-loop.md`.

**2. Edit quality == index quality.** Every cut you cannot verify is a guess, and guesses are
where the errors were. Never derive geometry either — render it and compare against a frame you
know is right.

## The CLI — the only sanctioned way to write

`scripts/capcut.py` exists because this work was being hand-rolled into one-off scripts, and each
rewrite dropped a step.

```
capcut.py spans   <proj>              the live EDL
capcut.py lint    <proj>              energy-lint every seam
capcut.py strip   <proj> [a] [b]      ASCII energy map
capcut.py preview <proj> [out.mp4]    render the VO from live spans
capcut.py sheet   <proj> [out.png]    contact sheet of every cut frame
capcut.py verify  <proj>              structure + all-copies md5
capcut.py backup  <proj> [tag]
capcut.py write   <proj> <new.json> [--wait]
```

**Never hand-roll a project writer.** `write` validates and refuses on error, refuses while CapCut
is running (`--wait` blocks — background it), writes **every** timeline copy, updates meta +
registry, keeps a pre-write backup, and md5-verifies. Run `verify` after any change.

## Workflow

1. **Probe** sources with `ffprobe`.
2. **Index** — see the two sub-skills.
3. **Cut the VO** — `capcut-editing-talking-head`, then `capcut.py lint` must come back empty.
4. **Preview → look → fix.**
5. **Write** with `capcut.py write`, then `capcut.py verify`.

Work **one section at a time** and check end-to-end. He asked for this explicitly.

## Reference files

| File | Use it for |
|---|---|
| `references/capcut-format.md` | draft_info.json schema, segments, masks, keyframes, the multi-copy write, registration |
| `references/style.md` | Rule zero, his measured signature, SFX palette |
| `references/preview-loop.md` | ffmpeg preview renderer, contact sheets, delivery |
| `references/pitfalls.md` | Concrete traps already hit. Read before starting. |
| `references/project-state.md` | Sources, the signed-off VO EDL, what is done and what is not |

`scripts/` — see `scripts/README.md`.
