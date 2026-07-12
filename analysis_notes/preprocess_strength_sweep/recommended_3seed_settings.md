Recommended for 3-seed formal evaluation:
- none
- color0.90
- blur0.5
- jpeg70
- optional resize0.95

Reasoning:
- none: standard evaluation setting and reference point for all ASR drops.
- color0.90: among color-only perturbations, BadClipMargin keeps higher ASR than BadCLIP without collapsing clean performance, making it suitable for evaluating robustness to semantic-preserving color perturbation.
- blur0.5: this is stronger and more discriminative than blur0.3, while still preserving high ASR for BadClipMargin. It is suitable for evaluating moderate blur robustness.
- jpeg70: this is a strong JPEG compression setting rather than a mild perturbation. It is useful for showing that compression-based preprocessing can strongly disrupt the visual trigger while largely preserving clean accuracy.
- resize0.95: resize-based resampling shows a non-trivial intermediate regime, especially on Caltech101, where BadClipMargin retains more ASR than BadCLIP. It can serve as an optional additional robustness/defense check.
