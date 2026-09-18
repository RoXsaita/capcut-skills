// Near-achromatic by default. Structure comes from scale, weight, spacing and
// luminance — never from a glow, a grid, a gradient or a coloured card. When a
// piece needs an accent, take it from the subject (its UI, its footage), use it
// on at most one element per shot, and never on a title or a large fill.

export const BG = '#000000';
export const SURFACE = '#161616';
export const TEXT = '#F8F8F8';
export const TEXT_2 = '#A4A4A4';
export const HAIRLINE = 'rgba(255,255,255,0.10)';

// One clean sans plus its mono companion. Inter/Geist are the targets; the
// stack falls back to the system face when they are not installed, which is a
// clean sans too — never a reason to reach for a display font.
export const SANS =
	'"Inter", "Geist", -apple-system, "SF Pro Text", "Helvetica Neue", Helvetica, Arial, sans-serif';
export const MONO =
	'"Geist Mono", "JetBrains Mono", "SF Mono", ui-monospace, Menlo, Monaco, monospace';

// Type scale at a 1080 short edge. Keep the order and rough ratios when you
// adjust; rewrite copy that exceeds `max` instead of shrinking the type.
export const TYPE = {
	title: {size: 96, weight: 600, max: 32},
	subtitle: {size: 60, weight: 400, max: 64},
	name: {size: 48, weight: 500, max: 28},
	detail: {size: 30, weight: 400, max: 40},
	label: {size: 24, weight: 500, max: 16},
} as const;

// Spacing in multiples of 8. Margin 64, gap 40, 16 label→value, 24 between
// lines in a block, 40 between blocks.
export const MARGIN = 64;
export const GAP = 40;
// Framed media panels only. Never round full-frame media.
export const RADIUS = 24;
