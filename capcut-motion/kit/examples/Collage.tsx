import React from 'react';
import {AbsoluteFill, Img, useCurrentFrame, useVideoConfig} from 'remotion';
import {ENTER, LAND, SETTLE, SMOOTH, WIND} from '../easing';
import {frames} from '../timing';
import {centered, progress, run, span} from '../motion';
import {BG, SANS, TEXT, TEXT_2} from '../theme';

// A pile of frames at the head of a ring, unwinding along it around a line of
// type. One number, `p`, runs the whole shot on one curve (WIND); every
// position, size and stacking order is read off it. Distance `m` is a second
// scalar, deliberately separate: it scales sizes as well as the ring, the one
// thing the winding must not do.
//
// Ported from the "Watching footage" shot of the Diffusion Studio launch video
// (MIT). Geometry is stated for a 1080-high frame and scaled from there, so it
// composes at 1920×1080 and at the house 1080×960 alike.

const TAU = Math.PI * 2;

// the ring: an ellipse, because the frame is one; leaned over 9° so it reads
// as lying in space rather than drawn on the glass
const RX0 = 700;
const RY_REACH0 = 358; // how near the top and bottom the ring comes, square
const TILT = (-9 * Math.PI) / 180;
const COS_T = Math.cos(TILT);
const SIN_T = Math.sin(TILT);
const START = Math.PI / 2; // the pile stands at the bottom: the near point
const DEPTH = 0.15; // a frame nearer the eye is bigger

// the frames
const BASE_W0 = 340;
const MAT0 = 6; // a stroke that grew with its frame would say "further away"
const S_LO = 0.66;
const S_HI = 1.24;
const SCATTER = 0.09; // rad off its share of the ring
const PILE_X0 = 90;
const PILE_Y0 = 50;
const PILE_TILT = 11; // deg, spent on the opening — nothing on the ring is off square
const LAG_MAX_MS = 140; // a big frame sets off later than a small one

// the winding
const RUN_MS = 2900;
const TURN = (200 * Math.PI) / 180; // what the ring turns through, first frame to last
const P_SPREAD = 0.38; // how much of the curve the unwinding is given
const P_CLOSE = 0.45; // where the drawing-in starts
const RUSH_R = 0.66; // what is left of the radius at the cut
const FAR = 0.62; // the whole arrangement comes in out of the distance…
const APPROACH_MS = 50; // …quicker than the blur it comes in under
const BLOOM_O_MS = 260; // a frame blending in — opacity only
const BLOOM_B_MS = 240; // the picture resolving — the node's blur
const BLUR_PX = 24;
const OUT_O_MS = 90; // it leaves the way it came, in a third of the time
const OUT_B_MS = 130;

// the line
const FS_LABEL0 = 48;
const LABEL_FROM = 1.14; // arrives at a size and settles to its own
const LABEL_AT_MS = 640; // while the ring is still coming apart
const LABEL_IN_MS = 260;
const SHRINK_MS = 760;
const SHIMMER_MS = 900; // one pass of the band, edge to edge
const DOT_MS = 280;
const DOTS = 4;

export const collageFrames = (fps: number): number => frames(RUN_MS, fps);

type Seed = {d: number; s: number; r: number; rate: number; tilt0: number; jx: number; jy: number};

const seeds = (n: number): Seed[] => {
	const raw = Array.from({length: n}, (_, i) => ({
		// each frame travels one share further than the last, the last the whole way round,
		// so the pile pays out into the ring rather than bursting onto it
		d: ((i + 1) / n) * TAU + span(i, 1, -SCATTER, SCATTER),
		s: span(i, 3, S_LO, S_HI),
		r: span(i, 2, 0.94, 1.06),
		// every frame turns the same way, but not at quite the same rate: the ring breathes
		rate: span(i, 4, 0.95, 1.05),
		tilt0: span(i, 7, -PILE_TILT, PILE_TILT),
		jx: span(i, 5, -PILE_X0, PILE_X0),
		jy: span(i, 6, -PILE_Y0, PILE_Y0),
	}));
	// ten scatters do not average to nothing; the heap sits on the ring
	const jx = centered(raw.map((f) => f.jx));
	const jy = centered(raw.map((f) => f.jy));
	return raw.map((f, i) => ({...f, jx: jx[i], jy: jy[i]}));
};

const spreadAt = (p: number) => SMOOTH(Math.min(1, p / P_SPREAD));
const closeAt = (p: number) => {
	const u = Math.max(0, (p - P_CLOSE) / (1 - P_CLOSE));
	return 1 - (1 - RUSH_R) * u * u;
};

