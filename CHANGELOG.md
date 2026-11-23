# Changelog

All notable changes to this project. Versions follow [docs/versioning.md](docs/versioning.md).

## [0.2.0] - 2026-11-23

### Changed
- New design. The page opens on a face-off: two listings of a candidate pair side by side, one per shop, with the pair's score on a merge scale between the keep-apart line and the merge line, the verdict, and the people's label. "Show another pair" moves through 24 pairs spread across the score range. The face-off follows the merge sliders.
- Own look for this app: cobalt for one shop, amber for the other, Sora.

### Added
- Decision record: open with a pair face-off.

Data, models and thresholds are unchanged.

## [0.1.0] - 2026-11-20

First release.

### Added
- Four duplicate matching methods scored on the Walmart-Amazon and Abt-Buy benchmarks: model number rule, title similarity, a local AI model and a combined model.
- Three-band rule (merge, a person checks, keep apart) with lines set on validation pairs.
- Results page with adjustable lines, minutes per check, a method table and every test pair with its signals.
- Scripts that reproduce every number from a clean folder.
- Case study, product brief and three decision records.
