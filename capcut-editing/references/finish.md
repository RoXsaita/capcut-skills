# Finish — the last pass

Run after A-roll, B-roll and layouts are picture-locked. Captions happen **outside** CapCut. Music happens **here**.

```bash
capcutctl timeline --project NAME
capcutctl finish   --project NAME                 # scorecard + ASCII (read-only)
capcutctl finish   --project NAME --music         # generate + place the bed
capcutctl polish   --project NAME --motivated     # seams only where the picture changes
capcutctl qa       --project NAME --times …
```

`--plan` on `finish` / `music` writes nothing.

## Laws

1. **A transition is a scene change the viewer can see.** B-roll shot change or layout class (split ↔ full-face). An A-roll splice over the same files list gets a hard cut, not a Flash. `polish --motivated` is this rule. Default `polish` still fires on every splice — do not use that on a finishing pass.
2. **Do not recut speech to a beat.** Voice stays locked. Beat-sync means: generate a bed whose hits are *prompted* at picture-change times, then offset the audio so detected beats land on those times (clamped to ±0.4s). Picture does not move.
3. **Music is background.** Volume ~0.08, fade in 0.4s, fade out into the CTA (Follow on the talking head, not the parked Preset 3 leftover). Instrumental, no vocals, no drop. Out before he asks for the comment.
4. **Do not burn captions** and do not invent a colour grade. Those are a style change; captions have a separate system.
5. **Watch mute, then on a phone.** If an effect is the first thing you notice, it goes.

## Scorecard

`finish` prints an ASCII timeline (tracks stacked the way CapCut shows them) and:

| Check | Fail when |
|---|---|
| same-screen cuts | any A-roll splice over an unchanged picture (do not decorate) |
| same-screen transitions | any existing transition on those splices — a fail, not a reminder |
| motivated vs all-cuts | all-cuts count is much higher — that's the grok-build tell |
| music | missing bed on a Shorts-length video, or volume ≥ 0.4 |
| B-roll volume | a screen-recording clip at 1.0 fighting the VO |
| layout class | a 15s+ stretch that never leaves split-screen and never punches full-screen B-roll |
| cold-open | first 5s are full-face with no screen — hook on the payoff |

## Music

Needs `GEMINI_API_KEY` in `cli/.env` (gitignored) or the environment. Lyria 3 Pro, one call, cached at `.capcutctl/music.mp3` until the picture-change prompt changes or you pass `--regen`.

```bash
capcutctl music --project NAME --plan     # prompt + whether a cache exists
capcutctl music --project NAME            # generate if needed, place, beat-offset
capcutctl music --project NAME --regen
```

The prompt lists picture-change timestamps so the model puts downbeats there. After the file lands, `detectBeats` (ffmpeg PCM, no extra deps) measures the real onsets and `beatOffset` slides the clip. Speech is not a beat target.

## Order

1. `pace` if B-roll is still 1× through waiting.
2. `polish --motivated`
3. `wrap` (logo / endcard / face push-in) if not already done.
4. `finish --music`
5. `timeline` then `qa` then a mute watch.

Do not add a fifth skill for this. The verbs live in `capcutctl`; the taste lives here.
