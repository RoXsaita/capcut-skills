---
name: capcut-editing
description: >
  Edit a talking-head + screen-recording short into a production-grade, highly animated CapCut
  project that is ready to post, with capcutctl. THE skill for any CapCut editing request: the
  first-run style question, the A-roll cut and sign-off, the shot list, writing edit.json (the
  judgement: hook, graphics on words, brands, CTA, music brief), `capcutctl build`, the blocking
  `capcutctl gate`, review and hand-off. The command reference is capcut-cli.
---

# CapCut editing

The deliverable is a **CapCut project** the user can still drag, not a rendered file. The
CLI does the mechanics; you make the calls a transcript cannot: which take, which order, which
shot proves which sentence, which words deserve a graphic, and what the music should feel like.

**The loop:** cut the face → user signs it off → shot list → `edit.json` → `build` → fix
until `gate` passes → review frames → hand off. Everything after sign-off is one command.

## 0. Setup and the one style question

`capcutctl` must be on PATH (see the CLI's SETUP.md; ffmpeg required; Playwright + Chromium for
graphics). Run `capcutctl preflight` once and read its non-blocking rows.

The creator's brand, styles and preferences live in **their profile**, outside every repo:
`~/.config/capcutctl/profile.json`, merged over the CLI's shipped, brand-neutral defaults.
Run `capcutctl profile where` first.

- **A user layer exists:** that is their style. Use it; don't ask again.
- **None:** ask **once, before the first write**:
  1. **Set up their profile** — `capcutctl profile init`, then fill `brand`, `tokens.color`,
     `tokens.font` and `styles` with them. [capcut-motion](../capcut-motion/SKILL.md) says what each part is for.
  2. **Measure their own edits** — `capcutctl harvest --profile FILE`, and copy what it measured
     into their profile (or pass `"profile": FILE` in `edit.json` for this video only).
  3. **The neutral defaults** — the shipped profile as it is. Placeholder colours; say so in the hand-off.
  4. **Blank** — `capcutctl new --blank`, and ask what they want before adding graphics or seams.

Never apply one creator's brand to another. Don't write a brand into a skill or a repo either.

If they hand over a **reference reel** ("edit it like this"), measure it before you plan:
`capcutctl reference --media reel.mp4 --sheet shots.png --profile-out ref-profile.json`.
Read the pacing numbers and the shot sheet, say in plain words what you would copy, and hold the
edit to it with `gate --profile ref-profile.json`. Details: [references/render-qa.md](references/render-qa.md).

## Every session: read the creative log first

`capcutctl notes --project NAME --brief` prints what was already tried and rejected, the accepted
look, the decisions, and what is still owed. Read it before proposing anything, and summarise the
last state in one sentence. When the user rejects something, record it with the reason
(`notes --reject … --why …`); when something lands, record that too (`notes --accept … --why …`).
The log lives outside snapshots, so it survives `restore`, a compaction and a new session.
Without it, the next round proposes the rejected look again.

## Non-negotiables

