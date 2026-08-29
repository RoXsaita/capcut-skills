# Pitfalls

Concrete traps already hit on this project. Read before starting.
## Process

- **Building blind.** The #1 failure. 83s of timeline written from arithmetic, never previewed,
  rated *"1/100"* by the user. Always render and look.
- **Showing a silent preview.** SFX existed in the CapCut build but not in the ffmpeg preview, so
  the user asked "where are the sounds". Include audio in anything you hand over.
- **Doing the whole video at once.** The user explicitly asked for one section at a time, checked
  end-to-end. Cut the talking head, get it signed off, *then* B-roll. Recutting the face after
  B-roll is on the timeline desyncs every shot.
- **Speeding the talking head.** `clip.trim` that lengthens the source window and leaves the
  target the same is a speed ramp. Used on `hermes-replies-to-comments` to "save" first words
  the energy snap had dropped — the face played at 1.02–1.44×. Faces stay 1×. To keep a word,
  re-run `cut --keep` so the clip gets *longer*, not faster. `pace` already refuses the
  principal track; trim does not, so do not reach for it on `content`.
## Indexing

- **Loose OCR keywords silently over-match.** `wave` returned 1006 seconds because the *prompt
  text* on screen said "wave progression". Always sanity-check span length — a 1000s match for a
  transient event is a bug, not a find.
- **OCR TSV-derived ROI is unreliable.** Multi-word keys never match single-word TSV tokens; after
  loosening, most results pinned to the clamp value. Use it as a hint; confirm visually.
- **240px frames are too small to OCR.** Use ~810px wide.
- **Whisper hallucinates a trailing Arabic subtitle credit.** Drop the last line.
## Content selection

- **Check the END of a shot, not just its start.** Screen content changes underneath a shot. Three
  separate shots drifted onto the wrong screen this way.
- **Real content windows can be seconds long.** The working game appeared for ~4s in a 31-minute
  recording. Slowing a shot (0.7–0.8×) stretches a narrow window without drifting past it.
- **Sidebars and menus look like content to OCR.** Several timestamps landed on the conversation
  list. Add `forbid` terms.
- **Avoid failure states unless intentional.** `"We can't generate this image / didn't pass the
  moderation"` appears repeatedly and should be excluded (`forbid=["moderation"]`).
## CapCut writing

- **CapCut rewrites `root_meta_info.json` on quit** — register only when it is closed.
- **Duplicating an existing project beats building one from scratch** — `draft_meta_info.json` has
  many fields whose purpose is unknown.
- **Duplication carries empty tracks.** Strip tracks with no segments.
- **The speed invariant** (`source = target × speed`) must hold on every segment.
- **Speed caps**: the user's own projects top out around 100×. To compress 900s into 1.5s you need
  600×, which is out of range — pick a shorter source span instead.
## Media / environment

- **Python 3.14 has no wheels for mlx-whisper.** Pin 3.12. Use `uv`, not `pip` (pip timed out at
  5 minutes; uv needed `UV_HTTP_TIMEOUT=300` for a large wheel).
- **`SendUserFile` caps at 30 MiB.** Downscale previews.
- **PIL lives in system python3**, not necessarily in the uv venv.
- **Screen recording permission** is required for `screencapture`; **Accessibility** is separate
  and required for `cliclick` / AppleScript UI scripting. Granting one does not grant the other.
## Privacy

- **Personal content in recordings.** Notification shade, DMs, lock-screen, and
  news pushes. Exclude by default; flag rather than silently including.
- **Never log keystroke content.** If building an input logger, record *timing only*. Content would
  capture passwords.
## The edit reverted after CapCut relaunched

Symptom: you write `draft_info.json` with CapCut closed, verify it on disk, report success — and
the next time CapCut opens, the old timeline is back and your file is overwritten.

Cause: `Timelines/<uuid>/draft_info.json` is the copy CapCut restores from. See
`capcut-format.md` → "CapCut keeps a second copy of the timeline".

Guard: after writing, `md5 -q` every copy and confirm they match. Then reopen CapCut and re-check
the duration before telling the user it is done.
## "Cover" means the main track

Do not read "cover" as "B-roll covering his face". In his vocabulary the **main track is the
cover**, and he never puts anything there. "Move it off the cover" = move it onto an overlay.

Tell for getting this right without asking: open `Preset 3` and look at track 0. It has zero
segments. That is the convention.
## Do not derive CapCut geometry — render it and compare to a real frame

Transform sign, scale semantics and mask offsets are easy to reason about and easy to get exactly
backwards. `transform.y` was documented as "positive = DOWN, confirmed by construction" on the
strength of split-line arithmetic. It is **positive = UP**. The arithmetic was self-consistent and
wrong, and it survived a preview render because the preview used the same wrong assumption.

Two rules follow:

1. When copying a layout, copy `clip` and `uniform_scale` **wholesale from a segment that already
   looks right**. Never recompute values you could copy. This is also how the user works by hand.
2. When you must state a geometric fact, render it **both ways** and match against a frame you
   know is correct (a reference image, or the preset's own endcard). A preview that only confirms
   your own assumption proves nothing.

The saving grace that time: the CapCut project was built by copying values verbatim, so it was
correct even though the documentation was not.
