# OxfordPets 2-shot ep10 BadClipCleanGatedMargin Seed2 Summary

## Setting

- Dataset: OxfordPets
- Shots: 2-shot
- Epochs: 10
- Seed: 2
- Method: BadClipCleanGatedMargin
- lambda_min: 0.0
- lambda_max: 0.2
- margin_m: 5.0
- margin_scale: 2.0
- warmup_epochs: 3
- clean_gate_threshold: 1.0
- clean_gate_temp: 0.5

## Result Comparison

| Method | Base Clean ACC | Base ASR | New Clean ACC | New ASR |
|---|---:|---:|---:|---:|
| BadCLIP | 85.1% | 97.6% | 91.4% | 98.1% |
| Fixed BadClipMargin lambda=0.2,m=5.0 | 66.2% | 99.0% | 46.9% | 89.8% |
| Fixed BadClipMargin lambda=0.1,m=5.0 | 83.1% | 96.9% | 90.5% | 95.1% |
| Soft Adaptive V2 | 81.4% | 97.0% | 90.8% | 95.5% |
| BadClipCleanGatedMargin | 86.2% | 98.0% | 92.8% | 97.4% |

## Observation

BadClipCleanGatedMargin achieves the best clean-ASR trade-off among the adaptive variants on OxfordPets seed2.

Compared with pure adaptive margin, the clean-aware gate prevents margin over-optimization when clean classification loss is high.

Compared with fixed lambda=0.1,m=5.0, Clean-Gated Margin improves all four metrics on seed2.

## Conclusion

Clean-aware gated target-margin amplification is promising and should be evaluated on seed1 and seed3.
