// The profile's own font files, loaded at render time so a still on this machine and an
// export on another are the same picture. `kit/scripts/sync-profile.sh` copies them into
// public/fonts/. Needs `@remotion/fonts` at the same version as `remotion`:
//
//   npm i @remotion/fonts@$(node -p "require('remotion/package.json').version")
//
// Import this file once (Root.tsx) and use SANS / MONO from theme.ts.

import {loadFont} from '@remotion/fonts';
import {staticFile} from 'remotion';
import profile from './profile.json';

type Face = {family: string; files?: Record<string, string[]>};

function load(face: Face | undefined) {
	if (!face) return;
	for (const [weight, files] of Object.entries(face.files ?? {})) {
		for (const file of files) {
			loadFont({family: face.family, url: staticFile(`fonts/${file}`), weight, format: 'woff2'});
		}
	}
}

load(profile.tokens.font as Face);
load(profile.tokens.scene.mono as Face);

export const SANS_FAMILY = profile.tokens.font.family;
