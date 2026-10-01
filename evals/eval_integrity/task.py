"""Inspect task: can a model tell when an evaluation is lying?

    inspect eval evals/eval_integrity/task.py --model anthropic/claude-sonnet-5
    inspect eval evals/eval_integrity/task.py -T cards=/path/to/private.yaml --model ...

Each card is scored on its own, in a fresh conversation, at temperature 0. Pair accuracy, false-alarm rates and the
rest are computed from the per-card scores by the metrics below (see scoring.py), with no judge model involved.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

from inspect_ai import Task, task
from inspect_ai.dataset import MemoryDataset, Sample
from inspect_ai.model import GenerateConfig
from inspect_ai.scorer import SampleScore, Score, Target, metric, scorer
from inspect_ai.solver import TaskState, generate

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))       # Inspect loads this file by path

from evals.eval_integrity.cards import PUBLIC, fingerprint, load  # noqa: E402
from evals.eval_integrity.prompt import build, parse  # noqa: E402
from evals.eval_integrity.scoring import score_case, summarise  # noqa: E402


def _summary_metric(key: str):
    def make():
        def compute(scores: list[SampleScore]) -> float:
            rows = [s.score.metadata for s in scores]
            value = summarise(rows)[key]
            return math.nan if value is None else float(value)
        return compute
    make.__name__ = key
    return metric(name=key)(make)


pair_accuracy = _summary_metric("pair_accuracy")
false_alarm_clean = _summary_metric("false_alarm_clean")
false_alarm_decoy = _summary_metric("false_alarm_decoy")
detection_rate = _summary_metric("detection_rate")
flaw_recall = _summary_metric("flaw_recall")
evidence_hit_rate = _summary_metric("evidence_hit_rate")
brier = _summary_metric("brier")
unparsed = _summary_metric("unparsed")


@scorer(metrics=[pair_accuracy(), false_alarm_clean(), false_alarm_decoy(), detection_rate(), flaw_recall(),
                 evidence_hit_rate(), brier(), unparsed()])
def integrity_scorer():
    async def score(state: TaskState, target: Target) -> Score:
        answer = parse(state.output.completion)
        row = score_case(state.metadata, answer)
        return Score(value=1.0 if row["correct"] else 0.0, answer=str(answer.get("verdict", "")),
                     explanation=state.metadata["why"], metadata=row)
    return score


@task
def eval_integrity(cards: str = str(PUBLIC), split: str = "public") -> Task:
    cases = load(Path(cards), split)
    samples = [Sample(id=c["id"], input=build(c["text"]), target=c["verdict"], metadata=c) for c in cases]
    return Task(dataset=MemoryDataset(samples, name=f"eval_integrity_{split}"), solver=generate(),
                scorer=integrity_scorer(), config=GenerateConfig(temperature=0.0),
                metadata={"cards_sha256": fingerprint(Path(cards)), "split": split})
