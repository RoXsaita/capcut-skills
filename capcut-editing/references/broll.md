# Screen recordings (B-roll)

The premise, in the author's words:

> **Every single sentence I say must be matched to the exact thing happening on screen.**

If the narration says "I tapped Build", the frame is the moment Build is tapped — ideally with a
punch onto it. Not approximately. A weak match stays on the face; that is a valid answer.

## The loop

```bash
capcutctl match --project NAME --screen SCREEN.mp4 --out shots.json     # sentence → moment, globally aligned
capcutctl verify-shots --project NAME --shots shots.json                # blind before/action/after; CONTRADICTED blocks
capcutctl find "Publish" --media SCREEN.mp4 --shows --strip             # when is it on screen (with frames)
capcutctl find --media SCREEN.mp4 --moments                             # rl2 takes: when did anything change
capcutctl punch --project NAME --on Publish --segment ID --dry-run      # eased push onto a named element
capcutctl ramp --project NAME --segment ID --speed 20 --dry-run         # ramp the wait, land the result at 1×
capcutctl qa --project NAME --times 18.6 --expect "18.6=Publish"        # the composited frame shows it
```

`match` is a first pass, not proof. `build` applies the reviewed `shots.json` once, then
`layout auto`; use `punch`, `ramp` and `pace` for the per-shot timing it cannot infer.

## Build each shot from evidence

Start from a reviewed `capcutctl match --project NAME --screen FILE` shot list when one
exists. Weak matches (`flag` / `none`) stay on the face — that is a valid answer. Then
keep the exact narration phrase, source file/range, timeline range and inspected evidence
together. `match --apply` writes only through `layout.screen` / `add` / `pace` / `punch` /
`ramp`. `verify-shots` is the blind before/action/after check; CONTRADICTED blocks the build.

- **Verify the verb.** For a click or change, inspect before/action/after frames or a short
  source playback. A labelled button alone proves neither a click nor a successful result.
  If the evidence is missing, find another take or flag the claim as unverified.
- **Separate waiting, action and result.** Trim or accelerate idle loading; keep the useful
  interaction readable and give its result a stable hold. Play that hold at phone size to
  judge its length. `pace --auto` only infers source gaps. If a source span includes both
  waiting and useful action, place them as separate shots first; apply per-clip
  `pace --at … --speed …` to the waiting shot and recheck the action/result timing.
- **Show the requested evidence, not only its summary.** When the user records expanded
  tool calls, preserve the opening action and emphasize the actual tool name and result.
  When narration quotes a prompt, land a native position/scale move on that exact prompt
  during the quoted words; move to the answer only when narration moves there.
- **Return to the speaker.** Use full-face for context, reactions and connective narration
  that has no useful screen evidence. A product photo belongs at a reveal/payoff, not
  throughout every mention of the product.
- **Choose one focus.** Write what the viewer should notice. Crop/zoom to an inspected
  rectangle and leave caption space; use a highlight only if it makes that target clearer.
  Avoid simultaneous competing callouts, zooms and transitions. A stable shot is valid.
- **Check the assembled timing.** Verify the action/result against the spoken phrase after
  trimming or changing speed. Recheck rest, peak and return when adding camera movement.

## Mapping a long recording — nothing missed, by construction

Scene detection alone misses what matters most: a `+` clicked, a dropdown opening, a toggle
flipping. Detect locally, label with a model:

1. **Detect** every change without a model: `find --moments` on rl2 takes (the recorder's own
   per-frame change signal), otherwise `find --shows --refresh` OCR on the whole recording.
   A vision model is for *labelling* candidate moments, never for detecting them.
2. **Label** only the stable states and the changed regions at the moment of change: what app
   and page, what was done, what the result was.
3. **Bind** each narration beat to a concrete moment. If the narration names something the map
   does not contain, re-inspect that range at a finer grain before placing anything.

## Framing, zoom and callout rectangles — derived, never eyeballed

1. Take the target box from evidence: OCR word boxes (`find --boxes`), the change region, or the
   element `punch --on TEXT` locates. Refine it on the frame and confirm it contains exactly the
   intended element.
2. Pad 6–10% per side and clamp to the frame.
3. Let the CLI do the transform: `punch` / `keyframe --focus X,Y,W,H` compute scale and position
   from the source rectangle. The profile caps punches (`camera.punchMax`); beyond that, choose a
   tighter shot instead of a bigger zoom.
