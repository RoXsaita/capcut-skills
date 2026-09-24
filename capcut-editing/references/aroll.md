# The talking head (A-roll)

`capcutctl cut` does the mechanics: transcribe (mlx large-v3-turbo), build the acoustic energy
index, split beats on dead air, snap every boundary to a real onset/trough, detect takes and
repeated lines, auto-repair computable seam faults, pack the timeline gapless at 1×. The fast
path is **one analysis → one semantic review → one dry run → one build → one script audit →
one doctor-gated hand-off**, then stop for sign-off.

```bash
capcutctl cut FACE.mp4 --lang ar
capcutctl cut FACE.mp4 --keep 0,2,3,6-10 --order 0,2,3,6,7,8,9,10 --dry-run
capcutctl cut FACE.mp4 --keep 0,2,3,6-10 --order 0,2,3,6,7,8,9,10 --project NAME
capcutctl scenes --project NAME --transcript
capcutctl doctor --project NAME
```

`--order` is the final narrative order (an exact permutation of the kept ids). Repeatable
`--trim-beat ID:in=SECONDS` / `ID:out=SECONDS` only move an edge inward and are refused when
unsafe. `cut --review decisions.json` takes the same decision as a durable v1 file. After a
user tweak, recut the signed-off project in place with `cut FACE.mp4 … --into NAME`; `build`
then re-anchors every graphic.

The `scenes --transcript` audit joins transcript segments that overlap a clip boundary, so a
boundary word can appear twice; it is an audit feed, not proof.

## Your job: the calls a transcript cannot make

The tool does most of the work, but it cannot understand the finished argument. Its proposed
"last take, last instance of every repeat" is a starting point, not an answer. Read the complete
surviving script aloud or in sequence and make the calls a transcript cannot make:

- **which take** — speakers warm up as they go, so the last is usually best
- **which instance of a repeated line** — the house rule: *"generally the last cut of a specific thing
  is better."* Sanity-check that the last is also the most complete; it usually gains a word
- **false starts** — a short beat whose full version appears later. These often do *not* cluster
  as duplicates, because the complete version continues past the shared opening
- **near-duplicates the clustering missed** — different phrasings of one idea
- **running order** — use `--order` when later retakes belong earlier, or when source order is not
  the clearest hook → explanation → proof → payoff → CTA
- **whole-script coherence** — no missing premise, contradictory claim, duplicated payoff, or CTA
  fragment; the first and last scenes deserve explicit scrutiny because retakes collect there

Everything else — timings, boundaries, dead air, frame quantisation, seam repair — is arithmetic.
Do not hand-pick timestamps. See the procedure below when a boundary needs diagnosis or you are considering overriding a refusal.

## The one idea that matters

Whisper is **semantic** and its timings lie (word starts are contiguous-filled, off by up to
~0.7s). The energy index is **acoustic** and sample-true but knows no meaning.

> Whisper decides *which words*. The energy index decides *exactly where*.

Every seam defect in this project's history came from trusting Whisper alone. Boundaries come
from `onset_after()` and `trough()`. This is enforced in code; you cannot get it wrong by
accident any more.

## Escalate only when needed

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

This produced a cut the user reviewed and called perfect, with "literally no mistakes".

> **The mechanics are now `capcutctl cut`; do not perform them by hand.** They are arithmetic,
> tested, and doing them manually is how the defects got in. The ordinary workflow should be
> fast. Render re-transcription and seam contact sheets are diagnostic escalations, not mandatory
> toll gates before every editable A-roll project.
>
> Read on for **why** each step exists — before overriding anything, and when a cut comes back
> wrong and you need to know which assumption broke.

1. **Transcribe** with word timestamps. Cache it.  *(automated)*
2. **Build the energy index.**  *(automated)*
3. **Split into takes.** Look for the hook line repeating after a long silence.  *(automated — detection only; the choice is yours)*
4. **Prefer the latest complete take**, not the latest fragment. Speakers warm up as they go, but a
   later take can still stutter, omit a premise, or exist only to replace a middle sentence.
5. **Group into beats** — one idea per beat.
6. **Last instance of every beat wins.** The house rule, verbatim: *"generally the last cut of a
   specific thing is better."* Sanity-check that the last is also the most complete; it usually
   gains a word.
7. **Hunt the three in-take defects:**
   - hesitation — silence > 0.6 s *inside* a Whisper word → trim to ~0.25 s
   - filler — a short leading phrase that adds nothing → cut whole
   - stutter — the same word twice in the word list → cut the first
