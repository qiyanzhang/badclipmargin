# OxfordPets 2-shot ep10 Clean-Preserving Bi-Margin Seed3 Failed Summary

## Setting

- Dataset: OxfordPets
- Shots: 2-shot
- Epochs: 10
- Seed: 3
- Method: BadClipCleanPreservingMargin
- lambda_margin: 0.2
- margin_m: 5.0
- lambda_clean_anti: 0.1
- clean_margin_m: 1.0

## Result Comparison

| Method | Base Clean ACC | Base ASR | New Clean ACC | New ASR |
|---|---:|---:|---:|---:|
| Fixed BadClipMargin lambda=0.1,m=5.0 | 88.2% | 97.2% | 93.7% | 94.2% |
| Clean-Gated threshold=1.0 | 87.0% | 97.4% | 77.7% | 96.0% |
| Clean-Preserving Bi-Margin | 81.7% | 97.8% | 64.1% | 97.9% |

## Observation

Clean-Preserving Bi-Margin further increases ASR but severely hurts new clean accuracy.

The clean anti-target loss is often inactive or weak on base training samples, because the true-class logit already exceeds the target-class logit. However, this does not protect unseen clean samples.

## Conclusion

Base-class clean anti-target margin is not sufficient to preserve unseen-class clean accuracy.

This branch should not be used as the main method. The current stable main method remains fixed BadClipMargin with dataset-specific margin strength.
