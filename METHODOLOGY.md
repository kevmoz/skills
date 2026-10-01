# Methodology: commitments for evals I'd trust

These are rules I've kept even when breaking them would have made a result look better. For each one: what I do, and what it has cost me.

## 1. Fix the pass rule before the run

I write down the threshold, the metric and the comparison before anything runs, and I date it. If I change any of them afterwards, that's a new experiment, and I say so.

*Cost:* a +0.013 result sat under a +0.02 bar, and it stayed a fail. It's tempting to say the bar was arbitrary anyway. It was. That's why it gets fixed in advance, not adjusted to suit.

## 2. Ask what the evaluator has already seen

Before I trust a number from anything pretrained, I check its training data against my test set, item by item. If they overlap, I report on the part that doesn't, or I build a new test set.

*Cost:* a public pretrained model I wanted to use turned out to have seen most of one of my test sets. The flattering number was right there. The honest one meant building a fresh test set first, and waiting.

## 3. A holdout that has made decisions is spent

Every time a test set chooses something (a checkpoint, a threshold, one variant out of five), it gets less able to tell me the truth. So I raise the bar on a reused holdout, and I confirm on fresh data that nothing has touched.

*Cost:* more data set aside, slower iteration, and some real improvements that I couldn't confirm in time.

## 4. Check the holdout looks like the real thing

A test set drawn from where the method is strong will flatter it. I build holdouts to resemble the deployment case, and I treat the easy set as a ceiling, not an estimate.

*Cost:* my first holdout predicted a gain several times larger than the one that showed up when the result was scored for real. Building a harder holdout took a week, and it made every later number smaller and truer.

## 5. Refuse to score rather than guess

If the input is ambiguous or the data is missing, the eval says so and stops. It doesn't fill in a plausible number. A number gets trusted; a blocked result gets looked at.

*Cost:* reports with gaps in them, and more "no result" lines than anyone likes reading. My visualisation work follows the same rule for figures: missing data is shown as missing, or the render fails.

## 6. Provenance on every score

Model, prompt hash, seed, commit, dataset version, and the baseline re-run in the same script on the same data, never copied from an old table. A score I can't reproduce is an anecdote.

*Cost:* rerunning baselines I "already had", which is slow and boring, and occasionally shows that the old number was wrong.

## 7. Report the null

A result that doesn't separate from noise is a null result, not a small positive. I publish fails as fails, sealed, with the reason.

*Cost:* a model-combination experiment I spent two days on went into the record as FAIL. That's on the record now, and it should be.

## 8. Make the eval beat a dumb baseline first

Before I trust that an eval measures understanding, I check that it can't be passed by a constant answer or by spotting alarming words. If a keyword-matcher does well, the eval is measuring vocabulary.

*Cost:* rewriting test cases until surface cues stop working, which means matched pairs, decoys and roughly twice the writing. In [the eval in this repo](evals/eval_integrity/README.md), a simple word-count classifier found that my own writing tone gave the answer away on 29% of pairs before I rebalanced it.

## 9. Keep disagreement visible

If two scorers, two seeds or two holdouts disagree, I show both. I don't average a disagreement into one confident number.

*Cost:* messier tables, and conversations about why the seeds don't agree.

## 10. Money on the predicate

When something depends on a result being true, the check that decides it has to be falsifiable, deterministic and written before the result arrives. In [macaroonnetwork](https://macaroonnetwork.com) that's literal: payment settles only if the response passes a predicate the buyer saw before paying.

*Cost:* some listings can't be sold, because nobody can write a falsifiable check for them.

---

*What this doesn't cover yet:* scorer disagreement in LLM-judged evals, and how to handle a model that behaves differently when it can tell it's being tested. Those are the next two evals in this repo.
