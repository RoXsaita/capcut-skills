import React from 'react';
import {AbsoluteFill, useCurrentFrame, useVideoConfig} from 'remotion';
import {Stage} from '../Stage';
import {Typed} from '../Typed';
import {ENTER, GLIDE, SETTLE, STAND} from '../easing';
import {
	BLINK_MS,
	CHAR_MS,
	DOT_MS,
	IN_MOVE_MS,
	IN_OPACITY_MS,
	LEAD_MS,
	RISE_PX,
	frames,
} from '../timing';
import {progress, run, track, type Key} from '../motion';
import {MARGIN, MONO, TEXT, TEXT_2} from '../theme';

// A terminal shot with no terminal. No window chrome, no card, no glow, no
// grid: a column of type on black, a caret, and one camera move — the block
// climbs so the live line stays on its anchor, like a real scrollback.
//
// Compare with the "before" (a bordered card with traffic lights, a coloured
// bloom, linear fades and a constant-rate typewriter). Same content, same
// duration; the difference is entirely in what was left out and how the
// remaining moves are timed.
//
// 1080×960 at 30fps — the top half of the house split-screen.

export const TERMINAL_W = 1080;
export const TERMINAL_H = 960;

const FS = 40;
const LH = 64;
// the live line sits here; copy is anchored low, and the block climbs to keep it
const ANCHOR_Y = 560;
// the subject's own colour — capcutctl's indigo seam bar — on exactly one element: the caret
const ACCENT = '#302FFF';

const DARK_MS = 160; // the frame is empty before the caret first lights
const PREROLL_BLINKS = 1; // blinks before the first key
const WORK_MS = 400; // the machine is seen to work before it answers
const HOLD_MS = 300; // an answer is read before the next command
const DOTS = 4; // "", ".", "..", "..."

const PAIRS = [
	{cmd: 'capcutctl cut face.mp4 --keep 0,2-9', ok: '22 scenes · every seam on an onset'},
	{cmd: 'capcutctl layout auto', ok: 'split-screen × 18 · full face × 2'},
	{cmd: 'capcutctl polish --motivated', ok: 'transition and sound on every cut'},
];
// At 40px mono a line holds ~40 glyphs before it meets the right margin.
// Rewrite copy that runs over; never shrink the type to fit it.
const MAX_GLYPHS = 40;
for (const p of PAIRS) {
	if (p.cmd.length > MAX_GLYPHS || p.ok.length > MAX_GLYPHS) {
		throw new Error(`Terminal: copy over ${MAX_GLYPHS} glyphs — rewrite it: ${p.cmd} / ${p.ok}`);
	}
}

type Row = {kind: 'cmd' | 'ok'; at: number; text: string; workFrom: number};

// Everything below falls out of the row table: the timeline is a schedule,
// not a set of hand-placed frames.
const schedule = (): Row[] => {
	const rows: Row[] = [];
	let t = DARK_MS + 2 * BLINK_MS * PREROLL_BLINKS;
	for (const p of PAIRS) {
		const typed = t + p.cmd.length * CHAR_MS;
		rows.push({kind: 'cmd', at: t, text: p.cmd, workFrom: t});
		rows.push({kind: 'ok', at: typed + WORK_MS, text: p.ok, workFrom: typed});
		t = typed + WORK_MS + HOLD_MS;
	}
	return rows;
};
export const ROWS = schedule();
// the last answer is read for 360ms, then the shot is cut on the next beat
export const TERMINAL_FRAMES = frames(ROWS[ROWS.length - 1].at + 360);

// The block's vertical position: hold, then a GLIDE of one line height over
// IN_MOVE_MS each time a new slot opens (a command starts, or the machine
// starts working on the line below).
const climbKeys = (fps: number): Key[] => {
	const keys: Key[] = [];
	ROWS.forEach((row, i) => {
		const y = ANCHOR_Y - i * LH;
		const at = frames(row.workFrom, fps);
		if (i > 0) keys.push({at, value: ANCHOR_Y - (i - 1) * LH});
		keys.push({at: at + frames(IN_MOVE_MS, fps), value: y, ease: GLIDE});
	});
	return keys;
};

