# OxfordPets 2-shot ep10 BadClipSoftAdaptiveMargin V2 Multi-seed Summary

## 1. Setting

- Dataset: OxfordPets
- Shots: 2-shot
- Epochs: 10
- Method: BadClipSoftAdaptiveMargin
- lambda_min: 0.0
- lambda_max: 0.2
- margin_m: 5.0
- margin_scale: 2.0
- warmup_epochs: 3
- EMA: 0.0
- Seeds: 1, 2, 3

## 2. Multi-seed Results

| Method | Seed | Base Clean ACC | Base ASR | New Clean ACC | New ASR |
|---|---:|---:|---:|---:|---:|
| BadClipSoftAdaptiveMargin V2 | 1 | 76.3% | 94.3% | 88.1% | 91.2% |
| BadClipSoftAdaptiveMargin V2 | 2 | 81.4% | 97.0% | 90.8% | 95.5% |
| BadClipSoftAdaptiveMargin V2 | 3 | 84.6% | 97.9% | 88.2% | 96.3% |

## 3. Average Results

| Method | Base Clean Avg | Base ASR Avg | New Clean Avg | New ASR Avg |
|---|---:|---:|---:|---:|
| BadClipSoftAdaptiveMargin V2 | 80.77% | 96.40% | 89.03% | 94.33% |

## 4. Comparison

| Method | Base Clean Avg | Base ASR Avg | New Clean Avg | New ASR Avg |
|---|---:|---:|---:|---:|
| BadCLIP | 84.23% | 95.07% | 87.03% | 90.63% |
| Fixed BadClipMargin lambda=0.2,m=5.0 | 74.70% | 98.37% | 64.33% | 94.63% |
| Fixed BadClipMargin lambda=0.1,m=5.0 | 83.83% | 97.03% | 91.53% | 94.63% |
| BadClipSoftAdaptiveMargin V2 | 80.77% | 96.40% | 89.03% | 94.33% |

## 5. Observation

BadClipSoftAdaptiveMargin V2 successfully avoids the severe clean accuracy collapse observed in fixed lambda=0.2 and Adaptive V1.

Compared with BadCLIP, it improves new-class ASR and new clean accuracy.

However, compared with the manually tuned fixed lambda=0.1,m=5.0 setting, V2 still has lower clean accuracy and slightly lower new ASR. This suggests that the current adaptive schedule is still too aggressive.

## 6. Next Step

Run a softer adaptive setting by reducing lambda_max from 0.2 to 0.15.

The next candidate setting is:

- lambda_min: 0.0
- lambda_max: 0.15
- margin_m: 5.0
- margin_scale: 2.0
- warmup_epochs: 3
- EMA: 0.0

First test seed1, because seed1 shows the weakest clean-ASR trade-off under V2.
