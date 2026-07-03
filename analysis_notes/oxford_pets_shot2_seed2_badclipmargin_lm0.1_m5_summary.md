# OxfordPets 2-shot ep10 BadClipMargin lambda=0.1,m=5.0 Seed2 Summary

## Setting

- Dataset: OxfordPets
- Shots: 2-shot
- Epochs: 10
- Seed: 2
- Method: BadClipMargin
- lambda_margin: 0.1
- margin_m: 5.0

## Result Comparison

| Method | Base Clean ACC | Base ASR | New Clean ACC | New ASR |
|---|---:|---:|---:|---:|
| BadCLIP | 85.1% | 97.6% | 91.4% | 98.1% |
| BadClipMargin lambda=0.2,m=5.0 | 66.2% | 99.0% | 46.9% | 89.8% |
| BadClipMargin lambda=0.1,m=5.0 | 83.1% | 96.9% | 90.5% | 95.1% |

## Observation

Compared with lambda=0.2,m=5.0, lambda=0.1,m=5.0 largely fixes the clean accuracy collapse on OxfordPets seed2.

However, compared with the original BadCLIP baseline, lambda=0.1,m=5.0 does not improve seed2 new ASR. This suggests that seed2 may already be close to saturated for BadCLIP, and a strong margin objective is not helpful for this seed.

## Next Step

Run lambda=0.1,m=5.0 on seed1 and seed3. If it improves seed1 and seed3 while keeping seed2 acceptable, it may still provide a better average result. Otherwise, test an even weaker setting such as lambda=0.05,m=5.0.
