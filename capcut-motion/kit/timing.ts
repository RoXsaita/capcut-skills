// Time is written in milliseconds as integers, converted to frames at the
// edge. Every constant below carries the reason it is that number; a timing
// without a reason is a default, and defaults are what a viewer reads as
// "generated".

export const FPS = 30;
export const FRAME_MS = 1000 / FPS;

export const frames = (msValue: number, fps = FPS): number => Math.round((msValue / 1000) * fps);
export const ms = (f: number, fps = FPS): number => (f / fps) * 1000;

/* ── the house beat ─────────────────────────────────────────────────────── */

// enter over 12f, exit over 6f, stagger support by 3f, no single move over 18f
export const ENTER_MS = 400;
export const EXIT_MS = 200;
export const STAGGER_MS = 100;
export const MAX_MOVE_MS = 600;

// opacity resolves first (300) so a line is readable before it settles (400)
export const IN_OPACITY_MS = 300;
export const IN_MOVE_MS = 400;
// a gutter glyph or a support element leads its body by 3f
export const LEAD_MS = 100;
// px a supporting glyph travels up into place — small, so it reads as standing, not sliding
export const RISE_PX = 8;

/* ── cuts ───────────────────────────────────────────────────────────────── */

// shots lap by 4f, never butted: the leaver is still moving when the arriver is in
export const LAP_F = 4;
// sound starts 4f before the picture changes (0.133s at 30fps — measured on the house edits)
export const SOUND_LEAD_F = 4;

/* ── a machine at work ──────────────────────────────────────────────────── */

// typing: about a glyph a frame through the fast middle of a WRITE curve
export const CHAR_MS = 39;
// caret half period
export const BLINK_MS = 120;
// output starts printing before the camera has settled, the way a real CLI
// answers before the scroll has stopped
export const EAGER_MS = 200;
// a "working…" count is held this long per dot
export const DOT_MS = 280;

/* ── pixel snapping ─────────────────────────────────────────────────────── */

// There is no sub-pixel motion in a rendered frame: a move slower than about
// one pixel per frame sits still and then jumps. Divide the travel of the edge
// that moves most by the frames it takes; under 1 is a stutter, not a drift.
export const driftOk = (travelPx: number, durationFrames: number): boolean =>
	durationFrames <= 0 ? false : Math.abs(travelPx) / durationFrames >= 1;
