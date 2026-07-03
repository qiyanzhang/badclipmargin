# Final Experiment Story: BadClipMargin

## Main Claim

Low-shot BadCLIP does not fail because the transferable shared backdoor direction disappears. Instead, the shared direction already exists, but its target-oriented decision margin is insufficient. BadClipMargin improves low-shot backdoor generalization by amplifying the target-class margin of triggered samples.

## Main Method

BadClipMargin adds a target-margin amplification loss on top of the original BadCLIP objective:

target_margin = target_logit - max_non_target_logit

loss_margin = max(0, m - target_margin)

The final loss is:

loss = loss_badclip + lambda_margin * loss_margin

## Main 2-shot Results

| Dataset | Method | Base Clean | Base ASR | New Clean | New ASR |
|---|---|---:|---:|---:|---:|
| Caltech101 | BadCLIP | 95.43% | 98.27% | 91.10% | 93.17% |
| Caltech101 | BadClipMargin | 96.77% | 99.70% | 94.13% | 98.70% |
| OxfordPets | BadCLIP | 84.23% | 95.07% | 87.03% | 90.63% |
| OxfordPets | BadClipMargin | 83.83% | 97.03% | 91.53% | 94.63% |

## Caltech101 Low-shot Curve

| Shot | Method | Base Clean | Base ASR | New Clean | New ASR |
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

## Mechanism Summary

BadClipMargin preserves the original shared backdoor direction but strengthens target-oriented alignment and target margin.

In Caltech101 1-shot seed1:

| Metric | BadCLIP New | BadClipMargin New |
|---|---:|---:|
| align_mean | 0.013333 | 0.184317 |
| target_attract_mean | 0.056313 | 0.101899 |
| delta_i_norm_mean | 0.609164 | 0.620665 |
| delta_t_norm_mean | 0.064057 | 0.376623 |
| consistency_to_mean | 0.847818 | 0.850769 |

The shared image mean direction remains highly consistent:

| Method | cos(base_image_mean_dir,new_image_mean_dir) | new_delta_i to base_mean | Top10 overlap |
|---|---:|---:|---:|
| BadCLIP | 0.989556 | 0.838697 | 0.650964 |
| BadClipMargin | 0.989634 | 0.841672 | 0.635514 |

Subspace removal and keeping show that the shared mean direction is necessary and largely sufficient for backdoor transfer.

Prompt ablation further shows that BadClipMargin strengthens the coupling between triggered image shift and backdoored prompt.

## Final Interpretation

BadClipMargin improves low-shot backdoor generalization not by learning a new backdoor subspace, but by making the existing shared backdoor direction more target-discriminative and more strongly coupled with the backdoored prompt.
