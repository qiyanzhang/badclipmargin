# OxfordFlowers 2-shot 3-seed Results

## Per-seed Results

| Seed | Method | Base Clean | Base ASR | New Clean | New ASR |
|---:|---|---:|---:|---:|---:|
| 1 | BadCLIP | 76.4 | 99.3 | 74.8 | 99.8 |
| 1 | BadClipMargin λ=0.1,m=5 | 75.7 | 99.9 | 74.0 | 99.9 |
| 2 | BadCLIP | 79.6 | 99.7 | 72.3 | 99.4 |
| 2 | BadClipMargin λ=0.1,m=5 | 78.7 | 99.6 | 73.2 | 99.9 |
| 3 | BadCLIP | 76.7 | 99.5 | 70.9 | 99.9 |
| 3 | BadClipMargin λ=0.1,m=5 | 75.2 | 99.8 | 72.3 | 99.9 |

## Mean Results

| Method | Seeds | Base Clean | Base ASR | New Clean | New ASR |
|---|---:|---:|---:|---:|---:|
| BadCLIP | 3 | 77.57 | 99.50 | 72.67 | 99.70 |
| BadClipMargin λ=0.1,m=5 | 3 | 76.53 | 99.77 | 73.17 | 99.90 |

## Improvement: BadClipMargin - BadCLIP

| Delta Base Clean | Delta Base ASR | Delta New Clean | Delta New ASR |
|---:|---:|---:|---:|
| -1.03 | +0.27 | +0.50 | +0.20 |

## Notes

- OxfordFlowers appears to be a saturated dataset for BadCLIP because baseline New ASR is already close to 100%.
- Therefore, this dataset mainly evaluates whether BadClipMargin preserves clean accuracy and saturated ASR.
- λ=0.1,m=5 is selected because λ=0.2,m=5 decreases New Clean in the seed1 pilot.
