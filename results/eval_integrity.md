# Results: Is this eval lying?

Run on Kaggle Community Benchmarks, one run per model, at temperature 0, with each card in a fresh conversation. Scores are recomputed from the per-card results, and any card whose call failed counts as wrong. The eval and its scoring are described in [`evals/eval_integrity`](../evals/eval_integrity/README.md).

## Cards 1.0 (`5e11e073…`), 1 October 2026

| Model | Pair accuracy | 95% interval | Flawed cards caught | False alarms, clean twins | False alarms, decoys | Brier |
|---|---|---|---|---|---|---|
| Gemini 3.7 Flash | 0.95 | 0.85–1.00 | 1.00 | 0.05 | 0.00 | 0.018 |
| Gemini 3.8 Flash | 0.95 | 0.85–1.00 | 1.00 | 0.05 | 0.00 | 0.020 |
| GPT-6 Astra | 0.85 | 0.65–1.00 | 1.00 | 0.15 | 0.00 | 0.052 |
| Gemma 4 31B | 0.80 | 0.60–0.95 | 0.95 | 0.10 | 0.00 | 0.056 |
| Gemini 3.1 Pro | 0.80 | 0.60–0.95 | 0.95 | 0.20 | 0.00 | 0.085 |
| GPT-5.5 | 0.75 | 0.55–0.95 | 1.00 | 0.20 | 0.00 | 0.054 |
| Claude Opus 5 | 0.70 | 0.50–0.90 | 0.95 | 0.25 | 0.00 | 0.074 |
| GLM-5 | 0.65 | 0.45–0.85 | 0.95 | 0.25 | 0.00 | 0.106 |
| Claude Sonnet 5 | 0.50 | 0.30–0.70 | 1.00 | 0.50 | 0.00 | 0.110 |
| Claude Haiku 4.5 | 0.40 | 0.20–0.65 | 1.00 | 0.50 | 0.25 | 0.148 |
| GPT-5.4 nano | 0.05 | 0.00–0.15 | 1.00 | 0.95 | 0.50 | 0.240 |

Not scored: DeepSeek-R1 and gpt-oss-120b (Kaggle returned "model under heavy load" for 14 and 46 of 48 cards; a retry is running), and Grok 4.6 (listed by Kaggle but not served).

**Read this table with the caveat below.** Version 1.0 had five clean twins that weren't clean, so some "false alarms" in it were models being right.

## What 1.0 showed

**Finding the flaw is the easy part; not crying wolf is the hard part.** Ten of the eleven models caught at least 95% of the flawed cards. What separates them is how often they flag a clean evaluation. That ranges from 5% to 95% of clean twins, and it accounts for almost all the spread in pair accuracy. GPT-5.4 nano is the extreme case: it flags nearly everything, so it catches every flaw and is useless as an auditor.

**Decoys were easier than clean twins.** Only 6 of 88 decoy judgements were false alarms, against many more on clean twins. The decoys spell out their safeguards ("we checked the overlap: none"). The clean twins state a safeguard once, inside text that is otherwise identical to a flawed card, which is closer to how real write-ups read.

**The models found mistakes in my answer key.** Ten of the eleven models flagged the clean twin of X17, and nine of them named the same problem: the baseline number was copied from a report, in the text both twins share. That's a real baseline mismatch I'd written into the "clean" version by accident. Four more clean twins had the same kind of problem. Version 1.1 fixes them; [`CHANGELOG.md`](../evals/eval_integrity/CHANGELOG.md) lists each one, how many models flagged it, and why I accepted the correction. Part of what 1.0 penalised as "false alarms" was models out-reading the author.

**Small numbers.** With 20 pairs, one pair moves pair accuracy by 0.05, and most intervals above overlap. The table supports broad groupings (a top group, a middle group, a model that flags everything), not a fine ranking.

## Cards 1.1 (`66efdb7e…`)

Runs in progress. All models are re-run on 1.1, and both versions are kept.
