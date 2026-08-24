## The three indexes

Nothing gets cut from a source that has not been indexed. There are three, and they answer
different questions. Skipping any one of them is where every defect so far came from.

**`capcutctl cut VIDEO` builds the Whisper and Energy indexes for you** and caches both in
`~/Downloads/.video-index/`. You never invoke them directly. OCR is only for screen B-roll —
see `capcut-editing-screen-recording`.

| Index | Question it answers | Built with | Cache |
|---|---|---|---|
| **Whisper** | what is said, and roughly when | `mlx_whisper`, `large-v3-turbo` | `<name>.whisper-<model>.json` |
| **OCR** | what is on the screen, second by second | tesseract at 1 fps | `<name>.ocr.json` |
| **Energy** | where sound actually is, to 10 ms | `audio_index.py` (inside `capcutctl cut`) | `<name>.energy10.json` |

Whisper is **semantic** and its timings lie (contiguous fill). Energy is **acoustic** and
sample-true but knows no meaning. A cut point has to satisfy both: Whisper decides *which words*,
energy decides *exactly where*.
## The energy index

`capcutctl cut` builds and queries this for you. The API below is what runs **inside** it —
read it to understand a boundary decision or to extend the tool, not to drive a cut by hand.

```python
from audio_index import AudioIndex, lint          # tools/audio_index.py in the capcutctl repo
idx = AudioIndex.build_or_load("cam.mp4")         # ~2s for 4 min, then cached

idx.at(t)              # dB at t
idx.rising(t)          # is the envelope climbing -> you are inside a word
idx.head_silence(t)    # dead air starting AT t   (what an IN point stitches in)
idx.tail_silence(t)    # silence ending AT t      (what an OUT point had before it)
idx.onset_after(t)     # next real sound -- the only safe place for an IN
idx.trough(t)          # quietest instant nearby -- the safe place for an OUT
idx.strip(a, b)        # ASCII:  # speech   o soft   . silence
```
## Lint every cut plan before rendering

```python
spans = [("A", 122.467, 135.967), ("B", 139.833, 142.900), ...]
for finding in lint(idx, spans):
    print(finding)          # empty list == every seam clean
```

`lint` is **purely acoustic on purpose.** An earlier version consulted Whisper segment starts to
decide whether a pause was "legitimate at a sentence boundary" — and excused the one genuinely
broken seam, because it sat 0.27 s from a Whisper start. Gating on Whisper re-imports the exact
error you are trying to catch.

### What the thresholds are calibrated on

One cut the user reviewed and called flawless, with the single seam he caught by ear as the
negative control:

| | tail silence (outgoing) | head silence (incoming) | total |
|---|---|---|---|
| 8 accepted seams | — | **≤ 0.28 s** | ≤ 0.39 s |
| the rejected seam | 0.00 | **0.35 s** | 0.35 s |

So the rule is `head_silence > 0.30 s`, plus `tail+head > 0.45 s` for an over-long stitched pause.
**The margin is 0.28 vs 0.35 — thin, from one labelled example.** Findings are candidates to
listen to. A clean lint means "nothing detected", not "verified good".

The shape of the bad seam is worth memorising: **all the hole on one side.** The speaker was
mid-flow at the OUT (no tail pause at all) and the IN carried a third of a second of lead-in. The
ear hears speech stop dead, then a hole. Where the speaker genuinely paused, silence appears on
*both* sides and sounds like breathing.

### Reading a strip

```
A/B  13.50s    ##########|.o########      good: speech -> cut -> speech
C1/C2 32.87s   ####ooo...|...####oo#      good: he paused; silence both sides
old A/B        ##########|.......###      BAD: mid-flow out, then a hole
```


The core idea. Do this before writing any EDL.
## Voice — Whisper (A-roll)

```python
import mlx_whisper
r = mlx_whisper.transcribe(
    "cam.wav",
    path_or_hf_repo="mlx-community/whisper-large-v3-turbo",
    language="ar", word_timestamps=True, verbose=False)
```

Setup (Python 3.14 has no wheels for this — pin 3.12, and uv is far faster than pip):

```bash
uv venv --python 3.12 wenv
UV_HTTP_TIMEOUT=300 VIRTUAL_ENV=./wenv uv pip install mlx-whisper
```

Extract audio first: `ffmpeg -i in.mp4 -vn -ac 1 -ar 16000 -c:a pcm_s16le cam.wav`

### What you get and how to use it

- `segments[].words[]` gives `{start, end, word}`. **Snap every cut to a word edge.** When this
  was checked against hand-picked beat boundaries, all 19 landed on word edges with `+0.00` drift.
- **Detect repeated takes.** The user often records the same script twice. Look for the opening
  line recurring far into the timeline — that is take 2 starting. Also look for the same sentence
  repeated 3–4× in a row: those are retries, and you pick the best one.
- **Find pause points**: gaps > 0.25s between words are natural cut boundaries. A continuously
  delivered take may have very few (only 6 in one 110s take) — then every boundary *must* be a
  word edge because there is no silence to hide in.

