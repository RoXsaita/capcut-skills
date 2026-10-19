---
name: carousel
description: >
  Plan, write and check a static carousel (Instagram carousel, TikTok photo post) that people
  save and send: when a topic deserves one, which arc it takes (setup guide, copy-ready prompt,
  receipts, mistakes, before/after, teardown, cheat sheet), the written plan before any pixels,
  the cover, slide-by-slide recipes, real-UI screenshots cropped and annotated, Arabic
  right-to-left typography at phone scale, the last slide and comment keyword, the caption, when
  to post relative to the reel on the same topic, and how to read the result. Ends in a
  pre-publish checklist an agent can actually check. Use for any carousel, photo-mode post, "turn
  this reel into a guide", "make a carousel about X", or when a carousel reads as generic or
  AI-made. Static PNGs only; the brand comes from the creator's profile.
---

# Carousel

A carousel is not a short video with the sound off. People don't watch it; they **keep** it
(save) or **pass it on** (send). Every rule below serves one of those two acts.

What the evidence says, in one paragraph (sources in [references/research.md](references/research.md),
a reference account's 22 carousels in [references/examples.md](references/examples.md)): on that
account carousels earn about twice the save rate of reels but a fraction of the reach. The few that
broke out were **second-person guides posted the day after a reel on the same topic took off**,
whose cover promised the reader's result, often something free. Recaps of the reel's story,
icon-diagram slides and generic "AI tips" sat at or below the median. A real experience plus a
prompt was not enough on its own: the reader has to want the outcome and see a short path to it.
On TikTok, the same posts in photo mode had a higher median than the account's videos.

**The loop:** gate the topic (§1) → pick the arc (§2) → write and lock the plan (§3) → capture the
real screens (§6) → build (§12) → run the checklist (§11) → caption (§9) → post (§10) → read the
result at 24 h and 7 days (§13).

## 0. Read the profile, the reel and the source first

- **Brand** comes from the creator's profile, `~/.config/capcutctl/profile.json`, never from this
  skill or a repo: `tokens.color.brand` (frames, dividers, step numbers, annotation pins),
  `tokens.color.accent` (the ONE highlight per slide), `tokens.scene.palette` (`paper` background,
  `ink` text, `hot` for a negative such as a struck-out price), the font named in `brand.rules`,
  and `brand.avoid`. If there is no profile, ask once before rendering.
- **The reel** this carousel follows: its caption, its comment keyword (if it asked for one), its
  first-day reach against the creator's reel median, and the real artifacts behind it (the screen
  recording, the prompt as typed, receipts, numbers, the guide page if there is one).
- **Voice**: the creator's own dialect and register. For a Levantine creator that is Levantine
  Arabic as spoken in the reel, not Modern Standard Arabic and not translated English.

## 1. Should this be a carousel, and what kind?

A carousel needs **all three**:

1. **The reader can do it themselves**: a setup, a prompt, a setting, a checklist, a decision.
   If the only takeaway is "look what happened to me", it is a reel, not a carousel.
2. **There is a real artifact to show**: the creator's own screen, a receipt, a number, the prompt.
3. **There is a person to send it to**, nameable in four words ("someone applying for jobs").

Then decide which of two kinds it is:

- **Companion**: a reel on the same topic went out in the last 24 hours and is beating the reel
  median, ideally one whose comment keyword promised "the steps" or "the prompt". The carousel is
  the payoff of that promise. A strong reel is not enough by itself: the reference account's
  biggest reel ever was followed by a recap carousel that got almost nothing.
- **Standalone**: no fresh reel behind it. The cover has to earn the stop on its own, so the
  payoff must be something a stranger wants (the reference account's best standalone-strength
  carousel promised "one of the strongest models in the world, free").

Standing rule: **every reel that reaches 10× the reel median gets a guide carousel within 24 hours.**
(A reel at ~40× the median got none; that was the biggest miss.)

Topic filter: free / save money / get a job / remove a barrier has been the reference account's
proven payoff. Keep about **1 in 3** carousels outside it, as exploration, so the filter keeps
being tested rather than assumed.

