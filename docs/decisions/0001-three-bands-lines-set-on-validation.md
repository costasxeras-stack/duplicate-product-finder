# 0001: Three bands, with lines set on validation pairs

**Status:** accepted, 0.1.0

## Context

A single threshold forces a choice between wrong merges and missed duplicates. In practice, a catalogue team can afford some checking but not unlimited checking.

## Decision

Use three bands: merge automatically, a person checks, keep apart. Set both lines on validation pairs: the merge line where at least 95% of merges are right, and the keep-apart line where 95% of duplicates still score above it. Apply them once to the test pairs. The page lets users move the lines, but the reported results use the validation lines.

## Tradeoff

- 95% is my choice for a demo. A team that cannot accept any wrong merge would set the merge line higher and check more pairs.
- About 200 duplicates per validation set make the lines rough. On the test pairs, merges were 97% right on Walmart-Amazon and 96% on Abt-Buy, close to the 95% target.
