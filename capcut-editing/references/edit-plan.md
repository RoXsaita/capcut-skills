# `edit.json` — the edit plan

`capcutctl build --project NAME --edit edit.json` compiles this file into the finished project.
Paths are relative to the plan file. Unknown top-level keys refuse, so a typo is never ignored.

```json
{
  "version": 1,
  "profile": "~/capcut-profile.json",
  "style": "demo",
  "words": "~/Downloads/.video-index/face.whisper-large-v3-turbo.json",
  "shots": "shots.json",
  "layout": "auto",
  "camera": { "stress": true, "reframe": false, "cursor": false },
  "graphics": [ { "id": "hook", "template": "hook-title", "say": "…", "params": { "text": "…" } } ],
  "logos": "auto",
  "endcard": { "text": "Follow" },
  "sound": { "seams": "motivated", "music": { "prompt": "…" }, "duck": true, "loudness": true },
  "notes": "free text for the next agent; ignored by build"
}
```

| Key | Default | Meaning |
|---|---|---|
| `profile` | yours | A per-video override (`harvest --profile` or `reference --profile-out` writes one). Merges over the shipped defaults and the creator's `~/.config/capcutctl/profile.json`. |
| `style` | none | A style from the profile's `styles` (`capcutctl profile` lists them). Its `pace.graphicEvery` becomes the gate's drought target; an unknown name refuses with the list. |
| `words` | the transcript `cut` cached for the face | Word-level Whisper JSON the anchors resolve against. |
| `shots` | none | A reviewed `match` shot list. Applied **once**; later changes go through `match`/`replace-media`, or restore a snapshot. |
| `layout` | `"auto"` | `layout auto`: split-screen where B-roll covers the face, full face elsewhere. `false` leaves layouts alone. |
| `camera.stress` | `true` | Small eased pushes on the words hit hardest (`zoom --stress`). Skipped, with the reason, if the energy index is missing. |
| `camera.reframe` / `cursor` | `false` | Opt-in Vision face reframing / pointer halo from telemetry. |
| `graphics` | `[]` | Rendered motion graphics, below. |
| `logos` | `"auto"` | Brands heard in the cut pop once, on the first surviving mention. `[{ "brand": "claude", "say": "كلود" }]` for explicit ones, `false` for none. A brand with no artwork becomes a text `brand-chip`. |
| `endcard` | none | `{ "text": "Follow" }` — the CTA card on the talking head near the end. |
| `sound.seams` | `"motivated"` | Transitions + their SFX on picture changes only. `false` for hard cuts (a profile with `seams.hardCutsByDefault`). |
| `sound.music` | `false` | `{ "file": "bed.mp3" }` or `{ "prompt": "…" }` (needs `GEMINI_API_KEY`); optional `volume`, `hits` (seconds). Default hits are the graphics and picture changes. |
| `sound.duck` | `true` | Duck the bed under speech with native volume keys. |
| `sound.loudness` | `true` | Match speech/SFX to the profile's LUFS target with peak headroom. A mix it cannot make safe is skipped and reported. |

## A graphic

```json
{ "id": "stat", "template": "number-pop", "say": "تسعين", "occurrence": 1, "offset": 0,
  "params": { "value": 90, "suffix": "%", "label": "أسرع" }, "format": "prores", "sfx": "pop", "allowUnsafe": false }
```

| Field | Meaning |
|---|---|
| `template` | One of `capcutctl mograph list`. |
| `say` / `occurrence` | Anchor: the words as the cut speaks them, and which surviving occurrence. The graphic lands the profile's lead frames (3 at 30fps) before the first word. A word the cut dropped refuses by name (`ANCHOR_ORPHANED`). |
| `at` / `offset` | Timeline seconds, for things with no word. `offset` nudges either form. |
| `params` | Template parameters, below. `layout` is filled from the look at that moment (full-face / split-screen / card) unless you set `layout`, `center` or `box`. |
| `format` | `prores` for rich motion (default), `png-still` for pop/slide templates (default for `brand-chip`), which CapCut animates with native eased keys. |
| `sfx` | Override the template's cue (`pop`, `impact`, `enter`, `select`, `click`, `idea`) or `null` for none — the gate then fails it unless another cue is there. |
| `allowUnsafe` | Permit a box inside the platform UI zones. Rarely right. |

Always look at a template with your real text before building:
`capcutctl mograph preview --template T --params '{…}' --out /tmp/t.png` (frames on a dark canvas,
platform-UI zones tinted red).

## Templates

| Template | Use it for | Params | Sound |
|---|---|---|---|
| `hook-title` | The first-second hook, 2–5 words, key word wiped under an indigo block | `text`, `key?` (word, index, or `false`), `layout?`, `center?`, `hold?` | impact |
| `keyword-super` | A claim's 1–3 key words, key word in the accent | `text`, `key?`, `layout?`, `center?`, `hold?` | pop |
| `number-pop` | A stat: counts up, holds, label under it; Latin digits | `value`, `prefix?`, `suffix?`/`unit?`, `label?`, `decimals?`, `layout?`, `center?`, `hold?` | pop |
| `callout-box` | A rounded stroke that draws around a UI target on a **static** shot | `box: [x, y, w, h]` canvas px, `label?`, `color?` (`accent`/`indigo`), `gap?`, `hold?` | enter |
| `cta-card` | "اكتب [keyword] في التعليقات" comment card, keyword in an indigo chip | `keyword`, `text?` (with a `{keyword}` slot), `layout?`, `center?`, `hold?` | select |
| `brand-chip` | A white pill naming a tool when there is no logo art (automatic under `logos: auto`) | `name`, `logo?`, `from?` (`right`/`left`), `layout?`, `center?`, `hold?` | pop |

`callout-box` coordinates are **canvas** pixels. Get them from the frame you will show: `qa --times T`
prints each segment's on-canvas rect, and `find --boxes` gives OCR boxes in source pixels — convert
through the shot's scale/transform, then confirm on a `mograph preview` with `--background` set to
that `qa` frame. Never place a callout over a clip that is moving (punching or panning) during it.

## Rebuilding

- Change the plan, rebuild. Graphics the plan no longer names are removed; the rest are replaced.
- Recut the face (`cut --into`), rebuild. Every anchored graphic lands on its word again.
- Fix a typo in one graphic without a rebuild: `capcutctl mograph rerender --project NAME --id ID --params '{"text":"…"}'`.
- `build --force` re-runs every stage even when nothing changed.
