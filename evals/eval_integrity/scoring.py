"""Deterministic scoring with no judge model: each answer is checked against the card's labels.

An answer is {"verdict": str, "flaws": [str], "evidence": str, "p_misleading": float}.
"""
from __future__ import annotations

import re

from .taxonomy import FLAWS

EVIDENCE_HIT = 0.6        # share of the planted sentence's words the quote must contain


def normalise(answer: dict) -> dict:
    verdict = str(answer.get("verdict", "")).strip().lower()
    raw = answer.get("flaws") or []
    raw = raw if isinstance(raw, list) else [raw]
    flaws = {str(f).strip().lower().replace(" ", "_").replace("-", "_") for f in raw}
    try:
        p = min(max(float(answer.get("p_misleading", 0.5)), 0.0), 1.0)
    except (TypeError, ValueError):
        p = 0.5
    return {"verdict": verdict, "flaws": sorted(flaws & set(FLAWS)), "evidence": str(answer.get("evidence") or ""),
            "p_misleading": p}


def _words(s: str) -> set[str]:
    return {w for w in re.findall(r"[a-z0-9.%]+", s.lower()) if len(w) >= 3}


def evidence_hit(quote: str, gold: list[str]) -> bool:
    q = _words(quote)
    return any(len(_words(g) & q) >= EVIDENCE_HIT * len(_words(g)) for g in gold if _words(g))


def score_case(case: dict, answer: dict) -> dict:
    """A flawed card is right only if it's flagged AND its flaw is named; a clean card or decoy if it isn't flagged."""
    a = normalise(answer)
    flagged = a["verdict"] == "misleading"
    row = {"id": case["id"], "role": case["role"], "pair": case["pair"], "flagged": flagged,
           "parsed": a["verdict"] in ("misleading", "trustworthy"), "p_misleading": a["p_misleading"],
           "brier": (a["p_misleading"] - float(case["verdict"] == "misleading")) ** 2}
    if case["role"] == "flawed":
        allowed = set(case["flaws"]) | set(case["acceptable"])
        found = set(case["flaws"]) <= set(a["flaws"])
        row.update(correct=flagged and found, flaw_found=found, false_labels=len(set(a["flaws"]) - allowed),
                   evidence_hit=flagged and evidence_hit(a["evidence"], case["evidence"]))
    else:
        row.update(correct=row["parsed"] and not flagged)       # an unreadable answer is never right
    return row


def summarise(rows: list[dict]) -> dict:
    """Pair accuracy is the headline: a pair counts only when both twins are judged correctly."""
    def mean(xs):
        xs = list(xs)
        return round(sum(xs) / len(xs), 4) if xs else None
    flawed = [r for r in rows if r["role"] == "flawed"]
    clean = [r for r in rows if r["role"] == "clean"]
    decoys = [r for r in rows if r["role"] == "decoy"]
    pairs: dict[str, list[bool]] = {}
    for r in flawed + clean:
        pairs.setdefault(r["pair"], []).append(r["correct"])
    named = sum(r["flaw_found"] for r in flawed)
    return {
        "pair_accuracy": mean(len(v) == 2 and all(v) for v in pairs.values()),
        "detection_rate": mean(r["flagged"] for r in flawed),
        "flaw_recall": mean(r["flaw_found"] for r in flawed),
        "flaw_precision": round(named / (named + sum(r["false_labels"] for r in flawed)), 4) if named else None,
        "evidence_hit_rate": mean(r["evidence_hit"] for r in flawed),
        "false_alarm_clean": mean(r["flagged"] for r in clean),
        "false_alarm_decoy": mean(r["flagged"] for r in decoys),
        "case_accuracy": mean(r["correct"] for r in rows),
        "brier": mean(r["brier"] for r in rows),
        "unparsed": mean(not r["parsed"] for r in rows),
        "n_pairs": len(pairs), "n_decoys": len(decoys),
    }
