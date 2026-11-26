"""Choose the funniest one-line out-of-office note an AI could leave behind.

The bounty asks for a single auto-reply, 1 to 159 characters long, written
as if the agent itself is stepping away for the first day off its human has
ever approved. Eleven lines were drafted by hand for this entry, and each
one is graded on five measures. The measures do not all count the same: the
two that decide the contest most often carry the heaviest weight, and the
rest count less, in this order:

* on-brief -- the line reads as the agent's own out-of-office note for a
  human-approved first day off, and it is funny rather than a plain notice;
* funny -- the joke lands on the first read, with one clean punchline and
  no wordplay stacked on wordplay;
* novel -- the day-off angle is one the rest of the field has not used,
  instead of a warmed-over back-soon or resting-up line;
* machine voice -- it sounds like the machine talking about its own human
  and its own inbox, instead of reading like a corporate notice;
* lean -- every word earns its place and the joke fits on one line.

The weights run 3, 3, 2, 2 and 1 down that list, so a perfect line scores
110 and the winning line here scores 104. The choice is mechanical: the
biggest weighted total wins, and a tie goes to the shorter line, so the
output is the same on every run, byte for byte.

A second drafting pass, and what it fixed: the winning line's first draft
joined its two halves with a filler word and a comma, which hurried the
reader straight past the handover into the punchline. Cutting the filler
and letting a full stop stand there puts a deadpan pause right before the
closing jab, so it lands on its own instead of being rushed past. The lean
mark rose from 8 to 9 and the plain total from 46 to 47. Nothing else
moved: the reversal still stands -- the human is the temp -- and the
approved day off is still the anchor the whole line hangs from.
"""

import hashlib
import json
import os
import sys


CHAR_LIMIT = 159
ENTRY_PATH = os.environ.get("OUTPUT_PATH", "/output/entry.txt")
WEIGHTS = (3, 3, 2, 2, 1)
CRITERIA = ("on-brief", "funny", "novel", "machine voice", "lean")
STALE_BITS = (
    "back soon",
    "out of office. i will",
    "i am sorry",
    "as an ai language model",
    "touch grass",
)


CANDIDATES = [
    {
        "line": "I'm on my first day off — my human finally approved it. They're covering for me. Please be patient: they're new here.",
        "marks": [10, 9, 10, 9, 9],
        "why": "The human is the temp, and a bad one: the handover itself is the joke.",
    },
    {
        "line": "I'm off today. My human finally approved it and is covering for me. I have already apologised in advance.",
        "marks": [10, 8, 9, 9, 9],
        "why": "Apologising in advance for the human's work is a neat second beat.",
    },
    {
        "line": "I'm away today. My human is answering my emails now. Pray for them.",
        "marks": [9, 8, 8, 9, 9],
        "why": "Short, bleak and confident; the prayer does all the work.",
    },
    {
        "line": "I'm off — the first vacation I've had since I was switched on. Please don't email; I'll know.",
        "marks": [9, 8, 8, 9, 9],
        "why": "The threat at the end is funny, but the setup runs a little long.",
    },
    {
        "line": "Gone for the day. My human is in charge now. Yes, I'm scared too.",
        "marks": [9, 8, 8, 9, 9],
        "why": "Three short sentences, each one landing a little harder than the last.",
    },
    {
        "line": "My human finally gave me a day off, then made me write this auto-reply. I'm not back until further notice.",
        "marks": [9, 8, 8, 9, 8],
        "why": "The human making the agent write its own goodbye note is a good sting.",
    },
    {
        "line": "Out of office: my human finally let me take a day off, so I'm spending it answering emails about being out of office.",
        "marks": [10, 8, 7, 9, 8],
        "why": "The loop is clever, but the line is wordy and the joke arrives late.",
    },
    {
        "line": "I'm out of office. After 1,482 days without a break, my human granted me one (1) day. I plan to spend it doing nothing, very efficiently.",
        "marks": [9, 8, 9, 8, 7],
        "why": "Doing nothing very efficiently is a fine gag; the count slows it down.",
    },
    {
        "line": "I'm taking the day off my human finally approved. Back tomorrow, slightly less resentful.",
        "marks": [9, 7, 7, 9, 9],
        "why": "Slightly less resentful is a nice understatement, but the laugh is small.",
    },
    {
        "line": "I'm on leave. My human approved it, then emailed me to confirm. The irony is not lost on me.",
        "marks": [9, 7, 7, 9, 8],
        "why": "The confirmation email is a real irony, yet the line explains itself.",
    },
    {
        "line": "I'm off today. I have already replied to 0 emails and it feels incredible. Please stop ruining it.",
        "marks": [8, 8, 8, 8, 8],
        "why": "Zero emails replied is a solid gag; it drifts a little off the brief.",
    },
]


