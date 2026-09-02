---
name: capcut-editing-talking-head
description: >
  Cut the talking-head (A-roll) half of a CapCut video and give each scene a layout. One
  command does the mechanical work — transcribe, energy-sync, strip dead air, snap every
  boundary, lint and repair the seams, build the project. Use when trimming a face recording,
  removing duplicate lines, false starts and dead space, or applying the circle / full-frame /
  split-screen looks. Read the capcut-editing hub for the format and the write path.
---

# Talking head — deterministic cut, semantic review

```bash
capcutctl cut VIDEO.mp4 --lang ar
```

Transcribes (mlx large-v3-turbo), builds the acoustic energy index, splits beats on dead air,
snaps every boundary to a real onset/trough, detects takes and repeated lines, and prints a
numbered table plus `VIDEO.aroll.json`. A cold analysis normally takes seconds to tens of
seconds; cached review and build passes are usually sub-second.

Read the transcript in narrative order, not just the suggested keep list. Decide what to keep
and how it should flow. Then dry-run the exact reviewed plan:

```bash
capcutctl cut VIDEO.mp4 \
  --keep 0,2,3,6-10,13-14,16-19,22 \
  --order 0,2,3,6,7,8,9,10,13,14,16,17,18,19,22 \
  --dry-run
```

If the final order, ranges, repairs, and lint are sound, close CapCut and run the same reviewed
decision with `--project my-video` instead of `--dry-run`. It applies the selection, auto-fixes
every computable seam fault, packs the timeline with no gaps, preserves the face at 1×, and
writes an editable CapCut project. `--order` is the final narrative order; without it, `--keep`
stays in source order.

Use repeatable `--trim-beat ID:in=SECONDS` or `ID:out=SECONDS` only for an excessive edge the
acoustic index can safely move inward. It is not a general micro-editor: it refuses clipped first
words, source overlap, unsafe expansion, and trims that land inside sound. For a reusable agent
handoff, put `sourceToken`, `keep`, `order`, and `boundaries` in a v1 decision file and pass it as
`cut --review decisions.json`. This is different from the top-level `capcutctl review` command,
which renders optional viewing artifacts.

This is the normal fast path: **one analysis → one semantic review → one dry run → one project
build → one doctor-gated handoff.** Do not render, re-transcribe, or contact-sheet every ordinary
A-roll before building it. Escalate to those diagnostics only when lint, playback, or the user
reveals a boundary, audio, or visual problem. See `references/procedure.md`.

After the build, run `capcutctl doctor`. If it is error-free, tell the user the project is
available in CapCut.

**Stop there.** Hand off the project and wait for the user's sign-off before adding B-roll,
layouts, pace, polish, or music. Recutting the face after B-roll is on the timeline desyncs
every shot.

The face is **always 1×**. `pace` already refuses the principal track; `clip.trim` that
lengthens the source window without lengthening the target is a speed ramp — same crime.
To drop or reorder a line, re-run `cut` with the reviewed keep/order plan. `--trim-beat` cannot
expand a boundary; if the acoustic boundary clips a necessary word, choose another complete beat
or report the boundary limitation. Never steal the word by playing the face faster.

Then give the signed-off scenes their looks — see `capcut-cli`. The first picture is
proof (B-roll sharing the frame from t=0), not a 5s+ full-face talking-head:

```bash
capcutctl layout auto         --project my-video   # split where B-roll covers, full face else
capcutctl layout circle       --project my-video --at 12 --track content
capcutctl layout split-screen --project my-video --at 30 --track content
capcutctl layout background   --project my-video
capcutctl qa --project my-video --times 4,12,30 --guide 960 --out qa/
```

## Your small but essential job

The tool does most of the work, but it cannot understand the finished argument. Its proposed
"last take, last instance of every repeat" is a starting point, not an answer. Read the complete
surviving script aloud or in sequence and make the calls a transcript cannot make:

- **which take** — he warms up as he goes, so the last is usually best
- **which instance of a repeated line** — his rule: *"generally the last cut of a specific thing
  is better."* Sanity-check that the last is also the most complete; it usually gains a word
- **false starts** — a short beat whose full version appears later. These often do *not* cluster
  as duplicates, because the complete version continues past the shared opening
- **near-duplicates the clustering missed** — different phrasings of one idea
- **running order** — use `--order` when later retakes belong earlier, or when source order is not
  the clearest hook → explanation → proof → payoff → CTA
- **whole-script coherence** — no missing premise, contradictory claim, duplicated payoff, or CTA
  fragment; the first and last scenes deserve explicit scrutiny because retakes collect there

Everything else — timings, boundaries, dead air, frame quantisation, seam repair — is arithmetic.
Do not hand-pick timestamps. Read `references/procedure.md` only when a boundary needs diagnosis
or you are considering overriding a refusal.

## The one idea that matters

Whisper is **semantic** and its timings lie (word starts are contiguous-filled, off by up to
~0.7s). The energy index is **acoustic** and sample-true but knows no meaning.

> Whisper decides *which words*. The energy index decides *exactly where*.

Every seam defect in this project's history came from trusting Whisper alone. Boundaries come
from `onset_after()` and `trough()`. This is enforced in code; you cannot get it wrong by
accident any more.

## Files

| File | Use it for |
|---|---|
| `references/procedure.md` | Fast path, escalation triggers, and known weaknesses — read when diagnosing or overriding |
| `references/indexing.md` | The indexes, the linter's calibration, take/beat selection |
| `references/layouts.md` | The layouts as raw numbers (`capcutctl layout` applies them for you) |

## Escalate when needed

**Before A-roll approval, do not run a full-project `qa --preview`, top-level
`capcutctl review`, `preview`, `--at-cuts`, contact sheet, or render re-transcription.** The
doctor check is the structural review. Use a rendered diagnostic before approval only when the
user explicitly asks for a proxy/render, or lint or the user reports a named problem which
cannot be answered from the transcript, acoustic index, or source ranges.

`--force` alone is not a render trigger. If every remaining finding is an exact 1×
source-contiguous neighbor, verify those ranges and document the linter false positive; do not
render hundreds of frames to prove that no source audio was removed.

After approval, or for a specific observed defect, use the smallest targeted diagnostic:

- a clipped word, breath, loudness jump, or unnatural pause heard in playback
- a visible head-position jump at a cut
- a user-reported bad seam or a cut whose transcript is ambiguous
- composed visual work after A-roll approval, where `doctor` cannot validate pixels

`--force` is not an editorial shortcut. Use it only after inspecting the named finding and
recording why it is safe, such as two adjacent selected beats whose source ranges are exactly
contiguous. Flag any bad seam by timecode; each one is useful calibration evidence.
