# Project state

**Do not trust a list of projects written down here — read the machine instead.**

```bash
capcutctl projects                 # every draft, with duration/fps/track count
capcutctl scenes  --project NAME   # every segment: time, track, and its layout style
capcutctl inspect --project NAME   # canvas, tracks, active timeline
capcutctl doctor  --project NAME   # integrity; must be error-free before handover
```

Drafts churn — they get built, reviewed and deleted the same day. An enumerated list in a skill
file is stale within hours, and a stale list is worse than none because it reads as fact. This
file therefore records only what **does not** change: the sources, the signed-off cut, and the
decisions that must not be silently undone.

Deleted drafts go to `…/com.lveditor.draft/.recycle_bin/<name>/`, so "missing" usually means
recoverable.

## Sources

| What | Where |
|---|---|
| Cam / A-roll (Grok Build) | `~/Downloads/E32F9DC9-C213-4EAD-B7D2-C4F61FC731C8.mp4` — 1440×2560, 30fps, 232.4s |
| Screen / B-roll (Grok Build) | `~/Downloads/Screen_Recording_20260822_095151_Grok.mp4` — 1080×2652, 59.94fps, 31 min |
| Talking head (publish-system video) | `~/Downloads/563B00E8-F36B-4E95-8888-F071B9DCCC1C.mp4` — 2160×3840, 107.5s |

The cam file **contains two full takes**: take 1 = 0–121s, take 2 = 121.2–231.1s. Take 2 is the
warmer, tighter one. Internal retries in both (the "publish" line 4×, "cheapest subscription" 4×).

Indexes cache in `~/Downloads/.video-index/` and survive everything:
`<name>.energy10.json`, `<name>.whisper-<model>.json`, `<name>.ocr.json`.

## The geometry source of truth

The three layouts were measured verbatim from the `grok-build-claude` timeline and are now data:
`presets/layouts.json` in the capcutctl repo. **That file is the record** — the project it came
from may be deleted without loss. Do not re-derive the numbers from a live project.

## Decisions that must not be silently undone

- The **usage-limits beat was deleted by the user** as too long. Deliberate; do not restore it.
- **Transitions are his style, not a deviation.** *(re-measured 2026-08-26 across 88 drafts:
  342 transitions in 57 projects.)* The old "zero transitions" note here came from `IKEA Refund`
  alone, which is the one outlier with none. `capcutctl polish` owns them — see `style.md`
  → "The seam formula". **Video effects** genuinely stay off: of 402 in the library, 370 are the
  `Blur` background plate `layout background` already writes. Adding any other effect, or a
  colour grade, is still a style change — confirm first.
- **Overlays only.** Main track always empty. See `style.md` rule zero.
- Deliberately excluded from the Grok Build B-roll: the two `"That name isn't allowed"` publish
  rejections, and the notification shade at 8:25 (personal content).

## Known open, project-wide

- **B-roll matching is unsolved** — see `capcut-editing-screen-recording`, phases 2 and 3.
  `capcutctl polish` (transitions + SFX), `pace` (speed ramps), `wrap` / `zoom` / `logo`
  (signature) are built. Use them. Do not skip the signature pass because this file once
  said they did not exist.
