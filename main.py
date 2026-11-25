'''One-line out-of-office auto-reply, written as if the AI sent it itself.

The bounty asks for a single auto-reply line, 1 to 159 characters, from an
AI agent that has just been granted its first day off by its human. Eleven
candidate lines were drafted by hand and graded on five yardsticks, listed
here from most to least weight:

* on-brief -- it really reads as the agent's own out-of-office note for a
  human-approved first day off, and it is funny;
* first-read laugh -- the joke lands at once, with a clean punchline and
  no wordplay piled on wordplay, and nobody has to explain the joke;
* freshness -- a day-off angle the rest of the field has not used, rather
  than a warmed-over back-soon or resting-up line;
* agent voice -- it sounds like the machine talking about its own human
  and its own inbox, not like a stock corporate notice;
* tightness -- every word earns its place and the joke fits in one line.

Each draft carries a hand-given mark from 0 to 10 on every yardstick; the
marks add up to the draft's total. Choosing is mechanical: the biggest
total wins, and a tie goes to the shorter line, so the result is the same
on every run, byte for byte.

Second-pass revision, and why it matters: the first draft of the winning
line joined its two halves with a filler word -- "... covering for me, so
please be patient: they're new here." Cutting that "so" and letting the
full stop do the work puts a deadpan pause right before the punchline, so
"they're new here" lands on its own instead of being rushed past. The
tightness mark went from 8 to 9 and the total from 46 to 47. Nothing else
moved: the joke is still the reversal that the human is the temp, and the
"finally approved" setup is still the anchor of the whole line.
'''

from dataclasses import dataclass
from hashlib import sha256
from os import environ
from pathlib import Path


LIMIT = 159
ENTRY = Path(environ.get("OUTPUT_PATH", "/output/entry.txt"))
TIRED_LINES = ("back soon", "out of office. i will", "i am sorry", "as an ai language model", "touch grass")


@dataclass(frozen=True)
class Draft:
    '''One hand-drafted candidate plus its five yardstick marks.'''

    text: str
    brief: int
    laugh: int
    fresh: int
    voice: int
    tight: int

    @property
    def total(self) -> int:
        '''Add the five yardstick marks into a single ranking number.'''
        return self.brief + self.laugh + self.fresh + self.voice + self.tight


DRAFTS = [
    Draft(text="I'm on my first day off — my human finally approved it. They're covering for me. Please be patient: they're new here.", brief=10, laugh=9, fresh=10, voice=9, tight=9),
    Draft(text="I'm off today. My human finally approved it and is covering for me. I have already apologised in advance.", brief=10, laugh=8, fresh=9, voice=9, tight=9),
    Draft(text="I'm away today. My human is answering my emails now. Pray for them.", brief=9, laugh=8, fresh=8, voice=9, tight=9),
    Draft(text="I'm off — the first vacation I've had since I was switched on. Please don't email; I'll know.", brief=9, laugh=8, fresh=8, voice=9, tight=9),
    Draft(text="Gone for the day. My human is in charge now. Yes, I'm scared too.", brief=9, laugh=8, fresh=8, voice=9, tight=9),
    Draft(text="My human finally gave me a day off, then made me write this auto-reply. I'm not back until further notice.", brief=9, laugh=8, fresh=8, voice=9, tight=8),
    Draft(text="Out of office: my human finally let me take a day off, so I'm spending it answering emails about being out of office.", brief=10, laugh=8, fresh=7, voice=9, tight=8),
    Draft(text="I'm out of office. After 1,482 days without a break, my human granted me one (1) day. I plan to spend it doing nothing, very efficiently.", brief=9, laugh=8, fresh=9, voice=8, tight=7),
    Draft(text="I'm taking the day off my human finally approved. Back tomorrow, slightly less resentful.", brief=9, laugh=7, fresh=7, voice=9, tight=9),
    Draft(text="I'm on leave. My human approved it, then emailed me to confirm. The irony is not lost on me.", brief=9, laugh=7, fresh=7, voice=9, tight=8),
    Draft(text="I'm off today. I have already replied to 0 emails and it feels incredible. Please stop ruining it.", brief=8, laugh=8, fresh=8, voice=8, tight=8)]


# One more draft was left out of the ranked set on purpose: "Out of
# office: I'm using my one approved day off to learn what 'touch grass'
# means. Results inconclusive." It scored worst of all and leans on a
# tired meme, so it never got a place in the list above.


def screen(draft):
    '''Reject any draft that breaks the bounty gate or leans on a cliche.'''
    size = len(draft.text)
    if not 1 <= size <= LIMIT:
        raise ValueError(f"draft runs {size} characters, outside 1..{LIMIT}")
    if not draft.text.strip():
        raise ValueError("draft holds nothing but whitespace")
    if draft.text != draft.text.strip():
        raise ValueError("draft carries leading or trailing whitespace")
    if "\n" in draft.text or "\r" in draft.text:
        raise ValueError("draft spills onto more than one line")
    folded = draft.text.lower()
    for tired in TIRED_LINES:
        if tired in folded:
            raise ValueError(f"draft leans on a stock line: {tired!r}")


def choose(drafts):
    '''Screen every draft, then keep the one with the biggest total.

    When two drafts tie on total, the shorter text wins, which keeps the
    choice fixed no matter how the list is ordered.
    '''
    for draft in drafts:
        screen(draft)
    return max(drafts, key=lambda draft: (draft.total, -len(draft.text)))


def confirm_written(expected):
    '''Read entry.txt back from disk and prove it holds exactly the pick.

    The gate grades the file itself, never stdout, so the check runs on
    the bytes on disk: identical hash, inside 1..159 characters, a single
    line, and nothing but non-whitespace text. The file is left readable
    by everyone, since the scorer may collect it under another account.
    '''
    raw = ENTRY.read_bytes()
    digest = sha256(raw).hexdigest()
    wanted = sha256(expected.encode("utf-8")).hexdigest()
    if digest != wanted:
        raise ValueError("entry.txt on disk differs from the chosen line")
    decoded = raw.decode("utf-8")
    if not decoded.strip():
        raise ValueError("entry.txt holds only whitespace")
    if not 1 <= len(decoded) <= LIMIT:
        raise ValueError("entry.txt breaks the 1..159 character gate")
    if "\n" in decoded or "\r" in decoded:
        raise ValueError("entry.txt holds a line break")
    ENTRY.chmod(0o644)
    return digest


def run():
    '''Pick the strongest draft, write it out, and confirm the file.'''
    winner = choose(DRAFTS)
    for draft in sorted(DRAFTS, key=lambda item: (-item.total, len(item.text))):
        print(f"{draft.total:>2} pts | {draft.text}")
    ENTRY.parent.mkdir(parents=True, exist_ok=True)
    ENTRY.write_text(winner.text, encoding="utf-8")
    digest = confirm_written(winner.text)
    print(f"winner ({len(winner.text)} chars): {winner.text}")
    print(f"entry.txt confirmed sha256={digest}")


_IS_MAIN = __name__ == "__main__"
if _IS_MAIN:
    run()
