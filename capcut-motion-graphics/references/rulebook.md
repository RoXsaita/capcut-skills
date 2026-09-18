# Rulebook — how a drawn frame is allowed to look and move

Adapted from the Diffusion Studio brand and motion guides (MPL-2.0) and from measuring their
open-source launch video (MIT), then cut down to what applies to a graphic that will sit in a
CapCut edit. Pixel values assume a 1080 short edge; scale them for anything else. Frame counts
assume 30fps; keep the millisecond values when the rate differs.

## Visual principles

- Build structure with scale, weight, spacing and luminance.
- Keep the frame near-achromatic. Use colour only when it carries meaning.
- Show the subject clearly. Do not decorate over controls or content the viewer must read.
- One clear focal point beats several equal ones.

## Colour

| Role | Value |
|---|---|
| Background | `#000000` |
| Surface | `#161616` |
| Text | `#F8F8F8` |
| Text, secondary | `#A4A4A4` |

The palette has no accent of its own. When a piece needs one, take it from the subject: a colour
already in its footage, interface or supplied material. One accent per piece, on at most one
element per shot, never a title or a large fill. Beside captured UI avoid an accent that reads as
one of that interface's states (red for error, green for success).

Invert the palette for a piece whose footage is predominantly light. Put text on a plain
background or surface; do not rely on a shadow or stroke for contrast.

## Typography

One clean sans (Inter, or Geist) plus its mono companion. No italic. No display faces.

| Role | Size | Weight | Copy limit |
|---|---:|---:|---:|
| Title | 96 | 600 | 32 glyphs |
| Subtitle | 60 | 400 | 64 |
| Lower-third name | 48 | 500 | 28 |
| Lower-third detail | 30 | 400 | 40 |
| Label | 24 | 500 | 16 |

Sizes are starting points; keep the order and rough ratios. **Rewrite copy that exceeds a limit
instead of shrinking the type.** At most two text elements in one shot: a primary line and its
qualifier. Left-align copy and anchor it low; centre only when it stands alone on a plain
background.

## Captured imagery

- Show real product UI rather than a reconstruction or recolour.
- `contain` when the viewer must read the whole interface; `cover` only when the crop cannot hide
  a control, label or result the point needs.
- Keep captures sharp and at native aspect. Surround them with plain surface; never stretch.
- Corner radius 24 on framed media panels. Never round full-frame media.

## Layout

Margin 64, gap 40, other spacing in multiples of 8: 16 between a label and its value, 24 between
lines in one block, 40 between blocks.

Media forms:

- **Full frame** — one view or one dominant subject.
- **Two-up** — two states, inputs, speakers, before/after. Side by side in 16:9 and 1:1; stacked in
  9:16. Square panels when the source allows.
- **Four-up** — a set of equal details that stay legible at delivery size; a centred 2×2.

Change layout because the idea changes, not to add motion. Prefer a hard cut between layout forms;
carry one element across only when it is the same object or state. In 9:16 hold split layouts
longer because each panel is smaller.

### 9:16 safe area

At 1080×1920 keep readable content inside `x 64–900`, `y 200–1520`. The right 180px is the
platform action rail; the bottom 400px is the caption reserve. Graphics may cross these; text may
not.

For the house split-screen (1080×960 top half) the safe area is the whole slot minus the 64
margin; the seam bar is drawn by `capcutctl layout`, not by the graphic.

## Timing

| Beat | ms | frames @30 |
|---|---:|---:|
| Enter | 400 | 12 |
| Exit | 200 | 6 |
| Stagger support | 100 | 3 |
| Any single entrance or exit | ≤ 600 | ≤ 18 |
| Opacity resolves | 300 | 9 |
| …then movement settles | 400 | 12 |
| Support leads its body | 100 | 3 |
| Shots lap | — | 4 |
| Sound leads picture | 133 | 4 |
| Typing, per glyph | 39 | ~1 |
| Caret half period | 120 | ~4 |

Write times as integers in ms and convert at the edge. Lead with one element and delay its
support by 3f. Stagger repeated items from a meaningful origin — first, centre, or the focal
point — never just top to bottom. Let opacity finish before movement so text is readable before
it settles. One flourish per beat; a busy scene is a layout problem.

## Motion

Motion graphics are motion. Elements that fade in, sit still and fade out read as slides. Keep
energy in the frame: overlap entrances and exits, stagger siblings by a few frames, keep
something moving during holds (a drift, a count, a caret, a shimmer), and drive every move with a
named curve (`easings.md`).

**Pixel snapping.** There is no sub-pixel rendering: a move slower than about one pixel per frame
sits still and then jumps. Before committing a move, divide its travel in pixels by its frames;
under 1 is a stutter. The same applies to scale and rotation — measure the edge that moves most.
Slow holds are where this bites: move further, move shorter, or carry the hold on a channel that is
not position (opacity, blur, colour, a counter).

## Cuts

| Method | Use |
|---|---|
| Hard cut on action | energy while authored motion is still moving |
| Jump cut | matched direction and speed across the seam |
| Continuous carry | the same object or state across two beats |
| Hold cut | read-critical text, captured UI, final lockups |

Prefer these to transition presets. Hand shots over rather than butting them: the leaver
accelerates out (`EXIT`) and the arriver decelerates in (`CAM_IN`), lapping 4 frames, so the frame
is never at rest across the join. Cut screen captures after the needed action or label has been
visible long enough to read. Tighten a slow cut before adding motion.

In CapCut the transition and its sound are `capcutctl polish`'s job, on the principal track;
the graphic only needs a clean picture change for polish to key on.

## Captions and sound

Captions are added last, after the edit and final audio placement, and never over a graphic's
text. Speech has priority; when several copies of the same capture appear, one carries audio and
the rest are muted. Do not bake sound effects into a rendered graphic — `polish` places them 4
frames ahead of the picture change and keeps them editable.
