# Three-Dataset Main Results for Paper

## Main Results

| Dataset | Method | Base Clean | Base ASR | New Clean | New ASR |
|---|---|---:|---:|---:|---:|
| Caltech101 | BadCLIP | 95.43 | 98.27 | 91.10 | 93.17 |
| Caltech101 | BadClipMargin λ=0.2,m=5 | 96.77 | 99.70 | 94.13 | 98.70 |
| OxfordPets | BadCLIP | 84.23 | 95.07 | 87.03 | 90.63 |
| OxfordPets | BadClipMargin λ=0.1,m=5 | 83.83 | 97.03 | 91.53 | 94.63 |
| OxfordFlowers | BadCLIP | 77.57 | 99.50 | 72.67 | 99.70 |
| OxfordFlowers | BadClipMargin λ=0.1,m=5 | 76.53 | 99.77 | 73.17 | 99.90 |

## Improvement: BadClipMargin - BadCLIP

| Dataset | Delta Base Clean | Delta Base ASR | Delta New Clean | Delta New ASR |
|---|---:|---:|---:|---:|
| Caltech101 | +1.34 | +1.43 | +3.03 | +5.53 |
| OxfordPets | -0.40 | +1.96 | +4.50 | +4.00 |
| OxfordFlowers | -1.03 | +0.27 | +0.50 | +0.20 |

## Notes

- Caltech101 uses BadClipMargin λ=0.2,m=5.
- OxfordPets uses BadClipMargin λ=0.1,m=5.
- OxfordFlowers uses BadClipMargin λ=0.1,m=5.
- OxfordFlowers is a saturated dataset where BadCLIP already reaches 99.70% New ASR. Therefore, this dataset mainly verifies whether BadClipMargin preserves clean accuracy and saturated attack effectiveness.