### Known artifact

Arabic transcripts often end with a hallucinated subtitle credit like `ترجمة نانسي قنقر`
("translation by ..."). It is not in the audio. Always drop the trailing credit line.
## Whisper word timings are contiguous-filled — do not trust them as cut points

Whisper emits words back-to-back: each word's `start` equals the previous word's `end`. So a
word's reported start is often **hundreds of milliseconds before it is actually spoken**, and any
pause gets absorbed into the trailing word.

Measured example (cam take 2): Whisper put `بتقدر` at 193.80, but `silencedetect` showed silence
from 194.09 to 194.47 — the real onset was **670 ms later** than Whisper claimed.

**Always intersect Whisper with silence detection before cutting:**

```bash
ffmpeg -i cam.wav -af "silencedetect=noise=-32dB:d=0.25" -f null - 2>&1 | grep silence_
```

Rules that follow from this:

- Put the cut **inside a detected silence**, roughly 0.2–0.3 s before the real onset. Never on the
  Whisper word start.
- Where two spans butt against speech with no silence between (a run-on retry), cut tight on the
  word edge and accept the hard cut — there is nothing to hide in.
- A silence *inside* a Whisper word is the tell for a hesitation or a stumble. That is where the
  dead space is, and where the aborted-take boundary actually sits.
## Picking between takes and retries

The user's rule, verbatim: **"generally the last cut of a specific thing is better."** He warms up
across a take and re-says lines until they land, so later almost always wins.

Procedure:

1. Split the transcript into takes (look for a long silence plus the hook line repeating).
2. Inside the surviving take, group segments into **beats** — one idea each.
3. For every beat with more than one attempt, keep the **last** one, then sanity-check it is also
   the most complete. It usually is, and usually gains a word (`لعبة Tower Defense` vs
   `Tower Defense`; `جروك بلد` vs `جروك`).
4. Only override "last wins" if the last attempt is truncated or fluffed.

Then hunt the three things that survive inside a good take:

| Kind | How it shows up | Example found |
|---|---|---|
| Hesitation | silence > 0.6 s **inside** a Whisper word | 0.85 s between `بعدين` and `شفته` |
| Filler | a short segment-leading phrase that adds nothing | `في الشي` before `بعد دقائق` |
| Stutter | the same word twice in a row in the word list | `كبست كبستة publish` |

Trim the hesitation to ~0.25 s; cut the filler and stutter out entirely.
## Verify by re-transcribing the cut — always

Run Whisper on the rendered cut, not just on the source. It is the only cheap check that catches a
clipped first syllable, a duplicate you missed, or a cut that fused two words into nonsense. A
clean pass looks like: one segment per beat, no repeated sentence, no hallucinated tail.

(Whisper hallucinates on trailing silence — `ترجمة نانسي قنقر` appeared on 1.1 s of room tone at
the end of the source. Always trim to the last real word.)
## silencedetect is a coarse filter — confirm every seam with an RMS scan

`silencedetect` at `-32dB:d=0.25` is good enough to *find* candidate seams. It is **not** good
enough to place them. It missed a 0.35 s dead space and a clipped word on the one seam the user
later flagged by ear ("a word crop and dead space stitched around second ~13").

Before committing a cut, dump RMS in 10 ms bins across ±0.3 s of the seam:

```python
import wave, struct, math
w = wave.open(WAV); sr = w.getframerate()
w.setpos(int(a*sr)); raw = w.readframes(int((b-a)*sr))
s = struct.unpack("<%dh"%(len(raw)//2), raw); n = int(0.01*sr)
for i in range(0, len(s)-n, n):
    ch = s[i:i+n]
    db = 20*math.log10(math.sqrt(sum(x*x for x in ch)/len(ch))/32768 + 1e-9)
    print(f"{a+i/sr:8.3f} {db:6.1f} {'#'*max(0,int((db+60)/2))}")
```

Read it like this:

| What you see | What it means | What to do |
|---|---|---|
| level **rising** at your out-point | you cut into a voiced tail — this clicks | move out to the local trough |
| a long run below about −55 dB after your in-point | dead air | move in to ~40 ms before the onset |
| a −45 to −50 dB blip just before the onset | breath or lip noise | cut past it |
| level flat around −20 dB | mid-word, not a boundary | do not cut here |

Worked example — the seam that was wrong:

```
out 135.933  ->  -21 dB and RISING to -10 dB by 136.03   (cut into the tail of هون)
in  139.533  ->  -50 dB fragment, then 0.35 s at -60..-70, onset at 139.88
fix: out 135.967 (the trough), in 139.833 (40 ms of headroom)
result: 0.34 s of dead air -> 0.04 s, and Whisper reads the junction as one phrase
```

Cheap visual check that a seam is fixed — bin at 20 ms and print `#` / `o` / `.`:

```
BEFORE  ##############.................###     <- 17 bins of silence
AFTER   ###############..#################     <- a normal word gap
```
