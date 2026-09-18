// Fonts loaded at render time so a still on this machine and an export on
// another are the same picture. Needs `@remotion/google-fonts` at the same
// version as `remotion`:
//
//   npm i @remotion/google-fonts@$(node -p "require('remotion/package.json').version")
//
// Import this file once (Root.tsx) and use the exported family names. If the
// package is not installed, delete this file and the stacks in theme.ts fall
// back to the system faces.

import {loadFont as loadInter} from '@remotion/google-fonts/Inter';
import {loadFont as loadAnton} from '@remotion/google-fonts/Anton';

// the house sans, three weights: body 400, name 500, title 600
export const INTER = loadInter('normal', {weights: ['400', '500', '600'], subsets: ['latin']}).fontFamily;

// the display face for a word too big for the frame — one weight, capitals only
export const ANTON = loadAnton('normal', {weights: ['400'], subsets: ['latin']}).fontFamily;
