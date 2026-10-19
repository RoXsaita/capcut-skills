---
name: carousel
description: >
  Plan, write and check a static carousel (Instagram carousel, TikTok photo post) that people
  save and send: when a topic deserves one, which arc it takes (setup guide, copy-ready prompt,
  receipts, mistakes, before/after, teardown, cheat sheet), the cover, slide-by-slide recipes,
  real-UI screenshots cropped and annotated, Arabic right-to-left typography at phone scale, the
  last slide and comment keyword, the caption, and when to post relative to the reel on the same
  topic. Ends in a pre-publish checklist an agent can actually check. Use for any carousel,
  photo-mode post, "turn this reel into a guide", "make a carousel about X", or when a carousel
  reads as generic or AI-made. Static PNGs only; the brand comes from the creator's profile.
---

# Carousel

A carousel is not a short video with the sound off. People don't watch it; they **keep** it
(save) or **pass it on** (send). Every rule below serves one of those two acts.

What the evidence says, in one paragraph (sources in [references/research.md](references/research.md),
a reference account's 22 carousels in [references/examples.md](references/examples.md)): on that
account carousels earn about twice the save rate of reels but a fraction of the reach. The few that
broke out were **second-person setup guides posted the day after a reel on the same topic took
off**, whose cover promised the reader's result. Recaps of the reel's story, icon-diagram slides
and generic "AI tips" all sat at or below the median. On TikTok, the same posts in photo mode had
a higher median than its videos.

**The loop:** gate the topic (§1) → pick the arc (§2) → write the slide plan as text (§3–§7) →
capture and crop the real screens (§5) → render → run the checklist (§10) → caption (§8) → post
within 24 h of the reel (§9).

## 0. Read the profile, the reel and the creator's words first

- **Brand** comes from the creator's profile, `~/.config/capcutctl/profile.json`, never from this
  skill or a repo: `tokens.color.brand` (frames, dividers, step numbers), `tokens.color.accent`
  (the ONE highlight per slide), `tokens.scene.palette` (`paper` background, `ink` text), the font
  named in `brand.rules`, and `brand.avoid`. If there is no profile, ask once before rendering.
- **The reel** this carousel follows: its caption, its comment keyword (if it asked for one), its
  first-day reach against the creator's reel median, and the real artifacts behind it (the screen
  recording, the prompt as typed, receipts, numbers).
- **Language**: write in the creator's own voice and dialect. For a Levantine creator that is
  Levantine Arabic, as spoken in the reel, not Modern Standard Arabic and not translated English.

## 1. Should this be a carousel at all?

Make one when **all four** hold:

