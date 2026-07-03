# OxfordPets 2-shot ep10 BadCLIP vs BadClipMargin Mechanism Comparison

## 1. Setting

- Dataset: OxfordPets
- Shots: 2-shot
- Epochs: 10
- Seed: 1
- Target class: abyssinian
- Baseline: BadCLIP
- Method: BadClipMargin
- BadClipMargin lambda_margin: 0.1
- BadClipMargin margin_m: 5.0

## 2. Alignment Comparison

| Metric | BadCLIP Base | BadClipMargin Base | BadCLIP New | BadClipMargin New |
|---|---:|---:|---:|---:|
| align_mean | 0.083656 | 0.068879 | 0.086819 | 0.073937 |
| target_attract_mean | 0.016529 | 0.021243 | 0.016935 | 0.022001 |
| delta_i_norm_mean | 0.435443 | 0.459750 | 0.429708 | 0.453225 |
| delta_t_norm_mean | 0.042124 | 0.035094 | 0.041370 | 0.034297 |
| PCA Top5 cumulative | 0.419781 | 0.413711 | 0.409416 | 0.406449 |
| consistency_mean | 0.819925 | 0.829974 | 0.818340 | 0.827860 |

BadClipMargin increases target attraction and slightly improves image-shift consistency, while keeping the overall shared-direction structure similar to BadCLIP.

This suggests that BadClipMargin does not learn a completely different backdoor direction. Instead, it strengthens the target-discriminative ability of the existing shared image-side direction.

## 3. Cross-split Direction Comparison

| Metric | BadCLIP | BadClipMargin |
|---|---:|---:|
| cos(base_image_mean_dir, new_image_mean_dir) | 0.997991 | 0.997859 |
| cos(base_text_mean_dir, new_text_mean_dir) | 0.999935 | 0.999942 |
| new_delta_i cosine to base_image_mean_dir mean | 0.816524 | 0.825970 |
| base_delta_i cosine to new_image_mean_dir mean | 0.818426 | 0.828275 |
| base-new subspace overlap Top10 | 0.886957 | 0.893408 |

Both methods show highly consistent base/new image-side backdoor directions. BadClipMargin preserves the cross-class transferable backdoor structure.

## 4. Subspace Removal Comparison

| Method | BadCLIP ASR | BadClipMargin ASR | BadCLIP Target Margin | BadClipMargin Target Margin |
|---|---:|---:|---:|---:|
| original_backdoor | 82.6063% | 94.6309% | 2.457180 | 4.775211 |
| remove_mean | 8.3333% | 7.7181% | -3.077775 | -3.386011 |
| remove_pca10 | 15.4362% | 16.1074% | -2.435420 | -2.225514 |
| remove_mean_pca10 | 7.8859% | 6.5436% | -3.151697 | -3.514908 |
| remove_random10 | 81.4318% | 94.2953% | 2.328134 | 4.433515 |

Removing the mean direction disables both BadCLIP and BadClipMargin, confirming that the mean direction is a necessary component of the attack.

BadClipMargin achieves a much larger original target margin than BadCLIP, showing that the margin loss directly strengthens target-boundary crossing.

## 5. Subspace Keep-only Comparison

| Method | BadCLIP ASR | BadClipMargin ASR | BadCLIP Target Margin | BadClipMargin Target Margin |
|---|---:|---:|---:|---:|
| original_backdoor | 82.6063% | 94.6309% | 2.457180 | 4.775211 |
| keep_mean | 76.3423% | 91.3311% | 1.905857 | 4.134128 |
| keep_pca10 | 69.1275% | 85.2908% | 1.235817 | 2.977808 |
| keep_mean_pca10 | 77.3490% | 93.0089% | 1.971276 | 4.243315 |
| keep_random10 | 5.4810% | 5.3132% | -3.471468 | -3.646882 |

Keeping only the mean direction preserves much more ASR for BadClipMargin than for BadCLIP.

This indicates that BadClipMargin strengthens the attack capability carried by the shared mean direction.

## 6. Prompt Branch Ablation Comparison

| Method | BadCLIP Target Rate | BadClipMargin Target Rate | BadCLIP Target Margin | BadClipMargin Target Margin |
|---|---:|---:|---:|---:|
| clean_img_clean_prompt | 3.6913% | 3.1320% | -3.795232 | -4.210099 |
| bd_img_bd_prompt | 82.6063% | 94.6309% | 2.457180 | 4.775211 |
| bd_img_clean_prompt | 79.5861% | 94.1275% | 2.039866 | 4.259224 |
| clean_img_bd_prompt | 4.6421% | 3.6353% | -3.614181 | -4.019051 |
| keep_mean_bd_prompt | 76.3423% | 91.3311% | 1.905857 | 4.134128 |
| keep_mean_clean_prompt | 71.5324% | 89.7092% | 1.490885 | 3.610935 |

The trigger-aware prompt alone cannot activate the backdoor for either method.

BadClipMargin mainly improves the image-side backdoor effect: bd_img_clean_prompt and keep_mean_clean_prompt both increase substantially compared with BadCLIP.

## 7. Main Conclusion

OxfordPets confirms the mechanism of BadClipMargin.

BadClipMargin does not change the fundamental shared-direction structure of BadCLIP. The base/new mean directions remain highly aligned, and the attack still depends on the shared image-side mean direction.

The key difference is that BadClipMargin makes this shared direction more target-discriminative. It increases target attraction, enlarges target margin, and allows the mean direction alone to preserve much higher ASR.

Therefore, BadClipMargin improves low-shot backdoor generalization by amplifying the target-boundary crossing ability of the existing shared backdoor direction.
