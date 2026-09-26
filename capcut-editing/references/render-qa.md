# Render QA, reference reels, scoped revisions and the creative log

These four came out of a survey of other open-source agent editors (video-use, VEED open-edit,
krusemedia's video-editor-agent); the CLI repo's `docs/specs/agent-editor-survey-2026-09.md` has
the comparison. Command syntax and every option live in
[capcut-cli/reference.md](../../capcut-cli/reference.md); this page is the judgement.

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
graphics. `shots.png` shows the first frame of every shot; read it for the style: caption register,
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
