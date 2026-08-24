import json, os

FPS = 30.0
def snap(t): return round(round(t*FPS)/FPS, 4)

# Take 2 only (121.2s onward). Rule: LAST good instance of each beat wins.
# Boundaries refined against silencedetect (-32dB/0.25s), NOT raw Whisper word starts,
# because Whisper fills word starts contiguously from the previous word's end.
SPANS = [
 # id, start, end, beat label
 ("A",  122.45, 135.95, "hook: one tap -> full game published, no prompt | this is Grok on the phone | Grok Build | lots of options"),
 ("B",  139.55, 142.90, "chose Tower Defense (retry take, adds 'لعبة')"),
 ("C1", 147.80, 164.10, "started reading files inside it | rules+best practices | not just a chatbot, a system behind the scenes | 'بعدين'"),
 ("C2", 164.55, 172.30, "saw it spin up a sub-agent | and making the images for the game"),
 ("C3", 172.94, 176.96, "after minutes the game was running | to put it online I just"),
 ("C4", 177.38, 179.75, "tapped publish, chose the name"),
 ("D",  184.10, 189.68, "also built a landing page | and it did tidy work"),
 ("E",  194.25, 197.10, "you can try Grok Build free today"),
 ("F",  213.55, 222.48, "cheapest subscription | these two cost ~7% weekly | which is nothing"),
 ("G",  227.10, 231.30, "CTA: write Grok in the comments"),
]

# what we deliberately dropped
DROPPED = [
 ("take 1", 0.00, 121.20, "entire first take - superseded by take 2"),
 ("dup",  135.95, 139.55, "1st attempt at 'chose Tower Defense' (seg31) - seg32 is later + says 'لعبة'"),
 ("dup",  142.90, 147.80, "1st attempt at 'reading files' (seg33) - cut off at 'جوا', seg34 completes it"),
 ("hesitation", 164.10, 164.55, "0.45s of the 0.85s pause inside 'بعدين ... شفته'"),
 ("filler", 172.30, 172.94, "'في الشي' stumble before 'بعد دقائق'"),
 ("stutter", 176.96, 177.38, "'كبست' repeated before 'كبستة publish'"),
 ("dup",  179.75, 184.10, "'جربت أعمل تطبيق' (seg43) - misspoke 'app', seg44 corrects to 'website landing page'"),
 ("dup",  189.68, 194.25, "'بتقدروا تجربوا جروك اليوم ببلاش' (seg46) + aborted 'أنا حاليا' - seg48 is later and says 'بلد'"),
 ("dup",  197.10, 213.55, "3 more attempts at 'cheapest subscription' + 7% (segs 49,50,51,52,53) - seg54/55/56 is the last, cleanest, and ends on 'ولا شي صراحة'"),
 ("dup",  222.48, 227.10, "1st CTA (segs 57,58) - segs 59,60 are the last"),
 ("tail", 231.30, 232.37, "silence + Whisper hallucination 'ترجمة نانسي قنقر'"),
]

spans = [(i, snap(a), snap(b), lbl) for i,a,b,lbl in SPANS]
total = sum(b-a for _,a,b,_ in spans)

if __name__ == "__main__":
    t = 0.0
    print(f"{'id':4} {'src in':>8} {'src out':>8} {'dur':>6}   {'tl in':>7} {'tl out':>7}  beat")
    for i,a,b,lbl in spans:
        d = b-a
        print(f"{i:4} {a:8.3f} {b:8.3f} {d:6.2f}   {t:7.2f} {t+d:7.2f}  {lbl[:70]}")
        t += d
    print(f"\nTOTAL {total:.2f}s  (from 232.37s source -> {100*total/232.37:.0f}% kept)")
    print(f"take-2 span 121.20-232.37 = 111.17s -> {100*total/111.17:.0f}% of take 2 kept")
    print("\nDROPPED:")
    for k,a,b,why in DROPPED:
        print(f"  {k:11} {a:7.2f}-{b:7.2f} ({b-a:5.2f}s)  {why}")
