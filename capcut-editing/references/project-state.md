# Project state

**Do not keep a live source list in this file.** Drafts churn. A stale list
reads as fact. Read the machine instead:

```bash
capcutctl projects                 # every draft, with duration/fps/track count
capcutctl scenes  --project NAME   # every segment: time, track, and its layout style
capcutctl inspect --project NAME   # canvas, tracks, active timeline
capcutctl doctor  --project NAME   # integrity; must be error-free before handover
```

Deleted drafts go to `…/com.lveditor.draft/.recycle_bin/<name>/`, so "missing"
usually means recoverable.

## Sources

Camera and screen-recording paths belong in the user's own notes, or as
environment variables for the legacy scripts:

```bash
export CAPCUT_CAM=/path/to/face.mp4
export CAPCUT_BROLL=/path/to/screen.mp4
```

Indexes cache under `~/Downloads/.video-index/` as
`<name>.energy10.json`, `<name>.whisper-<model>.json`, `<name>.ocr.json`.

## The geometry source of truth

The layouts were measured from a real timeline and live as data:
`presets/layouts.json` in the capcutctl repo. **That file is the record** —
the project it came from may be deleted without loss. Do not re-derive the
numbers from a live project.

## Decisions that must not be silently undone

- **Transitions are part of the house style**, not a deviation. See `style.md`
  → "The seam formula". `capcutctl polish` owns them. **Video effects** other
  than the `Blur` background plate (`layout background`) stay off unless the
  user asks.
- **Overlays only.** Main track always empty. See `style.md` rule zero.
- **Face stays 1×.** Recut length with `cut --keep`; never speed the talking head.

## Known open, project-wide

- **B-roll matching is unsolved** — see `capcut-editing-screen-recording`.
  `capcutctl polish`, `pace`, `wrap` / `zoom` / `logo`, `finish` / `music` /
  `timeline` are built. Use `polish --motivated` and `finish --music` on the
  last pass. See `finish.md`.
