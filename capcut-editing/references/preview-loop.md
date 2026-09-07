# Picture and sound review

Use the smallest check that answers the current risk. Ordinary A-roll assembly still
ends with `doctor` and user approval; it does not require a full proxy render.

## While editing

```bash
capcutctl qa --project NAME --times 3,9,15 --guide 960
capcutctl preview --project NAME --from 9 --to 15 --out preview.mp4
```

Use timestamped frames for source/action evidence, crops, caption space and camera
rest/peak/return. Use a bounded proxy when the question requires playback, such as a
cut syllable or the time spent waiting for a result. Default previews are 360x640 at
6fps; this is too sparse to approve fast animation. Check that motion in CapCut.

The proxy includes principal-video audio plus audio tracks, with clip volume, speed
and native fade durations. Fades keep their original clip timing when previewing a
subrange; the compositor mix preserves stereo. It does not reproduce native audio
effects, volume keyframes or every visual effect. Review audible B-roll in CapCut too.
Do not use the legacy split-screen renderer for delivery or add a proxy-only limiter
that conceals clipping in the actual project.

## Before final delivery

Play the current CapCut project at normal speed, with sound, at phone size. Check:

- the pictured action/result matches the narration and stays readable;
- speech sounds continuous, with no clipped syllables or distracting level jumps;
- music and SFX leave every word clear, including the hook and CTA;
- one clear focus, legible text, usable caption space and clean crop/motion boundaries;
- native transitions, masks, grading and fades look and sound right.

A mute watch can expose visual clutter; it does not approve the mix. Inspect the actual
export, including the opening and ending, then deliver it with the editable project and
localized source media. If playback/export verification has not happened, say so.
Repair identified timestamps and recheck the changed section before final playback.
