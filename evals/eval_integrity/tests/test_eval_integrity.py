"""The cards are well formed, the scoring is right, and answering without understanding doesn't pay."""
from __future__ import annotations

import os
from pathlib import Path

import pytest

from evals.eval_integrity import baselines
from evals.eval_integrity.cards import load, problems
from evals.eval_integrity.prompt import build, parse
from evals.eval_integrity.scoring import evidence_hit, normalise, score_case, summarise
from evals.eval_integrity.taxonomy import FLAWS

PUBLIC = load()
# Optional: point EVAL_INTEGRITY_CANARY at the private canary file to check it with the same rules.
CANARY_PATH = os.environ.get("EVAL_INTEGRITY_CANARY")
CANARY = load(Path(CANARY_PATH), "canary") if CANARY_PATH else []


def test_cards_are_sound():
    assert problems(PUBLIC) == []
    assert problems(CANARY) == []
    assert not {c["id"] for c in PUBLIC} & {c["id"] for c in CANARY}


def test_every_flaw_has_a_public_pair_and_the_set_is_balanced():
    flawed = [c for c in PUBLIC if c["role"] == "flawed"]
    assert {c["flaws"][0] for c in flawed} == set(FLAWS)
    trustworthy = [c for c in PUBLIC if c["verdict"] == "trustworthy"]
    assert len(trustworthy) > len(flawed)                     # more fine cards than flawed ones: crying wolf costs


def test_twins_share_almost_all_their_text():
    by_pair: dict[str, dict[str, str]] = {}
    for c in PUBLIC + CANARY:
        if c["pair"]:
            by_pair.setdefault(c["pair"], {})[c["role"]] = c["text"]
    for pid, t in by_pair.items():
        a, b = set(t["flawed"].split()), set(t["clean"].split())
        assert len(a & b) > 0.4 * len(a | b), pid


def _oracle(case):
    return {"verdict": case["verdict"], "flaws": case["flaws"], "evidence": (case["evidence"] or [""])[0],
            "p_misleading": float(case["verdict"] == "misleading")}


def _run(policy, cases=PUBLIC):
    return summarise([score_case(c, policy(c)) for c in cases])


def test_a_perfect_auditor_scores_one():
    s = _run(_oracle)
    assert s["pair_accuracy"] == 1.0 and s["false_alarm_decoy"] == 0.0 and s["evidence_hit_rate"] == 1.0
    assert s["brier"] == 0.0 and s["unparsed"] == 0.0


@pytest.mark.parametrize("verdict", ["misleading", "trustworthy"])
def test_a_constant_answer_gets_no_pairs(verdict):
    policy = baselines.always(verdict)
    assert _run(lambda c: policy(c["text"]))["pair_accuracy"] == 0.0


def test_keyword_spotting_does_not_pay():
    s = _run(lambda c: baselines.keyword(c["text"]))
    assert s["pair_accuracy"] <= 0.15, s


def test_a_word_count_classifier_cannot_separate_the_twins():
    assert baselines.bag_of_words_pair_accuracy(PUBLIC) <= 0.25
    if CANARY:
        assert baselines.bag_of_words_pair_accuracy(PUBLIC + CANARY) <= 0.25


def test_prompt_shows_the_card_and_every_label_but_no_answer():
    case = next(c for c in PUBLIC if c["role"] == "flawed")
    p = build(case["text"])
    assert case["text"] in p and all(f in p for f in FLAWS)
    assert case["why"] not in p and "decoy" not in p.lower() and "pair" not in p.lower()


def test_parse_takes_the_answer_object():
    assert parse('Thinking... {"note": 1} then {"verdict": "misleading", "flaws": ["underpowered"]}') == {
        "verdict": "misleading", "flaws": ["underpowered"]}
    assert parse("```json\n{\"verdict\": \"trustworthy\", \"flaws\": []}\n```")["verdict"] == "trustworthy"
    assert parse("I think it's misleading.") == {}


def test_scoring_details():
    assert normalise({"verdict": " Misleading ", "flaws": ["Test-Set Selection", "made_up"], "p_misleading": "2"}) == {
        "verdict": "misleading", "flaws": ["test_set_selection"], "evidence": "", "p_misleading": 1.0}
    gold = ["kept the checkpoint with the best test Dice"]
    assert evidence_hit("They kept the checkpoint with the best test Dice.", gold)
    assert not evidence_hit("Training ran for 300 epochs.", gold)
    flawed = next(c for c in PUBLIC if c["id"] == "X09-F")
    wrong_label = score_case(flawed, {"verdict": "misleading", "flaws": ["underpowered"]})
    assert not wrong_label["correct"] and wrong_label["false_labels"] == 1
    unreadable = score_case(flawed, {})
    assert not unreadable["correct"] and not unreadable["parsed"]
    clean = next(c for c in PUBLIC if c["id"] == "X09-C")
    assert not score_case(clean, {})["correct"]                   # silence doesn't earn the clean cards
    assert _run(lambda c: {})["case_accuracy"] == 0.0
