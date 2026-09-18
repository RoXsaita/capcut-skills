import {Easing} from 'remotion';

// Every move is on a named curve chosen for the *intent* of the motion. Never
// linear unless the movement is mechanical, and never Remotion's default
// spring — a bouncy pop on every element is the fingerprint of an unedited
// template.
//
// The six anchors are the Diffusion Studio motion guide (MPL-2.0); the named
// intents below them are ported from the open-source Diffusion Studio launch
// video (MIT, github.com/diffusionstudio/launch-video). Read each comment
// before reaching for a curve; if none fits, add one *with* its sentence.

export type Ease = (t: number) => number;
const bez = (a: number, b: number, c: number, d: number): Ease => Easing.bezier(a, b, c, d);

/* ── the six anchors, in mirrored pairs ─────────────────────────────────── */

// energetic entrances that settle softly
export const SNAPPY_OUT = bez(0, 0.6, 0.4, 1);
// dramatic reveals, scale pops, counters
export const EXPO_OUT = bez(0, 1, 0, 1);
// wind-ups that exit at full speed
export const SNAPPY_IN = bez(0.6, 0, 1, 0.4);
// anticipation into a hard exit or cut
export const EXPO_IN = bez(1, 0, 1, 0);
// motion carried across a cut — a whip
export const OUT_IN = bez(0, 0.7, 1, 0.3);
// A-to-B moves at rest on both ends
export const IN_OUT = bez(0.7, 0, 0.3, 1);

/* ── arriving and leaving ───────────────────────────────────────────────── */

// arriving: three quarters of the travel in the first fifth
export const ENTER = bez(0.2, 0.75, 0.34, 0.94);
// leaving: holds, then all of it at once
export const EXIT = bez(1, 0.02, 0.54, 0.42);
// landing or resolving
export const SETTLE = bez(0.25, 0.4, 0.35, 1);
// coming to rest: fast in, nearly all of it spent slowing
export const LAND = bez(0.16, 1, 0.3, 1);
// Apple's sheet-presentation settle: away at speed, then a long even landing
export const GLIDE = bez(0.66, 0.004, 0.376, 1.001);
// the way out: barely leaving, then all of it at once — a thing let go
export const DIVE = bez(0.86, 0.005, 0.999, 0.177);
// a letter standing up over a few frames — ENTER would be over before it was seen
export const STAND = bez(0.5, 0, 0.3, 1);
// gathers from rest, unlike EXIT which holds at the top
export const DEPART = bez(0.55, 0, 0.85, 0.55);

/* ── writing and reaching ───────────────────────────────────────────────── */

// typing: leaves rest and keeps gathering, quickest at the last key
export const WRITE = bez(0.3, 0, 0.75, 0.55);
// soft and symmetric: gentle at both ends, quick through the middle
export const FOLLOW = bez(0.45, 0, 0.55, 1);
// a hand's reach: one throw, quickest a third in, then homing onto the target
export const AIM = bez(0.32, 0.04, 0.3, 1);
// a quarter turn: gathering the whole way, quickest as it lands
export const TURN = bez(0.737, 0.195, 0.927, 0.549);

/* ── marks and cards ────────────────────────────────────────────────────── */

// a mark set down: in at full speed, seated in the first third, then one long even landing
export const STAMP = bez(0, 0.626, 0.369, 0.993);
// stepping aside: softer off the mark than STAMP, the rest easing into place
export const UNVEIL = bez(0, 0.36, 0.469, 0.993);
// a card's arrival: nearly all the travel in the first frames, then a long soft settle
export const ALIGHT = bez(0, 0.816, 0.135, 1.001);
// a card's whole stay on one curve: most of the shrink at the cut, a slow drift, closed at the end
export const DWINDLE = bez(0, 0.986, 1, 0.371);
// a collapse onto its own frame: full speed from the first frame, one long landing
export const COLLAPSE = bez(0.001, 0.725, 0.238, 0.99);
// a whole shot's rotation on one curve: quick, slow, then quickest; monotone throughout
export const WIND = bez(0.35, 0.45, 0.85, 0.28);

/* ── the camera ─────────────────────────────────────────────────────────── */

// Shots leave on the move they were already making and the next arrives at
// the speed the last one left at, so a hand-over reads as one swing.

// bringing a shot on: in at speed, the rest of the length is the settle
export const CAM_IN = bez(0.161, 0.708, 0.562, 0.916);
// a panel's arrival: off at full speed, then one long even settle
export const PANEL_IN = bez(0, 0.544, 0.414, 0.994);
// a pull: eased in from a still frame, gathering, easing off as it carries the subject out
export const PULL = bez(0.378, 0.226, 0.817, 0.634);
// a whole camera in one move: seven eighths near the subject's own rate, then the run-off
export const SWEEP = bez(0.705, 0.076, 0.965, 0.818);
// at rest while there is room, then gathering without let-up — quickest as it takes the block off
export const CLIMB = bez(0.512, 0.203, 1, 0.788);

// A smoothstep, for a value that must leave and arrive at a standstill.
export const SMOOTH: Ease = (u) => u * u * u * (u * (u * 6 - 15) + 10);
