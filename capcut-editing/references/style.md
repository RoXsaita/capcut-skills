# The user's editing style

Measured directly from his own finished projects, not inferred.
**Match this. Do not invent a vocabulary he doesn't use.**

**Provenance matters — read this before trusting a number.** The tables below were originally
measured from `IKEA Refund` ALONE, and that one project is an outlier: it is the only recent
video with zero transitions. Everything marked *(library)* was re-measured on 2026-08-26 across
all **88 drafts** in `~/Movies/CapCut/User Data/Projects/com.lveditor.draft/`. Where the two
disagree, the library number wins.

**Do not use `GrokBuild-20260825` as a style reference.** It is `capcutctl` output from an agent
test run, not a hand edit. It is useful as a readout of what the CLI produces unaided — which is
exactly the gap this file exists to close.
## Format

- **9:16, 1080×1920, 30fps.** Short vertical social video, ~45–75s.
- Talking head in Arabic + screen-recording B-roll.
## The signature

| Trait | Measurement |
|---|---|
| Cut rhythm | median **1.92s**, micro-cuts down to **0.1s** |
| Speed ramps | **0.4× / 0.5× / 0.7×** for emphasis, **20× / 50× / 100×** to kill dead time |
| SFX | **24 cues across 3 audio lanes**, hand-synced |
| Camera moves | **14 segments** with Position + Scale + Rotation keyframes (punch-ins, drifting pans) |
| Transitions | *(library)* **342 across 57 of 88 projects** — a core part of the style, NOT zero. `IKEA Refund` having none is the exception. See "The seam formula". |
| Video effects | *(library)* 402, but **370 of them are `Blur`** — the background plate `capcutctl layout background` already writes. Treat as "no effects except the blur plate". |
| Text | essentially none (one element) |

He cuts hard and lets **sound + speed** carry the edit. Adding a *video effect* or a colour grade
is a style change — confirm first. Adding a **transition + its paired sound** is not; that is his
normal seam, and omitting it is what makes CLI output read as mechanical.
## The seam formula — the single most copyable thing in this file

A cut is not a cut. It is **a transition plus its paired sound, fired together**, the sound
leading the picture by about **4 frames (0.13–0.14s at 30fps)**.

**Provenance, carefully.** The pairings and the lead were measured from his HAND-CUT projects
(Hermes-agent, Higgsfield Refund, Content System, IKEA Refund — median lead 0.14s across 20
paired cuts) and live in `presets/sfx.json`. `capcutctl polish` writes them. A re-check on
`GrokBuild-20260825` found 22 of 22 seams at −0.133s with zero deviation — but that project is
`polish` output, so it confirms the TOOL is consistent, not that the human is. Do not cite it as
evidence about his style. The lead is roughly constant across transition durations; it is not
`duration / 2` (Flash at 0.20s also leads by 0.133s).

| Transition | Typical dur | Paired SFX | SFX dur |
|---|---|---|---|
| **Horizontal Triptych** (layout change) | 0.27s / 8f | `Woosh` (or `swish_whoosh (large)` at 0.33s) | 0.40s |
| Flash · White Flash 2 · Glitch Flash II | 0.20–0.27s | `Decision / choice / stationery / click` | 0.50s |
| Glitch (the machine doing something) | 0.27s | `Glitch sound that matches the sound logo` | 0.63s |
| Flash, once, on the last cut into the CTA | 0.27s | `Coin cashier shop item get 4` | 0.77s |

Volume is `1.0` on every seam sound. No fades.

### The transition palette *(library — uses / projects)*

| Name | Uses | Projects | Durations seen (most common first) |
|---|---|---|---|
| Horizontal Triptych | 88 | 35 | 0.27, 0.33, 0.47, 0.40, 0.20, 0.13 |
| Glitch | 49 | 40 | 0.47, 0.27, 0.20, 0.13, 0.33 |
| Blur | 48 | 24 | 0.47, 0.33, 0.27, 0.20, 0.67, 0.13 |
| White Flash 2 | 37 | 23 | 0.27, 0.13, 0.20, 0.07 |
| Flash | 34 | 17 | 0.47, 0.20, 0.27, 0.40, 0.13 |
| Glitch Flash II | 31 | 19 | 0.67, 0.27, 0.40, 0.47 |
| Black Fade | 27 | 12 | 0.47, 0.27, 0.13 |

Everything else (Ripple Fade, Glitch Blur, Stretch Right, Whoosh Swipe, Cube Folds…) appears in
exactly one project. Treat those seven as the vocabulary.

**Durations are always an even number of frames at 30fps** — 0.13/0.20/0.27/0.33/0.40/0.47s are
4/6/8/10/12/14 frames. Never write an unquantized duration.

**Variety is part of the style.** `grok-build-final` used 6 distinct transitions across 16 seams.
The unaided-CLI `GrokBuild-20260825` used **the same Horizontal Triptych 18 times out of 24** —
that monotony is the single loudest "a machine made this" tell in the file. Cap any one
transition at roughly 40% of seams.

