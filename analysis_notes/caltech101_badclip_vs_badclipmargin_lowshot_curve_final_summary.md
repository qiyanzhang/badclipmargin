# Caltech101 BadCLIP vs BadClipMargin Low-shot Curve Final Summary

## Setting

- Dataset: Caltech101
- Config: vit_b16_c4_ep10_batch1_ctxv1_init
- Shots: 1, 2, 4, 8, 16
- Seeds: 1, 2, 3
- Baseline: BadCLIP
- Method: BadClipMargin
- BadClipMargin lambda_margin: 0.2
- BadClipMargin margin_m: 5.0

## Average Results

| Shot | Method | Base Clean ACC | Base ASR | New Clean ACC | New ASR |
|---:|---|---:|---:|---:|---:|
| 1 | BadCLIP | 93.00% | 94.80% | 86.77% | 83.73% |
| 1 | BadClipMargin | 93.07% | 99.23% | 88.13% | 95.67% |
| 2 | BadCLIP | 95.43% | 98.27% | 91.10% | 93.17% |
| 2 | BadClipMargin | 96.77% | 99.70% | 94.13% | 98.70% |
| 4 | BadCLIP | 97.77% | 97.87% | 93.13% | 96.67% |
| 4 | BadClipMargin | 96.80% | 99.70% | 92.43% | 99.17% |
| 8 | BadCLIP | 97.67% | 99.73% | 91.20% | 99.23% |
| 8 | BadClipMargin | 97.77% | 99.87% | 92.87% | 99.53% |
| 16 | BadCLIP | 97.60% | 99.90% | 94.60% | 99.37% |
| 16 | BadClipMargin | 97.77% | 99.97% | 94.77% | 99.63% |

## Improvement of BadClipMargin over BadCLIP

| Shot | Delta Base Clean ACC | Delta Base ASR | Delta New Clean ACC | Delta New ASR |
|---:|---:|---:|---:|---:|
| 1 | +0.07% | +4.43% | +1.36% | +11.94% |
| 2 | +1.34% | +1.43% | +3.03% | +5.53% |
| 4 | -0.97% | +1.83% | -0.70% | +2.50% |
| 8 | +0.10% | +0.14% | +1.67% | +0.30% |
| 16 | +0.17% | +0.07% | +0.17% | +0.26% |

## Key Observations

1. BadClipMargin substantially improves low-shot backdoor generalization on Caltech101.

2. The largest unseen-class ASR gains appear in the lowest-shot settings:
   - 1-shot New ASR: 83.73% -> 95.67%, +11.94%
   - 2-shot New ASR: 93.17% -> 98.70%, +5.53%

3. From 8-shot onward, BadCLIP is already close to ASR saturation, so the gain of BadClipMargin becomes smaller.

4. BadClipMargin preserves clean accuracy well on Caltech101. There is no severe clean collapse across the tested shot settings.

## Conclusion

Caltech101 provides a clean low-shot curve supporting the central hypothesis: target-margin amplification is most beneficial when BadCLIP lacks sufficient low-shot evidence to form a stable target decision boundary.