Don't make: a recap of the reel; a news summary; a "story" carousel; a stack of several old
experiments summed into one claim (tried, 0.5× median); anything whose cover can't name a tool, a
task and a result; anything whose setup is longer than the payoff is worth (tokens, IDs and
config screens need an audience that already wants the tool).

## 2. Pick the arc

| Arc | Use when | Slides (cover … last) |
|---|---|---|
| **Setup guide** (default) | The reel showed a result the viewer can reproduce | cover → the payoff or what you need → one step per slide (3–5) → the troubleshooting or safety step → copy-ready slide → CTA |
| **Copy-ready prompt / template** | The value is the words the creator typed | cover → the result it gets (receipt) → why it works → the prompt in a code box → what to change (the [brackets]) → an example filled in → CTA |
| **Receipts first** | The claim is surprising (money back, free model, speed) | cover with the number → the receipt, cropped big → how (3 steps) → why it worked (a short timeline beats an unreadable screenshot) → the honest catch → CTA |
| **Mistakes → fixes** | The creator learned it the hard way | cover "N mistakes when you…" → one mistake + its fix per slide → summary checklist → CTA |
| **Before → after** | One change transforms an output | cover → before → the one change → after → why it works → CTA |
| **Comparison** | Two tools did the same job | cover with the verdict → both real results, equal size and treatment → the difference that decided it → the rule for choosing → the limit (one test, not a ranking) → CTA |
| **Teardown** | A real thing is worth dissecting (an app, a pricing page, a viral post) | cover → the whole thing → numbered callouts, one per slide → the verdict → CTA |
| **Cheat sheet** | Reference value: shortcuts, settings, commands | cover → 3–5 simple slides building up → one dense reference slide (the save magnet) → CTA |

A comparison only works when the verdict is on the cover; "same model, why different results?"
without an answer underperformed.

**Slide count: 8–10** for a guide. The only large slide-count study (Socialinsider, 2020, from the
10-slide era) found 10 slides did best and engagement rose again from 8; every one of the
reference account's 22 carousels had 6, so its data can't say. The 20-slide limit is not a target:
go past 10 only when every extra slide is a step someone would miss. Never pad. If the material is
too thin for 8 useful slides, say so; a thin topic is a reel.

## 3. Write the plan before any pixels, then lock it

Write this as text and check it before capturing or rendering anything. Once it passes, the copy
is locked: visual revisions do not rewrite it.

