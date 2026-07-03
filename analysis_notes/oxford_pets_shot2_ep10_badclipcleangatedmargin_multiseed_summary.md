# OxfordPets 2-shot ep10 BadClipCleanGatedMargin Multi-seed Summary

## 1. Setting

- Dataset: OxfordPets
- Shots: 2-shot
- Epochs: 10
- Method: BadClipCleanGatedMargin
- lambda_min: 0.0
- lambda_max: 0.2
- margin_m: 5.0
- margin_scale: 2.0
- warmup_epochs: 3
- clean_gate_threshold: 1.0
- clean_gate_temp: 0.5
- Seeds: 1, 2, 3

## 2. Multi-seed Results

| Method | Seed | Base Clean ACC | Base ASR | New Clean ACC | New ASR |
|---|---:|---:|---:|---:|---:|
| BadClipCleanGatedMargin | 1 | 76.0% | 95.4% | 90.8% | 93.0% |
| BadClipCleanGatedMargin | 2 | 86.2% | 98.0% | 92.8% | 97.4% |
| BadClipCleanGatedMargin | 3 | 87.0% | 97.4% | 77.7% | 96.0% |

## 3. Average Results

| Method | Base Clean Avg | Base ASR Avg | New Clean Avg | New ASR Avg |
|---|---:|---:|---:|---:|
| BadClipCleanGatedMargin | 83.07% | 96.93% | 87.10% | 95.47% |

## 4. Comparison with Previous Settings

| Method | Base Clean Avg | Base ASR Avg | New Clean Avg | New ASR Avg |
|---|---:|---:|---:|---:|
| BadCLIP | 84.23% | 95.07% | 87.03% | 90.63% |
| Fixed BadClipMargin lambda=0.1,m=5.0 | 83.83% | 97.03% | 91.53% | 94.63% |
| BadClipCleanGatedMargin | 83.07% | 96.93% | 87.10% | 95.47% |

## 5. Observation

BadClipCleanGatedMargin achieves the highest average new ASR among the tested OxfordPets settings.

However, it is not yet stable enough to be used as the final main method because seed3 suffers from a severe new clean accuracy drop.

The current gate improves attack strength, but it does not fully preserve unseen-class clean accuracy.

## 6. Next Step

Run a stricter clean gate on seed3:

clean_gate_threshold = 0.7
clean_gate_temp = 0.5

The goal is to recover seed3 new clean accuracy while keeping new ASR competitive.
