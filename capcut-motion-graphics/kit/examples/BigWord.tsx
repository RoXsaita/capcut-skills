import React from 'react';
import {AbsoluteFill, useCurrentFrame, useVideoConfig} from 'remotion';
import {PULL, STAND} from '../easing';
import {frames} from '../timing';
import {progress, run} from '../motion';
import {BG, TEXT} from '../theme';

// A word too big for the frame, written on the move. Each capital is struck
// when the writing reaches its own place on the line — the rhythm is the
// type's measure, not a count — and stands up off the baseline over 180ms,
// smeared while it rises and sharp the frame it lands. The camera is pulled
// left through the whole line and does not stop: the word is read on the move
// and its end is carried off the left edge. The shot leaves on its own pull.
//
// Ported from the "Analyzing" shot of the Diffusion Studio launch video (MIT).
// Needs a condensed display face; `ANTON` from ../fonts is the reference.

// Anton's advances per 2048 units of em, for the letters the reference used.
// Anything else is set at the average — the pan's end will be a few pixels
// off, which the run-off hides. Add letters you use often.
const UPM = 2048;
const ADV: Record<string, number> = {A: 994, N: 1020, L: 814, Y: 914, Z: 840, I: 464, G: 993};
const ADV_DEFAULT = 900;
const SPACE = 480; // the word space the beam stands in
// Anton sets USE_TYPO_METRICS; the line box is built from these
const ASC = 2409 / UPM;
const DESC = 674 / UPM;
const CAP = 1760 / UPM;

const K0 = 0.12; // the height a letter arrives at, as a share of its struck height
const WRITE_MS = 900; // first letter struck to last
const GROW_MS = 180; // struck at K0, then standing up
const HELD_MS = 300; // the pull runs on after the last letter lands
const BLUR_FRAC = 0.01; // px of smear at the strike, per px of font size

export const bigWordFrames = (fps: number): number => frames(WRITE_MS + GROW_MS + HELD_MS, fps);

export const BigWord: React.FC<{
	word: string;
	fontFamily: string;
	at?: number; // frame of the first strike
	capFrac?: number; // cap height as a share of the frame height
	color?: string;
	transparent?: boolean;
}> = ({word, fontFamily, at = 0, capFrac = 0.58, color = TEXT, transparent = false}) => {
	const frame = useCurrentFrame();
	const {fps, width: W, height: H} = useVideoConfig();

	const letters = word.toUpperCase().split('');
	const FS = (capFrac * H) / CAP;
	const LH = Math.round((ASC + DESC) * FS);
	const advances = letters.map((c) => ((ADV[c] ?? ADV_DEFAULT) / UPM) * FS);
	const lefts = advances.reduce<number[]>((xs, adv) => [...xs, xs[xs.length - 1] + adv], [0]);
	const PAD = Math.round((SPACE / UPM) * FS);

	// the beam stands on the frame's centre; the line hangs off it
	const LINE_X = W / 2;
	const HALF_LEAD = (LH - (ASC + DESC) * FS) / 2;
	const CAP_MID = HALF_LEAD + (ASC - CAP / 2) * FS;
	const BASELINE = HALF_LEAD + ASC * FS;
	const LINE_Y = Math.round(H / 2 - CAP_MID);

	// a letter is struck when the writing reaches it
	const lastLeft = lefts[lefts.length - 2] || 1;
	const strike = lefts.slice(0, -1).map((x) => Math.round((WRITE_MS * x) / lastLeft));

	// the whole of it, beam included, carried off the left edge
	const extent = PAD + lefts[lefts.length - 1];
	const PAN_MS = WRITE_MS + GROW_MS + HELD_MS;
	const panX = run(frame, at, frames(PAN_MS, fps), PULL, 0, -(LINE_X + extent));

	const beamH = FS * CAP * 0.9;
	const blurAt = (k: number) => (FS * BLUR_FRAC * (1 - (k - K0) / (1 - K0))) / k;

	return (
		<AbsoluteFill style={{backgroundColor: transparent ? 'transparent' : BG, overflow: 'hidden'}}>
			<AbsoluteFill style={{transform: `translateX(${panX.toFixed(2)}px)`}}>
				{/* the I-beam, drawn: a stem and two serifs */}
				<div
					style={{
						position: 'absolute',
						left: LINE_X - FS * 0.06,
						top: H / 2 - beamH / 2,
						width: FS * 0.12,
						height: beamH,
					}}
				>
					<div style={{position: 'absolute', left: '50%', top: 0, width: FS * 0.022, height: '100%', marginLeft: -FS * 0.011, background: color}} />
					<div style={{position: 'absolute', left: 0, top: 0, width: '100%', height: FS * 0.022, background: color}} />
					<div style={{position: 'absolute', left: 0, bottom: 0, width: '100%', height: FS * 0.022, background: color}} />
				</div>

				{/* kerning off and each letter its own box, so the browser's advances match the table */}
				<div
					style={{
						position: 'absolute',
						left: LINE_X + PAD,
						top: LINE_Y,
						height: LH,
						fontFamily,
						fontWeight: 400,
						fontSize: FS,
						lineHeight: `${LH}px`,
						letterSpacing: 0,
						fontKerning: 'none',
						fontVariantLigatures: 'none',
						whiteSpace: 'pre',
						color,
						WebkitFontSmoothing: 'antialiased',
					}}
				>
					{letters.map((c, i) => {
						const s = at + frames(strike[i], fps);
						const on = frame >= s;
						const k = K0 + (1 - K0) * progress(frame, s, frames(GROW_MS, fps), STAND);
						return (
							<span
								key={i}
								style={{
									display: 'inline-block',
									transformOrigin: `0px ${BASELINE.toFixed(2)}px`,
									transform: `scale(${k.toFixed(4)})`,
									filter: k < 1 ? `blur(${blurAt(k).toFixed(2)}px)` : 'none',
									visibility: on ? 'visible' : 'hidden',
								}}
							>
								{c}
							</span>
						);
					})}
				</div>
			</AbsoluteFill>
		</AbsoluteFill>
	);
};
