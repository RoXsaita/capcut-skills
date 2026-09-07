# Finish — the last pass

Run after approved A-roll, B-roll and layouts are picture-locked. Captions happen
outside CapCut; preserve space for them. Keep voice, music and SFX on identifiable lanes.

```bash
capcutctl timeline --project NAME
capcutctl finish --project NAME                 # read-only scorecard and proposed seams
capcutctl polish --project NAME --motivated --dry-run
```

## Choose the seams

A picture change makes a transition eligible, not necessary. Read the existing shot
list: what should the viewer notice here? Keep a clean cut if an effect competes with
the action/result. Do not decorate an A-roll splice over an unchanged screen. Review
one focal move/callout at a time; a source path change does not prove a story change.

`polish --motivated` applies all eligible seams. For a reviewed subset, use the existing
`polish` operation's `only` timestamps (timeline seconds, rounded to two decimals):

```json
{"version":1,"operations":[{"op":"polish","motivated":true,"only":[6.2,18.4],"noInteractions":true}]}
```

Save the selected operation as `finish.json`, then dry-run and apply it:

```bash
capcutctl apply --project NAME --spec finish.json --dry-run
capcutctl apply --project NAME --spec finish.json
```

Polish rebuilds transitions and its transition SFX. Include every seam you want to keep.
To preserve hand-made transitions, use `keepExisting: true` and select only new,
undecorated seams; rerunning it on an existing seam can duplicate transitions.
`only` selects transition seams, not interaction/callout cues; `noInteractions: true`
suppresses automatic trace cues.
Keep manually chosen event sounds on their own lane/description. Do not use `polish:sfx`
for them. Check any reported `unavailableSfx` before promising sound is present.

## Mix around the voice

1. Listen to the voice alone across cuts; use native clip volume to fix distracting level
   jumps. Preserve 1x timing and natural dynamics. A-roll already has short seam ramps;
   do not add longer fades that swallow syllables. Apply noise cleanup/EQ only to an audible
   defect and compare in CapCut.
2. Choose a bed for this video's mood and energy, from a local file or a specific brief:

   ```bash
   capcutctl music --project NAME --file /absolute/music/selected.mp3 --volume 0.08
   capcutctl music --project NAME --prompt "VIDEO-SPECIFIC MUSIC BRIEF" --plan
   ```

   `0.08` is a starting gain, not a loudness target. Lower the bed until quiet/dense speech
   stays clear. The CLI writes constant gain plus in/out fades; any rises between phrases
   or ducking envelopes need native CapCut volume automation. Do not claim a flat bed is
   automatically ducked. Voice stays locked; beat alignment moves music only.
3. Audition SFX against the actual words. Lower or omit a cue that masks a syllable or
   creates a second focus. Mute screen-recording audio unless it is intentionally useful.
   Check the hook, a dense explanation, a quiet line and the CTA with everything playing.
4. Measure the **native export** when checking delivery loudness and peak headroom:

   ```bash
   ffmpeg -hide_banner -i final.mp4 -map 0:a:0 -af ebur128=peak=true -f null -
   ```

   Record integrated loudness and true peak against the delivery brief; fix audible
   imbalance/clipping in the editable project and export again. A clip's volume number
   alone cannot establish mix quality. The proxy omits native audio processing.

Music generation needs `GEMINI_API_KEY`; `--file` does not. The selected file/creative
brief is cached separately from picture timings. A first generated bed needs `--prompt`;
`--regen` retries that same direction. Choose a new prompt when the style is wrong.

## Finish and verify

Review B-roll waiting/action/result timing first, then selected seams, logo/endcard/face
emphasis if useful, then the voice/music/SFX balance. Keep source colour unless correcting
a specific defect; judge any correction in CapCut, with screen whites preserved.

`finish` is a structural scorecard: same-screen transitions and hot B-roll are useful
warnings. Cut counts, opening screen coverage and a music gain cannot prove readability,
semantic accuracy or a good mix. Follow [picture and sound review](preview-loop.md):
targeted QA after writes, normal-speed native playback at phone size **with sound**, then
check the export and run `doctor` before handing over the editable project.
