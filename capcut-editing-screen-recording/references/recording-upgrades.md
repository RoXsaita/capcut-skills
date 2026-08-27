# Recording-setup upgrades

Making the *capture* better is higher leverage than making the *editor* smarter.
## Recording Layout — superseded by `rl2`

`~/Applications/Recording Layout.app` is an **AppleScript applet** (decompile with
`osadecompile .../Contents/Resources/Scripts/main.scpt`). It clamps a chosen window to fixed bounds
`{100, 50, 820, 1330}` = **720×1280, exactly 9:16**, presets the macOS screenshot rectangle to
match, then exits. It emits no telemetry; the user starts the recording by hand.

**It is replaced by `rl2` (`~/Documents/Devving/rl2`).** See `recorder.md`. The four
upgrades proposed here are now built:

| Was proposed | Now |
|---|---|
| sidecar JSON per layout run | `session.json` — geometry, coordinate chain, clock offsets |
| marker hotkey during recording | `⌃⌥M`, plus full guided sentence markers on `⌃⌥N` |
| input-timing log (timing only, never which key) | `click` / `scroll_burst` / `typing_burst`, enforced in code |
| window-change events | `focus_change`, `window_geometry_change` |

Keep the applet only as a fallback for recording an app `rl2` cannot capture.

## Capture hygiene

- **Record screen at 30fps, not 60.** Halves file size, doubles every ffmpeg pass. Nothing lost.
  `rl2` defaults to 30 (`--fps`).
- **Leave ~3s of silence between takes** → `silencedetect` splits them automatically.
- **Say a marker word out loud** ("mark", "cut") → Whisper finds it instantly; flags the good take
  live instead of it being inferred.
- Keep the status-bar clock visible — OCR reads it, giving absolute wall-time anchors.
## Editor-side improvements not yet built

- **Punch-in keyframes on the preview renderer** (currently verified framing only; zoom on a wrong
  crop is just a bigger wrong crop, so framing was fixed first).
- **Tap detection by frame-differencing** a small region — still the only option for phone footage,
  where there is no event tap. On the Mac it is obsolete: `rl2` records the click itself.
- **Auto beat-to-content matching** — currently the keyword spec is hand-written per beat. It could
  be derived from the transcript by translating each Arabic line to expected English UI terms.
- **A round-trip reader** — parse an edited CapCut project back into an EDL to learn from what the
  user changed by hand. This is how the style profile would stay current automatically.
