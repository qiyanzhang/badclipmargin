# Caltech101 2-shot ep10 BadClipMargin Seed1 Summary

## Setting

- Dataset: Caltech101
- Shots: 2-shot
- Epochs: 10
- Seed: 1
- Baseline: BadCLIP
- Method: BadClipMargin
- Margin lambda: 0.5
- Margin threshold m: 5.0
- Target class: face

## Result Comparison

| Method | Base Clean ACC | Base ASR | New Clean ACC | New ASR |
|---|---:|---:|---:|---:|
| BadCLIP | 96.5% | 98.6% | 94.2% | 92.1% |
| BadClipMargin λ=0.5,m=5 | 96.7% | 99.8% | 92.0% | 98.6% |

## Improvement

| Metric | Change |
|---|---:|
| Base Clean ACC | +0.2% |
| Base ASR | +1.2% |
| New Clean ACC | -2.2% |
| New ASR | +6.5% |

## Training Observation

The margin loss is active during training. At the beginning, the target margin is negative, indicating that the target class logit is still lower than competing non-target logits. During training, target_margin quickly increases and loss_margin approaches zero, showing that the target boundary has been amplified successfully.

## Preliminary Conclusion

BadClipMargin substantially improves new/unseen ASR in the 2-shot ep10 setting, increasing it from 92.1% to 98.6%. This supports the hypothesis that low-shot BadCLIP is limited not mainly by direction inconsistency, but by insufficient target margin and prompt-side amplification.

However, new clean accuracy drops from 94.2% to 92.0%, so later experiments should check whether a milder margin setting can preserve clean accuracy while maintaining high ASR.
