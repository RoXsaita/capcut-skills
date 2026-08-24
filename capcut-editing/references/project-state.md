# Project state — "Grok Build" (as of 2026-08-23)
## Sources

- **Cam / A-roll**: `/Users/roxsa/Downloads/E32F9DC9-C213-4EAD-B7D2-C4F61FC731C8.mp4`
  1440×2560, 30fps, 232.4s, HEVC. **Contains two full takes**:
  take 1 = 0–121s, take 2 = 121.2–231.1s. Take 2 is the warmer, tighter one and is what the
  current edit uses. Internal retries in both (the "publish" line 4×, "cheapest subscription" 4×).
- **Screen / B-roll**: `/Users/roxsa/Downloads/Screen_Recording_20260822_095151_Grok.mp4`
  1080×2652, 59.94fps, 1861.6s (31 min). Phone recording of Grok's App Builder.
## The story

Building a tower-defense game ("Cinderkeep") on a phone with Grok Build, plus a second app
(NumbyAI landing page) in parallel. Arc: prompt → Grok reads its own `AGENTS.md` + loads skills →
spawns a sub-agent → generates sprites via Imagine → game runs → publish to `suheil-td-game.grok.me`
→ usage went **3% → 10%** of weekly SuperGrok limit (hence his "~7%" claim, which is correct).
## VO cut — SIGNED OFF 2026-08-23

User's verdict: *"just fucking perfect ... literally no mistakes."* **Do not re-cut this.**
Take 2 only, last-instance-wins, boundaries placed with the energy index. 232.37s -> 59.63s.

| # | src in | src out | dur | tl in | beat |
|---|---|---|---|---|---|
| A | 122.467 | 135.967 | 13.50 | 0.00 | hook: one tap -> full game published, no prompt/this is |
| B | 139.833 | 142.900 | 3.07 | 13.50 | chose Tower Defense (retry take, adds 'لعبة') |
| C1 | 147.800 | 164.100 | 16.30 | 16.57 | started reading files inside it/rules+best practices/n |
| C2 | 164.533 | 172.300 | 7.77 | 32.87 | saw it spin up a sub-agent/and making the images for the |
| C3 | 172.933 | 176.967 | 4.03 | 40.63 | after minutes the game was running/to put it online I ju |
| C4 | 177.367 | 179.733 | 2.37 | 44.67 | tapped publish, chose the name |
| D | 184.100 | 189.667 | 5.57 | 47.03 | also built a landing page/and it did tidy work |
| E | 194.267 | 197.100 | 2.83 | 52.60 | you can try Grok Build free today |
| G | 227.100 | 231.300 | 4.20 | 55.43 | CTA: write Grok in the comments |

Passes `lint()` with **zero findings**. Its seam profile is the calibration set for
`scripts/audio_index.py` — 8 seams with head silence <= 0.28s. The one seam the user rejected by
ear (old B IN at 139.533, 0.35s of head silence) is the negative control.

Note the **usage-limits beat (F) was deleted by the user** as too long — that is deliberate, do
not restore it.
## Status

- CapCut project **"Grok Build"** has been **wiped and rebuilt from the VO cut above**
  (2026-08-23). It now holds exactly: one 10-segment cam track at 1:1 scale, plus the Preset 3
  outro re-anchored to 68.833s. Total 76.267s. All B-roll and all 22 SFX were deleted; orphaned
  materials pruned and de-duplicated (35 video materials -> 7).
- **B-roll is not yet placed.** That is the next job, and the OCR index is the tool for it.
- Structure is **overlays only**: main track empty, VO on `tri=1`, endcard stack on `tri=2..7`.
  67.067s total. This matches `Preset 3` and `IKEA Refund`; see `style-profile.md`.
- `Grok Build` (the older project) is stale at 82.9s and is NOT the working copy.
- Backups: `Grok Build/draft_info.PRESET_BACKUP.json`,
  `root_meta_info.json.bak_before_grokbuild`. `Preset 3` itself untouched.
## Known open items

- No punch-in zooms yet (framing was fixed first, deliberately).
- No transitions (matches his zero-transition style — confirm before adding).
- SFX all removed in the rebuild; they need re-placing against actual taps in the OCR index, not
  beat math.
- The A->B cut at tl 13.47 is the only one with no silence on the outgoing side; it is a hard cut.
- Deliberately excluded: the two `"That name isn't allowed"` publish rejections (could be a good
  honest beat if wanted) and the notification shade at 8:25 (personal content).
## Next session focus

Per the user: **perfect the talking-head video first**, then revisit the rest.
## Cached artifacts (survive session end)

| What | Where |
|---|---|
| Arabic transcript, word-level | `~/Downloads/.video-index/E32F9DC9_transcript_ar.json` |
| OCR index, 1862 seconds | `~/Downloads/.video-index/Screen_Recording_20260822_095151_Grok.ocr.json` |
| Rendered master (1080×1920, no zooms) | `~/Movies/GrokBuild-wip/GrokBuild_master_1080x1920.mp4` |
| Preview with SFX (old, bad pass) | `~/Movies/GrokBuild-wip/GrokBuild_preview_withSFX.mp4` |
| **VO cut master + preview + after-transcript** | `~/Movies/GrokBuild-wip/vo/` |
| mlx-whisper venv (persistent) | `~/Downloads/.video-index/.venv` |
| Pre-rebuild timeline backup | `Grok Build/draft_info.BEFORE_VO_REBUILD.json` |

Load the OCR index directly instead of re-running tesseract:

```python
idx = {int(k): v.lower() for k, v in json.load(open(
    os.path.expanduser("~/Downloads/.video-index/Screen_Recording_20260822_095151_Grok.ocr.json"))).items()}
```