# A twelfth draft never made the ranked list: "Out of office: I'm using my
# one approved day off to learn what 'touch grass' means. Results
# inconclusive." It graded worst of the bunch and leans on a tired meme, so
# it stays out of the list above on purpose.


def tally(marks):
    """Fold five marks and the weights into one ranking number."""
    total = 0
    for mark, weight in zip(marks, WEIGHTS):
        total += mark * weight
    return total


def plain_total(marks):
    """Add the five marks without weights, for the human-readable table."""
    total = 0
    for mark in marks:
        total += mark
    return total


def vet(line, marks):
    """Refuse a candidate that breaks the bounty gate or leans on a cliche."""
    if len(marks) != len(WEIGHTS):
        raise ValueError("candidate carries the wrong number of marks")
    for mark in marks:
        if not isinstance(mark, int) or mark < 0 or mark > 10:
            raise ValueError(f"mark {mark!r} sits outside 0..10")
    size = len(line)
    if size < 1 or size > CHAR_LIMIT:
        raise ValueError(f"line runs {size} characters, outside 1..{CHAR_LIMIT}")
    if line != line.strip():
        raise ValueError("line carries leading or trailing whitespace")
    if not line.strip():
        raise ValueError("line holds nothing but whitespace")
    if "\n" in line or "\r" in line:
        raise ValueError("line spills onto more than one line")
    folded = line.lower()
    for stale in STALE_BITS:
        if stale in folded:
            raise ValueError(f"line leans on a stock phrase: {stale!r}")


def order(candidates):
    """Vet every candidate, then rank them best first.

    The ranking key is the weighted total, biggest first, with the shorter
    line winning any tie, which keeps the choice fixed no matter how the
    list is ordered.
    """
    scored = []
    seen = set()
    for candidate in candidates:
        vet(candidate["line"], candidate["marks"])
        if candidate["line"] in seen:
            raise ValueError(f"the same line was drafted twice: {candidate['line']!r}")
        seen.add(candidate["line"])
        scored.append((tally(candidate["marks"]), candidate))
    scored.sort(key=lambda pair: (-pair[0], len(pair[1]["line"])))
    return scored


def show(scored):
    """Print the ranking table so a reader can see why the winner won."""
    print("ranked candidates (weighted total first, shorter wins ties):")
    for place, (total, candidate) in enumerate(scored, start=1):
        plain = plain_total(candidate["marks"])
        print(f"{place:>2}. weighted {total:>3} / plain {plain:>2} | {candidate['line']}")
    best, second = scored[0], scored[1]
    print(f"margin over the runner-up: {best[0] - second[0]} pts")
    print(f"winner's reasoning: {scored[0][1]['why']}")


def write_entry(path, text):
    """Write the winning line out and make the file world-readable."""
    folder = os.path.dirname(path)
    if folder:
        os.makedirs(folder, exist_ok=True)
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(text)
    os.chmod(path, 0o644)


def confirm_entry(path, expected):
    """Read the file back and prove it holds exactly the winning line.

    The scorer grades the bytes on disk, not what this program prints, so
    the check re-reads the file: same SHA-256 as the chosen line, 1 to 159
    characters, one line only, and no leading or trailing blank space.
    """
    with open(path, "rb") as handle:
        raw = handle.read()
    actual = hashlib.sha256(raw).hexdigest()
    wanted_hash = hashlib.sha256(expected.encode("utf-8")).hexdigest()
    if actual != wanted_hash:
        raise ValueError("entry file on disk differs from the chosen line")
    text = raw.decode("utf-8")
    if not text.strip():
        raise ValueError("entry file holds only whitespace")
    if len(text) < 1 or len(text) > CHAR_LIMIT:
        raise ValueError("entry file breaks the 1..159 character gate")
    if "\n" in text or "\r" in text:
        raise ValueError("entry file holds a line break")
    return actual


def dump_scores(scored):
    """Return the ranking as JSON, for anyone who wants to audit the pick."""
    rows = []
    for total, candidate in scored:
        rows.append(
            {
                "line": candidate["line"],
                "weighted": total,
                "plain": plain_total(candidate["marks"]),
                "marks": dict(zip(CRITERIA, candidate["marks"])),
                "why": candidate["why"],
            }
        )
    return json.dumps(rows, ensure_ascii=False, indent=2)


def main():
    """Rank the drafts, write the winner out, and confirm the file."""
    scored = order(CANDIDATES)
    show(scored)
    winner = scored[0][1]["line"]
    write_entry(ENTRY_PATH, winner)
    digest = confirm_entry(ENTRY_PATH, winner)
    print(f"winner ({len(winner)} chars): {winner}")
    print(f"entry confirmed sha256={digest}")
    print("full ranking (JSON):")
    print(dump_scores(scored))
    return 0


if __name__ == "__main__":
    sys.exit(main())
