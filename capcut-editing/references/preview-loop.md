# Picture and sound review

Use the smallest check that answers the current risk. Ordinary A-roll assembly still
ends with `doctor` and user approval; it does not require a full proxy render.

## While editing

```bash
capcutctl qa --project NAME --times 3,9,15 --guide 960
capcutctl preview --project NAME --from 9 --to 15 --out preview.mp4
```

Use timestamped frames for source/action evidence, crops, caption space and camera
rest/peak/return. Use a bounded proxy when the question requires playback, such as a
cut syllable or the time spent waiting for a result. Default previews are 360x640 at
6fps; this is too sparse to approve fast animation. Check that motion in CapCut.

The proxy includes principal-video audio plus audio tracks, with clip volume, speed
and native fade durations. Fades keep their original clip timing when previewing a
subrange; the compositor mix preserves stereo. It does not reproduce native audio
effects, volume keyframes or every visual effect. Review audible B-roll in CapCut too.
Do not use the legacy split-screen renderer for delivery or add a proxy-only limiter
that conceals clipping in the actual project.

## Before final delivery

Prefer a CLI-produced grid over repeatedly opening CapCut and manually clicking through
its timeline. When the user explicitly authorizes export, use the native export bridge:

```bash
capcutctl export --project NAME --out final.mp4 --overwrite --grid final-grid.png --times 0,8,15,24
capcutctl export-grid --media final.mp4 --out final-grid.png --times 0,8,15,24
```

The export command invokes CapCut's real rendering engine through a bounded macOS native
UI bridge; it is not a headless renderer. It needs CapCut open on Home or the requested
project and briefly needs app focus. It checks project identity, stages a unique output,
checks duration and decoding, and preserves the prior output if rendering fails. Unknown
controls or lost focus are named failures; do not blindly retry clicks or claim success.

Inspect the actual export grid at changed shots and camera rest/peak/return, including the
opening and ending. Check that the pictured prompt, action, price and result match the
spoken words; the text remains readable; split-screen seams and crops are clean; and each
shot has one clear focus. For a browsing montage, show the wider browser and real activity,
then ramp through the search. Hold proof shots long enough to read.

A grid does not prove sound or motion. Check short normal-speed sections of the exported
video when reviewing a ramp, transition, speech seam or SFX hit. Use the house
“Enter / click / select” cue on the actual screen-zoom landing; confirm it is audible under
the voice. Do not substitute a generic whoosh or an intended timeline placement for an
actual audible cue. Recheck only the repaired sections unless a change affects the whole mix.

Deliver the editable project and localized media. Export only when explicitly requested;
“finish/finalise” and edit approval alone are not export requests. Without export permission,
use bounded CLI QA/proxies and reserve native playback for unresolved native-only effects.
Do not open the export dialog speculatively. Report unperformed checks honestly. A clean
`doctor` validates structure, not visual or audio quality.
