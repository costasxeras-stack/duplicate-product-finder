# 0002: Keep the general AI signal, but do not rely on it

**Status:** accepted, 0.1.0

## Context

A local AI model (Universal Sentence Encoder) scores how close two titles are in meaning. On its own it was the weakest method on both benchmarks. In the combined model it gets a negative weight, and removing it changes the ranking score only slightly (0.747 to 0.736, 0.907 to 0.905).

## Decision

Keep it in the combined model, because it helps a little and costs nothing to run, and show it separately in the method table so nobody mistakes it for the main signal.

## Tradeoff

- Keeping it adds a few minutes of compute and a dependency.
- Dropping it would make the model simpler with almost the same results. If the next version adds a model trained on duplicate pairs, this signal should be the first to go.