## The SFX palette *(library — 88 drafts)*

All cached locally under `~/Library/Containers/com.lemon.lvoverseas/Data/Movies/CapCut/User Data/Cache/music/<md5>.mp3`
and reusable. Keep to these — they are his established sound.

| Name | Dur | Uses | Projects | Cache md5 |
|---|---|---|---|---|
| Mouse click (single) | 0.30s | 257 | 35 | `c651fe9e2c689a98afbbf03e114e6891` |
| **Woosh** (seam sound) | 0.40s | 130 | 44 | `7785b04dd58d6f7a816e7d9744448ae5` |
| PC enter keyboard click | 0.50s | 92 | 33 | `6048e7c00aed1a1b57c23518d0a86afd` |
| Typing sound (keyboard x 3p) | 60.33s | 76 | 29 | `51c6842d59d720932576a5a89797840e` |
| Enter / click / select (picon) | 1.07s | 65 | 33 | `769d41a88cecf6d6a0f24828a1996180` |
| Mouse click sound | 0.20s | 64 | 18 | `d91f21d1c2b6ec21cf77a8d7185bdb47` |
| **Decision / choice / stationery / click** (seam sound) | 0.50s | 62 | 29 | `d7084c064481b95a03c976f57346848a` |
| "Pop!" "Pon!" Pitch height | 0.37s | 58 | 30 | `a0f3cad66351f21dd6456c0719135cb2` |
| Click_Mouse_Click_02 | 0.87s | 56 | 14 | `33f11a55221681b3fefec3346290169e` |
| Enter / Click / Select sound | 0.97s | 48 | 27 | `4cd0c7ee14c07e29164fd10df012a008` |
| Glitch sound that matches the sound logo | 0.63s | 36 | 33 | `da69cbae92d82c441866a7752c51acd9` |
| Culin (light-bulb / idea) | 1.30s | 27 | 24 | `7bf4f2fdf526cb32b2286a78db96d7a6` |
| swish_whoosh (large) | 0.80s | 27 | 21 | `b1a4a2a65f2e152a864be94637be9e83` |
| Realistic typing | 3.40s | 22 | 12 | `2ec69836badb594b44950d6cbf32741e` |
| RISER_01 | 4.10s | 16 | 16 | `874eca3d6e3a582988e860409c0f332d` |
| Shutter / cashier / camera | 0.60s | 14 | 13 | `c41a3fa1aa68fd2608e32f915792151a` |
| Coin cashier shop item get 4 | 0.77s | 12 | 12 | `2f1afdadff2934e4a5f43260d37b53fc` |
| Sundon: Impact sound | 6.47s | 10 | 10 | `07d7ecbf820c0a668adb491c04cf76fb` |

Placement conventions observed:
- **Woosh / Decision / Pop** on seams — see "The seam formula" for the exact offset
- **Mouse click** on every visible on-screen click
- **Typing** under keyboard activity
- **Stopwatch** under a long speed ramp (sells the time passing)
- **Coin / cashier** on a success or payoff moment
- **Impact / RISER** on the opening hook
- **Pop** on reveals and number beats

### SFX are NOT frame-snapped to cuts

*(library, 6 hand-cut projects — IKEA Refund, Hermes-agent, Applies for Job, Content System,
Skills, ElevenLabs Refund — ~189 cues)* Only **11–17%** of cues land within ±50ms of a cut.
Median offset is **+0.00 to +0.17s (trailing)** for click/typing cues; seam sounds LEAD by about
0.13s. A tool that snaps SFX to the nearest cut will sound *worse* than his hand edit. Encode the
offset; do not quantize it away.

## Presets

`Preset 3` is a **branded endcard**, 7.43s, with all content parked at the end of the timeline
(68.83→76.27s of a 76.27s project). Assets: `suheilai-rect-indigo-1080x1920 (2).png` (indigo
frame), `suheilai-circle-white-1080x1920.png`, `circle-1080x1080.gif`, plus two clips.

Standard workflow: duplicate it, build content in front, shift the endcard to the absolute end.
## Structure that works

Hook on the payoff (show the result first), then chronological build-up, then proof/receipts,
then CTA. His CTA is consistently *"write [keyword] in the comments"*.
## He edits on OVERLAYS ONLY — the main track stays empty

His words: *"i never use the 'Main' which is cover, i use overlays, fully, so just use overlays,
never a Main timeline."*

**"Cover" = CapCut's main track**, not "B-roll covering the face". When he says take something
off the cover, he means move it off `flag=0` and onto an overlay track. Getting this backwards
wasted two rounds.

Build every timeline this way:

```
[0] flag=0   MAIN — present but EMPTY (n=0). Never place a segment here.
[1] flag=2   tri=1   A-roll (the cam / VO clips), all on one track
[2] flag=2   tri=2   B-roll, endcard base, etc.
[3..] flag=2         one track per additional layer
```

