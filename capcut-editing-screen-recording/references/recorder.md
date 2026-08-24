# `rl2` — the instrumented recorder (Phase 1)

Source: `~/Projects/recording-layout-v2`. Binary symlinked at `~/.local/bin/rl2`.
Rebuild with `swift build -c release` in that directory.

Replaces `~/Applications/Recording Layout.app`, which positioned a window to 720×1280 and quit.
`rl2 --layout` still does that; everything else is new.

## The app

**Recording Layout v2.app** (`~/Applications`) is the normal way in — build it with `./make-app.sh`.
It is the same binary as the CLI: no arguments inside the bundle opens the GUI, a subcommand runs
the CLI.

It keeps every behaviour of the original applet — app picker, window picker, clamp to the visible
frame, read back what was actually achieved, arm ⌘⇧5 on the same rect — and adds a screen picker,
ratio presets (`Full visible area` first for window mode; 9:16 720×1280 still in the list),
per-app layout memory keyed to bundle ID, and the recording itself with a menu-bar stop.

`Apply + open ⌘⇧5` is the deliberate fallback: if `rl2` cannot capture something, Apple's recorder
opens already snapped to the window. That take will have no trace.

**Rebuilding costs the permissions.** The bundle is ad-hoc signed and macOS stores a signature with
each TCC grant, so any rebuild silently revokes Screen Recording / Accessibility / Input Monitoring
while System Settings still shows them enabled. The app detects it and offers `Fix…`. This is not a
bug to chase — it is how TCC treats unsigned rebuilds.

## Running a take

```bash
rl2 doctor                                  # says exactly which permissions are missing
rl2 windows --app Chrome                    # what can be captured
rl2 record                                  # whole screen — the usual take
rl2 record --app "Google Chrome" \
           --layout 1728x999 \
           --script beats.txt \
           --out ~/Movies/rl2/take-01
```

`⌃⌥N` next sentence · `⌃⌥M` marker · `⌃⌥S` stop. `--duration N` auto-stops (for tests).

Permissions: **Screen Recording** (or nothing works), **Input Monitoring** (or no events at all),
**Accessibility** (or every click target is `coords_only`, and `--layout` refuses). They attach to
the terminal or app that launches `rl2`.

## Guided mode is the point

`--script beats.txt` (one sentence per line, `#` comments) opens a floating teleprompter. Each
`⌃⌥N` writes `sentence_begin` / `sentence_end` into the trace.

That converts the hard problem into an easy one: instead of searching 31 minutes for the moment
that matches a sentence, the trace already says which ~7-second window it is, and the editor only
has to **verify**. Use it whenever a script exists. For unscripted takes, `⌃⌥M` at least drops an
anchor.

The panel is a `.nonactivatingPanel` — pressing Next never pulls focus out of the recorded app,
which would both break AX gating and show up on camera. It is not in the captured pixels because
the capture filter is the target window only.

## Output

| File | Contents |
|---|---|
| `screen.mp4` | video plus one audio track — microphone by default, cursor visible by default |
| `system-audio.m4a` | only in `--audio both` |
| `frames.ndjson` | `{n, host, pts, vt, dirty}` for every written frame |
| `change.ndjson` | `{n, vt, score, blocks, mask}` — the L0 change signal |
| `trace.ndjson` | events, one JSON object per line |
| `session.json` | geometry, coordinate chain, clock offsets, privacy declaration |

Trace record types: `click`, `drag`, `pointer`, `scroll_burst`, `typing_burst`, `marker`,
`sentence_begin`, `sentence_end`, `focus_change`, `title_change`, `window_geometry_change`,
`session_end`, `privacy_violation`.

Click records also carry `in_capture`, `duration_ms`, `dwell_ms`, and (when AX resolved)
`inside_target` plus a target `{role, title, bounds, source}`. `source` is `coords_only`
with a `miss` reason (`no_permission` / `no_element` / `foreign_process` / `outside_capture`)
when the tree did not resolve.

Complete frames are always written. Idle SCK frames (static picture) are kept as a 0.5 s
heartbeat, and a timer duplicates the last pixels if SCK goes silent, so the mp4 and frame
index cover the full session wall-time. A take that ends on a static screen must still map a
click at t=9.1 s into a frame. Heartbeat frames are tagged `"heartbeat": true`.

Frame `host` is the sample PTS (already on the host clock). Do not use a callback-sampled
clock to join events — startup jitter on frames 1–3 made that look like a mapping error.

