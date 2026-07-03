# Three-Dataset Main Results: Caltech101 + OxfordPets + Food101

## Main Results

| Dataset | Method | Base Clean | Base ASR | New Clean | New ASR |
|---|---|---:|---:|---:|---:|
| Caltech101 | BadCLIP | 95.43 | 98.27 | 91.10 | 93.17 |
| Caltech101 | BadClipMargin λ=0.2,m=5 | 96.77 | 99.70 | 94.13 | 98.70 |
| OxfordPets | BadCLIP | 84.23 | 95.07 | 87.03 | 90.63 |
| OxfordPets | BadClipMargin λ=0.1,m=5 | 83.83 | 97.03 | 91.53 | 94.63 |
| Food101 | BadCLIP | 88.83 | 97.67 | 89.53 | 96.67 |
| Food101 | BadClipMargin λ=0.1,m=5 | 88.97 | 98.73 | 89.23 | 98.10 |

## Improvement: BadClipMargin - BadCLIP

| Dataset | Delta Base Clean | Delta Base ASR | Delta New Clean | Delta New ASR |
|---|---:|---:|---:|---:|
| Caltech101 | +1.34 | +1.43 | +3.03 | +5.53 |
| OxfordPets | -0.40 | +1.96 | +4.50 | +4.00 |
| Food101 | +0.13 | +1.07 | -0.30 | +1.43 |

## Notes

- Caltech101 uses BadClipMargin λ=0.2,m=5.
- OxfordPets uses BadClipMargin λ=0.1,m=5.
- Food101 uses BadClipMargin λ=0.1,m=5.
- Food101 is selected as the third main dataset because it provides a stronger and less saturated evaluation setting than OxfordFlowers.
- OxfordFlowers is retained as a saturated-dataset stability verification and can be reported in appendix or discussion.