Verified against his own projects:

| Project | main track | A-roll lives on |
|---|---|---|
| `Preset 3` | `flag=0, n=0` (empty) | — (endcard only, tri 1–6) |
| `IKEA Refund` | 1 filler segment | overlay `tri=1`, 30 segments |

Why he works this way: main-track clips auto-ripple — deleting one closes the gap and drags
everything left. Overlay clips move independently, so he can nudge, trim and restack without the
timeline fighting him. Respect it; it is the whole reason he wants a CapCut handoff at all.

### Layering

`render_index` on the segment is the true z-order (lower = further back), independent of track
order. `track_render_index` must equal the track's position in `tracks`. His endcard stack uses
20 (indigo frame) < 36 (screen rec) < 43 (avatar) < 45 (endcard video) < 46 (white circle) <
47 (gif) — preserve those exactly. A-roll can sit at a low index like 2.

## Pace — measured, not felt

Compression = source seconds consumed per screen second on the B-roll track.

| project | compression | B-roll ramped | plays at 1× |
|---|---|---|---|
| IKEA Refund | 19.7× | 21/30 (70%) | 38% |
| Hermes-agent | 1.5× | 9/18 (50%) | 62% |

Speeds he actually uses: **20–100×** for an agent working (IKEA: 260s→2.6s, 463s→4.6s),
**2–4×** for navigating and typing (Hermes: 2.0 / 2.2 / 3.1 / 4.0), **1.0×** for the thing
he is naming right now, **0.4–0.7×** for the payoff. IKEA ends on 0.4×.

## Motion — two zoom idioms and nothing else

Every keyframed move in every project is **2 keyframes across 4 properties**
(PositionX, PositionY, ScaleX, Rotation). Rotation is `0.0` everywhere — he never tilts.

- **Snap punch** — ramp **0.10–0.33s** (median 0.20), scale 1.0 → 2.0–4.5.
- **Punch → hold → release** — 4 keyframes: in over 0.2s, hold ~1.8s, back over 0.2s.
  IKEA uses it on its money shot.
- **Slow drift** — ramp **6.7–30s**, and it appears *only over a speed-ramped timelapse*.
- **Pop-in** — anything that appears scales from `0.01` over **0.07–0.17s** (the IKEA
  logo, the Hermes endcard, grok's circle GIF).

A single keyframe on a property is a static hold doing nothing. Two of grok-build-final's
nine keyframed segments were that — dead weight.

## What he does not do — verified across all 88 drafts, so stop wondering

These are not "probably nots". Each was counted across the whole library:

| Thing | Evidence | Verdict |
|---|---|---|
| Colour grading | 312 `hsl` objects, **every one at default**; 1 project has `color_curves`, unused | never |
| Loudness normalisation | all 592 `loudnesses` have `enable: false` | never — CapCut's own LUFS tool is one he has never switched on |
| Beat sync | all 1225 `beats` are `mode: 404`, `enable_ai_beats: false` (auto-generated per audio, ignored) | never |
| Animations | 1493 `material_animations`, of which **3** are a real "Fade In" | effectively never |
| Music bed | 4 stray tracks across 88 projects | historically never *in CapCut* — he added it after export. `capcutctl finish --music` now writes a quiet generated bed; see `finish.md`. Do not turn on CapCut's `enable_ai_beats`. |
| Captions | 106 `texts` across 31 projects, 0–1 per video | essentially never |
| Rotation | `KFTypeRotation` present 435× but the value is `0.0` everywhere | never tilts |

The premium feel is entirely **pace, motion, and the seam formula**.

### Eased keyframes exist and are underused

*(library)* 57 keyframe points across 10 projects use **`FreeCurveInOut`** (real bezier
`left_control` / `right_control` handles) rather than `Line` — `Higgsfield Refund` alone has 16.
Both grok builds are 100% `Line`. A linear scale punch reads mechanical; an eased one reads like
a camera. Harvest one `FreeCurveInOut` point from a real draft rather than inventing handles.

### Motion coverage is the biggest single quality gap

*(library)* `IKEA Refund` keyframes **10 of 30** A-roll segments. The unaided-CLI
`GrokBuild-20260825` keyframes **1 of 25**, and its B-roll track has **zero**. Camera moves are
half the signature and they are the first thing an automated build drops. Roughly **a third of
A-roll segments should carry a move**.

### B-roll audio level is an open decision, not a style

IKEA holds screen-recording audio at **0.4** under the voice (19 clips), Hermes at **0.49**,
`ElevenLabs Refund` runs B-roll at **1.51**, and both grok builds mute all of it to **0.0**.
That spread is an unmade decision, not a preference. UI ticking at ~0.4 is real texture; silence
is flat. Phone-sourced B-roll may genuinely need muting for room noise — test one clip.
