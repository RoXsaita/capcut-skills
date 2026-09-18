import React from 'react';
import {AbsoluteFill} from 'remotion';
import {BG} from './theme';

// A plain stage. No glow, no grid, no gradient, no vignette: the frame is the
// subject and the type. `transparent` renders with no background at all for
// an alpha export that will be laid over footage in CapCut.
//
// `camera` is one CSS transform string for the whole picture (see
// `track()` in motion.ts for the values). Every shot should have one — a frame
// that only fades in, sits, and fades out reads as a slide.
export const Stage: React.FC<{
	children: React.ReactNode;
	transparent?: boolean;
	camera?: string;
	origin?: string;
}> = ({children, transparent = false, camera, origin = '50% 50%'}) => (
	<AbsoluteFill style={{backgroundColor: transparent ? 'transparent' : BG, overflow: 'hidden'}}>
		<AbsoluteFill style={{transform: camera, transformOrigin: origin}}>{children}</AbsoluteFill>
	</AbsoluteFill>
);