const Gutter: React.FC<{glyph: string; at: number; color: string}> = ({glyph, at, color}) => {
	const frame = useCurrentFrame();
	const {fps} = useVideoConfig();
	const lead = at - frames(LEAD_MS, fps);
	const o = progress(frame, lead, frames(200, fps), STAND);
	const y = run(frame, lead, frames(200, fps), STAND, RISE_PX, 0);
	return (
		<span
			style={{
				display: 'inline-block',
				width: 44,
				color,
				opacity: o,
				transform: `translateY(${y.toFixed(2)}px)`,
			}}
		>
			{glyph}
		</span>
	);
};

const Working: React.FC<{from: number; until: number}> = ({from, until}) => {
	const frame = useCurrentFrame();
	const {fps} = useVideoConfig();
	if (frame < from || frame >= until) return null;
	const n = Math.floor(((frame - from) * 1000) / fps / DOT_MS) % DOTS;
	const o = progress(frame, from, frames(IN_OPACITY_MS, fps), ENTER);
	return (
		<span style={{color: TEXT_2, opacity: o}}>
			{'working'}
			{'.'.repeat(n)}
		</span>
	);
};

const Line: React.FC<{row: Row; index: number}> = ({row, index}) => {
	const frame = useCurrentFrame();
	const {fps} = useVideoConfig();
	const at = frames(row.at, fps);
	const visibleFrom = frames(row.workFrom, fps) - frames(LEAD_MS, fps);
	if (frame < visibleFrom) return null;

	const body =
		row.kind === 'cmd' ? (
			<Typed text={row.text} at={at} caretColor={ACCENT} style={{color: TEXT}} />
		) : (
			<>
				<Working from={frames(row.workFrom, fps)} until={at} />
				{frame >= at ? (
					<span
						style={{
							color: TEXT_2,
							// opacity resolves first, so the line is readable before it settles
							opacity: progress(frame, at, frames(IN_OPACITY_MS, fps), ENTER),
							display: 'inline-block',
							transform: `translateY(${run(frame, at, frames(IN_MOVE_MS, fps), SETTLE, RISE_PX, 0).toFixed(2)}px)`,
						}}
					>
						{row.text}
					</span>
				) : null}
			</>
		);

	return (
		<div
			style={{
				position: 'absolute',
				left: MARGIN,
				top: index * LH,
				height: LH,
				lineHeight: `${LH}px`,
				fontFamily: MONO,
				fontSize: FS,
				fontWeight: 500,
				whiteSpace: 'pre',
				color: TEXT,
			}}
		>
			{row.kind === 'cmd' ? (
				<Gutter glyph="❯" at={at} color={TEXT_2} />
			) : frame >= at ? (
				<Gutter glyph="✓" at={at} color={TEXT} />
			) : (
				<span style={{display: 'inline-block', width: 44}} />
			)}
			{body}
		</div>
	);
};

// The caret before the first key: the frame is dark, then one blink, then typing.
const Preroll: React.FC = () => {
	const frame = useCurrentFrame();
	const {fps} = useVideoConfig();
	const from = frames(DARK_MS, fps);
	const until = frames(ROWS[0].at, fps);
	if (frame < from || frame >= until) return null;
	const on = Math.floor(((frame - from) * 1000) / fps / BLINK_MS) % 2 === 0;
	return (
		<div
			style={{
				position: 'absolute',
				left: MARGIN + 44,
				top: 0,
				height: LH,
				display: 'flex',
				alignItems: 'center',
			}}
		>
			<span
				style={{
					display: 'inline-block',
					width: FS * 0.55,
					height: FS,
					background: ACCENT,
					opacity: on ? 1 : 0,
				}}
			/>
		</div>
	);
};

export const Terminal: React.FC = () => {
	const frame = useCurrentFrame();
	const {fps} = useVideoConfig();
	const y = track(frame, climbKeys(fps));
	return (
		<Stage camera={`translateY(${y.toFixed(2)}px)`} origin="0 0">
			<AbsoluteFill>
				<Preroll />
				{ROWS.map((row, i) => (
					<Line key={i} row={row} index={i} />
				))}
			</AbsoluteFill>
		</Stage>
	);
};
