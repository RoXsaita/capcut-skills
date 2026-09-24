# Motion grammar

The numbers live in the profile (`capcutctl profile` → `density`, `grammar`, `tokens`, `never`);
`capcutctl gate` enforces them. This page is the reasoning, so the judgement in `edit.json`
matches what the gate will check.

**Premium is contrast, not quantity.** A short is judged in its first second, then held by
rhythm: something new every few seconds, rests between, one focus at a time, and every picture
event paired with a sound. Constant motion reads as machine-made just as surely as none.

## What each beat gets

| Beat | Camera | Graphic | Sound |
|---|---|---|---|
| Hook (0–1.5s) | proof on screen by 1.5s; a snap punch | `hook-title` | impact on frame 0 |
| Claim | stress push (automatic) | `keyword-super` (1–3 words) | pop |
| Number | hold still | `number-pop` | pop |
| Brand mention | — | logo pop (native), or `brand-chip` without art | pop |
| Instruction | `punch` onto the element | `callout-box` on a static shot | enter/click |
| Demo action | 1× on the thing named; ramp the waiting | — | click / typing (from the trace) |
| Result | punch → hold → release; 0.4–0.7× | — | idea / coin |
| Reaction | face at 1×, clean | — | none |
| CTA | full face | `cta-card` + endcard | select; music out |

## Density (profile defaults)

- Something moves by **0.5s**; proof on screen by **1.5s**.
- First **6s**: a visual event at least every second.
- Body: a visual change at least every **3s**; a graphic every **5–8s**.
- After the hook, a **2s rest** with no overlay in every **15s**.
- At most **2** things animating at once — one graphic plus one camera move.
- No template twice within **10s**; no two entrances within **6 frames**.
- Transitions only on picture changes; no one transition on more than **40%** of seams.

## Never

- Anything that spins or loops forever; rotation.
- Linear easing on an entrance.
- Letter-by-letter Arabic, or Arabic in a Latin fallback face; more than one font family.
- Text that repeats the whole spoken sentence (that is subtitling, not emphasis).
- A graphic without a sound, or a sound without a reason on screen.
- Anything inside the platform UI (top bar, bottom caption band, right action rail).
- A punch and a callout on the same target; camera motion on the circle layout.
- An endcard longer than 3s with nothing new on it.

## Design system (tokens)

One family (IBM Plex Sans Arabic, 600/700, bundled). Colours: indigo `#4040FE` (the card's
measured fill), white ring, ink, white text, and one accent for the key word. Type scale at
1080 wide: hook 120, numeral 200, super 84, list 56, chip 44. Entrances ease out
(`cubic-bezier(.16,1,.3,1)`), exits are faster, pops overshoot at most 6%. Timings are in
frames at 30fps and even. Graphics lead their word by 3 frames and land their sound with
them. Templates read all of this from the profile; change the profile, not the templates.