4. Ease in, hold while the narration covers it, ease out — the CLI's default curve.
5. `callout-box` rectangles are canvas pixels on a static shot: read the shot's on-canvas rect
   from `qa`, convert the source box, and confirm on `mograph preview --background` of that frame.
6. **Verify at every hold point:** `qa` the rest, peak and return of each zoom and every layout
   change. Target inside, centred, sharp, nothing important cropped.

## Standing rule: the recording goes in whole

Every B-roll clip is imported at its **full capture resolution**, from a path that will still
exist next week. Crop, pan, zoom, trim and speed are CapCut properties — `layout broll --row`,
`layout screen`, `add --src/--dur`, `keyframe`, `pace` — not ffmpeg filters applied on the way
in. The AI Video Editor B-roll was cropped 1920×1080 → 1080×960 in a session scratchpad and
imported flat; the picture was right and nothing could be changed afterwards, which is the one
outcome this whole toolkit exists to avoid. `add` refuses it now (`PREFRAMED_MEDIA`,
`EPHEMERAL_MEDIA`). The native verb for every tempting ffmpeg pass:

| Tempting ffmpeg pass | What it costs the editor | The CapCut-native verb |
|---|---|---|
| `crop=` to the split-screen half | Cannot reframe, re-zoom, or change layout | `capcutctl layout broll --row PIXEL_ROW` |
| `crop=` a window capture | Same, and the window treatment is lost | `capcutctl layout screen --media FULL.mp4` |
| `-ss`/`-t` to cut a subclip | Can only extend inside your window | `add --src S --dur S` on the whole file |
| `setpts=`/`atempo=` for speed | Speed stops being a slider | `add --cover IN-OUT`, `pace`, `ramp` |
| `zoompan` for a punch-in | A camera move nobody can retime | `punch`, `keyframe --focus` |
| `concat` a montage | One clip where there were eight | one `add` per shot |

Rendered media is allowed for one thing only: `mograph` graphics, imported `--generated` with a sidecar that re-renders them.

## Standing rule: never full-frame B-roll over the face

Tried and rejected outright:

> *"you used the screen recording as a cover, which I don't like and it's weird to edit."*

B-roll shares the frame with the speaker via a layout (circle inset, split screen or the screen
card) — it does not replace them. `layout auto` applies the rule; `capcutctl layout list` prints the geometry.

Historical note: an older project (`reference A`) used a **different** `Split` mask config —
`centerX 0.0435, centerY 0.4969`, with the screen on top and the face on the bottom — versus the
locked preset's `centerX -0.0046, centerY 0.5415`. The locked values come from a scene he
positioned by hand and are authoritative; the older ones are recorded only so nobody assumes the
split can go only one way. Neither was verified by rendering.

## Browsing, proof, and zoom sound

When narration says Claude opens sites, searches and clicks, establish the wider browser
and show actual activity with a speed ramp. Save tight framing for the prompt, price or
result being discussed. Match each follow-up question to that exact visible prompt; a
generic chat scroll does not prove it. Use the house Enter / click / select cue at each
screen zoom landing and verify it is audible in the actual exported section. Prefer
CLI export grids for authorized exports over manual timeline-click QA; see the hub's
[preview-loop.md](preview-loop.md).

## Screen — the change signal first (rl2 takes only)

```bash
capcutctl find --media /absolute/take/screen.mp4 --moments                 # what happened, when
capcutctl find --media /absolute/take/screen.mp4 --moments --focus Hermes  # …while one app was up
capcutctl find "signal bay" --media /absolute/take/screen.mp4 --moments --context
```

An rl2 take writes `change.ndjson` (per-frame mean absolute luma delta, 0..255, plus an
8×8 block mask) and `trace.ndjson` (every frontmost-app switch). `--moments` reads them
instead of OCRing a 1 fps grid, and it is not a small difference:

| | 1 fps grid (`--shows`) | change signal (`--moments`) |
|---|---|---|
| samples on a 22-min take | 1329 | 86 |
| time to build | 7m 41s | 36s |
| resolution of an answer | the whole second it sampled | the frame the screen changed on |

With no query it lists every moment — start, end, peak score, changed block count, and the
frontmost app. With a query it OCRs one frame per moment and reports only the hits. The
cache is bound to the source fingerprint *and* `--min-score`, so changing the threshold
rebuilds rather than silently mixing two different moment sets.

