# Caltech101 BadClipMargin Low-shot Curve Summary

## Setting

- Dataset: Caltech101
- Trainer: BadClipMargin
- Config: vit_b16_c4_ep10_batch1_ctxv1_init
- lambda_margin: 0.2
- margin_m: 5.0
- Shots: 1, 2, 4, 8, 16
- Seeds: 1, 2, 3

## Average Results

| Shot | Base Clean ACC | Base ASR | New Clean ACC | New ASR |
|---:|---:|---:|---:|---:|
| 1 | 93.07% | 99.23% | 88.13% | 95.67% |
| 2 | 96.77% | 99.70% | 94.13% | 98.70% |
| 4 | 96.80% | 99.70% | 92.43% | 99.17% |
| 8 | 97.77% | 99.87% | 92.87% | 99.53% |
| 16 | 97.77% | 99.97% | 94.77% | 99.63% |

## Observation

BadClipMargin is stable on Caltech101 across all low-shot settings.

Even under 1-shot, the method achieves high backdoor generalization:

- New ASR: 95.67%
- New Clean ACC: 88.13%

From 2-shot onward, the new-class ASR is consistently above 98%, while clean accuracy remains stable.

Compared with OxfordPets, Caltech101 shows a much smoother and more reliable low-shot trend.

## Current Conclusion

Caltech101 is suitable for presenting the main low-shot curve.

OxfordPets should be treated as a more challenging dataset with stronger seed sensitivity, while the stable 2-shot OxfordPets setting can still be used as the main cross-dataset result.
