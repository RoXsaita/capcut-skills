# Writing, forking and promoting a scene

Scenes live in the CLI repository at `mograph/scenes/<id>.js` and run on
`mograph/scenes/runtime.js`. The authoritative version of this page is
[mograph/scenes/README.md in capcut-editor-cli](https://github.com/RoXsaita/capcut-editor-cli/blob/main/mograph/scenes/README.md).
This copy is the part an agent needs mid-edit.

## Decide before you write

1. **The catalog has it.** Use params only.
2. **A param would do it.** Add the param to that scene. Update its header's `params:` line
   and its entry in `test/mograph-scenes.test.mjs`.
3. **A new job, or a clearly different motion idea.** Fork the closest scene:

   ```bash
   cp mograph/scenes/word-slam.js mograph/scenes/my-idea.js   # then set id: 'my-idea'
   ```

   Keep the structure and rewrite only `draw` (and `setup` and `cues` as needed).
4. **Never:** the same idea in a new colour (colour is a param), a scene with this video's copy
   baked in (copy is a param), or a one-off outside the library.

## Anatomy

```js
/*
 * my-idea — one sentence: what the viewer sees, in order.
 * params: { text: 1–3 words, to?: palette role (default paper) }
 * beats: 4 (2.0 s)
 * handoff: ink → params.to
 * use: when in a video this is the right scene, and how often.
 *
 * Timing: what happens on each beat, with the eases.
 */
SCENE.define({
  id: 'my-idea',
  beats: () => 4,
  handoff: p => ({ in: 'ink', out: p.to || 'paper' }),
  impacts: () => [[0, 0.8]],
  cues: () => [{ at: 0, kind: 'impact' }],
  setup(p, K) { return {}; },
  draw(ctx, t, p, s, K) { /* paint time t */ },
});
```

## The kit (`K`)

| Need | Use |
|---|---|
| Canvas and tempo | `K.W K.H K.CX K.CY K.FPS K.BPM K.BEAT K.b(n) K.duration` |
| Timing | `K.prog(t, a, b)`, `K.E.outExpo / inOutCubic / outBack / inExpo…`, `K.spring(t, freq, damp)`, `K.wobble(dt)` |
| Randomness | `K.hash(a, b, c)`, `K.rand(seed)`, `K.noise1 / noise2 / fbm`; never `Math.random` |
| Colour | `K.color('brand')`, `K.rgba('ink', 0.3)`, `K.mix('hot', 'accent', p)`: roles from `tokens.scene.palette` |
| Type | `K.font(700, 200)` for the profile face and `K.font(400, 20, 'mono')` for mono. `K.words(ctx, text)` returns `{ items, width, rtl }` and `K.dir(text)` gives the direction |
| Readable text | `K.text(ctx, str, x, y, { align })` and `K.mark(x, y, w, h)` record the box for the safe-zone check |
| Particles from text | `K.textPoints(text, { size, cx, cy, count })` |
| Shapes and camera | `K.circle`, `K.superellipse`, `K.shape(ctx, type, x, y, s, rot, role)`, `K.camera(ctx, { x, y, zoom, rot })` |
| Info-safe box | `K.safe` (canvas minus the top bar, bottom UI and right rail) |
| Sound | `cues()` kinds: impact, kick, thud, click, blip, pluck, bell, stab, whoosh, riser, tone, glitch, sparkle |

## Promotion checklist

- [ ] The header has a summary plus `params:`, `beats:`, `handoff:` and `use:`, and a timing paragraph.
- [ ] Only roles and `K.font`. There's no hex, no rgb() and no font names; the lint test enforces this.
- [ ] Deterministic: no `Math.random`, clock or timers.
- [ ] The length is whole half beats, and the last frame is exactly the declared hand-off.
- [ ] Readable text uses `K.text` or `K.mark`, and there's no unsafe text for realistic Arabic and Latin params.
- [ ] A cue on every hit.
- [ ] It's added to `CASES` in `test/mograph-scenes.test.mjs`, and the test passes.
- [ ] A preview sheet was looked at: the hits, the first and last frames, Arabic joins and punctuation.
- [ ] The catalog tables (the CLI's `mograph/scenes/README.md` and this skill's `SKILL.md`) have its row.

```bash
capcutctl mograph scene-preview --scene my-idea --params '{"text":"كود"}' --out sheet.png
capcutctl mograph scene-preview --scene my-idea --params '{"text":"كود"}' --out hits.png --times 0,0.5,1,1.95
capcutctl mograph scene-render  --scene my-idea --params '{"text":"كود"}' --out my-idea.mp4 --format mp4
```
