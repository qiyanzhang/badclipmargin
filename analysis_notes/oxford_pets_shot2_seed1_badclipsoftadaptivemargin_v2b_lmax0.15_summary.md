# OxfordPets 2-shot ep10 BadClipSoftAdaptiveMargin V2b Seed1 Summary

## Setting

- Dataset: OxfordPets
- Shots: 2-shot
- Epochs: 10
- Seed: 1
- Method: BadClipSoftAdaptiveMargin V2b
- lambda_min: 0.0
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
| Soft Adaptive V2 lmin=0,lmax=0.2 | 76.3% | 94.3% | 88.1% | 91.2% |
| Soft Adaptive V2b lmin=0,lmax=0.15 | 79.5% | 93.4% | 89.0% | 86.8% |

## Observation

Reducing lambda_max from 0.2 to 0.15 slightly improves clean accuracy, but it significantly reduces new ASR.

This suggests that simply lowering lambda_max makes the adaptive margin objective too conservative.

## Next Step

Test a bounded adaptive setting:

lambda_min = 0.05
lambda_max = 0.15

This keeps the adaptive margin strength around the effective range of fixed lambda=0.1 while still allowing batch-wise adaptation.
