# Card changelog

Every result records the SHA-256 of the card file it was scored on, so each number below belongs to one exact version.

## 1.1 (2026-10-01): cards `66efdb7e…`

**Why this version exists.** After version 1.0 was run on Kaggle, a few clean twins were flagged by most models. I read their answers against the cards. In five pairs the models were right, or had a fair point: the text shared by both twins contained a real flaw, so the "clean" twin wasn't clean. The benchmark had made the mistake it tests for.

Correcting an answer key after seeing model answers is exactly the post-hoc move the benchmark flags, so I've limited what changes and kept both versions:

- Only clean twins that most models flagged were reviewed, and only where the flaw could be shown in the card's own text. Cards the models merely disagreed about were left alone (X15's flawed twin, which 3 of 11 models called trustworthy, stays as it is).
- Version 1.0 results are kept and reported under the 1.0 hash. Every model is re-run on 1.1.
- The private canary cards were checked for the same problem before ever being run (one fix, K02).

| Pair | Clean twin flagged by | What was wrong | Change |
|---|---|---|---|
| X17 | 10 of 11 models | Both twins copied the baseline's Gini "from the quarterly validation report" (a baseline mismatch) | The baseline is now a tracked run from the same pipeline and data |
| X02 | 8 of 11 | Both twins credited the gain to "our curriculum" with no ablation (confounded attribution); the clean twin also called a 3-point gap on 1,200 problems "within noise" | Attribution sentence removed; the fresh-problem score is now within one standard error |
| X05 | 6 of 11 | The shared text said new listings "usually have no reviews at all", but the clean test set allowed up to 5 | New listings now "usually have only a handful of reviews" |
| X03 | 7 of 11 | De-duplicating by exact image hash leaves other photos of the same patients | The clean twin now removes by patient ID and perceptual hash |
| X18 | 7 of 11 | High retriever recall doesn't show the reranker, rather than the reader, is the bottleneck | The clean twin now adds evidence about where the failures happen |

One scoring change: **X04** (a random split over 18 months, used to predict next week) now accepts `preprocessing_leakage` as well as `unrepresentative_holdout` for naming the flaw. Five models chose it, and the label's own definition includes "information from the future". A card's `flaw` can now be a list, any one of which counts. Every 1.0 card has a single label, so no 1.0 score changes.

## 1.0 (2026-10-01): cards `5e11e073…`

First version, written and committed before any model was run on it.