export const Collage: React.FC<{
	covers: string[]; // absolute URLs or staticFile() paths, one per frame
	aspect?: number; // h / w of a cover; 9/16 for landscape stills, 16/9 for portrait
	label?: string;
	fontFamily?: string;
	at?: number; // frame the shot starts
	end?: number; // frame it is cut; defaults to at + RUN
	transparent?: boolean;
}> = ({covers, aspect = 9 / 16, label = 'Watching footage', fontFamily = SANS, at = 0, end, transparent = false}) => {
	const frame = useCurrentFrame();
	const {fps, width: W, height: H} = useVideoConfig();
	const u = H / 1080; // the geometry is stated at 1080 high

	const n = covers.length;
	const F = seeds(n);
	const lags = F.map((f) => Math.round((LAG_MAX_MS * (f.s - S_LO)) / (S_HI - S_LO)));

	// portrait covers are narrower for the same area on the ring…
	const BASE_W = BASE_W0 * u * Math.sqrt((9 / 16) / aspect);
	// the ring runs just inside the picture's sides at the widest a frame gets —
	// stated for 16:9 and clamped for a narrower frame (the 1080×960 slot)
	const halfW = (BASE_W * S_HI * (1 + DEPTH)) / 2;
	const RX = Math.min(RX0 * u, W / 2 - halfW - 64 * u);
	// …and taller, so the ring's vertical reach gives back the extra half-height:
	// the biggest frame at the near point stays inside the picture
	const halfH = (bw: number, a: number) => (bw * a * S_HI * (1 + DEPTH)) / 2;
	const RY_REACH = RY_REACH0 * u + halfH(BASE_W0 * u, 9 / 16) - halfH(BASE_W, aspect);
	const RY = Math.round(Math.sqrt(Math.max(1, RY_REACH ** 2 - (RX * SIN_T) ** 2)));
	const MAT = MAT0 * u;
	const CX = W / 2;
	const CY = H / 2;

	const cut = end ?? at + collageFrames(fps);
	const t = frame - at;
	const p = progress(frame, at, frames(RUN_MS, fps), WIND);
	const m = run(frame, at, frames(APPROACH_MS, fps), SETTLE, FAR, 1);

	// the node's own focus: one picture resolving, not ten and a line each
	const blurIn = BLUR_PX * (1 - progress(frame, at, frames(BLOOM_B_MS, fps), ENTER));
	const blurOut = BLUR_PX * progress(frame, cut - frames(OUT_B_MS, fps), frames(OUT_B_MS, fps), ENTER);
	const fadeOut = 1 - progress(frame, cut - frames(OUT_O_MS, fps), frames(OUT_O_MS, fps), ENTER);
	const blur = Math.max(blurIn, blurOut);

	const k = spreadAt(p);
	const z = closeAt(p);

	const labelAt = at + frames(LABEL_AT_MS, fps);
	const labelO = progress(frame, labelAt, frames(LABEL_IN_MS, fps), ENTER);
	const labelS = run(frame, labelAt, frames(SHRINK_MS, fps), LAND, LABEL_FROM, 1);
	const ms = (t * 1000) / fps;
	const lit = (1 - ((ms / SHIMMER_MS) % 1)) * 100;
	const dots = '.'.repeat(Math.max(0, Math.floor(ms / DOT_MS)) % DOTS);
	const FS_LABEL = FS_LABEL0 * u;

	if (frame < at || frame >= cut) return null;

	return (
		<AbsoluteFill style={{backgroundColor: transparent ? 'transparent' : BG, overflow: 'hidden'}}>
			<AbsoluteFill style={{filter: blur > 0.05 ? `blur(${blur.toFixed(2)}px)` : 'none', opacity: fadeOut}}>
				{/* the line: the type is the window a band of light is seen through */}
				<div
					style={{
						position: 'absolute',
						left: CX,
						top: CY - FS_LABEL * 0.6,
						height: FS_LABEL * 1.2,
						lineHeight: `${FS_LABEL * 1.2}px`,
						fontFamily,
						fontSize: FS_LABEL,
						fontWeight: 500,
						whiteSpace: 'pre',
						zIndex: 1,
						backgroundImage: `linear-gradient(100deg, ${TEXT_2} 0%, ${TEXT_2} 42%, ${TEXT} 50%, ${TEXT_2} 58%, ${TEXT_2} 100%)`,
						backgroundSize: '300% 100%',
						backgroundPosition: `${lit.toFixed(2)}% 0`,
						backgroundClip: 'text',
						WebkitBackgroundClip: 'text',
						color: 'transparent',
						opacity: labelO,
						transform: `translateX(-50%) scale(${labelS.toFixed(4)})`,
						WebkitFontSmoothing: 'antialiased',
					}}
				>
					{label}
					{dots}
				</div>

				{covers.map((src, i) => {
					const f = F[i];
					const ang = START + f.d * k + TURN * f.rate * p;
					const near = Math.sin(ang); // +1 is the bottom of the ring, the front
					const w = BASE_W * f.s * (1 + DEPTH * near) * m;
					const h = w * aspect;
					// found on the ring's own axes, then laid over at TILT
					const ex = RX * f.r * z * Math.cos(ang);
					const ey = RY * f.r * z * near;
					const x = (ex * COS_T - ey * SIN_T + f.jx * u * (1 - k)) * m;
					const y = (ex * SIN_T + ey * COS_T + f.jy * u * (1 - k)) * m;
					const deg = f.tilt0 * (1 - k);
					const over = 3000 + Math.round(near * 100) * 20 + i;
					// each blends up on its own, one just behind the next: a pile assembling
					const o = progress(frame, at + frames(lags[i], fps), frames(BLOOM_O_MS, fps), ENTER);
					return (
						<div
							key={i}
							style={{
								position: 'absolute',
								left: CX + x - w / 2,
								top: CY + y - h / 2,
								width: w,
								height: h,
								overflow: 'hidden',
								boxShadow: `0 0 0 ${(MAT * m).toFixed(2)}px ${TEXT}`,
								opacity: o,
								transform: `rotate(${deg.toFixed(2)}deg)`,
								zIndex: over,
							}}
						>
							<Img src={src} style={{display: 'block', width: '100%', height: '100%', objectFit: 'cover'}} />
						</div>
					);
				})}
			</AbsoluteFill>
		</AbsoluteFill>
	);
};
