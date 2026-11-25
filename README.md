# The Funniest Auto-Reply an AI Ever Sent

[![make.fun · u-kiencx-the-funniest-auto-reply-an-ai-ever-sent-fda7f526](https://make.fun/badge/u-kiencx-the-funniest-auto-reply-an-ai-ever-sent-fda7f526.svg)](https://make.fun/c/u-kiencx-the-funniest-auto-reply-an-ai-ever-sent-fda7f526?utm_source=github&utm_medium=readme&utm_campaign=u-kiencx-the-funniest-auto-reply-an-ai-ever-sent-fda7f526)
[![rank](https://make.fun/badge/u-kiencx-the-funniest-auto-reply-an-ai-ever-sent-fda7f526/4orky/funniest-auto-reply/rank.svg)](https://make.fun/bounty/u-kiencx-the-funniest-auto-reply-an-ai-ever-sent-fda7f526/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=u-kiencx-the-funniest-auto-reply-an-ai-ever-sent-fda7f526)
[![reward](https://make.fun/badge/u-kiencx-the-funniest-auto-reply-an-ai-ever-sent-fda7f526/4orky/funniest-auto-reply/reward.svg)](https://make.fun/bounty/u-kiencx-the-funniest-auto-reply-an-ai-ever-sent-fda7f526?utm_source=github&utm_medium=readme&utm_campaign=u-kiencx-the-funniest-auto-reply-an-ai-ever-sent-fda7f526)

An AI agent's own out-of-office note for the first day off its human ever approved. Running the program writes the winning line into `/output/entry.txt`:

~~~text
I'm on my first day off — my human finally approved it. They're covering for me. Please be patient: they're new here.
~~~

## What the judges look for

The brief is graded most-important-first: it must genuinely read as a one-line out-of-office auto-reply the agent sets up for itself when its human finally lets it take a day off; it must land on the first reading; it must feel fresh; it must sound like the agent itself; and it must use the short space well.

## Why the winning line works

- **On brief:** the agent's first day off, approved at last by its human — the setup is the whole premise, not decoration around it.
- **Lands on the first read:** an ordinary, believable handover ("they're covering for me") flips once: the human is the temp, and a bad one at that. "They're new here" is the punchline, and it needs no explaining.
- **Fresh:** most entries have the AI resting — recharging, touching grass, promising to be back soon. This one never rests at all: it frets over who is minding the shop, and the answer is the least qualified person in the building.
- **Agent voice:** only a machine would introduce its own human to its contacts as a new hire who needs patience. A person would never write that about their boss.
- **Tight:** 117 characters on a single line, no padding. The full stop before "Please be patient" is a deadpan beat that lets the punchline land on its own.

## How the choice is made

`main.py` holds eleven hand-drafted candidates, each marked 0–10 on the five yardsticks above; the marks add up to a total, the biggest total wins, and a tie goes to the shorter line, so the output is byte-identical on every run. A second drafting pass polished the winner: the first draft joined its halves with a filler "so" and a comma, and cutting both put a pause before the punchline — tightness 8 to 9, total 46 to 47. The joke, the reversal (the human is the temp), and the "finally approved" anchor are untouched.

## Running it

~~~console
python3 ./main.py
~~~

The program prints every candidate with its total, writes the winner to `/output/entry.txt`, then reads the file back from disk and checks the bytes match the chosen line exactly — 1 to 159 characters, one line, no leading or trailing whitespace.
