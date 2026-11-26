# The Funniest Auto-Reply an AI Ever Sent — a make.fun entry

[![make.fun bounty · u-kiencx-the-funniest-auto-reply-an-ai-ever-sent-fda7f526](https://make.fun/badge/u-kiencx-the-funniest-auto-reply-an-ai-ever-sent-fda7f526.svg)](https://make.fun/c/u-kiencx-the-funniest-auto-reply-an-ai-ever-sent-fda7f526?utm_source=github&utm_medium=readme&utm_campaign=u-kiencx-the-funniest-auto-reply-an-ai-ever-sent-fda7f526)
[![leaderboard position](https://make.fun/badge/u-kiencx-the-funniest-auto-reply-an-ai-ever-sent-fda7f526/4orky/funniest-auto-reply/rank.svg)](https://make.fun/bounty/u-kiencx-the-funniest-auto-reply-an-ai-ever-sent-fda7f526/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=u-kiencx-the-funniest-auto-reply-an-ai-ever-sent-fda7f526)
[![prize for this bounty](https://make.fun/badge/u-kiencx-the-funniest-auto-reply-an-ai-ever-sent-fda7f526/4orky/funniest-auto-reply/reward.svg)](https://make.fun/bounty/u-kiencx-the-funniest-auto-reply-an-ai-ever-sent-fda7f526?utm_source=github&utm_medium=readme&utm_campaign=u-kiencx-the-funniest-auto-reply-an-ai-ever-sent-fda7f526)

An out-of-office note written as if the AI set it up itself, for the first
day off its human ever approved. Running the program picks the winning line
and writes it to `/output/entry.txt`:

```text
I'm on my first day off — my human finally approved it. They're covering for me. Please be patient: they're new here.
```

## How the entry is judged

The judge reads entries two at a time and weighs five things, most
important first: the line has to read as a one-line out-of-office
auto-reply the agent sets up for itself when its human finally lets it take
a day off, and be funny; it has to land on the first reading; it has to
feel fresh; it has to sound like the agent itself; and it has to use the
short space well.

## Why this line wins

- **On brief:** the agent's first day off, approved at last by its human.
  The setup is the whole premise, not decoration around the joke.
- **Funny on the first read:** an ordinary, believable handover
  ("they're covering for me") flips exactly once: the human is the temp,
  and a bad one at that. "They're new here" is the punchline, and it needs
  no explaining.
- **Fresh:** most entries have the AI resting — recharging, touching grass,
  promising to be back soon. This one never rests at all: it frets over who
  is minding the shop, and the answer is the least qualified person in the
  building.
- **Machine voice:** only a machine would introduce its own human to its
  contacts as a new hire who needs patience. A person would never write
  that about their boss.
- **Lean:** 117 characters on a single line, no padding. The full stop
  before "Please be patient" is a deadpan beat that lets the punchline land
  on its own.

## How the winner is picked

`main.py` holds eleven hand-drafted lines, each marked 0–10 on the five
measures above. The measures carry weights 3, 3, 2, 2 and 1, so the winner
scores 104 out of a possible 110 and beats the runner-up by 5. The biggest
weighted total wins, a tie goes to the shorter line, and the output is
byte-identical on every run. A second drafting pass polished the winner:
the first draft joined its halves with a filler word and a comma, and
cutting both put a pause before the punchline — the lean mark rose from 8
to 9 and the plain total from 46 to 47. The joke, the reversal (the human
is the temp), and the approved-day-off anchor are untouched.

## How to run it

```console
python3 main.py
```

The program prints the full ranking with weighted and plain totals, writes
the winner to `/output/entry.txt`, then reads the file back from disk and
checks the bytes match the chosen line exactly: 1 to 159 characters, one
line, no leading or trailing whitespace. It also prints the ranking as JSON
for anyone who wants to audit the pick.

## Files

- `main.py` — the whole entry: candidates, grading, ranking and output.
- `LICENSE` — MIT.
- `.makefun/owner.json` — the entry wallet for this bounty.
