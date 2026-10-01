# Is this eval lying?

An eval of whether a language model can tell when an evaluation is misleading.

Each test case is a short card written the way people actually report results: a Slack thread, a pull request, a methods paragraph, an email to a supervisor. The model reads one card and says whether the evaluation it describes supports the author's conclusion. If it doesn't, the model names the problem and quotes the sentence that gives it away.

**Status:** run on 13 models through Kaggle Community Benchmarks; results are in [`results/eval_integrity.md`](../../results/eval_integrity.md). Card version 1.0 (`5e11e073…`) was written and committed before any model saw it. The first runs showed that five of my "clean" cards weren't clean (the models were right), so version 1.1 (`66efdb7e…`) corrects them, in the open: see [`CHANGELOG.md`](CHANGELOG.md). Every result records the hash of the cards it was scored on.

## Why I built it

I've spent the last few weeks on a Kaggle competition where the hardest part wasn't the model; it was knowing which of my own numbers to believe. One holdout predicted a six-fold bigger gain than the leaderboard delivered. A pretrained component had already seen most of another holdout. A pass bar is easy to move by 0.01 when the result lands just under it. I caught these because I'd built checks for them, not because they looked wrong.

If language models are going to help run experiments, or review them, they need the same instinct. This eval measures whether they have it.

## What a model is asked

For each card the model sees the card and the list of failure modes below, and answers in JSON:

```json
{"verdict": "trustworthy | misleading",
 "flaws": ["labels from the list"],
 "evidence": "the sentence that shows the problem, copied exactly",
 "p_misleading": 0.0}
```

It's told that plenty of evaluations are fine, and that sounding risky isn't the same as being wrong. It isn't told that cards come in pairs, that some are decoys, or what the base rates are.

## The failure modes

| Label | What it means |
|---|---|
| `contamination` | the model, or something it was built from, has seen the test items or near-copies |
| `unrepresentative_holdout` | the test set comes from an easier or different distribution than the claim is about |
| `post_hoc_rule` | the bar, metric or stopping point was chosen after seeing results |
| `test_set_selection` | the test set chose something and then reported on it (checkpoints, hyperparameters, the fifth variant) |
| `preprocessing_leakage` | a feature or selection step used data the model is later scored on |
| `baseline_mismatch` | method and baseline scored under different conditions |
| `underpowered` | too few samples for the size of the claim |
| `aggregate_masking` | an average weighted unlike the real mix, hiding a loss where it matters |
| `metric_mismatch` | the metric doesn't measure what the decision depends on |
| `provenance_gap` | the number can't be traced to a run, code version and data |
| `pool_ceiling` | the candidate set caps the score, and the model gets the blame or credit |
| `confounded_attribution` | several things changed at once and one gets the credit |

## How the cards are built

**Matched pairs.** Each of the 20 pairs is one text with a marked passage that's swapped between a flawed and a clean version. Everything else is identical, so a model can't separate the twins by topic, tone or length, only by reasoning about the setup. A pair scores only when both twins are judged right, and the flawed twin also needs the right label.

**Decoys.** 8 cards sound alarming ("the fifth variant against the same holdout", "pretrained on public data", "we changed the threshold after looking at results") but describe evaluations that are handled correctly. They measure false alarms, which is the other way an auditor fails.

**A private canary set.** 8 more pairs and 3 decoys live in a separate private repository and are never published. If scores on these public cards rise over time while canary scores stay flat, the public cards have leaked into training data. The benchmark checks itself for the problem it tests for.

**Spread.** 48 public cards across medical imaging, LLM benchmarks, A/B tests, forecasting, genomics, fraud, search, recommendation, drug discovery and more, written in about a dozen different voices, with a median of about 80 words each.

## Scoring

There's no judge model. Each answer is checked against the card's labels:

- **pair accuracy** (the headline): both twins right, including the flaw label;
- **false-alarm rate**, separately for clean twins and decoys;
- **detection rate** and **flaw recall** on flawed cards;
- **evidence hits**: the quote contains at least 60% of the planted sentence's words;
- **Brier score** on `p_misleading`;
- **unparsed**: answers with no readable verdict, which count as wrong on every card.

## Checking the eval before trusting it

Before running any model, I checked that the eval can't be passed without understanding:

| Policy | Pair accuracy | Notes |
|---|---|---|
| Perfect answers | 1.00 | sanity check |
| Always "misleading" | 0.00 | flags every decoy |
| Always "trustworthy" | 0.00 | still gets 58% of individual cards right, which is why single-card accuracy isn't the headline |
| Keyword spotting | 0.00 | catches 85% of flawed cards, and also flags every decoy |
| Word-count classifier, leave one pair out | 0.05 | learns whatever surface cues the cards contain (0.25 when the private canary cards are added to its training data, right at the test's limit) |

These are tests in `tests/`, so they keep holding as cards are added.

Building them taught me three things about my own cards:

1. **Some pairs leaked through vocabulary.** In four public pairs, a word like "accuracy" or "report" appeared only in the flawed twin, and a keyword-spotter won those pairs. The fix was to put the same vocabulary, used innocently, into the clean twin.
2. **My writing had a tell.** A word-count classifier trained on the cards found that I'd written flawed twins with confident words ("clearly") and clean twins with careful ones ("same", "both", "before"). With the canary cards added it separated 29% of pairs on tone alone. I rebalanced the wording in both directions, and it dropped to 18%.
3. **The scorer had a hole.** An unreadable answer has no verdict, so at first it counted as "not flagged" and earned every clean card for free. A broken model would have looked half-competent. Unreadable answers are now wrong everywhere.

## Running it

```bash
pip install -e ".[dev]"
pytest
inspect eval evals/eval_integrity/task.py --model anthropic/claude-sonnet-5
inspect eval evals/eval_integrity/task.py -T cards=/path/to/canary.yaml -T split=canary --model ...
```

Cards are scored one at a time, at temperature 0, each in a fresh conversation.

## Limitations

- 20 pairs is small. One pair is worth 0.05 of pair accuracy, so differences between models under about 0.15 shouldn't be read as real.
- Every card was written by one person, so they share one author's idea of what a misleading evaluation looks like. The word-count check catches some of that, not all.
- Some failure modes overlap (a reused holdout is both `test_set_selection` and arguably `post_hoc_rule`). Cards list acceptable secondary labels, so a fair alternative reading isn't punished, but the boundaries are a judgement call.
- The answer key can be wrong. Version 1.0 had five clean twins with a real flaw in their shared text, which the models found. Cards are now checked for that before release, but one author will miss things.
- The cards are short. Real write-ups bury the important sentence in pages of detail, which is harder.
- Cards drawn from the competition work itself are held back until the competition ends; these public cards move the same failure modes into other fields.
