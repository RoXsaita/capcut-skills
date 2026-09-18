# kit — the Remotion motion kit

Copy this directory into a Remotion project as `src/motion/` and import from it. It depends on
`remotion` and `react` only.

| File | What it is |
|---|---|
| `theme.ts` | The achromatic palette, the type scale with copy limits, spacing constants |
| `easing.ts` | Every curve, named for its intent, with the sentence that justifies it |
| `timing.ts` | The house beat in integer milliseconds, `frames()` / `ms()`, the pixel-snapping check |
| `motion.ts` | `progress`, `run`, `track` (keyframes), `handOver`, `staggerDelay`, `seed`/`span` (deterministic scatter), `cycle` |
| `Stage.tsx` | A plain stage with an optional camera transform and a `transparent` mode for alpha exports |
| `Typed.tsx` | Text typed on the WRITE curve with a blinking caret |
| `examples/Terminal.tsx` | A complete shot built on the kit: the reference for what "on the rules" looks like |
| `scripts/stills.sh` | Still-render QA gate |
| `scripts/render-alpha.sh` | ProRes 4444 alpha render + the `capcutctl add --generated` line |

Register the example in your `Root.tsx`:

```tsx
import {Terminal, TERMINAL_FRAMES, TERMINAL_W, TERMINAL_H} from './motion/examples/Terminal';

<Composition id="Terminal" component={Terminal} durationInFrames={TERMINAL_FRAMES}
  fps={30} width={TERMINAL_W} height={TERMINAL_H} />
```

The curves and the timing constants are adapted from the Diffusion Studio motion guide (MPL-2.0)
and its open-source launch video (MIT). Add a curve only with the sentence that says what it is for.