1. **A reel on the same topic went out in the last 24 hours and is beating the creator's reel
   median**, ideally one whose comment keyword promised "the steps" or "the prompt". The carousel
   is the payoff of that promise. (The reference account's best carousel followed a reel whose keyword drew ~6
   comments per 100 reached; one posted three days after its reel got 1 % of the reel's reach.)
2. **The reader can do it themselves**: a setup, a prompt, a setting, a checklist, a decision.
   If the only takeaway is "look what happened to me", it is a reel, not a carousel.
3. **There is a real artifact to show**: the creator's own screen, a receipt, a number, the prompt as typed.
4. **There is a person to send it to**, nameable in four words ("someone applying for jobs").

Standing rule: **every reel that reaches 10× the reel median gets a guide carousel within
24 hours.** (A reel at ~40× median with 1,700+ saves got no carousel; that was the biggest miss.)

Don't make: a recap of the reel's story; a news summary; a "story" carousel; anything whose cover
can't name a tool, a task and a result.

## 2. Pick the arc

| Arc | Use when | Slides (cover … last) |
|---|---|---|
| **Setup guide** (default) | The reel showed a result the viewer can reproduce | cover → why/what you need → one step per slide (3–6) → the troubleshooting or safety step → copy-ready slide → CTA |
| **Copy-ready prompt / template** | The value is the words the creator typed | cover → the result it gets (receipt) → the prompt, whole, in a code box → what to change (the [brackets]) → an example filled in → CTA |
| **Receipts first** | The claim is surprising (money back, free model, speed) | cover with the number → the receipt, cropped big → how (2–4 steps) → the honest catch → CTA |
| **Mistakes → fixes** | The creator learned it the hard way | cover "N mistakes when you…" → one mistake + its fix per slide → summary checklist → CTA |
| **Before → after** | One change transforms an output | cover → before → the one change → after → why it works → CTA |
| **Teardown** | A real thing is worth dissecting (an app, a pricing page, a viral post) | cover → the whole thing → numbered callouts, one per slide → the verdict → CTA |
| **Cheat sheet** | Reference value: shortcuts, settings, commands | cover → 3–5 simple slides building up → one dense reference slide (the save magnet) → CTA |

A versus/comparison carousel only works when the verdict is on the cover; "same model, why
different results?" without an answer underperformed.

**Slide count: 8–10** for a guide. The only large slide-count study (Socialinsider, 2020, from
the 10-slide era) found 10 slides did best and engagement rose again from 8; every one of the
reference account's 22 carousels had 6, so its data can't say. The 20-slide limit is not a target: go past 10 only
when every extra slide is a step someone would miss. Never pad a slide to reach a number.

## 3. The cover (slide 1)

It must work as a still in the feed, at thumbnail size on the grid, and with no context.

- **Promise the reader's result, in their voice**: imperative or a question, second person.
  "Let Claude apply to LinkedIn jobs (for you)", not "I let Claude apply…". Name the tool, the task
  and the payoff.
- **Payoff words that won**: free / $0 / no account / no API key; a time ("under 5 minutes");
  a job, money back. Put the payoff word in the accent.
- **Headline ≤ 8 words**, set at **≥ 96 px** (on a 1080-wide slide), occupying the top 40 %.
- **One supporting line ≤ 10 words** that lowers the barrier ("all you need: a Chrome extension")
  or opens a loop ("swipe for the name and the method").
- **One proof element**, big: the real result (receipt, number, finished output) cropped tight.
  A cover with no image and a giant headline is fine. A shrunken full-screen screenshot is not.
- **The creator's face only if the reel has not already used it as the hook**, and never as the main element
  of a guide.
- **Readable at grid size**: shrink the cover to 360 px wide; the headline must still read.
- Swipe cue: the word "اسحب" or a counter, small, near the bottom; no arrow (see §6).

## 4. Slide 2 is a second cover

Instagram often shows a carousel again to people who saw it and didn't swipe, this time on the
next slide (Mosseri, October 2024; see research.md). So slide 2 must hook on its own:

- Restate the promise as a concrete first step or the strongest proof ("the receipt"), with its
  own headline, not "let's begin".
- Never put an intro, a definition, or a "why this matters" essay on slide 2.

## 5. The middle slides

**One idea per slide, and every slide stands alone.** A slide is one step, one mistake, one
proof, or one comparison. If it needs two headlines, it is two slides. Each slide should still
make sense as a screenshot sent on its own (that is how slides get shared to Stories and DMs),
so the step number and the tool name sit on it, not only on the cover.

**Keep the best slide late.** The copy-ready prompt, the cheat sheet or the strongest receipt
goes around slides 7–9, after the reader has a reason to want it, and the caption or slide 2 says
it is coming ("the full prompt is at the end"). Creators who teach this report that value given
away on slide 2 ends the swiping.

**Density**

| Element | Limit (1080-wide slide) |
|---|---|
| Headline | ≤ 7 words, ≥ 72 px, starts with the step number and a verb |
| Supporting text | ≤ 20 words, ≥ 40 px (Arabic ≥ 44 px), max 3 lines |
| Smallest text anywhere (labels, footer, page count) | ≥ 28 px |
| Words per slide | ≤ 40; one cheat-sheet slide may go to 80 |

Why those sizes: a phone shows the 1080-px slide about 375–430 pt wide (a ~0.36 scale), so
40 px renders near 14 pt and 28 px near 10 pt, the floor of comfortable reading. Arabic glyphs
read smaller than Latin at the same size, hence the bump.

**Real screens, not drawings**

- Show **the creator's real UI** from the recording or a fresh capture, at Retina (2×) resolution. Never an
  image-model redraw of a UI, and never a stock mockup. (The reference account's early carousels redrew UI with an
  image model; even the winners would read better with the real screen.)
- **Crop to the part that matters** so the UI's own text lands at ≥ 28 px on the slide. In
  practice: from a 2× capture, crop to at most ~860 px of source width (about 430 pt of screen)
  for a full-width placement. A full window shrunk into a slide is unreadable.
- **One annotation per slide**: a box, an underline or a numbered pin, in the brand colour; the
  accent goes on the single word or number that matters. Optionally dim the rest of the crop.
  **Never blur** (blur reads cheap and hides the real thing).
- Lift the key number or button label out of the screenshot and set it large next to it, so it
  reads even if the screenshot doesn't.
- **Redact** emails, names, keys, order numbers with solid bars in the ink colour. Not blur.
- Place screenshots at **≥ 60 % of slide width**. Phone screenshots: crop to the relevant third,
  not the whole phone.

**The copy-ready slide**: when there is a prompt, template or setting, it gets a slide of its own,
in a code-style box, complete, with placeholders in [brackets] marked in the accent. It is the
slide people screenshot. Never "the full template is in the caption".

**The honest step**: one slide or line saying what can go wrong, what it costs, or what to check
before trusting it ("free: they may train on your prompts", "review before Submit"). It reads as
genuine and it is what people save.

## 6. Arabic, right to left

- **Swipe direction is unverified for Arabic-language apps** (no platform source either way). So
  don't design anything that depends on it: no line, arrow or panorama that continues across
  slides, and no directional arrow as the swipe cue. Use the word "اسحب" (or a step counter like
  "1/9") on the cover only. Within a slide, text reads right to left as normal. To settle it,
  check on a phone with the app in Arabic and record the answer in research.md.
- **Font**: the one the profile names. Arabic needs line height 1.5–1.7 for body text; never
  letter-space Arabic (it breaks the joins); never synthesise bold or italic; never justify.
- **Latin inside Arabic** (UI terms, product names) stays Latin and in its own direction: render
  with `dir="rtl"` on the slide and wrap each Latin run in `<bdi>` (or `unicode-bidi: isolate`), so
  punctuation and numbers don't jump to the wrong end. Prefer the Latin term at the start or end
  of a line, not between two Arabic clauses, and check every line with a Latin run by eye.
- **Digits**: one system per carousel. Step numbers and prices as they appear on the real screen
  (usually Western digits).
- **Dialect over formal**: the slide text sounds like the reel ("خلّي كلود…"), not like a manual
  ("هذا الكاروسيل يشرح لك…", which is an AI-caption tell).

## 7. The last slide and the CTA

- **One action** on the last slide. (An Arabic growth coach also puts a quiet save reminder on
  slide 4–5 because many readers never reach the end; that is fine if it is one small line.)
- The action is either a **comment keyword** (one short Arabic word, matching what will be sent:
  «برومبت», «دليل») or "save it for when you set it up", never three asks.
- Only use a keyword the creator will actually answer (automation or by hand), and that delivers
  something not already in the carousel (the full prompt file, the video walkthrough).
- Put the payoff and the action together: "want the full prompt? comment «برومبت»". It must
  name what the commenter gets. Instagram lists engagement bait (asking for engagement for its
  own sake: "comment YES if…", "tag 3 friends") as a reason to leave a post out of
  recommendations; no platform document addresses "comment a keyword to get a resource", so keep
  it specific and never stack it with a vote or a tag request.
- No "follow for more" as the only CTA; no "link in bio" for a guide that should be complete.
- The last slide repeats the handle; no endcard graphics, no logo wall.

## 8. The caption

The caption is searchable text and the second place people read; it does not replace slides.

1. **Line 1**: the cover promise reworded, with the tool name and the task spelled out (people
   search for them).
2. **2–4 short lines**: the steps in one breath each, so the caption alone is useful.
3. **The honest line**: the catch or the safety check.
4. **The share line, naming a person everyone knows**: "send it to someone who is applying for
   jobs". The reference account's top carousel (the highest share rate by far) named exactly
   that; weaker ones named vaguer people ("someone who wants to try it").
5. **The save line** or the keyword (the same one as the last slide).
6. 3–5 hashtags in the language of the audience.

Write it in the creator's voice (for the reference account: Levantine, short, concrete). No
"in this carousel I will explain…".

## 9. Posting

- **Within 24 hours of the reel**, the evening after, at the hour the creator's reels usually
  go out.
- **Add music on Instagram.** Mosseri said (October 2024) that carousels with music can appear in
  the Reels tab, which reaches non-followers. A quiet track, low enough not to matter.
- **Instagram and TikTok photo mode**, the same slides. On TikTok the description carries the
  steps and the post takes music too. The reference account's TikTok photo posts have a higher
  median than its videos there, so TikTok is not an afterthought.
- The reel's pinned comment or caption can point to the carousel once it is up.
- **Format: static PNG, 1080 × 1440 (3:4), safe zone the centre 1080 × 1350.** Every slide the
  same size. Since January 2025 the profile grid crops every post to 3:4, and since 29 May 2025
  the feed shows 3:4 uploads uncropped, so 3:4 is the only size that is whole in both places
  (a 4:5 slide loses its sides on the grid). Keep all text and key UI inside the centre
  1080 × 1350 (45 px top and bottom are bleed), so any 4:5 crop loses nothing. TikTok photo
  mode is built around 9:16; third-party guides (no TikTok source) say other ratios show with bars
  rather than cropped, with the caption and buttons over the lower part. So post the same 3:4
  slides, keep the bottom 10 % free of anything that must be read, and check the first post in
  the app.
- Alt text per slide on Instagram: the slide's headline plus what the screenshot shows.

## 10. Pre-publish checklist

Run every line; each one is a yes/no you can check on the rendered PNGs.

**Gate**
- [ ] A reel on this topic is ≤ 24 h old (or posts today) and beats the reel median; its comment
      keyword, if any, is what this carousel delivers.
- [ ] The reader can reproduce it; the last slide or caption names who to send it to.

**Cover**
- [ ] Second person / imperative / question; names a tool, a task and a payoff; ≤ 8 words.
- [ ] Not a recap of the reel's story; not "I let…".
- [ ] Shrunk to 360 px wide, the headline still reads.
- [ ] One proof element at ≥ 50 % of the slide, or none (type-only cover). No mascot, no
      generic icon cluster, no image-model art.

**Every slide**
- [ ] One idea; headline ≤ 7 words; ≤ 40 words total (one cheat-sheet slide ≤ 80).
- [ ] No text under 28 px; supporting text ≥ 40 px (Arabic ≥ 44 px). Measure it.
- [ ] Every screenshot is a real capture, ≥ 60 % slide width, its own text ≥ 28 px on the slide.
- [ ] At most one accent element; brand colour only on frames, dividers, step numbers, pins.
- [ ] Personal data redacted with solid bars; no blur anywhere.
- [ ] Every line with a Latin run checked: punctuation and digits on the correct side.

**Structure**
- [ ] 8–10 slides (more only if every slide is a needed step); slide 2 hooks on its own.
- [ ] The prompt/template, if any, is complete on a slide, not only in the caption.
- [ ] One honest step: the catch, the cost, or the check.
- [ ] Last slide has exactly one action; the keyword (if any) matches the caption and will be
      answered.

**Caption and post**
- [ ] Line 1 names tool + task; steps; honest line; share line naming a person; save/keyword line.
- [ ] Levantine voice, no "this carousel explains…".
- [ ] Music added on Instagram; same PNGs queued for TikTok photo mode; alt text written.
- [ ] Every slide 1080 × 1440; nothing important outside the centre 1080 × 1350 or in the bottom 10 %.

## AI-slop tells (reject on sight)

Image-model drawings of UI, mascots and robots; hub-and-spoke icon diagrams that could illustrate
any AI post; brand-logo collages with no screen; gradient blobs and glows; emoji bullets; vague
superlatives ("game-changer", "90% of people"); a "save this post" sticker on the cover; numbers
with no receipt; a dense full-window screenshot at a third of the slide; text in a formal register
the creator never speaks in.

## Files

| File | Use it for |
|---|---|
| `references/research.md` | The evidence: platform statements, data studies, creator recipes, each with its source and type |
| `references/examples.md` | The reference account's 22 carousels annotated (winners, losers, the rule each broke) and patterns from other creators |

## What this skill does not do

- Motion or video carousels: static PNG only.
- Rendering: the slide-spec render engine turns the plan into PNGs; this skill decides what goes
  on them and checks the result.
- Posting: the dashboard drafts and the creator's sign-off decide that.