- **Overlays only.** The main track (CapCut's "cover") stays empty; every clip is on an overlay.
- **Every decision stays a CapCut property.** Import full-frame originals from durable paths;
  crops, zooms, speed and cuts are native (`add` refuses `PREFRAMED_MEDIA` / `EPHEMERAL_MEDIA`).
  The only rendered media are `mograph` graphics and scenes, imported `--generated` with a
  re-render sidecar. Motion design is the one thing that *is* rendered: `capcutctl mograph`
  scenes and templates become `--generated` clips and the edit around them stays native.
  Brand, style and the video's own idea: [capcut-motion](../capcut-motion/SKILL.md).
- **The face is always 1×.** Recut length with `cut`; never speed or trim-stretch the talking head.
- **Never hand-write `draft_info.json`.** If the CLI cannot express an edit, extend the CLI.
- **CapCut closed for writes** (`capcutctl close`). `doctor` error-free before any hand-off.
- **Export only when the user explicitly asks.** "Finish/polish/finalise" means the editable project.

## 1. The talking head — then stop

```bash
capcutctl cut FACE.mp4 --lang ar                                   # table + FACE.aroll.json
capcutctl cut FACE.mp4 --keep 0,2-9 --order 0,2,3,4,5,6,7,8,9 --dry-run
capcutctl cut FACE.mp4 --keep 0,2-9 --order 0,2,3,4,5,6,7,8,9 --project NAME
capcutctl scenes --project NAME --transcript                       # read the final script
capcutctl doctor --project NAME
```

Read the whole transcript in story order and decide: which complete take, which instance of a
repeated line (usually the last, if it is also the most complete), false starts, near-duplicates,
and the running order (hook → explanation → proof → payoff → CTA). Boundaries, dead air and seam
repair are arithmetic — never hand-pick timestamps. Details: [references/aroll.md](references/aroll.md).

**Stop and get the cut signed off.** Everything else anchors to it. After sign-off a recut is
cheap — `build` re-anchors every graphic to its words — but a wrong keep-list poisons all of it.

## 2. The shot list

```bash
capcutctl match --project NAME --screen SCREEN.mp4 --out shots.json   # sentence → moment
capcutctl verify-shots --project NAME --shots shots.json               # CONTRADICTED blocks
```

Edit `shots.json`: weak matches stay on the face (a valid answer). The picture must **prove the
words**: verify the verb on before/action/after frames, separate waiting (ramp it) from the action
(readable) and the result (hold it), one focus per shot, and the first 1.5s must show proof.
Details and OCR discipline: [references/broll.md](references/broll.md).

## 3. Write `edit.json` — the judgement

```json
{
  "version": 1,
  "shots": "shots.json",
  "graphics": [
    { "template": "hook-title",    "say": "بنيت موقع كامل", "params": { "text": "موقع كامل بدقيقة" } },
    { "template": "keyword-super", "say": "مجاني",          "params": { "text": "مجاني بالكامل" } },
    { "template": "number-pop",    "say": "تسعين",          "params": { "value": 90, "suffix": "%", "label": "أسرع" } },
    { "template": "callout-box",   "at": 21.4,               "params": { "box": [210, 640, 520, 120], "label": "Publish" } },
    { "template": "cta-card",      "say": "اكتب",            "params": { "keyword": "AI" } }
  ],
  "logos": "auto",
  "endcard": { "text": "Follow" },
  "sound": { "music": { "prompt": "minimal tense synth pulse, opens up warm at the reveal, no drums under speech" } }
}
```

- **`say`** anchors a graphic to the words as spoken in the cut (Whisper's spelling; hamza/dots fold).
  It lands the profile's lead frames before the word. Use `occurrence` for the Nth time it is heard.
  `at` is only for things with no word (a callout on a screen moment).
- **Hook:** a `hook-title` inside the first second, over proof. **Claims:** one `keyword-super` of
  1–3 words, never the whole sentence, at most one per ~6s. **Numbers:** `number-pop`.
  **Instructions:** `punch` onto the element, or a `callout-box` on a *static* shot (never both on
  one target). **CTA:** `cta-card` + endcard. Leave rests: not every sentence gets a graphic.
- **Brands:** `"logos": "auto"` pops each brand once, on its first surviving mention; a brand with no
  artwork becomes a text `brand-chip`. A versus video pops both or neither.
- **Music:** a story-specific brief or a local `file`; the bed aligns to the graphics and picture
  changes, ducks under speech, and never moves the picture.

Full schema, every template's params, and defaults: [references/edit-plan.md](references/edit-plan.md).
The grammar behind these choices: [references/grammar.md](references/grammar.md).

## 4. Build, then pass the gate

```bash
capcutctl mograph preview --template number-pop --params '{"value":90,"suffix":"%"}' --out /tmp/n.png   # look first
capcutctl build --project NAME --edit edit.json --dry-run
capcutctl close
capcutctl build --project NAME --edit edit.json          # exit 1 while the gate fails
capcutctl gate --project NAME                            # re-check on its own at any time
```

`build` applies, in order: reviewed shots (once) → `layout auto` → stress pushes → graphics on their
words with their sounds → logo pops → endcard → motivated seams → music → duck → loudness → gate.
Every stage replaces its own output; an unchanged plan on an unchanged cut is a no-op.

Fix every **FAIL**, then rebuild:

| Gate check | Usual fix |
|---|---|
| `hook` / `proof` / `first-picture` | Put a shot at 0s in `shots.json`; add a `hook-title` said in the first second |
| `max-static` | A graphic, a `punch`, or a shorter shot in that window — or cut the dead air |
| `simultaneity` / `entrance-spacing` | Move one graphic to a different word; drop it if the camera already moves |
| `template-repeat` | A different template, or drop the second one |
| `safe-zones` | `params.layout` or `params.center` into the text band |
| `graphic-sfx` | The cue is missing on this machine (`preflight`), or `"sfx": null` was set by mistake |
| `chip-and-logo` | Remove the brand-chip; the logo pop already names the brand |
| `same-screen-transitions` / `seam-variety` | Rebuild (motivated seams) — never decorate an A-roll splice |

**WARN** rows are not blockers, but each one goes in the hand-off by name.

## 5. Review and hand off

```bash
capcutctl qa --project NAME --times 0.4,3.2,9.8 --sheet        # hook, each graphic's hold, each punch
capcutctl preview --project NAME --from 0 --to 8 --out /tmp/open.mp4
capcutctl doctor --project NAME
```

Look at the frames: the graphic reads at phone size, sits clear of the face and the UI element
being discussed, and the picture proves the words. Check the opening and one dense section with
sound. Then tell the user, in this order:

1. The project name, and that it is ready in CapCut.
2. The gate verdict and every WARN (e.g. `mograph-import` until the Mac checklist in the CLI's
   `docs/mograph.md` has passed; `unseen` native layers; missing SFX).
3. What you could not check (sound in native effects, motion easing at full speed).
4. Ask how many minutes of manual fixing it took, and record it — the target is under ten.

**Any rendered file** — an authorized export, or one the user supplies — gets
`capcutctl check-export --media FILE --project NAME` first. It reads the render, not the draft:
black inside the edit, stray 1–2 frame shots, dead air, loudness, true peak, canvas and length.
FAIL exits 1. Then `export-grid --times` on the moments it lists, and look at them before calling
any of them a defect. Thresholds and what FAIL vs WARN means:
[references/render-qa.md](references/render-qa.md).

**For anything that will be published, get a fresh-eyes critique before hand-off.** Give a
sub-agent with no context the grid or contact sheet, the `check-export` report, the creative log
and any reference sheet. Brief it to find problems, not to praise: a verdict, then ranked problems
with timecodes and evidence, then the five fixes to do first. You stop seeing your own edit; a
reader with no context still sees a payoff line cut short or text too small to read at phone size.

**Revisions.** For a note like "change only X", snapshot, make the change, then prove its scope
before saying it is done: `capcutctl diff --project NAME --snapshot LABEL --allow SEGMENT-ID,track:NAME`.
It exits 1 and names every change outside that scope. Record rejections in `notes` as they come.

## Reference files

| File | Use it for |
|---|---|
| `references/edit-plan.md` | The `edit.json` schema, template catalogue and parameters, defaults |
| `references/grammar.md` | Motion grammar: what each beat gets, density, rest, the never-list |
| `references/aroll.md` | Talking-head judgement, the acoustic boundary rules, escalation |
| `references/aroll-indexing.md` | The three indexes and the linter's calibration — when diagnosing a seam |
| `references/broll.md` | Shot evidence, `find`/`match`/`verify-shots`, OCR discipline, framing and bbox rules |
| `../capcut-motion/SKILL.md` | Motion design: brand from the profile, a style per video type, one idea per video; overlay graphics, full-frame scenes, drawn B-roll |
| `references/render-qa.md` | `check-export` thresholds, reference reels, scoped revisions with `diff --allow`, the creative log |
| `references/preview-loop.md` | Frame/proxy review, export permission, the native export bridge |
| `references/capcut-format.md` | The draft format, mirrors, geometry and layer stack |
| `references/pitfalls.md` | Traps already hit. Read before a first edit |
| `references/style.md` | Where the house style came from (provenance); the targets live in the profile |
| `references/project-state.md` | Reading current drafts, caches and decisions that must not be undone |