## Cursor and audio

Both default to **on**, and both were wrong at first. The Phase 1 spec said never burn cursors in
and treated audio as out of scope, so the first build shipped `showsCursor = false` and
`capturesAudio = false` — and the first real take came back with no mouse and no voice.

The spec's reasoning does not survive contact with the deliverable. This is a video people watch:
you cannot follow a click you cannot see. And the clean-pixels argument is weak anyway, because the
trace already carries exact click coordinates — the cursor is not how the pipeline locates
anything. `--no-cursor` is there when a take really is only for analysis.

Audio modes: **`both` (default)**, `mic`, `system`, `none`. "Record my screen" normally means the
narration *and* whatever the machine is doing, so mixed is the default — mic-only was the first
guess and it was wrong for the same reason the missing cursor was.

Mixing happens at stop, via ffmpeg (`amix ... normalize=0` — the default halves both inputs and the
take comes back quiet). AVFoundation cannot fold two tracks into one without a full render, and two
audio tracks in an mp4 is a coin flip over which one a player picks. Video is stream-copied, so only
the audio is re-encoded and a long take costs seconds. `system-audio.m4a` is kept afterwards: it is
the only route to a different balance without re-recording. Without ffmpeg the mix is skipped and
the two files are left side by side, with a message saying so.

## Window or whole screen

Two modes, from how the takes actually happen:

1. **Whole screen** (the usual take, GUI default, `rl2 record` with no `--app`). Stories cross
   ChatGPT / Terminal / Finder. Notifications are in the pixels; the session privacy block says so.
