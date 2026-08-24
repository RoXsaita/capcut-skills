# The VO cut — the locked procedure

This produced a cut the user reviewed and called perfect, with "literally no mistakes". Follow it
in order. It is ~10 minutes of work for a 4-minute source.

1. **Transcribe** with word timestamps. Cache it.
2. **Build the energy index.** `AudioIndex.build_or_load(source)`.
3. **Split into takes.** Look for the hook line repeating after a long silence.
4. **Keep only the last take** unless it is visibly worse. He warms up as he goes.
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
9. **Lint.** `lint(idx, spans)` must come back empty.
10. **Quantise to whole frames** using position differences (`us(t+n) - us(t)`).
11. **Render, then re-transcribe the render.** One segment per beat, no repeats, no
    hallucinated tail.
12. **Contact-sheet every cut frame** and confirm head size and position hold across each pair.
13. **Then** write CapCut — overlays only, main track empty.
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
- **Take detection is manual.** It should fall out of the transcript (hook line repeated after a
  long gap).
- **Nothing is verified end-to-end after the CapCut write.** The rendered ffmpeg preview is
  verified; the CapCut project is only structurally validated. Worst case they diverge silently.
