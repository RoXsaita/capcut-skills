// The creator's brand, read from their profile — never typed in here.
//
// `kit/scripts/sync-profile.sh <project>` writes ./profile.json: the CLI's shipped defaults
// with the creator's ~/.config/capcutctl/profile.json merged over it. Change the brand there
// and re-sync; the CapCut graphics (`capcutctl mograph`) and these renders then agree.
//
// Structure still comes from scale, weight, spacing and luminance. Colours are ROLES:
// BRAND fills a block behind text; ACCENT marks one element per shot, never a title or a
// large fill. Which role leads in a given video is the style's call (profile `styles`).

import profile from './profile.json';

const palette = profile.tokens.scene.palette;

export const BG = palette.ink;
export const TEXT = palette.text;
export const TEXT_2 = palette.muted;
export const PAPER = palette.paper;
export const BRAND = profile.tokens.color.brand ?? palette.brand;
export const ACCENT = profile.tokens.color.accent ?? palette.accent;

/** `hex` moved `amount` (0–1) of the way to `toward`: surfaces and hairlines from the roles. */
export function mix(hex: string, toward: string, amount: number): string {
	const rgb = (h: string) => [0, 2, 4].map((i) => parseInt(h.replace('#', '').slice(i, i + 2), 16));
	const [a, b] = [rgb(hex), rgb(toward)];
	return `rgb(${a.map((v, i) => Math.round(v + (b[i] - v) * amount)).join(',')})`;
}
export const SURFACE = mix(BG, TEXT, 0.06);
export const HAIRLINE = mix(BG, TEXT, 0.1);

// The profile's family (loaded by fonts.ts) with the system sans behind it.
export const SANS = `"${profile.tokens.font.family}", -apple-system, "SF Pro Text", "Helvetica Neue", Arial, sans-serif`;
export const MONO = `"${profile.tokens.scene.mono?.family ?? 'JetBrains Mono'}", "SF Mono", ui-monospace, Menlo, monospace`;
export const WEIGHT = {display: profile.tokens.font.display, body: profile.tokens.font.body};

// Type scale at a 1080 short edge, for a drawn piece that sits beside the profile's supers.
// Keep the order and rough ratios; rewrite copy that exceeds `max` instead of shrinking.
export const TYPE = {
	title: {size: 96, weight: WEIGHT.display, max: 32},
	subtitle: {size: 60, weight: WEIGHT.body, max: 64},
	name: {size: 48, weight: WEIGHT.body, max: 28},
	detail: {size: 30, weight: WEIGHT.body, max: 40},
	label: {size: 24, weight: WEIGHT.body, max: 16},
} as const;

// Spacing in multiples of 8. Margin 64, gap 40, 16 label→value, 24 between
// lines in a block, 40 between blocks.
export const MARGIN = 64;
export const GAP = 40;
// Framed media panels only. Never round full-frame media.
export const RADIUS = profile.tokens.radius?.box ?? 24;