2. **One window at full visible** (1728×999 on the 16" — the display's safe area). Isolates one app
   when the rest of the desktop is not the story. 9:16 720×1280 stays in the layout list for
   talking-head B-roll; it is not the window-mode default.

| | Whole screen (usual) | One window (full visible) |
|---|---|---|
| Privacy | everything visible, notifications included | only that window is in the pixels |
| Coordinate origin | display origin | window origin |
| AX targets | frontmost app; the click record says which | captured app's tree |
| Layout | not applicable | full visible by default; 9:16 still a preset |
| `window_geometry_change` | not watched | watched |
| `title_change` | not polled; `focus_change` has app name only | captured window, spinner-debounced |

Our own teleprompter is excluded from the display filter — otherwise it would be in every take.

## One clock — measured, not assumed

`CMSampleBuffer` presentation timestamps are on the host clock. `CGEventGetTimestamp` is **not**
reliably `mach_absolute_time` ticks: on Apple Silicon the first eight takes wrote click `host`
values ~125/3 too large, because the recorder applied `mach_timebase_info` to a timestamp that
was already nanoseconds. Intel hid this (timebase 1/1).

The recorder pins the unit at write time (nanoseconds vs mach ticks — never a hard-coded ratio)
and asserts a synthetic event against the first frame within 100 ms. Result is
`clock.self_check` in `session.json`. That class of bug must not ship again.

**The recorder never converts a host time into a video time.** That is the compiler's job, from
`frames.ndjson`. A recorder that guessed at the mapping would bake an error into every event.
Join events to frames on `pts` / frame `host`, not on a callback-sampled clock.

## Coordinates

`session.json` states the chain once:

```
src_px = (global_pt - window_origin) * point_pixel_scale
```

Verified on a real capture: window 720×999 pt at global origin (84, 38), `scale_factor` 2,
`content_rect` 720×999 at (0,0) → 1440×1998 px source. Every point in the trace is written in all
three spaces (`global`, `window`, `src_px`) so nothing downstream redoes this arithmetic and gets
it subtly wrong. Clicks also carry `in_capture`; negative `src_px` without that flag being
false is a formula bug.

`content_scale ≠ 1` is recorded, not folded into `src_px` — the crosshair test verified the
unscaled chain. A right-edge click in a letterboxed window is the check that would change this.

A window moved or resized mid-take emits `window_geometry_change` — it invalidates the mapping for
every event after it.

## The change signal (L0)

32×32 luma grid per frame, diffed against the previous frame. Reports a mean absolute delta plus
an 8×8 dirty-block bitmask. Model-free and cheap enough for a 31-minute take.

It exists so "when did the UI actually react to that click" is a **measurement**. Noise floor is a
mean block delta of 6/255, which clears compression shimmer without missing a real repaint.

`rl2 selftest-change` drives it with synthetic frames whose answers are known: baseline, identical
frame, localised patch (checks the mask points at the right block), full-frame saturation, and a
sub-threshold 2-level drift that must **not** register. All pass.

## Privacy is enforced in code

* `InputSample` has no field that could hold a keystroke identity; the keyDown path never reads
  `.keyboardEventKeycode`.
* Typing persists only as `{start, end, count}`.
* Element text is the `title` of a clicked **interactive** control and nothing else. `AXValue` is
  never read.
* Every record passes `PrivacyGuard` before disk. A banned field name anywhere in the record drops
  it and writes a `privacy_violation` naming the key path, never the value. Verified by
  `rl2 selftest`, which deliberately tries to write a `keycode` and is refused.
* Hotkeys use Carbon `RegisterEventHotKey`, not a global key monitor — noticing three combinations
  must not require observing every keystroke.
* One-window capture uses `SCContentFilter(desktopIndependentWindow:)`, so a notification that
  never renders into these pixels cannot leak into the edit. Whole-screen (the usual take) includes
  whatever is on the display; Focus/DND is the real notification control there.
* Window titles of the **captured** window are recorded (Chrome tab changes). They are
  spinner-normalized so a Terminal `✳` glyph is not a scene cut. Whole-screen does not poll
  frontmost titles — those were leaking Claude chat names and firing every 500 ms on a spinner.
* AX is queried against the **captured app** (`AXUIElementCreateApplication(pid)`), not only
  the system-wide element, and no longer requires that app to be frontmost — our own status
  item used to steal focus and zero every target. A hit in another process is discarded.
  Chrome/Electron get `AXManualAccessibility` enabled for the web tree.

## What is not yet proven

The first eight real takes (Desktop `Screen Recordings/*-20260823-*`) proved the timing and
pixel layer and failed the semantic layer. All 17 clicks were `coords_only`; click `host` was
raw-converted ticks; session 2's static tail left a click past video end; no take used guided
mode. Those recorder bugs are fixed in v2.1. They have not been re-verified on a new take.

Acceptance test, still unrun: 2–3 minutes, **whole screen** (the usual mode) *or* one window at
full visible, clicking 10 named controls, plus scrolling, typing, and a script so guided mode
writes `sentence_begin`. Pass = ≥80% of in-capture clicks resolve with role+title+bbox, every
event timestamp maps inside the frame range, and heartbeat covers any static tail.

If targets come back empty in Electron or webview UIs after Accessibility is granted, that is
expected for some pages — the fallback is coords plus OCR of the click crop, which is Phase 2's
job. `in_capture: false` clicks (outside the window) must stay `coords_only`.

## Gotchas found while building it

* **`CGEvent.timestamp` is nanoseconds, not mach ticks**, on Apple Silicon (timebase 125/3). The first eight takes wrote click `host` values 41× too large because `HostClock.seconds` was applied a second time. Intel hid this (1/1). `EventClock` pins the unit at write time and a synthetic-event self-check against the first frame is in `session.json`. Never hard-code 125/3.

* **Writes after close abort the process.** `FileHandle.write(_:)` raises an ObjC exception Swift
  cannot catch, so a sample-buffer callback still in flight when teardown closes a log took the
  whole app down with `SIGABRT` — three crashes, one cause. Fixed twice over: a `closed` flag
  checked inside the writer queue, and `write(contentsOf:)` so a genuine I/O failure is reported
  instead of fatal. `Capture` also sets `stopped` before it closes anything.
* `Recorder.run()` is a nonisolated `async` method, so everything after its first `await` resumes
  off the main thread. `Timer.scheduledTimer` there attaches to a run loop nobody runs and simply
  never fires — the first bounded take ran for 149 s instead of 8. All timers go through
  `mainTimer(...)`, and AppKit calls through `onMain { }`.
* `print` is block-buffered when stdout is a pipe; `setvbuf(stdout, nil, _IOLBF, 0)` in the record
  path, otherwise a running capture looks dead.
* Posting a synthetic `CGEvent` needs Accessibility. That is why `rl2 selftest`'s scroll leg fails
  without it — the tap is fine, the test's own stimulus is blocked.
* `SCDisplay` has no `nsScreen`; match `displayID` against `NSScreen.screens` for the backing scale.
* Ctrl-C must run the same teardown as `⌃⌥S`, or `AVAssetWriter` leaves an unfinalised mp4.
