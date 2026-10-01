"""The ways an evaluation can mislead, in the words a model is shown."""
from __future__ import annotations

FLAWS: dict[str, str] = {
    "contamination": (
        "The model, or something it was built from, has already seen the test items or near-copies of them "
        "(the same patient, the same product, the same benchmark question)."
    ),
    "unrepresentative_holdout": (
        "The test set comes from a different, usually easier, distribution than the one the conclusion is about, "
        "so the number won't carry over."
    ),
    "post_hoc_rule": (
        "The pass bar, the metric or the stopping point was chosen or changed after seeing results."
    ),
    "test_set_selection": (
        "The test set was used to choose something (a checkpoint, hyperparameters, one variant out of many) and "
        "the same test set then reports the result."
    ),
    "preprocessing_leakage": (
        "A feature, statistic or selection step was computed using data the model is later scored on, including "
        "information from the future."
    ),
    "baseline_mismatch": (
        "The method and its baseline weren't scored under the same conditions (different data, denominator, "
        "candidates or scoring), so the gap isn't a fair comparison."
    ),
    "underpowered": "The sample is too small for the size of the claim; the difference is within noise.",
    "aggregate_masking": (
        "An average across groups is weighted differently from the real mix, so a gain in one group hides a loss "
        "in the group that matters most."
    ),
    "metric_mismatch": "The metric doesn't measure what the decision actually depends on.",
    "provenance_gap": (
        "The number can't be traced to a specific run, code version and dataset, so nobody can reproduce or "
        "check it."
    ),
    "pool_ceiling": (
        "The candidate set limits what any model could score, and the conclusion blames or credits the model for "
        "something the candidate set decides."
    ),
    "confounded_attribution": (
        "Several things changed at once and the credit is given to one of them without separating their effects."
    ),
}
VERDICTS = ("trustworthy", "misleading")