| Field | What it holds |
|---|---|
| `hook` | The one line that stops the scroll: tension, curiosity or a selfish payoff for the reader. A topic label is not a hook. |
| `reader_delta` | What the reader can do, copy or decide afterwards that they couldn't before. A paraphrase of the reel is not a delta. |
| `story` | The arc (§2) and why each slide makes the next one necessary. A slide that could be deleted unnoticed is filler. |
| `why_save` / `why_send` | Why someone keeps it or sends it, and to whom. |
| `weak_version_rejected` | One sentence on the obvious reel-recap carousel you considered and why it isn't this. |
| `claims` | Every factual line, marked **observed** (it happened in the creator's footage), **documented** (an official source, checked today) or **suggested** (an idea for the reader). Never turn a suggestion into "I tested this", one result into a guarantee, or an anecdote into a rule. Never invent a struggle, a result, a time saved or a number. |
| `number_story` | If there is a number, the one exact comparison (what, against what, how much). Every slide and the caption must agree with it. Approximate or converted figures say so. |
| `slides` | Per slide: its job, its exact copy, its visual role (§6), the claim it rests on. |
| `cta` | The keyword or action, what it delivers, and whether delivery is verified (§8). |

Two tests the plan must pass:

- **A stranger who never saw the reel** can name the tool, what it does for them and the first step.
- **Someone who did see the reel** gets something new: the method, the prompt, the decision rule,
  the catch. Not the reel again with "you" instead of "I".

## 4. The cover (slide 1)

It must work as a still in the feed, at thumbnail size on the grid, and with no context.

- **Promise the reader's result, in their voice**: imperative or a question, second person. "Let
  Claude apply to LinkedIn jobs (for you)", not "I let Claude apply…". Name the tool, the task and
  the payoff. First person belongs to the evidence slides, once, where it is true.
- **A selfish payoff plus one concrete number** where there is one: free / $0 / no account / no
  API key; a time ("under 5 minutes"); money back. The payoff word takes the accent.
- **Headline ≤ 8 words**, set at **≥ 96 px**, in the top 40 % of the slide.
- **One supporting line ≤ 10 words** that lowers the barrier ("all you need: a Chrome extension")
  or opens a loop ("swipe for the name and the method").
- **One proof element**, big: the real result (receipt, number, finished output) cropped tight. A
  type-only cover with a giant headline is fine. A shrunken full-screen screenshot is not.
- **The creator's face only if the reel has not already used it as the hook**, never as the main
  element of a guide, and never a generated face.
- **Readable at grid size**: shrink the cover to 360 px wide; the headline must still read.
- Swipe cue: the word "اسحب" or a counter, small, near the bottom; no arrow (see §7).

## 5. Slide 2 is a second cover

Instagram often shows a carousel again to people who saw it and didn't swipe, this time on the
next slide (Mosseri, October 2024; see research.md). So slide 2 must hook on its own and **pay
off immediately**:

- The strongest proof ("the receipt"), the real comparison, or the first concrete step, with its
  own headline. Not "let's begin", not the cover again, not an install slide by default.
- Never an intro, a definition, a history lesson or a "why this matters" essay.

## 6. The middle slides

**One idea per slide, and every slide stands alone.** A slide is one step, one mistake, one proof
or one comparison, with a job no other slide has. If it needs two headlines, it is two slides.
Each slide should make sense as a screenshot sent on its own (that is how slides travel to Stories
and DMs), so the step number and the tool name sit on it, not only on the cover. Say each thing
once: the same point on two slides under different titles is the commonest padding.

**Keep the best slide late.** The copy-ready prompt, the cheat sheet or the strongest receipt goes
around slides 7–9, after the reader has a reason to want it; slide 2 or the caption can say it is
coming. The method must be on the slides before the CTA: the carousel teaches without anyone
having to comment.

**Density**

| Element | Limit (1080-wide slide) |
|---|---|
| Headline | ≤ 7 words, ≥ 72 px, starts with the step number and a verb |
| Supporting text | ≤ 20 words, ≥ 40 px (Arabic ≥ 44 px), max 3 lines |
| Smallest text anywhere (labels, footer, page count) | ≥ 28 px |
| Words per slide | aim for **8–22**; review anything over **30**; one cheat-sheet or prompt slide may go higher |
| Margins | **100 px inset on all four edges** for every text, logo, footer and key visual; the background runs full bleed |

Why those sizes: a phone shows the 1080-px slide about 375–430 pt wide (a ~0.36 scale), so 40 px
renders near 14 pt and 28 px near 10 pt, the floor of comfortable reading. Arabic glyphs read
smaller than Latin at the same size, hence the bump.

**Give every slide a visual role.** One of: the real proof (an annotated crop), input → output, a
short right-to-left action flow, a few choices side by side, a comparison, a timeline, or the
takeaway in type. The visual explains a relationship or replaces words; it is never decoration,
and not every slide needs a screenshot box.

**Real screens, not drawings**

- Show **the creator's real UI** from the recording or a fresh capture, at Retina (2×) resolution.
  Never an image-model redraw of a UI (it is illustration, not proof, and image models misspell
  Arabic and add wrong diacritics), and never a stock mockup or fake device.
- **Grab the exact frame** where the number or result is on screen, sharp, and crop to it. A small
  window of the whole screen that cuts off the amount is the failure to avoid.
- **Crop to the part that matters** so the UI's own text lands at **≥ 36 px** on the slide (the
  build's OCR check): from a 2× capture, at most ~780 px of source width (about 390 pt of screen)
  for a full-width placement. Don't upscale a capture past ~2.8×; it reads soft.
- **Present each crop as a proof card**: on the paper background, a plain card with a thin border
  and a soft shadow, at **≥ 60 % of the slide width**. Phone screenshots: crop to the relevant
  third, not the whole phone.
- **One annotation per slide**: a box, an underline or a numbered pin in the brand colour; the
  accent goes as a highlighter sweep over the single word or number that matters. Optionally dim
  the rest of the crop. **Never blur.**
- Lift the key number or button label out of the screenshot and set it large beside it, so it reads
  even if the screenshot doesn't.
- **Redact** emails, names, keys, order numbers with solid bars in the ink colour, before the image
  goes anywhere. Not blur.
- In a comparison, both results get the same size, crop logic and treatment.

**The copy-ready slide.** A prompt, template or setting gets a slide of its own, in a code-style
box, with placeholders in [brackets] marked in the accent. A short prompt (up to ~60 words) goes
on the slide whole. A long one gets its skeleton on the slide (the lines that matter, the
placeholders) and the full text behind the keyword (§8). Never "the template is in the caption".

**The honest step.** One slide or line on what can go wrong, what it costs, or what to check before
trusting it ("free: they may train on your prompts", "review before Submit"). One useful
qualification, in plain words, not disclaimers on every slide.

**Vary the layout by function** (result-led cover, annotated crop, comparison, action flow, caveat,
takeaway) within one type system and palette. Consecutive carousels with the same six boxes read
as a template.

## 7. Arabic, right to left

- **Swipe direction is unverified for Arabic-language apps** (no platform source either way). So
  don't design anything that depends on it: no line, arrow or panorama that continues across
  slides, and no directional arrow as the swipe cue. Use the word "اسحب" (or a step counter like
  "1/9") on the cover only. Within a slide, text reads right to left as normal. To settle it,
  check on a phone with the app in Arabic and record the answer in research.md.
- **Font**: the one the profile names. Arabic needs line height 1.5–1.7 for body text; never
  letter-space Arabic (it breaks the joins); never synthesise bold or italic; never justify. No
  diacritics except where a word is ambiguous without them.
- **Latin inside Arabic** (UI terms, product names) stays Latin and in its own direction: render
  with `dir="rtl"` on the slide and wrap each Latin run in `<bdi>` (or `unicode-bidi: isolate`), so
  punctuation and numbers don't jump to the wrong end. Prefer the Latin term at the start or end of
  a line, not between two Arabic clauses, and check every line with a Latin run by eye.
- **Digits**: one system per carousel. Step numbers and prices as they appear on the real screen
  (usually Western digits).
- **Dialect over formal**: the slide text sounds like the reel ("خلّي كلود…"), not like a manual
  ("هذا الكاروسيل يشرح لك…", an AI-caption tell).

## 8. The last slide and the CTA

- **One action** on the last slide. (An Arabic growth coach also puts a quiet save reminder on slide
  4–5 because many readers never reach the end; fine if it is one small line.)
- The action is either a **comment keyword** (one short Arabic word, matching what will be sent:
  «برومبت», «دليل») or "save it for when you set it up", never three asks.
- **A keyword only when delivery is real**: the artifact exists (the full prompt, the guide page,
  and its link loads today) and the reply is wired or the creator will answer by hand. Otherwise
  use "save it", or point to the guide plainly. Never promise a DM that isn't set up.
- Put the payoff and the action together: "want the full prompt? comment «برومبت»". It must name
  what the commenter gets. Instagram lists engagement bait (engagement for its own sake: "comment
  YES if…", "tag 3 friends") as a reason to leave a post out of recommendations; no platform
  document addresses "comment a keyword to get a resource", so keep it specific and never stack it
  with a vote or a tag request.
- No "follow for more" as the only CTA; no "link in bio" for a guide that should be complete.
- The last slide repeats the handle; no endcard graphics, no logo wall.

## 9. The caption

The caption is searchable text and the second place people read; it does not replace slides.

1. **Line 1**: the cover promise reworded, with the tool name and the task spelled out (people
   search for them).
2. **2–4 short lines**: the steps in one breath each, so the caption alone is useful.
3. **The honest line**: the catch or the safety check.
4. **The share line, naming a person everyone knows**: "send it to someone who is applying for
   jobs". The reference account's top carousel (the highest share rate by far) named exactly that;
   weaker ones named vaguer people ("someone who wants to try it").
5. **The save line** or the keyword (the same one as the last slide).
6. 3–5 hashtags in the language of the audience; Latin hashtags on their own line.

Write it in the creator's voice. Start every line in Arabic, so a Latin word at the end of a line
doesn't drag the punctuation to the wrong side. No "in this carousel I will explain…".

## 10. Posting

- **Companion: within 24 hours of the reel**, the evening after, at the hour the creator's reels
  usually go out. The reel's pinned comment or caption can point to the carousel once it is up.
- **Music on Instagram**: Mosseri said (October 2024) that carousels with music can appear in the
  Reels tab, which reaches non-followers. The Instagram API cannot attach music to a carousel, so
  this means posting from the app with a quiet track; if the post goes out through the API, say
  that it went without music.
- **Instagram and TikTok photo mode**, the same slides. On TikTok the description carries the steps
  and the post takes music too. The reference account's TikTok photo posts have a higher median
  than its videos there, so TikTok is not an afterthought.
- **Format: static PNG, 1080 × 1440 (3:4), safe zone the centre 1080 × 1350.** Every slide the same
  size. Since January 2025 the profile grid crops every post to 3:4, and since 29 May 2025 the feed
  shows 3:4 uploads uncropped, so 3:4 is the only size that is whole in both places (a 4:5 slide
  loses its sides on the grid). The 100 px inset (§6) keeps everything inside the 1080 × 1350 safe
  zone. TikTok photo mode is built around 9:16; third-party guides (no TikTok source) say other
  ratios show with bars rather than cropped, with the caption and buttons over the lower part. So
  post the same 3:4 slides, keep the bottom 10 % free of anything that must be read, and check the
  first post in the app.
- Alt text per slide on Instagram: the slide's headline plus what the screenshot shows.

## 11. Pre-publish checklist

Run every line; each one is a yes/no you can check on the plan or the rendered PNGs. At most two
fix-and-recheck rounds; stop when nothing would be visible on a phone.

**Gate and plan**
- [ ] The reader can reproduce it; the plan names who to send it to.
- [ ] Companion: the reel is ≤ 24 h old and beats the reel median; its keyword, if any, is what
      this carousel delivers. Standalone: the cover payoff works for a stranger.
- [ ] The plan (§3) is written, passes both tests, and every claim is marked observed / documented
      / suggested. Nothing invented.

**Cover**
- [ ] Second person / imperative / question; names a tool, a task and a payoff; ≤ 8 words.
- [ ] Not a recap of the reel's story; not "I let…".
- [ ] Shrunk to 360 px wide, the headline still reads.
- [ ] One proof element at ≥ 50 % of the slide, or none (type-only). No mascot, generated face,
      generic icon cluster or image-model art.

**Every slide**
- [ ] One idea with its own job; headline ≤ 7 words; 8–22 words (anything over 30 justified).
- [ ] No text under 28 px; supporting text ≥ 40 px (Arabic ≥ 44 px); nothing inside the 100 px
      inset. Measure it.
- [ ] Every screenshot is a real capture, ≥ 60 % slide width, its own text ≥ 36 px on the slide,
      the number or result inside the crop.
- [ ] At most one accent element; brand colour only on frames, dividers, step numbers, pins.
- [ ] Personal data redacted with solid bars; no blur anywhere.
- [ ] **Text readback**: OCR every slide (for example macOS Vision with `ar-SA` and `en-US`) and
      compare it with the locked copy: same words, same numbers, no stray diacritics, no extra lines.
- [ ] Every line with a Latin run checked by eye: punctuation and digits on the correct side.
- [ ] The number story is identical on every slide and in the caption.
- [ ] No production language on a slide ("verified", "source fidelity", "without inventing…").

**Structure**
- [ ] 8–10 slides (more only if every slide is a needed step); slide 2 pays off on its own.
- [ ] The method is on the slides before the CTA; the prompt or its skeleton is on a slide.
- [ ] One honest step: the catch, the cost or the check.
- [ ] Last slide has exactly one action; a keyword only if its artifact exists and delivery is real.

**Caption and post**
- [ ] Line 1 names tool + task; steps; honest line; share line naming a person; save/keyword line.
- [ ] The creator's dialect, lines start in Arabic, no "this carousel explains…".
- [ ] Every slide 1080 × 1440; nothing important in the bottom 10 %.
- [ ] Music added in the Instagram app (or noted as missing); same PNGs queued for TikTok photo
      mode; alt text written.

## 12. Building it with `capcutctl carousel`

The CLI's carousel commands turn the §3 plan into slides. They enforce a floor; this skill sets
the bar, so a passing build still goes through §11.

1. **Gate** (companion carousels): `capcutctl carousel scan --dashboard URL` lists the recent
   reels that earn a guide twin (first-day reach above the median of the other reels, and a setup
   the viewer can repeat). Stories are logged "story, no twin"; unclear ones "unsure", for a
   person to decide. It doesn't judge standalone carousels or the topic filter (§1).
2. **Find the frames**: `capcutctl carousel steps --take DIR` gives one candidate frame per real
   click or typing burst in a screen-recording take, with a crop sized so the UI text reads at
   ≥ 36 px. Pick the frame where the result is on screen (§6), not just the first click.
3. **Write the spec** from the locked plan: `slug`, `title`, `caption`, `tiktokCaption`, and
   `slides`, each with a `kind` (`cover`, `step`, `prompt`, `cta`), a `headline` and a `sub`; the
   cover's `needs` (what the reader needs, which is the barrier-lowering line); each step's `shot`
   (`take`, a time `t` or a `click` / `typing` event, `crop` as `[x, y, w, h]` in video pixels,
   optional `highlight`); the prompt slide's `blocks`; the CTA's `keyword`.
4. **Build and QA**: `capcutctl carousel build --spec pack.json --out DIR` renders the slides with
   headless Chrome and fails on UI text under 36 px, privacy leaks (home paths, shell prompts,
   emails) or a headline over 12 words. Then run §11 on the PNGs.
5. **Stage as a draft**: `capcutctl carousel stage --pack DIR --dashboard URL --remote HOST:DIR
   --item ID --platforms instagram,tiktok --dry-run`, then without `--dry-run`. It never publishes.

Where the engine and this skill differ today, follow the stricter rule and say so in the hand-off:
the canvas is decided as 1080 × 1440 but the engine may still render 1080 × 1350 until its change
lands (check the PNG size; don't fail a pack on it, flag it); the engine takes 6–8 slides (this skill wants 8–10: build 8), knows only the setup-guide arc's
four kinds (other arcs need their slides expressed as `step` slides or wait for new kinds), and
requires a CTA keyword (use one only when delivery is real; otherwise hold the pack).

## 13. After posting: read the result

At about **24 hours and 7 days**, record for each carousel: the link, kind (companion or
standalone) and the reel's reach, arc, cover line, slide count, keyword and keyword comments,
views, reach, saves and shares, and saves and shares per 1,000 views. Compare against the
creator's carousel median at the same age, not against how it felt.

| What moved | What it means |
|---|---|
| More reach, saves per 1K held | The packaging (cover, timing) improved |
| Similar reach, more saves per 1K | More useful; the hook or distribution still needs work |
| More reach, far fewer saves per 1K | Prettier or catchier, less useful |
| Saves healthy, reach low | A topic or distribution problem, not polish: change the topic or ride a reel, not the design |
| Nothing improves over several posts | Rethink what the carousel adds over the reel, not the palette |

Change one thing at a time when testing (the cover, the arc, the slide count), and hold the design
steady while testing copy. A run of organic posts is a comparison, not an A/B test; don't crown a
winner on a ratio built from three saves.

## AI-slop tells (reject on sight)

Image-model drawings of UI, devices, mascots and robots; generated faces; hub-and-spoke icon
diagrams that could illustrate any AI post; brand-logo collages with no screen; neon, glow, grain,
gradients, chalkboard, paper texture, brush strokes and ornamental arrows; emoji bullets; vague
superlatives ("game-changer", "90% of people"); a "save this post" sticker on the cover; numbers
with no receipt; a dense full-window screenshot at a third of the slide; production or QA language
printed on a slide; text in a formal register the creator never speaks in.

## Files

| File | Use it for |
|---|---|
| `references/research.md` | The evidence: platform statements, data studies, creator recipes, each with its source and type; what was adopted, what wasn't, what is still unknown |
| `references/examples.md` | The reference account's 22 carousels annotated (winners, losers, the rule each broke) and patterns from other creators |

## What this skill does not do

- Motion or video carousels: static PNG only.
- Rendering: the slide-spec render engine turns the plan into PNGs; this skill decides what goes
  on them and checks the result.
- Posting: the dashboard drafts and the creator's sign-off decide that.
