# The user's editing style

Measured directly from his own finished project (`IKEA Refund`), not inferred.
**Match this. Do not invent a vocabulary he doesn't use.**
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
| Transitions | **ZERO** |
| Video effects | **ZERO** |
| Text | essentially none (one element) |

He cuts hard and lets **sound + speed** carry the edit. Adding transitions or effects is a style
change — confirm before doing it, don't just add them.
## The SFX palette

All cached locally and reusable. Keep to these — they are his established sound.

| Name | Dur | Cache md5 |
|---|---|---|
| Sundon: Impact sound | 6.47s | `07d7ecbf820c0a668adb491c04cf76fb` |
| Coin cashier shop item get 4 | 0.77s | `2f1afdadff2934e4a5f43260d37b53fc` |
| Mouse click (single) | 0.30s | `c651fe9e2c689a98afbbf03e114e6891` |
| PC enter keyboard click | 0.50s | `6048e7c00aed1a1b57c23518d0a86afd` |
| "Pop!" "Pon!" Pitch height | 0.37s | `a0f3cad66351f21dd6456c0719135cb2` |
| Mouse click sound | 0.20s | `d91f21d1c2b6ec21cf77a8d7185bdb47` |
| Shutter sound, cashier, camera | 0.60s | `c41a3fa1aa68fd2608e32f915792151a` |
| Enter / Click / Select sound | 0.97s | `4cd0c7ee14c07e29164fd10df012a008` |
| Typing sound (keyboard x 3p) | 60.33s | `51c6842d59d720932576a5a89797840e` |
| Clock, timer, stopwatch_B_7 | 4.07s | `14567402c4be0b62e096b036a117ad65` |
| Enter/click/select (picon) | 1.07s | `769d41a88cecf6d6a0f24828a1996180` |

Placement conventions observed:
- **Mouse click** on every visible on-screen click
- **Typing** under keyboard activity
- **Stopwatch** under a long speed ramp (sells the time passing)
- **Coin / cashier** on a success or payoff moment
- **Impact** on the opening hook
- **Pop** on reveals and number beats
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

## What he does not do

Worth knowing so nobody builds it: **no music bed** (zero audio segments over 10s in any
project), **no captions** (0–1 text materials each), **no colour grade** (`filters=0`,
`effects=0` everywhere; the only video effect in the set is the Blur on Hermes' backdrop),
**no rotation**. The premium feel is entirely pace and motion.

Open question: IKEA holds its screen-recording audio at **0.4** under the voice (19 clips),
Hermes at 0.49; grok-build-final mutes all 19 to **0.0**. UI ticking under the VO is real
texture — but grok's B-roll is a *phone* recording, so it may be room noise. Test one clip
before making it a default.