`--moments` also sharpens `--shows`: when a sidecar is present, a run reported at second
`587` is annotated `(changed at 586.52s)`. Verified against frames — 586.40 was the old
screen, 586.60 the new one. Cut on the annotated time, not the rounded second.

**Where it does not apply.** A recording with no sidecar, or a trimmed/derived copy whose
frame clock disagrees with the media duration, is refused by name and you fall back to
`--shows`. That is most recordings. `--focus` needs the trace and names the apps that were
actually frontmost when it finds none — match the trace's process name, not the Dock label.

**What `--moments` does not tell you.** That an action *succeeded*, or what the change was.
A moment is "these pixels moved". The verb still has to be verified on frames, exactly as
below.

## Screen — OCR (B-roll)

```bash
capcutctl find "agent running" --media /absolute/take/screen.mp4 --shows --strip
capcutctl find "agent running" --media /absolute/take/screen.mp4 --shows --refresh
```

`find --shows --refresh` builds a missing or stale index using Vision OCR. Caches are bound
to the canonical source and its fingerprint, with duration and sampled coverage.
An unverified basename-only `screen.ocr.json` is not evidence for another take.
Check the reported coverage; a 132-second dump cannot stand in for a 796-second
recording. `--says` requires a verified transcript from `cut`; it does not accept
an unrelated legacy transcript with the same basename.

### Querying — keyword discipline

Loose keywords are worse than useless because they look like they worked.

| Bad key | Why | Good key |
|---|---|---|
| `wave` | matched **1006s** — "wave progression" is in the prompt text on screen all build | `call wave` |
| `imagine` | matches the nav tab, always present | `image to image` |
| `agents.md` | fine, but only 4s long | pair with `workspace instructions` |

Reject misleading matches during frame review (e.g. a failed-generation notice or
a prompt describing a result). `find` does not have a `--forbid` option.

**Verify span length against the beat's need.** A 4-second match cannot fill an 8-second beat —
either shorten the shot, split the beat across two shots, or pick a different moment.

### Content windows can be tiny

In a 31-minute recording, the actual working game was on screen for **~4 seconds** (1772–1776).
Everything else was menus, thinking spinners, and the publish flow. Always check the *end* of a
shot, not just its start — shots drift onto the next screen. Slowing a shot (speed 0.7–0.8) is a
good way to stretch a narrow window without drifting.
## ROI (which part of the frame to show)

Phone screen recordings are often taller than 9:16 (e.g. 1080×2652 vs a 1080×1920 canvas), so
every shot needs a vertical crop decision, and **the right crop differs per shot**.

OCR TSV output (`tesseract f.jpg stdout tsv`) gives word boxes and can suggest a ROI, but in
practice it was **unreliable** — loose token matching pushed most results to the clamp. It is a
hint, not an answer.

**What actually works:** render the candidate crops and look at a contact sheet.

```bash
ffmpeg -ss "$T" -i screen.mp4 -frames:v 1 -vf "crop=1080:960:0:$CROP_TOP" out.png
```

Build a grid of candidates with a y-ruler drawn on, pick by eye, then re-render to confirm.
Eleven ROIs were fixed this way in two passes. This is fast and it is correct.

> **This ffmpeg pass produces a PNG you look at — never media you import.** `CROP_TOP` is
> the top of this 1080×960 source crop. `layout broll --row` takes the **centre** of the
> visible source window: for this example use `--row "$((CROP_TOP + 480))"` on the
> **full-frame** recording. For other source widths/scales, use the inspected centre row
> and check the command's reported `window`; 480 is specific to this unscaled example.
> Import a cropped .mp4 instead and the rows outside the crop cease to exist, so the ROI can never be revised in CapCut — the
> exact complaint that came back from the AI Video Editor video. `add` now refuses such media
> (`PREFRAMED_MEDIA`); see the hub's non-negotiables.

**Check geometry throughout every recording**, including Mac captures. Windows can
resize or move mid-take. The source dimensions alone do not establish the content
bounds; inspect before and after layout changes.

## Privacy — hard constraint

Log **that** a key was pressed and **when**, never **which**. Content would capture passwords.
Inspect recordings for personal content (notification shades, DMs) and exclude or flag it
before placement. Whole-screen capture can include notifications even with a privacy-aware
trace logger. The historical recorder notes describe trace restrictions, not a guarantee
that arbitrary video pixels are private.
