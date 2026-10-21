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
  "scenes": [ { "scene": "seam-wipe", "say": "…", "offset": -0.9, "params": { "text": "…", "beats": 2.5 } } ],
  "logos": "auto",
  "endcard": { "text": "KEYWORD" },
  "sound": { "seams": "motivated", "music": { "file": "bed.wav" }, "duck": true, "loudness": true },
  "notes": "free text for the next agent; ignored by build"
}
```

| Key | Default | Meaning |
|---|---|---|
| `profile` | yours | A per-video override (`harvest --profile` or `reference --profile-out` writes one). Merges over the shipped defaults and the creator's `~/.config/capcutctl/profile.json`. |
| `style` | none | A style from the profile's `styles` (`capcutctl profile` lists them). Its `pace.graphicEvery` becomes the gate's drought target; an unknown name refuses with the list. |
| `words` | the transcript `cut` cached for the face | Word-level Whisper JSON the anchors resolve against. Required after a derived-face swap (`replace-media --derived-from`): the derived file has no transcript or energy index, so point this at the ORIGINAL face's `.whisper` JSON. |
| `shots` | none | A reviewed `match` shot list. Applied **once**; later changes go through `match`/`replace-media`, or restore a snapshot by label (`restore --snapshot pre-build`) and run a plain `build`, which rebuilds when its outputs are missing. |
| `layout` | `"auto"` | `layout auto` turns a circle face over non-layout B-roll into a split, and leaves a `layout:screen-recording` card alone. `false` keeps hand-set looks: use it to keep full-screen content under the face circle, which auto would turn into a split. A shot's own `ops` in `shots.json` replaces `match`'s default `layout.screen` (accepted: `clip.add`, `layout.screen`, `layout.apply`, `pace`, `punch`, `ramp`). |
| `camera.stress` | `true` | Small eased pushes on the words hit hardest (`zoom --stress`). Skipped, with the reason, if the energy index is missing. |
| `camera.reframe` / `cursor` | `false` | Opt-in Vision face reframing / pointer halo from telemetry. |
| `graphics` | `[]` | Rendered motion graphics, below. |
| `scenes` | `[]` | Full-frame scenes (`capcutctl mograph scenes`): `scene`, `say`/`at`/`offset`, `params`, `id`. A scene starts **on** its word (it is a cut, not a super that leads it). Placement and the seam-wipe rules: [Scenes](#scenes). |
| `logos` | `"auto"` | Brands heard in the cut pop once, on the first surviving mention. `[{ "brand": "claude", "say": "كلود" }]` for explicit ones, `false` for none. `false` removes earlier `sig:logo` pops and their SFX; a plan whose logos resolve to none also clears the last build's pops (`stages.graphics.cleared` lists `clearLogos`), unless there was no transcript to judge. A brand with no artwork becomes a text `brand-chip`. |
| `endcard` | none | `{ "text": "KEYWORD" }` — the keyword card on the full-face CTA in the last 2–4s; KEYWORD is the word the CTA line asks viewers to comment. This is the default CTA. `false` clears the endcard and its cue (`clearEndcard`); omitted or `null` keeps the one already there. |
| `ending` | the profile's `ending.auto` | The 3-second follow ending appended after the last frame. It opens on the edit's own last picture (captured from the final clip's media with its scale/position), so it continues seamlessly. `true` / `false` (`false` also removes one placed earlier) / `{ "pill", "headline", "sub", "badge", "frame", "noSfx" }` to override the profile's copy for this video (`"badge": ""` hides the badge; e.g. `{ "pill": "الجزء الثاني جاي", "badge": "2" }` for a two-parter). Copy lives in the profile, never in the repo. |
| `sound.seams` | `"motivated"` | Transitions + their SFX on picture changes only. `false` for hard cuts (a profile with `seams.hardCutsByDefault`). `false`, or a seams stage skipped because the first picture is not proof, removes the `polish:*` cues and the transitions build recorded placing; hand-made transitions stay. |
| `sound.music` | `false` | `{ "file": "bed.wav" }` first: the creator's own track from the brief. `{ "prompt": "…" }` is optional, a paid API (`GEMINI_API_KEY`), only when the creator or profile allows it. Optional `volume`, `hits` (seconds); default hits are the graphics and picture changes. With no brief and no file, or a prompt with no key, `build` refuses before its first write (`MUSIC_BRIEF_REQUIRED` / `NO_API_KEY`, pointing at `sound.music.file`). |
| `sound.duck` | `true` | Duck the bed under speech with native volume keys. |
| `sound.loudness` | `true` | Match speech/SFX to the profile's LUFS target with peak headroom. A mix it cannot make safe is skipped and reported. |

**Skipped stages and rollback.** A stage that cannot run is skipped, never silent: it is in
`result.skipped[]` and prints a `SKIPPED <stage> (<code>)` line. Gate `build-stages` FAILs when
loudness was skipped and WARNs for any other skip; name each one in the hand-off. A throw after
a stage has committed rolls the build back to its pre-build snapshot (the error's details carry
`rolledBack`, `snapshot` and `failedStage`): the previous graphics stay, so read build's exit
code, not just the gate. A draft CapCut re-saved (duplicate ids, stripped metadata) is repaired
before a real build.

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

`build` does not read `brand.house`. When the profile names one, write its super template
(e.g. `slab-super`) for Hook and Claim graphics instead of `hook-title` / `keyword-super`, and put
its transition scene in `scenes` at a chapter change. The beats and their sounds stay the same.

| Template | Use it for | Params | Sound |
|---|---|---|---|
| `hook-title` | The first-second hook, 2–5 words, key word wiped under an indigo block | `text`, `key?` (word, index, or `false`), `layout?`, `center?`, `hold?` | impact |
| `keyword-super` | A claim's 1–3 key words, key word in the accent | `text`, `key?`, `layout?`, `center?`, `hold?` | pop |
| `number-pop` | A stat: counts up, holds, label under it; Latin digits | `value`, `prefix?`, `suffix?`/`unit?`, `label?`, `decimals?`, `layout?`, `center?`, `hold?` | pop |
| `callout-box` | A rounded stroke that draws around a UI target on a **static** shot | `box: [x, y, w, h]` canvas px, `label?`, `color?` (`accent`/`indigo`), `gap?`, `hold?` | enter |
| `cta-card` | Opt-in only when the creator asks; never over a full-face clip; the default CTA is `endcard`. "اكتب [keyword] في التعليقات" comment card, keyword in an indigo chip | `keyword`, `text?` (with a `{keyword}` slot), `layout?`, `center?`, `hold?` | select |
| `slab-super` | A hook or claim on solid square slabs: optional small tag above, the line in an ink slab and a brand slab for the key, text rising inside each, accent underline under the key | `text` (1–4 words), `key?` (words of `text`, or `false`), `tag?` (1–3 words), `underline?`, `layout?`, `center?`, `hold?` | pop |
| `brand-chip` | A white pill naming a tool when there is no logo art (automatic under `logos: auto`) | `name`, `logo?`, `from?` (`right`/`left`), `layout?`, `center?`, `hold?` | pop |

`callout-box` coordinates are **canvas** pixels. Get them from the frame you will show: `qa --times T`
prints each segment's on-canvas rect, and `find --boxes` gives OCR boxes in source pixels — convert
through the shot's scale/transform, then confirm on a `mograph preview` with `--background` set to
that `qa` frame. Never place a callout over a clip that is moving (punching or panning) during it.

## Scenes

```json
{ "scene": "seam-wipe", "say": "<first word after the cut>", "offset": -0.9, "params": { "text": "<1-3 words>", "beats": 2.5 } }
```

A scene starts on its word, so `offset` sets where the wipe sits against the cut. A bare
`seam-wipe` goes at cut − 0.2s. A labelled one at cut − (beats × 0.5 − 0.35): −0.9 at
`beats` 2.5, −1.15 at the default 3 (it scales with `tokens.scene.bpm`). At most two per video,
at chapter changes. Sample `qa` every 0.3s through each wipe.

## Rebuilding

- Change the plan, rebuild. Graphics the plan no longer names are removed; the rest are replaced.
- Recut the face (`cut --into`), rebuild. Every anchored graphic lands on its word again.
- Fix a typo in one graphic without a rebuild: `capcutctl mograph rerender --project NAME --id ID --params '{"text":"…"}'`.
- After `restore`, a plain `build` rebuilds by itself ("build outputs missing (restore?)").
  `build --force` is only for a deliberate re-run with nothing changed, or a snapshot taken
  before snapshots carried `.capcutctl/build.json`.
