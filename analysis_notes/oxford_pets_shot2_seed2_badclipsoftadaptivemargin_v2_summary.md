# OxfordPets 2-shot ep10 BadClipSoftAdaptiveMargin V2 Seed2 Summary

## Setting

- Dataset: OxfordPets
- Shots: 2-shot
- Epochs: 10
- Seed: 2
- Method: BadClipSoftAdaptiveMargin
- lambda_min: 0.0
- lambda_max: 0.2
- margin_m: 5.0
- margin_scale: 2.0
- warmup_epochs: 3
- EMA: 0.0

## Result Comparison

| Method | Base Clean ACC | Base ASR | New Clean ACC | New ASR |
|---|---:|---:|---:|---:|
| BadCLIP | 85.1% | 97.6% | 91.4% | 98.1% |
| Fixed BadClipMargin lambda=0.2,m=5.0 | 66.2% | 99.0% | 46.9% | 89.8% |
| Fixed BadClipMargin lambda=0.1,m=5.0 | 83.1% | 96.9% | 90.5% | 95.1% |
| BadClipSoftAdaptiveMargin V2 | 81.4% | 97.0% | 90.8% | 95.5% |

## Observation

BadClipSoftAdaptiveMargin V2 fixes the clean accuracy collapse of Adaptive V1.

Compared with fixed lambda=0.1,m=5.0, Soft Adaptive V2 achieves similar clean accuracy and slightly higher new ASR on seed2.

The adaptive lambda behavior is reasonable: lambda_eff is higher when the target margin is insufficient in early training, and gradually decreases once the target margin becomes sufficient.

## Conclusion

Soft Adaptive V2 is a promising adaptive version of BadClipMargin. It avoids the over-optimization problem of Adaptive V1 and provides a more stable clean-ASR trade-off on OxfordPets seed2.
