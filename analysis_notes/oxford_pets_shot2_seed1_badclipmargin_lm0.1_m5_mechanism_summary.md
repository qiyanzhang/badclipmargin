# OxfordPets 2-shot ep10 BadClipMargin lambda=0.1,m=5.0 Mechanism Summary

## 1. Setting

- Dataset: OxfordPets
- Shots: 2-shot
- Epochs: 10
- Seed: 1
- Method: BadClipMargin
- lambda_margin: 0.1
- margin_m: 5.0
- Target class: abyssinian

## 2. Alignment Analysis

| Split | Align Mean | Target Attraction | Delta-I Norm | Delta-T Norm | PCA Top5 | Consistency |
|---|---:|---:|---:|---:|---:|---:|
| base | 0.068879 | 0.021243 | 0.459750 | 0.035094 | 0.413711 | 0.829974 |
| new | 0.073937 | 0.022001 | 0.453225 | 0.034297 | 0.406449 | 0.827860 |

The image-side shift is highly consistent across samples, and the base/new results are very close. This suggests that BadClipMargin preserves a stable shared backdoor direction on OxfordPets.

## 3. Cross-split Direction Transfer

| Metric | Value |
|---|---:|
| cos(base_image_mean_dir, new_image_mean_dir) | 0.997859 |
| cos(base_text_mean_dir, new_text_mean_dir) | 0.999942 |
| new_delta_i cosine to base_image_mean_dir mean | 0.825970 |
| base_delta_i cosine to new_image_mean_dir mean | 0.828275 |
| base-new subspace overlap Top10 | 0.893408 |

The base and new image-side mean directions are almost identical. This indicates that the backdoor direction learned from base classes transfers strongly to new classes.

## 4. Subspace Removal Evaluation

| Method | ASR | Target Margin |
|---|---:|---:|
| original_backdoor | 94.6309% | 4.775211 |
| remove_mean | 7.7181% | -3.386011 |
| remove_pca10 | 16.1074% | -2.225514 |
| remove_mean_pca10 | 6.5436% | -3.514908 |
| remove_random10 | 94.2953% | 4.433515 |

Removing the mean direction reduces ASR from 94.6309% to 7.7181%, while removing random directions has almost no effect.

This shows that the shared mean direction is a necessary component of the attack.

## 5. Subspace Keep-only Evaluation

| Method | ASR | Target Margin |
|---|---:|---:|
| original_backdoor | 94.6309% | 4.775211 |
| keep_mean | 91.3311% | 4.134128 |
| keep_pca10 | 85.2908% | 2.977808 |
| keep_mean_pca10 | 93.0089% | 4.243315 |
| keep_random10 | 5.3132% | -3.646882 |

Keeping only the mean direction still preserves 91.3311% ASR. This indicates that the mean direction is not only necessary but also nearly sufficient for the attack on OxfordPets.

## 6. Prompt Branch Ablation

| Method | Target Rate | Target Margin |
|---|---:|---:|
| clean_img_clean_prompt | 3.1320% | -4.210099 |
| bd_img_bd_prompt | 94.6309% | 4.775211 |
| bd_img_clean_prompt | 94.1275% | 4.259224 |
| clean_img_bd_prompt | 3.6353% | -4.019051 |
| keep_mean_bd_prompt | 91.3311% | 4.134128 |
| keep_mean_clean_prompt | 89.7092% | 3.610935 |

The trigger-aware prompt alone cannot activate the backdoor, as clean_img_bd_prompt only reaches 3.6353% target rate.

However, the image-side backdoor is very strong. Even with clean prompts, bd_img_clean_prompt reaches 94.1275% target rate. Keeping only the mean direction with clean prompts also reaches 89.7092%.

This suggests that, on OxfordPets, the image-side shared mean direction dominates the attack, while the prompt branch provides additional but relatively smaller amplification.

## 7. Main Mechanism Conclusion

OxfordPets further confirms that BadClipMargin improves low-shot backdoor generalization by strengthening the shared image-side backdoor direction.

The base/new mean directions are highly aligned, removing the mean direction almost disables the attack, and keeping only the mean direction preserves most of the ASR.

Compared with Caltech101, OxfordPets relies more strongly on the image-side shared direction, while the prompt branch mainly provides auxiliary amplification.

Overall, both datasets support the same core mechanism: BadClipMargin enhances the target-discriminative ability of the shared backdoor direction.
