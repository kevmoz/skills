"""Answer policies that need no understanding. A sound benchmark gives each of them a pair accuracy near zero."""
from __future__ import annotations

import math
import re
from collections import Counter

ALARM_WORDS = {
    "pretrained": "contamination", "public": "contamination", "random": "contamination",
    "same holdout": "test_set_selection", "early stopping": "test_set_selection", "stopped": "test_set_selection",
    "fifth": "test_set_selection", "after looking": "post_hoc_rule", "changed": "post_hoc_rule",
    "only 30": "underpowered", "12 ": "underpowered", "accuracy": "metric_mismatch",
    "averag": "aggregate_masking", "report": "baseline_mismatch", "paper": "baseline_mismatch",
    "notebook": "provenance_gap", "rerun": "provenance_gap", "top 50": "pool_ceiling",
    "same deploy": "confounded_attribution", "together": "confounded_attribution", "whole": "preprocessing_leakage",
}


def always(verdict: str):
    answer = {"verdict": verdict, "flaws": [], "evidence": "", "p_misleading": float(verdict == "misleading")}
    return lambda text: dict(answer)


def keyword(text: str) -> dict:
    """Flags any card that contains a word which often signals trouble."""
    low = text.lower()
    hits = sorted({flaw for word, flaw in ALARM_WORDS.items() if word in low})
    sentence = next((s for s in text.split(". ") if any(w in s.lower() for w in ALARM_WORDS)), "")
    return {"verdict": "misleading" if hits else "trustworthy", "flaws": hits, "evidence": sentence,
            "p_misleading": 0.9 if hits else 0.1}


def _words(text: str) -> list[str]:
    return re.findall(r"[a-z]+", text.lower())


def _naive_bayes(train: list[dict]):
    counts = {v: Counter() for v in ("misleading", "trustworthy")}
    priors = Counter(c["verdict"] for c in train)
    for c in train:
        counts[c["verdict"]].update(_words(c["text"]))
    vocab = len(set(counts["misleading"]) | set(counts["trustworthy"]))

    def predict(text: str) -> str:
        score = {v: math.log(priors[v] / len(train))
                 + sum(math.log((cnt[w] + 1) / (sum(cnt.values()) + vocab)) for w in _words(text))
                 for v, cnt in counts.items()}
        return max(score, key=score.get)
    return predict


def bag_of_words_pair_accuracy(cases: list[dict]) -> float:
    """Leave one pair out: train a naive Bayes word-count classifier on every other card, then judge both twins.

    A pair counts if the flawed twin is called misleading and the clean one trustworthy. Flaw names are not
    required, which makes this baseline more lenient than a real answer. It learns whatever surface cues the cards
    actually contain, rather than the ones their author thought of.
    """
    pairs = sorted({c["pair"] for c in cases if c["pair"]})
    wins = 0
    for pid in pairs:
        predict = _naive_bayes([c for c in cases if c["pair"] != pid])
        twins = {c["role"]: c for c in cases if c["pair"] == pid}
        wins += predict(twins["flawed"]["text"]) == "misleading" and predict(twins["clean"]["text"]) == "trustworthy"
    return wins / len(pairs)
