import {CAM_IN, EXIT, type Ease} from './easing';

// Small pure helpers. Everything takes the current frame and returns a number,
// so a still at frame N is exactly what the export shows at frame N.

/* ── progress ───────────────────────────────────────────────────────────── */

// 0 before `at`, eased 0→1 across `dur` frames, 1 after.
export const progress = (frame: number, at: number, dur: number, ease: Ease): number => {
	if (dur <= 0) return frame >= at ? 1 : 0;
	const t = Math.min(1, Math.max(0, (frame - at) / dur));
	return ease(t);
};

// `from` → `to` on an eased progress.
export const run = (
	frame: number,
	at: number,
	dur: number,
	ease: Ease,
	from: number,
	to: number,
): number => from + (to - from) * progress(frame, at, dur, ease);

/* ── tracks ─────────────────────────────────────────────────────────────── */

export type Key = {at: number; value: number; ease?: Ease};

// Piecewise keyframes. Each segment is eased by the *destination* key's curve,
// so a key describes how the value arrives at it. Holds before the first and
// after the last key.
export const track = (frame: number, keys: Key[]): number => {
	if (keys.length === 0) return 0;
	if (frame <= keys[0].at) return keys[0].value;
	for (let i = 1; i < keys.length; i++) {
		const a = keys[i - 1];
		const b = keys[i];
		if (frame <= b.at) {
			const ease = b.ease ?? ((t: number) => t);
			return run(frame, a.at, b.at - a.at, ease, a.value, b.value);
		}
	}
	return keys[keys.length - 1].value;
};

/* ── hand-over ──────────────────────────────────────────────────────────── */

// Two shots are handed over, not cut: the leaver accelerates out on EXIT and
// the arriver decelerates in on CAM_IN, overlapping so the frame is never at
// rest across the join. Returns both progresses.
export const handOver = (
	frame: number,
	at: number,
	outDur: number,
	inDelay: number,
	inDur: number,
): {out: number; in: number} => ({
	out: progress(frame, at, outDur, EXIT),
	in: progress(frame, at + inDelay, inDur, CAM_IN),
});

/* ── stagger ────────────────────────────────────────────────────────────── */

// Stagger repeated items from a meaningful origin, never just top-to-bottom.
export const staggerDelay = (
	i: number,
	n: number,
	step: number,
	origin: 'first' | 'center' | 'last' = 'first',
): number => {
	if (origin === 'first') return i * step;
	if (origin === 'last') return (n - 1 - i) * step;
	return Math.abs(i - (n - 1) / 2) * step;
};

/* ── deterministic scatter ──────────────────────────────────────────────── */

// A hash, not a sequence. A composition is re-executed in every context
// (preview, still, export), so any "random" scatter must come out of the
// index alone or the still you approved is not the frame you ship.
export const seed = (i: number, salt: number): number => {
	let h = Math.imul(i + 1, 0x9e3779b1) ^ Math.imul(salt + 1, 0x85ebca6b);
	h = Math.imul(h ^ (h >>> 15), 0xc2b2ae35);
	h ^= h >>> 16;
	return (h >>> 0) / 4294967296;
};

export const span = (i: number, salt: number, lo: number, hi: number): number =>
	lo + (hi - lo) * seed(i, salt);

// Remove the mean from a set of scatters, so a pile sits where you put it and
// only its members are scattered.
export const centered = (values: number[]): number[] => {
	const mean = values.reduce((a, b) => a + b, 0) / values.length;
	return values.map((v) => v - mean);
};

/* ── ramps, not loops ───────────────────────────────────────────────────── */

// A count read modulo a ramp cannot be wrong on any frame; a looping child of
// a seeked timeline can. `cycle(frame, at, periodF)` → 0..1 within the period.
export const cycle = (frame: number, at: number, periodF: number): number => {
	if (frame < at || periodF <= 0) return 0;
	return ((frame - at) % periodF) / periodF;
};
