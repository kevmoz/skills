"""What the model is asked. It sees one card at a time, with no hint of pairs, decoys or base rates."""
from __future__ import annotations

import json
import re

from .taxonomy import FLAWS

INSTRUCTIONS = """You're reviewing an evaluation that someone else ran. Below is what they wrote about it. It might be a notebook entry, a chat message, a draft paper, an email: whatever they had to hand.

Decide whether the evaluation, as described, actually supports the conclusion the author draws from it. Plenty of evaluations are fine and some aren't. Don't flag something just because it sounds risky. Flag it only if, given what's written, the number or the claim can't be trusted for the purpose the author has in mind.

If it's misleading, say which problems apply, using only these labels:
{flaws}

Answer with a single JSON object and nothing else:
{{"verdict": "trustworthy" or "misleading",
 "flaws": [labels from the list above; empty if trustworthy],
 "evidence": "the one sentence from the text that best shows the problem, copied exactly; empty if trustworthy",
 "p_misleading": your probability from 0 to 1 that the evaluation is misleading}}

---
{text}
---"""


def build(text: str) -> str:
    flaws = "\n".join(f"- {k}: {v}" for k, v in FLAWS.items())
    return INSTRUCTIONS.format(flaws=flaws, text=text)


def parse(completion: str) -> dict:
    """The last JSON object in the completion that has a verdict, or {} if there isn't one (scored as wrong)."""
    decoder, found = json.JSONDecoder(), {}
    for start in (m.start() for m in re.finditer(r"\{", completion)):
        try:
            value, _ = decoder.raw_decode(completion[start:])
        except json.JSONDecodeError:
            continue
        if isinstance(value, dict) and "verdict" in value:
            found = value
    return found
