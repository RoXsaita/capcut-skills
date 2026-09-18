# Scene vocabulary — what a graphic beat can be

A graphic is not "a card with text". It is one of a small number of *shots*, each built around
one object, one move and one idea, and each chosen because the spoken beat under it is a
particular kind of beat (`shotlist.md` says how to choose). Nothing here is a template to
fill; each entry is a recipe an agent can build from the kit in an hour, with the pitfalls
that make the result read as generated.

Geometry below is stated for a 1080-high frame; the two house slots are the **top half**
(1080×960, the face keeps the bottom) and **full frame** (1080×1920). Everything must work in
both; the kit examples take `width`/`height` from the composition.

| Archetype | The beat it serves | In the kit |
|---|---|---|
| Big Word | one verb or claim that *is* the moment | `examples/BigWord.tsx` |
| Collage ring | "all of it", a set, many inputs, "I went through everything" | `examples/Collage.tsx` |
| Block climb | a process running, steps, a machine at work | `examples/Terminal.tsx` |
| Prop drama | one object handled: dropped in, pressed, flipped | recipe |
| Number | a statistic, a count, a multiplier | recipe |
| Two-up | before/after, X vs Y, then vs now | recipe |
| Word ticker | a list of three to five: tools, steps, names | recipe |
| Callout on capture | pointing at one thing in a real recording | recipe (picture is the recording) |
| Mark set-down | a brand named | **native** — `capcutctl logo`, not a render |
| Card | the end, a title | **native** — `capcutctl endcard`; render only if the type must move |

Never two of the same archetype running. Never more than one archetype in a shot.

---

## Big Word

**Beat.** One word carries the moment: *analyzing*, *published*, *done*, *broke*. The word is
spoken (or is the obvious name for what is being shown) and everything else can go.

**Picture.** One capital word in a condensed display face (Anton), cap height ~58% of the frame,
so the line is 1.5–3× wider than the frame. An I-beam stands where the writing begins.

