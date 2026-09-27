# kit — the Remotion motion kit

Copy this directory into a Remotion project as `src/motion/`, then bring the creator's profile in:

```bash
kit/scripts/sync-profile.sh PROJECT_DIR      # writes src/motion/profile.json, copies the fonts to public/fonts/
```

The kit has **no brand of its own**. Colours, font and weights come from that `profile.json` — the
CLI's shipped defaults with the creator's `~/.config/capcutctl/profile.json` merged over it — so a
Remotion render and a `capcutctl mograph` graphic in the same video agree. Re-sync when the profile
changes. It depends on `remotion`, `react` and `@remotion/fonts`.

| File | What it is |
|---|---|
| `theme.ts` | The profile's colour roles (`BG`, `TEXT`, `TEXT_2`, `BRAND`, `ACCENT`, `PAPER`), `SANS`/`MONO`, the type scale with copy limits, spacing |
| `easing.ts` | Every curve, named for its intent, with the sentence that justifies it |
| `timing.ts` | The house beat in integer milliseconds, `frames()` / `ms()`, the pixel-snapping check |
| `motion.ts` | `progress`, `run`, `track` (keyframes), `handOver`, `staggerDelay`, `seed`/`span` (deterministic scatter), `cycle` |
| `fonts.ts` | Loads the profile's font files from `public/fonts/` |
| `Stage.tsx` | A plain stage with an optional camera transform and a `transparent` mode for alpha exports |
| `Typed.tsx` | Text typed on the WRITE curve with a blinking caret |
| `examples/BigWord.tsx` | One capital word wider than the frame, struck letter by letter, pulled off left |
| `examples/Collage.tsx` | 8–12 real stills unwinding round a shimmering label; clamps to the slot |
| `examples/Terminal.tsx` | A process seen running: typed commands, "working…", answers, the block climbing |
| `scripts/sync-profile.sh` | The profile and its fonts into the Remotion project |
| `scripts/stills.sh` | Still-render QA gate |
| `scripts/render-alpha.sh` | ProRes 4444 alpha render + the `capcutctl add --generated` line |

Every example takes its size from the composition, so register each at the slot you need — the
house top half (1080×960) or full frame (1080×1920):

```tsx
import {staticFile} from 'remotion';
import {Terminal, TERMINAL_FRAMES} from './motion/examples/Terminal';
import {BigWord, bigWordFrames} from './motion/examples/BigWord';
import {Collage, collageFrames} from './motion/examples/Collage';
import './motion/fonts';
import {SANS} from './motion/theme';

// stills of the real material go in public/covers/01.png … 10.png
const COVERS = Array.from({length: 10}, (_, i) => staticFile(`covers/${String(i + 1).padStart(2, '0')}.png`));

<Composition id="Terminal" component={Terminal} durationInFrames={TERMINAL_FRAMES} fps={30} width={1080} height={960} />
<Composition id="Analyzing" component={() => <BigWord word="ANALYZING" fontFamily="Anton" />}
  durationInFrames={bigWordFrames(30)} fps={30} width={1080} height={1920} />
<Composition id="Watching" component={() => <Collage covers={COVERS} aspect={16 / 9} fontFamily={SANS} />}
  durationInFrames={collageFrames(30)} fps={30} width={1080} height={960} />
```

`aspect` is a cover's height over its width: `9/16` for landscape stills, `16/9` for frames
pulled from a 9:16 recording. Pull them with `ffmpeg -ss T -i FILE -frames:v 1 -vf scale=640:-2`.

Fonts: `npm i @remotion/fonts@<your remotion version>`. Big Word is the one exception to the
profile's family: its pan is measured against Anton's Latin advances, so it needs Anton installed
and Latin capitals. Skip it when the brand rules say one family, or for Arabic copy.

The curves and the timing constants are adapted from the Diffusion Studio motion guide (MPL-2.0)
and its open-source launch video (MIT). Add a curve only with the sentence that says what it is for.
