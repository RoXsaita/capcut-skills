# Recording-setup upgrades

Making the *capture* better is higher leverage than making the *editor* smarter.
## Historical recorder integration

The private Recording Layout applet was superseded by the private `rl2` recorder.
Neither is distributed here. [recorder.md](recorder.md) records its historical trace
schema and acceptance gaps; use an installed recorder's current documentation for setup.
Ordinary screen recordings need no trace to work with `capcutctl find` / `layout`.

## Capture hygiene

- **Choose capture fps for the content.** 30fps often suits UI demonstrations; use 60fps
  when fast movement matters. File size and processing cost depend on encoding and content.
- **Leave ~3s of silence between takes** → `silencedetect` splits them automatically.
- **Say a marker word out loud** ("mark", "cut") → Whisper finds it instantly; flags the good take
  live instead of it being inferred.
- A visible status-bar clock can help cross-check a recording, but does not establish
  exact event timestamps; use verified trace/frame timing where available.
## Editor-side improvements not yet built

- **Automatic semantic zoom selection.** `qa` and `preview` already evaluate native keyframes
  with linear interpolation; native easing/effects still need CapCut playback.
- **Tap detection by frame-differencing** a small region — still the only option for phone footage,
  where there is no event tap. On the Mac it is obsolete: `rl2` records the click itself.
- **Auto beat-to-content matching** — currently the keyword spec is hand-written per beat. It could
  be derived from the transcript by translating each Arabic line to expected English UI terms.
- **Automatic style learning from edits.** `scenes`, `diff` and `harvest` already inspect a
  current draft; inferring new style rules from those changes remains an editorial task.