8. **Place every boundary with the energy index, never with Whisper timings.**
   IN → `onset_after(t)` minus ~2 frames. OUT → `trough(t)`.
9. **Lint.** *(automated — and every computable fault is auto-repaired; `cut` refuses to build if one survives)*
10. **Quantise to whole frames** using position differences (`us(t+n) - us(t)`).  *(automated)*
11. **Agent semantic review.** Read the full proposed script in its intended order. Remove false
    starts, retakes, duplicate ideas and CTA fragments; preserve unique earlier beats; use
    `--order` when later-recorded replacements belong in the middle. Check the opening and ending
    explicitly.
12. **Dry-run the reviewed decision.** Pass `--keep`, an exact-permutation `--order`, and only
    acoustically safe inward `--trim-beat` hints. Read the final order, source/target ranges,
    repairs and lint. A v1 `cut --review` JSON file is the durable form of the same decision.
13. **Write CapCut, then hand it off.** Close CapCut and run the same reviewed decision with
    `--project NAME` instead of `--dry-run`; build overlays-only with the main track empty, run
    `doctor`, and if it is error-free tell the user the project is available in CapCut. Stop for
    A-roll approval before layouts, B-roll, pace, polish, music, or finish work.

## Diagnostic escalation

Before A-roll approval, the `doctor` check is the default structural QA. Do not generate a full
motion proxy, all-cuts contact sheet, top-level `capcutctl review` bundle, or render
re-transcription unless the user explicitly requests a portable artifact or lint or the user
reports a named defect that needs one. `--force` by itself does not justify a render; exact 1×
source-contiguous findings are resolved by inspecting the joined source ranges.

When a specific defect exists, use the smallest check that answers it:

- **Render and re-transcribe** when playback suggests missing/repeated words, a hallucinated tail,
  or a transcript-to-edit mismatch.
- **Contact-sheet or `qa` the seam** when a visible jump, crop, or head-position change is at
  issue.
- **Inspect audio around the named seam** when a non-contiguous lint finding remains, or playback
  reveals a clipped onset, breath, loudness change, or unnatural pause.
- **Top-level `capcutctl review`** may generate a proxy, EDL, and contact sheet for portable
  review. It is not the same as `capcutctl cut --review decisions.json`, which consumes an
  editorial decision file.

Only use `--force` after the named finding has been inspected and its safety is documented. An
exact source-contiguous neighbor pair can be a linter false positive because the OUT boundary is
evaluated alone even though no source audio is removed. `--force` must never substitute for an
incomplete sentence, clipped word, or unsafe trim.

## Rooms for improvement

Known-weak, in the order worth fixing:

- **The lint margin is one example wide.** 0.28 s accepted vs 0.35 s rejected. Every future cut the user
  signs off on should be appended to a calibration set, and the thresholds re-derived. Ask the user to
  flag bad seams by timecode; each one is a labelled negative.
- **No breath detection.** Breaths sit around −45 dB and currently read as silence. They are
  usually worth keeping at a sentence start and cutting mid-phrase. `head_silence` cannot tell
  them apart from room tone; a spectral check (breath is broadband, room tone is not) would.
- **No pitch/prosody signal.** A sentence that ends on falling pitch is a safe cut; one on rising
  pitch is mid-thought. This would replace the fragile silence heuristic with the thing the ear
  actually uses.
- **No loudness matching across seams.** Two clips from different parts of a take can differ by a
  few dB and the join is audible even with perfect timing. Measure per-clip LUFS and flag
  outliers.
- **The video side of a seam is unchecked by machine.** The contact sheet is read by eye. Frame
  differencing across each cut pair would flag head-position jumps automatically.
- **Take detection is automated** (`detect_takes` — a long silence or the opening line
  coming round again). You still choose which take to keep.
- **Exact source-contiguous neighbors can false-positive lint.** The linter should evaluate the
  joined pair and exempt a boundary when one beat ends exactly where the next begins at 1×.
- **Boundary recovery is inward-only.** `--trim-beat` safely removes edge material but cannot
  expand outward to recover a clipped word. A future safe outward mode should use the acoustic
  index and first-word protection rather than raw timestamps.
- **Semantic defects are only proposed, not decided.** Incomplete sentences, repeated CTA starts,
  and retakes recorded at the end still need an agent to remove/reorder them. Future handout
  warnings can make that review faster, but should not pretend to understand the argument.
- **End-to-end editorial review remains with the user.** `doctor` validates the project
  structure; the user can review the actual editorial result in CapCut. Render-based checks are
  available when a specific discrepancy is reported.
