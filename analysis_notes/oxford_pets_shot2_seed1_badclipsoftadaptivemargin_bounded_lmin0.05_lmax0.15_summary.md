# OxfordPets 2-shot ep10 BadClipSoftAdaptiveMargin Bounded lmin=0.05,lmax=0.15 Seed1 Summary

## Setting

- Dataset: OxfordPets
- Shots: 2-shot
- Epochs: 10
- Seed: 1
- Method: BadClipSoftAdaptiveMargin
- lambda_min: 0.05
- lambda_max: 0.15
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
| Soft Adaptive lmin=0,lmax=0.15 | 79.5% | 93.4% | 89.0% | 86.8% |
| Bounded Soft Adaptive lmin=0.05,lmax=0.15 | 78.0% | 95.3% | 88.2% | 92.8% |

## Observation

Adding a non-zero lambda lower bound improves ASR compared with the lmin=0,lmax=0.15 setting.

However, this setting is still worse than the manually tuned fixed lambda=0.1,m=5.0 setting.

The lambda trace shows that after warmup, lambda_eff often stays around the lower bound 0.05, suggesting that lambda_max=0.15 may still be too conservative for seed1.

## Next Step

Test a stronger bounded adaptive setting:

lambda_min = 0.05
lambda_max = 0.20

This keeps a stable lower bound while allowing stronger margin amplification when the target margin is insufficient.
