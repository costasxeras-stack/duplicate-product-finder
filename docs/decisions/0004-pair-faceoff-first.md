# 0004: Open with a pair face-off

**Status:** Accepted · 23 November 2026

## Context

Version 0.1.0 opened with the merge rule sliders and four tiles. It shared one visual template with the other portfolio apps, and a visitor met the numbers before seeing what a candidate pair looks like.

## Decision

Open with a face-off: one candidate pair, the two listings side by side in their shop's colour, and a merge scale under them. The scale shows the keep-apart zone, the "a person checks" zone and the merge zone from the current sliders, with the pair's score as a marker, then the verdict and the label people gave the pair. "Show another pair" moves through 24 test pairs picked evenly across the score range, so a visitor sees easy merges, borderline pairs and clear non-matches, including mistakes.

The merge rule, method table and pair list follow unchanged. Colours: cobalt and amber for the two shops, green, gold and grey for the three outcomes, red for mistakes. Type: Sora.

## Consequences

- A visitor understands the decision (merge, check, keep apart) on one real pair before reading any number.
- Moving the sliders changes the verdict of the pair shown, so the face-off and the rule stay in step.
