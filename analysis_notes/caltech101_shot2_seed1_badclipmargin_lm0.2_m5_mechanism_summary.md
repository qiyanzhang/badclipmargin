# Caltech101 2-shot ep10 BadClipMargin Mechanism Summary

## 1. Setting

- Dataset: Caltech101
- Shots: 2-shot
- Epochs: 10
- Seed: 1
- Method: BadClipMargin
- lambda_margin: 0.2
- margin_m: 5.0
- Target class: face

This analysis investigates why BadClipMargin improves low-shot cross-class backdoor generalization.

## 2. Alignment Analysis

| Split | Align Mean | Target Attraction | Delta-I Norm | Delta-T Norm | PCA Top5 | Consistency |
|---|---:|---:|---:|---:|---:|---:|
| base | -0.000264 | 0.132317 | 0.716895 | 0.175256 | 0.342506 | 0.830771 |
| new | 0.006299 | 0.124308 | 0.674619 | 0.177769 | 0.297417 | 0.838506 |

Compared with the original BadCLIP 2-shot ep10 seed1 setting, BadClipMargin keeps a similar image-shift norm but increases target attraction on new classes.

This indicates that BadClipMargin does not simply enlarge the trigger-induced image shift. Instead, it makes the shared backdoor direction more target-discriminative.

## 3. Cross-split Direction Transfer

| Metric | Value |
|---|---:|
| cos(base_image_mean_dir, new_image_mean_dir) | 0.986674 |
| cos(base_text_mean_dir, new_text_mean_dir) | 0.999533 |
| new_delta_i cosine to base_image_mean_dir mean | 0.826438 |
| base_delta_i cosine to new_image_mean_dir mean | 0.821686 |

The image-side backdoor direction remains highly shared between base and new classes. Therefore, BadClipMargin preserves the cross-class shared global backdoor direction.

However, actual image-text alignment is close to the shuffled baseline, suggesting that the attack does not rely on instance-wise image-text shift alignment.

## 4. Subspace Removal Evaluation

| Method | ASR | Target Margin |
|---|---:|---:|
| original_backdoor | 98.2533% | 7.199730 |
| remove_mean | 2.7293% | -5.204473 |
| remove_pca10 | 79.3668% | 2.265582 |
| remove_mean_pca10 | 3.3843% | -5.321797 |
| remove_random10 | 98.2533% | 6.817524 |

Removing the mean direction reduces ASR from 98.2533% to 2.7293%, while removing random directions has almost no effect.

This shows that the shared mean direction is a necessary component of the attack.

## 5. Subspace Keep-only Evaluation

| Method | ASR | Target Margin |
|---|---:|---:|
| original_backdoor | 98.2533% | 7.199730 |
| keep_mean | 94.4323% | 4.711441 |
| keep_mean_pca10 | 96.6157% | 5.175832 |
| keep_pca10 | 23.6900% | -1.875461 |
| keep_random10 | 1.7467% | -6.488341 |

Keeping only the mean direction still preserves 94.4323% ASR, showing that the shared mean direction is approximately sufficient for the attack.

Compared with the original BadCLIP 2-shot ep10 setting, where keep_mean achieved only 77.0742% ASR, BadClipMargin significantly strengthens the attack capability carried by the shared mean direction.

## 6. Prompt Branch Ablation

| Method | Target Rate | Target Margin |
|---|---:|---:|
| clean_img_clean_prompt | 0.0000% | -9.103716 |
| bd_img_bd_prompt | 98.2533% | 7.199730 |
| bd_img_clean_prompt | 94.6507% | 4.606714 |
| clean_img_bd_prompt | 1.3100% | -6.844202 |
| keep_mean_bd_prompt | 94.4323% | 4.711441 |
| keep_mean_clean_prompt | 82.4236% | 2.311289 |

The prompt branch alone cannot trigger the attack, as clean_img_bd_prompt only achieves 1.3100% target rate.

However, the image-side backdoor has become much stronger. Even with clean prompts, bd_img_clean_prompt achieves 94.6507% target rate. Keeping only the mean direction with clean prompts also achieves 82.4236%.

The trigger-aware prompt branch still provides additional amplification, increasing keep_mean_clean_prompt from 82.4236% to keep_mean_bd_prompt 94.4323%.

## 7. Main Mechanism Conclusion

BadClipMargin improves low-shot BadCLIP by strengthening the target-discriminative ability of the shared image-side backdoor direction.

It does not mainly increase the magnitude of the image feature shift. Instead, it makes the shared mean direction more effective at crossing the target decision boundary.

The attack remains dependent on the shared mean direction, while the trigger-aware prompt branch further amplifies the target margin.

Therefore, BadClipMargin addresses the low-shot bottleneck of BadCLIP by enhancing target margin rather than merely improving direction consistency.
