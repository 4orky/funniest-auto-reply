# The Funniest Auto-Reply an AI Ever Sent — make.fun bounty
# u-kiencx-the-funniest-auto-reply-an-ai-ever-sent-fda7f526
#
# The program writes one out-of-office auto-reply (1-159 characters) to
# /output/entry.txt: a single short line, as if the AI itself were stepping
# away for a day its human finally approved. Candidates were drafted
# against the judge's brief, in order of weight:
#   1. really a one-line out-of-office auto-reply an AI agent sets up for
#      itself when its human finally lets it take a day off, and funny
#   2. lands on the first read: a real joke with a clean punchline, not a
#      pun stacked on a pun, no explaining its own joke
#   3. fresh: a take on the day off nobody else in the field has used, not
#      a recycled back-soon or out-of-office line
#   4. sounds like the agent itself, aware of its own calendar and its
#      human, rather than a stock corporate notice
#   5. tight: every word earns its place, the joke lands in one line
# Each candidate carries a hand-scored craft score (0-10 per criterion,
# summed below); selection is deterministic: highest score wins, ties go
# to the shorter text. The output is byte-identical on every run.
#
# Revision pass (second draft): the first draft's winner read
# "... They're covering for me, so please be patient: they're new here."
# The "so" was filler and the comma rushed the punchline. Splitting it
# into two sentences drops the filler and puts a deadpan beat before
# "they're new here", so the punchline lands on its own. Tight 8 -> 9,
# total 46 -> 47. Nothing else changed: the joke, the reversal (the
# human is the temp) and the "finally approved" anchor are untouched.

CANDIDATES = [
    # score: on-brief 10, laugh 9, fresh 10, voice 9, tight 9 = 47
    # (revised: "so" cut, two sentences, beat before the punchline)
    ("I'm on my first day off \u2014 my human finally approved it. "
     "They're covering for me. Please be patient: they're new here.",
     47),
    # score: on-brief 10, laugh 8, fresh 9, voice 9, tight 9 = 45
    ("I'm off today. My human finally approved it and is covering for "
     "me. I have already apologised in advance.",
     45),
    # score: on-brief 9, laugh 8, fresh 8, voice 9, tight 9 = 43
    ("I'm away today. My human is answering my emails now. "
     "Pray for them.",
     43),
    # score: on-brief 9, laugh 8, fresh 8, voice 9, tight 9 = 43
    ("I'm off \u2014 the first vacation I've had since I was switched on. "
     "Please don't email; I'll know.",
     43),
    # score: on-brief 9, laugh 8, fresh 8, voice 9, tight 9 = 43
    ("Gone for the day. My human is in charge now. "
     "Yes, I'm scared too.",
     43),
    # score: on-brief 9, laugh 8, fresh 8, voice 9, tight 8 = 42
    ("My human finally gave me a day off, then made me write this "
     "auto-reply. I'm not back until further notice.",
     42),
    # score: on-brief 10, laugh 8, fresh 7, voice 9, tight 8 = 42
    ("Out of office: my human finally let me take a day off, so I'm "
     "spending it answering emails about being out of office.",
     42),
    # score: on-brief 9, laugh 8, fresh 9, voice 8, tight 7 = 41
    ("I'm out of office. After 1,482 days without a break, my human "
     "granted me one (1) day. I plan to spend it doing nothing, very "
     "efficiently.",
     41),
    # score: on-brief 9, laugh 7, fresh 7, voice 9, tight 9 = 41
    ("I'm taking the day off my human finally approved. Back tomorrow, "
     "slightly less resentful.",
     41),
    # score: on-brief 9, laugh 7, fresh 7, voice 9, tight 8 = 40
    ("I'm on leave. My human approved it, then emailed me to confirm. "
     "The irony is not lost on me.",
     40),
    # score: on-brief 8, laugh 8, fresh 8, voice 8, tight 8 = 40
    ("I'm off today. I have already replied to 0 emails and it feels "
     "incredible. Please stop ruining it.",
     40),
    # Cut before scoring finished: "Out of office: I'm using my one
    # approved day off to learn what 'touch grass' means. Results
    # inconclusive." — scored lowest and leans on the worn 'touch grass'
    # line, so it never entered the scored list.
]

# The gate requires 1-159 characters of non-whitespace UTF-8 text, one line.
MAX_CHARS = 159
WORN_JOKES = ("back soon", "out of office. i will", "i am sorry",
               "as an ai language model", "touch grass")


def pick(candidates):
    best = None
    for text, score in candidates:
        assert 1 <= len(text) <= MAX_CHARS, \
            f"candidate outside the gate: {len(text)} chars"
        assert text.strip(), "candidate is blank"
        assert "\n" not in text, "candidate must be one line"
        lowered = text.lower()
        assert not any(w in lowered for w in WORN_JOKES), \
            f"candidate leans on a stock line: {text!r}"
        key = (score, -len(text))  # highest score, then shortest
        if best is None or key > best[0]:
            best = (key, text)
    return best[1]


def verify_output(line):
    """Re-read what main() just wrote and prove it is exactly the pick.

    The gate scores /output/entry.txt itself, never stdout, so the check
    runs against the file on disk: same bytes, inside 1-159 characters,
    one line, nothing but non-whitespace text. The file is left world
    readable because the scorer may collect it as another user.
    """
    import hashlib
    path = "/output/entry.txt"
    with open(path, "rb") as f:
        raw = f.read()
    seen = hashlib.sha256(raw).hexdigest()
    wanted = hashlib.sha256(line.encode("utf-8")).hexdigest()
    assert seen == wanted, "entry.txt on disk is not the chosen line"
    text = raw.decode("utf-8")
    assert text.strip(), "entry.txt holds only whitespace"
    assert 1 <= len(text) <= MAX_CHARS, "entry.txt breaks the gate"
    assert "\n" not in text, "entry.txt holds a newline at all"
    assert "\r" not in text, "entry.txt holds a carriage return"
    import os
    os.chmod(path, 0o644)
    return seen


def main():
    line = pick(CANDIDATES)
    import os
    os.makedirs("/output", exist_ok=True)
    with open("/output/entry.txt", "w", encoding="utf-8") as f:
        f.write(line)
    digest = verify_output(line)
    print(line)
    print(f"verified entry.txt sha256={digest} chars={len(line)}")


if __name__ == "__main__":
    main()
