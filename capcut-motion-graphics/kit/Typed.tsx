import React from 'react';
import {useCurrentFrame, useVideoConfig} from 'remotion';
import {WRITE, type Ease} from './easing';
import {BLINK_MS, CHAR_MS, frames} from './timing';
import {progress} from './motion';

// Text typed by a hand, not a metronome. The reveal runs on WRITE — leaving
// rest and gathering, quickest at the last key — so the cadence accelerates
// the way real typing does. The caret blinks on a 120ms half period from
// `at` and holds for `caretHoldMs` after the last key.
export const Typed: React.FC<{
	text: string;
	at: number; // frame the first key lands
	charMs?: number;
	ease?: Ease;
	caret?: boolean;
	caretHoldMs?: number;
	caretColor?: string;
	style?: React.CSSProperties;
}> = ({
	text,
	at,
	charMs = CHAR_MS,
	ease = WRITE,
	caret = true,
	caretHoldMs = 600,
	caretColor,
	style,
}) => {
	const frame = useCurrentFrame();
	const {fps} = useVideoConfig();
	const dur = frames(text.length * charMs, fps);
	const p = progress(frame, at, dur, ease);
	const shown = Math.min(text.length, Math.floor(p * text.length + 1e-6));
	const done = frame >= at + dur;
	const caretOn =
		caret &&
		frame >= at &&
		frame < at + dur + frames(caretHoldMs, fps) &&
		(done ? true : Math.floor(((frame - at) * 1000) / fps / BLINK_MS) % 2 === 0);

	return (
		<span style={{whiteSpace: 'pre', ...style}}>
			{text.slice(0, shown)}
			<span
				style={{
					display: 'inline-block',
					width: '0.55em',
					height: '1em',
					verticalAlign: '-0.15em',
					marginLeft: '0.06em',
					background: caretColor ?? 'currentColor',
					opacity: caretOn ? 1 : 0,
				}}
			/>
		</span>
	);
};

// Frames the whole line takes to type, for laying out what follows it.
export const typedDuration = (text: string, fps: number, charMs = CHAR_MS): number =>
	frames(text.length * charMs, fps);
