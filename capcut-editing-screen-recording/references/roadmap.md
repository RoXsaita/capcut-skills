# Phase 2 and 3 — design, not yet built

Phase 1 (`rl2`) exists. This file is the agreed design for the two phases after it, so nothing has
to be re-derived. **Gate: do not start Phase 3 until a real recording round-trips through Phase 2.**

---

# Phase 2 — event compiler and index

A CLI that compiles `screen.mp4` + `trace.ndjson` into a SQLite session DB. Four levels, and the
level a fact came from is itself a confidence signal.

**L0 — change signal.** Already emitted by the recorder (`change.ndjson`), plus SCK dirty rects.
No models. Yields stable states and transitions.

**L1 — events. This is the primary retrieval corpus.** The telemetry events, plus **synthetic
`state_transition` events**: a large persistent visual change with no nearby input — an AI finishing
a generation, a modal appearing, an animation starting. That fills the one real hole in pure
interaction telemetry, since the most quotable moments in these videos are things the machine did,
not things the user clicked.

Cross-validate while compiling:

| Pattern | Meaning |
|---|---|
| click with no visual change | dead click — do not offer it as B-roll for "I tapped X" |
| visual change with no click | passive event — an arrival, not an action |
| click then change then settle | causal; the useful case |

Resolve the three temporal anchors here, not in the recorder:

* `input_time` — from the trace.
* `visual_onset` — first frame after `input_time` where the change signal crosses the floor.
* `settled_time` — where it falls back and stays.

**L2 — semantic keyframes.** OCR and cheap image embeddings on event before/settled frames and
change-points **only** — never uniform per-second sampling. OCR must be **region-tagged** (chat
panel vs app canvas vs toolbar). AX geometry gives the regions on Mac; phone footage needs one-time
layout labelling per app. Region tags are what make it possible to reject *text describing a thing*
in favour of *the thing* — the exact failure that returned chat text for `gold`+`wave`.

**L3 — VLM evidence.** None at index time. A VLM runs only at query time, on 5–15 candidates.

**Precision must not degrade with length.** Length may affect storage and cheap preprocessing. It
must never affect temporal accuracy. A 31-minute take is normal, not an edge case.

---

# Phase 3 — the editing skill

Companion to the talking-head skill, which is solved. Deliverable stays `draft_info.json`.

## 1. Visual obligation contracts

Each script sentence compiles to a contract:

* **type** — `user_action` / `dynamic_result` / `state_shown` / `narrative` / `no_broll`
* **target semantics** and expected AX role
* **required evidence** — e.g. target visible before, click inside target bounds, UI reacts after
* **preferred anchor** — `input_time` for "I clicked X"; `settled_time` for "it opens Y" / "you can
  see Z"
* **reject clauses**, enforced through region tags — reject OCR-only mentions, reject chat text
  describing the event

The rule underneath all of it: **search for proof of an event, not for words.**

## 2. Global alignment, not per-sentence retrieval

DP/Viterbi over sentences × events, maximising semantic score plus sequence, causal and app-state
consistency; penalise backwards jumps and event reuse. Allow sentence → no B-roll, and
many-sentences → one state. Order is a strong prior, not a hard constraint.

Guided-mode sentence markers, where present, collapse this to verification of the marked window.

## 3. Evidence-based confidence

Never use raw "VLM confidence." Score observable components: semantic match, interaction type,
click-inside-bbox, before-state visibility, expected after-transition, modality correctness,
sequence consistency, label provenance (`accessibility` | `crop_ocr` | `coords_only`), and the
**top1-vs-top2 margin**.

A low margin means *the system does not know* — a first-class state, not a low score.

> **A missing B-roll shot beats a wrong one.** Low evidence → leave the talking head, flag for review.

## 4. Zoom synthesis

**The agent decides whether and what. Code decides geometry. The model never emits a coordinate.**

Agent: does the viewer need help finding the referent? Is the target under ~15% of frame? Is small
text being read aloud?

Code: a deterministic function from target bbox → context padding → max scale → crop bounds → 9:16
safe area → CapCut scale/translate keyframes, through the known transform chain and the locked
presets.

Bbox source hierarchy, best first: AX/CDP bounds → OCR word boxes → grounding model (verified by
cropping the proposed rect) → click coordinate alone (anchor only, never a box).

Timing grammar by event type:

| Event | Zoom behaviour |
|---|---|
| click | zoom arrives **before** the click (~250 ms lead), holds through the reaction |
| result | settle first, then zoom |
| scrolling | never zoom mid-scroll |
| big visual effect | usually do not zoom |

No consecutive punch-ins without a wide reset. If a target moves — menus, scrolling — track its
bbox across the clip and keyframe accordingly.

## 5. Verification (strict)

Per sentence, a machine-checkable proof package: the claim, the chosen source range, the event ID,
evidence frames (before / input / after / settled), the target bbox, the input position, and
assertions:

* target visible before input
* input inside bbox
* response onset detected
* the final crop contains the full bbox for the whole zoom
* the event lies inside the inserted clip, with pre- and post-context

Then a **blind independent verifier**: a second model gets only the claim, the evidence frames and
the highlighted bbox — **never the selector's reasoning** — and returns `SUPPORTED` /
`CONTRADICTED` / `INSUFFICIENT`.

Then project-level QA: re-read the emitted `draft_info.json`, mathematically reconstruct the
viewer's 1080×1920 viewport for each B-roll segment (timeline time → source time → transform and
keyframe interpolation), render QA frames, and assert visibility, containment and no overshoot.

Unit tests, for video editing.

## 6. Benchmark

Freeze approved edits and known failures as a regression corpus. Must include:

* the `gold`+`wave` chat-text false positive
* the same button clicked several times
* right screen, wrong instance
* before-action vs after-action frames

Metrics: recall@5, exact-event accuracy, temporal error, wrong-modality rate, zoom-target IoU, crop
containment, and above all **wrong edits emitted without a flag — drive that to zero.**

> 95% auto + 5% flagged beats 99% auto + 1% convincingly wrong.

---

## Adapters, for later

Common `InteractionEvent` / `TargetRegion` / `VisualStateBefore` / `VisualStateAfter` abstraction
with pluggable sources: CGEventTap + AX for generic macOS (built), optionally CDP
(`DOM.getNodeForLocation` + box model) for Chromium, pixels-only for phone footage. Do not chase
one universal API.
