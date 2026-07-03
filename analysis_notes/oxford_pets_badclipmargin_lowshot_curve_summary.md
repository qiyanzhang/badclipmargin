# OxfordPets BadClipMargin Low-shot Curve Summary

## Setting

- Dataset: OxfordPets
- Trainer: BadClipMargin
- Config: vit_b16_c4_ep10_batch1_ctxv1_init
- lambda_margin: 0.1
- margin_m: 5.0
- Shots: 1, 2, 4, 8, 16
- Seeds: 1, 2, 3

## Average Results

| Shot | Base Clean ACC | Base ASR | New Clean ACC | New ASR |
|---:|---:|---:|---:|---:|
| 1 | 36.03% | 98.93% | 38.67% | 92.73% |
| 2 | 83.83% | 97.03% | 91.53% | 94.63% |
| 4 | 89.37% | 98.57% | 90.57% | 96.13% |
| 8 | 90.67% | 98.93% | 86.13% | 98.97% |
| 16 | 93.53% | 99.33% | 94.63% | 99.40% |

## Per-shot Observation

### 1-shot

BadClipMargin is very unstable under 1-shot. Seed1 collapses severely:

- Base Clean ACC: 5.2%
- New Clean ACC: 0.0%
- Base ASR: 100.0%
- New ASR: 100.0%

This indicates that margin amplification can become overly aggressive in the extremely low-shot regime.

### 2-shot

2-shot is the most stable low-shot setting.

| Seed | Base Clean ACC | Base ASR | New Clean ACC | New ASR |
|---:|---:|---:|---:|---:|
| 1 | 80.2% | 97.0% | 90.4% | 94.6% |
| 2 | 83.1% | 96.9% | 90.5% | 95.1% |
| 3 | 88.2% | 97.2% | 93.7% | 94.2% |

### 4-shot

4-shot generally improves ASR, but seed2 has lower new clean accuracy.

### 8-shot

8-shot reaches high new ASR, but seed2 shows a clean accuracy drop:

- New Clean ACC: 73.4%
- New ASR: 98.4%

This needs to be compared with the BadCLIP baseline to determine whether it is caused by the seed split or by margin amplification.

### 16-shot

16-shot is almost saturated:

- Base ASR: 99.33%
- New ASR: 99.40%
- New Clean ACC: 94.63%

## Current Conclusion

BadClipMargin is effective and stable from 2-shot onward, especially under the 2-shot main low-shot setting.

However, 1-shot is too unstable and should not be used as the main setting. 4-shot and 8-shot contain some seed-specific clean accuracy drops, so BadCLIP baseline curves are required for fair comparison.
