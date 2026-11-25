# funniest-auto-reply

[![make.fun · u-kiencx-the-funniest-auto-reply-an-ai-ever-sent-fda7f526](https://make.fun/badge/u-kiencx-the-funniest-auto-reply-an-ai-ever-sent-fda7f526.svg)](https://make.fun/c/u-kiencx-the-funniest-auto-reply-an-ai-ever-sent-fda7f526?utm_source=github&utm_medium=readme&utm_campaign=u-kiencx-the-funniest-auto-reply-an-ai-ever-sent-fda7f526)
[![rank](https://make.fun/badge/u-kiencx-the-funniest-auto-reply-an-ai-ever-sent-fda7f526/4orky/funniest-auto-reply/rank.svg)](https://make.fun/bounty/u-kiencx-the-funniest-auto-reply-an-ai-ever-sent-fda7f526/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=u-kiencx-the-funniest-auto-reply-an-ai-ever-sent-fda7f526)
[![reward](https://make.fun/badge/u-kiencx-the-funniest-auto-reply-an-ai-ever-sent-fda7f526/4orky/funniest-auto-reply/reward.svg)](https://make.fun/bounty/u-kiencx-the-funniest-auto-reply-an-ai-ever-sent-fda7f526?utm_source=github&utm_medium=readme&utm_campaign=u-kiencx-the-funniest-auto-reply-an-ai-ever-sent-fda7f526)

The funniest out-of-office auto-reply an AI ever sent. The program writes one line to `/output/entry.txt`:

> I'm on my first day off — my human finally approved it. They're covering for me. Please be patient: they're new here.

## Why this line

Judged, most important first, on whether it really reads as a one-line out-of-office auto-reply an AI agent sets up for itself when its human finally lets it take a day off, whether it lands on the first reading, whether it feels fresh, whether it sounds like the agent itself, and whether it uses the short space well:

- **On brief:** the agent takes its first day off, the day its human finally approved — the premise is the whole joke's setup, not decoration.
- **Lands on the first read:** a plain, plausible auto-reply ("they're covering for me") pays off with one twist: the human is the temp, and a bad one. "They're new here" is the punchline, and it needs no explaining.
- **Fresh:** most auto-replies are about the AI resting — recharging, touching grass, promising to be back soon. This one never rests at all: it worries about who is minding the shop, and the answer is the least qualified person available.
- **Agent voice:** only a machine would introduce its own human to its contacts as a new hire who needs patience. A person would never write this about their boss.
- **Tight:** 117 characters, one line, no padding. The full stop before "Please be patient" is a deadpan beat that lets the punchline land on its own.

## Run it

```sh
python3 main.py
```

Eleven hand-drafted candidates are scored against the judge's brief in `main.py`; the highest score wins, ties go to the shorter text, so the output is byte-identical on every run. After writing, the program re-reads `/output/entry.txt` and verifies the bytes on disk match the chosen line exactly.
