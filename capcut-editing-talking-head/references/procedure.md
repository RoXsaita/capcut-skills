# The VO cut — fast path and diagnostic procedure

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
4. **Prefer the latest complete take**, not the latest fragment. He warms up as he goes, but a
   later take can still stutter, omit a premise, or exist only to replace a middle sentence.
5. **Group into beats** — one idea per beat.
6. **Last instance of every beat wins.** His rule, verbatim: *"generally the last cut of a
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
13. **Write CapCut, then watch it.** Close CapCut and run the same reviewed decision with
    `--project NAME` instead of `--dry-run`; build overlays-only with the main track empty, run
    `doctor`, and watch the actual content start to finish in CapCut. Stop for A-roll approval
    before layouts, B-roll, pace, polish, music, or finish work.

## Diagnostic escalation

Do not generate these artifacts routinely. Use the smallest check that answers the observed
risk:

- **Render and re-transcribe** when playback suggests missing/repeated words, a hallucinated tail,
  or a transcript-to-edit mismatch.
- **Contact-sheet or `qa` the seam** when a visible jump, crop, or head-position change is at
  issue.
- **Inspect audio around the seam** when lint remains, `--force` is being considered, or playback
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

- **The lint margin is one example wide.** 0.28 s accepted vs 0.35 s rejected. Every future cut he
  signs off on should be appended to a calibration set, and the thresholds re-derived. Ask him to
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
- **End-to-end verification remains human.** `doctor` validates the project structure; the
  start-to-finish CapCut watch validates the actual editorial result. Render-based checks are
  available when that watch exposes a specific discrepancy.
