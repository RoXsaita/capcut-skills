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
> (`PREFRAMED_MEDIA`); see the `capcut-editing` hub, rule 3.

**Check geometry throughout every recording**, including Mac captures. Windows can
resize or move mid-take. The source dimensions alone do not establish the content
bounds; inspect before and after layout changes.
