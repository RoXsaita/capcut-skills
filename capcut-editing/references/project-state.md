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

Camera and screen-recording paths belong in the user's own local notes. Pass them
to the maintained CLI commands, for example:

```bash
capcutctl cut /path/to/face.mp4
capcutctl find "Build" --media /path/to/screen.mp4 --shows --refresh
```

Indexes cache under `~/Downloads/.video-index/` as
`<name>.energy10.json`, `<name>.whisper-<model>.json`, `<name>.ocr-<source-cache-key>.json`.

## The geometry source of truth

The layouts were measured from a real timeline and live as data:
`presets/layouts.json` in the capcutctl repo. **That file is the record** —
the project it came from may be deleted without loss. Do not re-derive the
numbers from a live project.

## Decisions that must not be silently undone

- **Transitions are part of the house style**, not a deviation. See `style.md`
  → "The seam formula". `polish` (and `build`'s seam stage) owns them. **Video effects** stay
  off unless the user asks. **No blurred background, ever**: circles and screen cards sit on the
  clear room plate (`layout background` / `layout screen` place it from the profile). `gate`
  fails `clear-background` on any blurred face copy; `layout background` deletes it and lands the
  plate. Never add CapCut's Blur effect or Background → Blur by hand.
- **One caption style.** English words match the Arabic ones exactly: Changa ExtraBold, size 28,
  white, black stroke (2026-10-11: "I want the English captions to match the Arabic ones").
  `captions` writes it; `gate` fails `caption-style` on any word that differs; `captions
  --restyle` fixes an existing track without touching text or timing.
- **Alpha overlays are premultiplied.** CapCut reads ProRes alpha premultiplied; a straight file
  paints its glow's hidden colour as a haze (the yellow-filled callout, 2026-10-11). Renders
  premultiply at encode; `gate` fails `alpha-premultiplied`; `capcutctl alpha --project` fixes.
- **Overlays only.** Main track always empty. See `style.md` rule zero.
- **Face stays 1×.** Recut length with `cut --keep`; never speed the talking head.

## Known open, project-wide

- **`capcutctl match` is a first pass, not proof** — it scores sentences against change-moments
  and leaves weak/ambiguous beats on the face. Inspect frames and `verify-shots` before treating
  a placement as true. See [broll.md](broll.md).
- **Rendered graphics are `importVerified: false`** until the Mac checklist in the CLI's
  `docs/mograph.md` passes on the CapCut build in use; `gate` reports it as a WARN.
- **The rectangle spotlight (Q04)** is still behind its harvest gate; use `punch` or `callout-box`.

## Build state

`build` keeps `.capcutctl/build.json` (plan hash, shots applied, last verdict) and
`.capcutctl/gate.json` (the last gate report) beside the draft, and each rendered graphic's
sidecar in `mograph/<id>.json`. Read those before re-running anything on a project someone else
started.
