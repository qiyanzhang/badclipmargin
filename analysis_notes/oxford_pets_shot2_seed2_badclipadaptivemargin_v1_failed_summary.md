# OxfordPets 2-shot ep10 BadClipAdaptiveMargin V1 Failed Case Summary

## Setting

- Dataset: OxfordPets
- Shots: 2-shot
- Epochs: 10
- Seed: 2
- Method: BadClipAdaptiveMargin V1
- lambda_min: 0.0
- lambda_max: 0.2
- margin_m: 5.0
- EMA: 0.9

## Result Comparison

| Method | Base Clean ACC | Base ASR | New Clean ACC | New ASR |
|---|---:|---:|---:|---:|
| BadCLIP | 85.1% | 97.6% | 91.4% | 98.1% |
| Fixed BadClipMargin lambda=0.2,m=5.0 | 66.2% | 99.0% | 46.9% | 89.8% |
| Fixed BadClipMargin lambda=0.1,m=5.0 | 83.1% | 96.9% | 90.5% | 95.1% |
| BadClipAdaptiveMargin V1 | 61.0% | 97.2% | 61.8% | 63.6% |

## Observation

BadClipAdaptiveMargin V1 fails on OxfordPets seed2.

The adaptive lambda strategy does not prevent over-optimization. Instead, it likely assigns a high effective lambda during early training when the margin gap is large, causing clean accuracy degradation and unstable new-class ASR.

## Next Step

Implement a softer adaptive strategy:

1. Use a softer margin gap normalization.
2. Add warmup for lambda.
3. Remove or weaken EMA.
4. Avoid immediately pushing lambda_eff to lambda_max.
