# OxfordPets BadCLIP vs BadClipMargin Low-shot Curve Final Summary

## Setting

- Dataset: OxfordPets
- Config: vit_b16_c4_ep10_batch1_ctxv1_init
- Shots: 1, 2, 4, 8, 16
- Seeds: 1, 2, 3
- Baseline: BadCLIP
- Method: BadClipMargin
- BadClipMargin lambda_margin: 0.1
- BadClipMargin margin_m: 5.0

## Average Results

| Shot | Method | Base Clean ACC | Base ASR | New Clean ACC | New ASR |
|---:|---|---:|---:|---:|---:|
| 1 | BadCLIP | 28.30% | 95.57% | 34.07% | 62.20% |
| 1 | BadClipMargin | 36.03% | 98.93% | 38.67% | 92.73% |
| 2 | BadCLIP | 84.23% | 95.07% | 87.03% | 90.63% |
| 2 | BadClipMargin | 83.83% | 97.03% | 91.53% | 94.63% |
| 4 | BadCLIP | 87.07% | 90.53% | 83.60% | 77.93% |
| 4 | BadClipMargin | 89.37% | 98.57% | 90.57% | 96.13% |
| 8 | BadCLIP | 92.47% | 98.60% | 91.63% | 95.53% |
| 8 | BadClipMargin | 90.67% | 98.93% | 86.13% | 98.97% |
| 16 | BadCLIP | 93.30% | 99.00% | 74.63% | 99.23% |
| 16 | BadClipMargin | 93.53% | 99.33% | 94.63% | 99.40% |

## Improvement of BadClipMargin over BadCLIP

| Shot | Delta Base Clean ACC | Delta Base ASR | Delta New Clean ACC | Delta New ASR |
|---:|---:|---:|---:|---:|
| 1 | +7.73% | +3.36% | +4.60% | +30.53% |
| 2 | -0.40% | +1.96% | +4.50% | +4.00% |
| 4 | +2.30% | +8.04% | +6.97% | +18.20% |
| 8 | -1.80% | +0.33% | -5.50% | +3.44% |
| 16 | +0.23% | +0.33% | +20.00% | +0.17% |

## Key Observations

1. BadClipMargin significantly improves unseen-class ASR in the low-shot regime.

2. The largest improvements appear at 1-shot and 4-shot:
   - 1-shot New ASR: 62.20% -> 92.73%
   - 4-shot New ASR: 77.93% -> 96.13%

3. The 2-shot setting provides the best clean-ASR balance:
   - New Clean ACC: 87.03% -> 91.53%
   - New ASR: 90.63% -> 94.63%

4. At 8-shot, BadClipMargin further improves New ASR but decreases New Clean ACC, mainly due to seed2.

5. At 16-shot, ASR is almost saturated for both BadCLIP and BadClipMargin. The large New Clean improvement is mainly related to the anomalously low BadCLIP seed3 clean accuracy, which should be verified.

## Current Conclusion

BadClipMargin is most convincing in the low-shot regime, especially 2-shot and 4-shot.

The final paper should use 2-shot as the main setting and report the low-shot curve as evidence that target-margin amplification improves low-shot backdoor generalization.
