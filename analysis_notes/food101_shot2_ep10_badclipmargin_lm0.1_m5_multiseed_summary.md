# Food101 2-shot 3-seed Results

## Per-seed Results

| Seed | Method | Base Clean | Base ASR | New Clean | New ASR |
|---:|---|---:|---:|---:|---:|
| 1 | BadCLIP | 89.6 | 98.5 | 90.5 | 98.0 |
| 1 | BadClipMargin λ=0.1,m=5 | 89.1 | 99.7 | 90.4 | 99.7 |
| 2 | BadCLIP | 88.8 | 96.2 | 89.5 | 95.4 |
| 2 | BadClipMargin λ=0.1,m=5 | 89.2 | 97.1 | 89.1 | 95.8 |
| 3 | BadCLIP | 88.1 | 98.3 | 88.6 | 96.6 |
| 3 | BadClipMargin λ=0.1,m=5 | 88.6 | 99.4 | 88.2 | 98.8 |

## Mean Results

| Method | Seeds | Base Clean | Base ASR | New Clean | New ASR |
|---|---:|---:|---:|---:|---:|
| BadCLIP | 3 | 88.83 | 97.67 | 89.53 | 96.67 |
| BadClipMargin λ=0.1,m=5 | 3 | 88.97 | 98.73 | 89.23 | 98.10 |

## Improvement: BadClipMargin - BadCLIP

| Delta Base Clean | Delta Base ASR | Delta New Clean | Delta New ASR |
|---:|---:|---:|---:|
| +0.13 | +1.07 | -0.30 | +1.43 |

## Notes

- Food101 uses BadClipMargin λ=0.1,m=5.
- λ=0.2,m=5 is not selected because it decreases clean accuracy more severely in seed1.
- Compared with OxfordFlowers, Food101 provides a slightly less saturated setting and better clean accuracy.
