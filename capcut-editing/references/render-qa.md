# Render QA, reference reels, scoped revisions and the creative log

These four came out of a survey of other open-source agent editors (video-use, VEED open-edit,
krusemedia's video-editor-agent); the CLI repo's `docs/specs/agent-editor-survey-2026-09.md` has
the comparison. Command syntax and every option live in
[capcut-cli/reference.md](../../capcut-cli/reference.md); this page is the judgement.

## `xray` measures the whole render

`check-export` (below) is the quick summary; the X-ray is the full evidence and a superset of it.

```bash
capcutctl xray scan final.mp4 --project NAME --speech [--lang ar] [--jev]   # exit 1 on FAIL
capcutctl xray window final.mp4 --frames 470-479                            # exact frames, by PTS
capcutctl xray frame final.mp4 --t 15.9 --crop 0,1300,1080,400              # native-resolution look
capcutctl gate --project NAME --xray final.xray                             # its FAILs block
```

**Four verdicts.** FAIL is a defect a detector is sure of. UNKNOWN needs your eyes: a one-frame
state at a cut, a stutter, a click, a caption over screen text. NOT CHECKED names what it cannot
see (logos, lip sync, motion the draft does not declare). Never report UNKNOWN or NOT CHECKED as
clean. Numbers are tagged A (authored in the draft), M (measured on the export) or E (estimated).

**What it reads.** Every frame (luma in 30px tiles) and every audio sample; text and faces with
Vision on every 6th frame plus the middle of every authored caption, Latin-first and Arabic-first.
With `--project`: transitions, effects, graphics and animations from the draft explain findings
inside them; captions are the draft's text read on screen. `--speech` transcribes the export and
checks captions and spoken numbers against it. `--jev` (sends transcript and screen text to
TypeSafe) judges whether the screen backs each sentence and ranks UNKNOWNs by how noticeable they
are; it only reorders the queue, never a verdict. One-time setup: `capcutctl xray jev-setup`.

**Measured** with `xray bench` (planted defects in re-encoded copies of two finished videos): one
black frame and two white frames 24/24 and 16/16 (every one mid-shot at FAIL; beside a cut it is UNKNOWN), clicks 15/16,
clipping 10/14, a one-frame local patch 11/18, repeated frames in motion 4/4, zero false alarms.
**Blind spots:** a one-frame local patch in a handheld or moving shot or the frame before a cut;
mild clipping; screen text under a caption that is itself caption-sized; Arabic ligatures OCR
misses (an unread caption is UNKNOWN). Run `xray bench` on a new kind of footage before trusting
a PASS on it.

## `check-export` reads the rendered file

Every other check reads the draft, and the file that gets posted can still be wrong. Run it on any
export, or any file the user hands over:

```bash
capcutctl check-export --media final.mp4 --project NAME        # exit 1 on FAIL
capcutctl export-grid  --media final.mp4 --out look.png --times 8.02,12.02   # the times it lists
```

**FAIL:** black inside the edit (a gap between clips), a true peak over the limit, no audio, and
with `--project` the wrong canvas or length.

**WARN:** opens on black, black tail, 1–2 frame flashes, 1–2 frame micro-shots (a stray frame
between clips), picture frozen past `density.maxStatic`, sound starting after 0.5s, dead air ≥1s,
loudness off target by more than 1 LU.

A flash may be a deliberate flash transition. **Look at the listed frames before you call it a
defect.** The output lists every flagged time for `export-grid`.

## `reference` measures a reel the user wants to copy

It reports in the gate's own vocabulary: visual events are hard cuts *plus* in-shot builds (pops,
pushes, text landing), because perceived pace tracks events, not cuts. A clone that matches cuts
per second but not builds reads slow.

```bash
capcutctl reference --media reel.mp4 --project NAME --sheet shots.png --profile-out ref-profile.json
capcutctl gate --project NAME --profile ref-profile.json
```

`compare` lists the reel, the profile and (with `--project`) the edit side by side for the first
visual event, longest static stretch, opening gap and median shot. `--profile-out` writes only
`density.hookEventBy`, `openingMaxGap` and `maxStatic` — a decode cannot tell which events are
graphics. To recalibrate `opening-density` for good, copy what it measured into the user profile
(`capcutctl profile where`), never the public preset: the shipped `presets/profile.json` in the
CLI repo stays brand-neutral. `shots.png` shows the first frame of every shot; read it for the style: caption register,
framing, graphic vocabulary, the once-per-video trick. The numbers cannot show those. Raise
`--cut-threshold` if screen scrolling reads as cuts.

## `diff --allow` proves a scoped revision

When the note is "change only X", snapshot first, make the change, then show it touched nothing
else:

```bash
capcutctl snapshot --project NAME --label before-note-3
capcutctl diff --project NAME --snapshot before-note-3 --allow SEGMENT-ID,track:broll
```

A bare token is a segment id; `track:NAME` or `track:N` admits every segment on that track,
including ones the edit added. Anything else that changed is listed under `scope.outOfScope` with
both values, and the command exits 1. Track index shifts from an inserted overlay track are not
findings.

Each diff segment row carries `clip`, `keyframes` (a short hash of the keys), `mask`, `refs`
(speed, animation, transition, mask and canvas extras) and, on caption rows, `text`. So a reframe,
a keyframe change, a re-speed or a re-caption outside the allowed ids is reported even when the
clip did not move: `scope.ok: false`, exit 1. When that change was intended, add its id to
`--allow`. Never treat exit 1 as noise.

## `notes` is the creative log

Record what the user rejected and why, what landed, and the decisions a later round must not undo.
It lives in `<project>/.capcutctl/notes.json`, outside snapshots, so `restore` never erases it.

```bash
capcutctl notes --project NAME --brief                                   # first thing, every session
capcutctl notes --project NAME --reject "orange captions" --why "fights the indigo frame"
capcutctl notes --project NAME --accept "white captions, indigo accent" --why "matches the frame"
capcutctl notes --project NAME --decide "keep beat 4" --why "only take with the number"
capcutctl notes --project NAME --todo "louder end card"
capcutctl notes --project NAME --done 1
```

A rejection needs `--why`, because the reason is what stops the next round proposing the same thing
reworded. Paste `--brief` into any sub-agent brief.
