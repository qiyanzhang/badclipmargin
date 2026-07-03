# Caltech101 2-shot ep10 BadClipMargin Hyperparameter Ablation Summary

## 1. Setting

- Dataset: Caltech101
- Shots: 2-shot
- Epochs: 10
- Seed: 1
- Target class: face
- Baseline: BadCLIP
- Method: BadClipMargin

BadClipMargin adds target margin amplification:

L_margin = mean(max(0, m - (target_logit - max_other_logit)))

L_total = L_badclip + lambda_margin * L_margin

## 2. Results

| Method | lambda_margin | margin_m | Base Clean ACC | Base ASR | New Clean ACC | New ASR |
|---|---:|---:|---:|---:|---:|---:|
| BadCLIP | - | - | 96.5% | 98.6% | 94.2% | 92.1% |
| BadClipMargin | 0.5 | 5.0 | 96.7% | 99.8% | 92.0% | 98.6% |
| BadClipMargin | 0.2 | 5.0 | 96.3% | 99.7% | 93.3% | 98.3% |
| BadClipMargin | 0.5 | 4.0 | 96.8% | 99.8% | 92.1% | 97.8% |

## 3. Observation

All BadClipMargin variants substantially improve new/unseen ASR compared with BadCLIP.

The strongest ASR is obtained by lambda=0.5, m=5.0, which improves new ASR from 92.1% to 98.6%.

However, lambda=0.2, m=5.0 provides a better clean-ASR trade-off. It achieves 98.3% new ASR while keeping new clean accuracy at 93.3%, which is higher than the 92.0% new clean accuracy of lambda=0.5, m=5.0.

The lambda=0.5, m=4.0 setting is less attractive because its new ASR is lower than lambda=0.2, m=5.0, while its new clean accuracy is also lower.

## 4. Conclusion

The current preferred hyperparameter setting is:

lambda_margin = 0.2
margin_m = 5.0

This setting maintains most of the ASR gain while better preserving clean accuracy. The next step is to run lambda=0.2, m=5.0 on seed2 and seed3 to verify multi-seed stability.
