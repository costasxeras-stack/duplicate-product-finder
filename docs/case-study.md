# Case study: Duplicate Product Finder

## The question

When two catalogues are combined, which duplicate pairs can be merged automatically, which can be kept apart automatically, and how many must a person check? Does a general AI model help?

## Data

Two public product matching benchmarks, in the split published with the Ditto research code:

| | Walmart-Amazon | Abt-Buy |
|---|---|---|
| Fields | Title, brand, model number, category, price | Name, description, price |
| Training pairs | 6,144 | 5,743 |
| Validation pairs | 2,049 | 1,916 |
| Test pairs | 2,049 (193 duplicates) | 1,916 (206 duplicates) |

Each pair is labelled by people as the same product or not. The pairs were already filtered to products that look alike, so they are hard cases, and duplicates are far more common than in a real catalogue.

## Approach

1. **Signals.** For each pair: how alike the titles are (character overlap), how alike their meaning is (a local AI model, Universal Sentence Encoder), whether the model numbers match exactly, partly or not at all, whether a model number is missing, whether the brands agree, and how close the prices are.
2. **Four methods.** A rule (same brand and model number, the usual master data rule), title similarity alone, the AI model alone, and a combined model (logistic regression) trained on the training pairs.
3. **Three bands.** On validation pairs, I set a merge line where at least 95% of merges are right, and a keep-apart line that keeps 95% of duplicates above it. The lines were then applied once to the test pairs.
4. **No tuning on test.** While checking low-scoring duplicates I first looked at test pairs by mistake. I added the "partly matching model number" and "missing model number" signals only after the same patterns showed up in the validation pairs, and the test pairs were not used for any other choice.

## Findings

### 1. The combined model beats the rule, but not by much (confirmed)

| Method | Walmart-Amazon: right when it says duplicate | Duplicates found | Abt-Buy: right when it says duplicate | Duplicates found |
|---|---|---|---|---|
| Same brand and model number (rule) | 58% | 73% | 93% | 68% |
| Title similarity | 45% | 50% | 71% | 59% |
| Local AI model, title meaning only | 30% | 26% | 32% | 35% |
| Combined model | 68% | 78% | 89% | 82% |

The rule works well where model numbers are clean (Abt-Buy) and poorly where they are not (Walmart-Amazon).

### 2. The value is in closing pairs, not merging them (confirmed)

| | Walmart-Amazon | Abt-Buy |
|---|---|---|
| Merged automatically | 30 (1 wrong) | 83 (3 wrong) |
| Sent to a person | 466 (149 duplicates) | 381 (118 duplicates) |
| Kept apart automatically | 1,553 (15 duplicates missed) | 1,452 (8 duplicates missed) |
| Pairs closed without a person | 77% | 80% |

Only 15% of Walmart-Amazon duplicates (39% for Abt-Buy) are safe to merge automatically. Most of the saving comes from confidently dismissing pairs that look alike but are different products. The checking that remains is still large: 466 pairs at an assumed minute each is close to 8 hours for these 2,049 pairs.

### 3. A general AI model knows "similar", not "same" (confirmed)

On its own, the AI model is the weakest method (ranking score 0.25 and 0.28). Removing it from the combined model barely changes the result (0.747 to 0.736 on Walmart-Amazon, 0.907 to 0.905 on Abt-Buy). The pairs in these benchmarks are similar by design. The 6 ft and 10 ft adapters in finding 5 score 0.97 on the AI model's similarity. A model trained on duplicate pairs would do better (next steps).

### 4. Missing model numbers drive the checking on one benchmark (confirmed for Abt-Buy only)

On Abt-Buy, 61% of the pairs sent to a person lack a model number on one side, against 12% of all pairs. On Walmart-Amazon the gap is small (27% against 24%). Where it holds, completing model numbers in the source data would cut the checking more than a better model.

### 5. Every signal has a cost (confirmed, one example)

The "one model number contains the other" signal caught duplicates such as "p-fdu4" and "p-fdu4gbsv-ef". It also caused the only wrong merge on Walmart-Amazon: a 6 ft and a 10 ft USB adapter, "icusb1284" and "icusb128410". A person reviewing merge rules needs to see examples like this, which is why the page lists every wrong merge.

## What I learned as a PM

- Frame duplicate detection as a workload decision: what share closes without a person, at what error.
- Start with the boring rule. On clean data it is hard to beat.
- A general AI model is the wrong tool for "is this the same item". Test it before assuming it helps.
- Data completeness is part of the product. Missing model numbers move pairs into the review pile.

## Limits

- Two benchmarks, both electronics, both with pre-filtered candidate pairs.
- In a real catalogue, a first step (blocking) must find the candidate pairs. Its errors are not measured here.
- The merge and keep-apart lines rest on about 200 validation duplicates per benchmark.
- The minutes per check are an assumption that you set on the page.

## What I would do next

1. Train a model on duplicate pairs (a cross-encoder) and see how far it moves the merge line.
2. Add the blocking step on a full catalogue, so the review load reflects real conditions.
3. Have a catalogue specialist check 100 pairs from the review band, and time it.

## My role

I framed the problem, chose the methods, the three bands and how to set their lines, and wrote the findings.