**Move.** Letters are struck when the writing reaches their place on the line (the rhythm is the
type's measure, not a count), each standing up from 12% on `STAND` over 180ms, smeared while it
rises, sharp the frame it lands. The camera is pulled left on `PULL` through the whole line and
does not stop; the end of the word is carried off the left edge. ~1.4s. The shot leaves on its
own pull; the next shot comes up under it (a dissolve is allowed here and nowhere else).

**Slot.** Full frame (the face is under it, audible). In the top half only if the word is short.

**Pitfalls.** More than one word. A word that is not spoken or obvious. Letters fading in
instead of standing up. Stopping the camera so the word can be "read" — it is read on the move.

## Collage ring

**Beat.** Many things at once: the footage that was watched, the drafts that were harvested,
every screenshot, all the comments. The line under it names the act (*Watching footage*).

**Picture.** 8–12 stills of the real material, white-matted (a stroke that does not scale with
the frame — a mat says "different sizes", a scaling stroke says "different distances"). A label
in Inter 500 at the centre, with a band of light passing through the type every 900ms and a
dot count ticking every 280ms.

**Move.** A pile at the near point of a tilted ellipse unwinds along it while the ring turns
200° on one curve (`WIND`); the ring closes to 66% of its radius as it runs, so the shot is
"being taken up" rather than ending. Each still blends in on its own lag (big frames later),
the whole picture blurs in as one, and it leaves undone — blur up in 130ms, opacity out in 90.
2.9s.

**Slot.** Either; the kit clamps the ring to the slot width.

**Pitfalls.** Stock imagery instead of the real material. `Math.random`. Frames that stop moving.
A label that arrives after the ring has settled ("reads as two halves").

## Block climb

**Beat.** A process the viewer should see *happen*: commands running, a checklist completing,
a log filling. The machine is the subject.

**Picture.** A column of mono type on black, left margin 64, live line anchored low. No window,
no chrome, no traffic lights. A caret in the one accent colour.

**Move.** The frame is dark 160ms, the caret blinks once, typing runs on `WRITE` at ~39ms a
glyph; after each command the machine is seen to work ("working…") before it answers; each
answer's gutter leads by 3f, opacity in 300ms then an 8px settle; the block climbs one line on
`GLIDE` each time a slot opens. Ends on the last answer, cut on action.

**Slot.** Top half.

**Pitfalls.** A card. Constant-rate typing. Answers that appear at once. Colour on the ✓.

## Prop drama

**Beat.** One object is acted on and something happens: a file dropped into a prompt box, a
button pressed, a card turned over, a toggle flipped. The act is the sentence's verb.

**Picture.** Flat props drawn as SVG at the frame's scale — a panel with a 24 radius on
`#161616`, a folder, a button in the one accent. A pointer that is a *pointer*: white arrow with
a dark edge, at cursor scale ×3–4 so it reads as a hand, not a UI cursor.

**Move.** The pointer reaches on `AIM` (one throw, homing), the prop leans as it is carried
(`swing` a few degrees, `A_DRAG`), hover state comes up on `ENTER` 100ms, the drop lands on
`STAMP`, the panel acknowledges (a pill rises, placeholder dims). Then one push-in on the
result (`PULL` or a 1.15× scale) so the next shot can be handed over. 2–3s.

**Slot.** Top half.

**Pitfalls.** Reconstructing a real app's UI — capture it instead (see *Callout on capture*).
Springy overshoot on the drop. Two props moving at once. A cursor at 1× (it vanishes).

## Number

**Beat.** A statistic or count is spoken: *450K*, *18 out of 18*, *ten times faster*, *0.13s*.

**Picture.** The figure alone, Inter 600 at title size, unit or qualifier in `TEXT_2` at label
size below or beside. The number may be the shot's accent. Nothing else in the frame.

**Move.** Digits arrive on `EXPO_OUT` (a counter: the last 20% of the travel takes 60% of the
time, so it lands rather than stops), 600ms; the qualifier leads or trails by 3f on `ENTER`.
Hold as long as the words need, keep a slow drift *above 1px/frame* or a subtle blur/opacity
change so the frame is never still. Leave on `EXIT`.

**Slot.** Either. In full frame, beside or below the head, never over it.

**Pitfalls.** A number in a box. Comma-rolling every digit for two seconds. Two numbers.

## Two-up

**Beat.** Comparison: before/after, tool A vs tool B, the wrong way and the right way.

**Picture.** Two panels of the real material, square where the source allows, gap 40, radius
24. In the top half: side by side. In full frame: stacked. Labels in `TEXT_2`, one word each.
The winner (if there is one) gets the accent, on one element.

**Move.** Hard cut in; the labels lead their panels by 3f. If the two states are the *same*
object, a continuous carry across the cut; if not, no motion between them. A step from state A
to state B is one slide on `IN_OUT`. Nothing else moves.

**Pitfalls.** A "VS" graphic. Arrows. Panels that slide in from opposite sides. Different
crops.

## Word ticker

**Beat.** A short list is spoken: three tools, four steps, the five things.

**Picture.** Each item one line, Inter 500, left-aligned, anchored low, a hairline or nothing
between them. Optional mark per item (a monochrome glyph, not a colour logo — brands are
`capcutctl logo`'s job on the *face*).

**Move.** Each item rises inside its own clip box (masked `translateY` from 100% to 0 on
`ENTER`, 260ms), staggered from the *focal* item, not from the top — if the third tool is the
point, it lands first or last, and the stagger fans out from it. Sizes or delays vary per item
via `span(i, salt, …)`, never identical.

**Pitfalls.** Cards. Bullets. Identical pops. Logos in colour on a dark card (that is the
pattern the tells table calls a landing page).

## Callout on capture

**Beat.** "This button", "that line", "here" — pointing at one element in a real recording.

**Picture.** The recording is the picture. Draw only what does not exist on screen: a rectangle
in the accent at 2px, a one-word label in `TEXT`, or a dimming of everything but the focus.

**Move.** The rectangle stands up on `STAND` (200ms) from its centre, the label leads by 3f,
the dim comes up in 300ms. Then the native `capcutctl keyframe --focus` push-in does the
camera, in CapCut, editable.

**Slot.** Top half, on the recording placed by `capcut-editing-screen-recording`.

**Pitfalls.** Redrawing the UI. Arrows. A rectangle that pulses.

---

## What every archetype shares

- One object, one move, one idea. If the brief needs two, it is two shots.
- The camera is always doing something, and it hands over to the next shot rather than stopping.
- Every value is on a named curve and every constant is in ms with a sentence.
- Real material (his footage, his UI, his numbers) over illustration; illustration over stock.
- The still is the truth. If a frame from `stills.sh` does not look like a frame from a film you
  would stop scrolling for, the shot is not finished.
