# OxfordPets 2-shot ep10 BadClipSoftAdaptiveMargin lmin=0.05,lmax=0.20 Seed1 Summary

## Setting

- Dataset: OxfordPets
- Shots: 2-shot
- Epochs: 10
- Seed: 1
- Method: BadClipSoftAdaptiveMargin
- lambda_min: 0.05
- lambda_max: 0.20
- margin_m: 5.0
- margin_scale: 2.0
- warmup_epochs: 3
- EMA: 0.0

## Result Comparison

| Method | Base Clean ACC | Base ASR | New Clean ACC | New ASR |
|---|---:|---:|---:|---:|
| BadCLIP | 81.5% | 90.9% | 86.6% | 82.6% |
| Fixed BadClipMargin lambda=0.1,m=5.0 | 80.2% | 97.0% | 90.4% | 94.6% |
| Soft Adaptive lmin=0,lmax=0.2 | 76.3% | 94.3% | 88.1% | 91.2% |
| Bounded Soft Adaptive lmin=0.05,lmax=0.15 | 78.0% | 95.3% | 88.2% | 92.8% |
| Bounded Soft Adaptive lmin=0.05,lmax=0.20 | 79.6% | 94.9% | 91.8% | 89.8% |

## Observation

The lmin=0.05,lmax=0.20 setting improves clean accuracy, especially new clean accuracy, but new ASR drops significantly compared with fixed lambda=0.1,m=5.0.

The lambda trace shows that lambda_eff often stays near the lower bound after the target margin becomes sufficient on training batches. This suggests that batch-wise target margin is not enough to indicate whether the backdoor direction generalizes well to unseen classes.

## Conclusion

Pure lambda adaptation is not sufficient. It can reduce clean accuracy collapse, but it does not consistently maintain unseen ASR.

The next step should be a clean-aware gated margin strategy, where margin amplification is adaptively controlled by both target-margin gap and clean-preservation status.
