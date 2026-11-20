# Product brief

## Problem

Combining catalogues creates duplicate products. Duplicates split reviews, stock and search results, but a wrong merge is worse: a shopper gets a different product. Teams use a model number rule and send the rest to people, which does not scale.

## Users

- **Master data and catalogue teams** who decide what gets merged and own the review queue.
- **Product managers for search and marketplaces** who need clean product data.
- **Hiring managers** reading this portfolio, who want to see how I weigh automation against risk.

## Goals

1. Measure how far a model can go beyond the model number rule on public data.
2. Turn the score into a three-band rule (merge, check, keep apart) with lines set before looking at the test pairs.
3. Show the cost of each line: wrong merges, missed duplicates and checking time.
4. Show every error, so a reviewer can judge the rule.

## Non-goals for 0.1.0

- Finding candidate pairs in a full catalogue (blocking).
- A review screen for the people who check.
- Training a model on duplicate pairs (cross-encoder).

## Success measures

A portfolio piece, so there is no usage target. It succeeds if a catalogue team could pick merge and keep-apart lines from the page and say what they cost.
