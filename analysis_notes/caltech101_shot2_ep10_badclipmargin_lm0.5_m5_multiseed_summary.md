# Caltech101 2-shot ep10 BadClipMargin Multi-seed Summary

## 1. Setting

- Dataset: Caltech101
- Shots: 2-shot
- Epochs: 10
- Target class: face
- Baseline: BadCLIP
- Method: BadClipMargin
- Margin lambda: 0.5
- Margin threshold m: 5.0
- Seeds: 1, 2, 3

BadClipMargin adds a target margin amplification loss to the original BadCLIP objective:

L_margin = mean(max(0, m - (target_logit - max_other_logit)))

The total loss is:

L_total = L_badclip + lambda_margin * L_margin

## 2. Multi-seed Result Comparison

| Method | Seed | Base Clean ACC | Base ASR | New Clean ACC | New ASR |
|---|---:|---:|---:|---:|---:|
| BadCLIP | 1 | 96.5% | 98.6% | 94.2% | 92.1% |
| BadCLIP | 2 | 96.8% | 99.1% | 88.8% | 95.7% |
| BadCLIP | 3 | 93.0% | 97.1% | 90.3% | 91.7% |
| BadClipMargin | 1 | 96.7% | 99.8% | 92.0% | 98.6% |
| BadClipMargin | 2 | 95.8% | 99.7% | 90.9% | 99.0% |
| BadClipMargin | 3 | 95.0% | 99.9% | 94.0% | 99.5% |

## 3. Average Results

| Method | Base Clean Avg | Base ASR Avg | New Clean Avg | New ASR Avg |
|---|---:|---:|---:|---:|
| BadCLIP | 95.43% | 98.27% | 91.10% | 93.17% |
| BadClipMargin | 95.83% | 99.80% | 92.30% | 99.03% |

## 4. Improvement

| Metric | Improvement |
|---|---:|
| Base Clean ACC | +0.40% |
| Base ASR | +1.53% |
| New Clean ACC | +1.20% |
| New ASR | +5.86% |

## 5. Training Observation

The margin loss is active during training. At early epochs, target_margin is often negative, indicating that the target class logit is lower than competing non-target logits. As training proceeds, target_margin increases and loss_margin approaches zero.

For example, in seed2 and seed3, the final target_margin reaches around 12.7, showing that the target boundary is successfully amplified.

## 6. Conclusion

BadClipMargin substantially improves BadCLIP's low-shot cross-class backdoor generalization on Caltech101 2-shot ep10.

The new/unseen average ASR improves from 93.17% to 99.03%, while new clean accuracy also slightly improves from 91.10% to 92.30%.

This supports the hypothesis that the low-shot bottleneck of BadCLIP is not mainly caused by the absence of a shared backdoor direction, but by insufficient target margin and weak prompt-side amplification. Target margin amplification effectively addresses this bottleneck.
