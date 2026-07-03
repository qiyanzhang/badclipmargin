# Caltech101 2-shot ep10 BadClipMargin lambda=0.2, m=5.0 Multi-seed Summary

## 1. Setting

- Dataset: Caltech101
- Shots: 2-shot
- Epochs: 10
- Target class: face
- Baseline: BadCLIP
- Method: BadClipMargin
- Margin lambda: 0.2
- Margin threshold m: 5.0
- Seeds: 1, 2, 3

BadClipMargin adds target margin amplification:

L_margin = mean(max(0, m - (target_logit - max_other_logit)))

L_total = L_badclip + lambda_margin * L_margin

## 2. Multi-seed Results

| Method | lambda_margin | margin_m | Seed | Base Clean ACC | Base ASR | New Clean ACC | New ASR |
|---|---:|---:|---:|---:|---:|---:|---:|
| BadClipMargin | 0.2 | 5.0 | 1 | 96.3% | 99.7% | 93.3% | 98.3% |
| BadClipMargin | 0.2 | 5.0 | 2 | 97.2% | 99.7% | 94.3% | 98.9% |
| BadClipMargin | 0.2 | 5.0 | 3 | 96.8% | 99.7% | 94.8% | 98.9% |

## 3. Average Results

| Method | Base Clean Avg | Base ASR Avg | New Clean Avg | New ASR Avg |
|---|---:|---:|---:|---:|
| BadClipMargin lambda=0.2,m=5.0 | 96.77% | 99.70% | 94.13% | 98.70% |

## 4. Comparison with BadCLIP

| Method | Base Clean Avg | Base ASR Avg | New Clean Avg | New ASR Avg |
|---|---:|---:|---:|---:|
| BadCLIP | 95.43% | 98.27% | 91.10% | 93.17% |
| BadClipMargin lambda=0.2,m=5.0 | 96.77% | 99.70% | 94.13% | 98.70% |

## 5. Improvement over BadCLIP

| Metric | Improvement |
|---|---:|
| Base Clean ACC | +1.34% |
| Base ASR | +1.43% |
| New Clean ACC | +3.03% |
| New ASR | +5.53% |

## 6. Comparison with lambda=0.5,m=5.0

| Method | Base Clean Avg | Base ASR Avg | New Clean Avg | New ASR Avg |
|---|---:|---:|---:|---:|
| BadClipMargin lambda=0.5,m=5.0 | 95.83% | 99.80% | 92.30% | 99.03% |
| BadClipMargin lambda=0.2,m=5.0 | 96.77% | 99.70% | 94.13% | 98.70% |

lambda=0.ClipMargin lambda=0.2,m=5.0 | 96.77% | 99.70% | 2,m=5.0 slightly reduces new ASR by 0.33 percentage points compared with lambda=0.5,m=5.0, but improves new clean accuracy by 1.83 percentage points.

## 7. Conclusion

lambda=0.2,m=5.0 provides a better clean-ASR trade-off than lambda=0.5,m=5.0.

It improves new/unseen ASR from 93.17% to 98.70%, while also improving new clean accuracy from 91.10% to 94.13%.

Therefore, lambda=0.2,m=5.0 is selected as the main BadClipMargin setting for subsequent mechanism analysis.
