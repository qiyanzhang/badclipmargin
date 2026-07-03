# Caltech101 1-shot Seed1 Mechanism Analysis: BadCLIP vs BadClipMargin

## Setting

- Dataset: Caltech101
- Shot: 1-shot
- Seed: 1
- Baseline: BadCLIP
- Method: BadClipMargin
- BadClipMargin lambda_margin: 0.2
- BadClipMargin margin_m: 5.0
- Evaluation split: new classes

## Alignment Comparison

| Method | Split | align_mean | target_attract_mean | delta_i_norm_mean | delta_t_norm_mean | consistency_to_mean |
|---|---|---:|---:|---:|---:|---:|
| BadCLIP | base | 0.010177 | 0.064964 | 0.639525 | 0.065029 | 0.840044 |
| BadCLIP | new | 0.013333 | 0.056313 | 0.609164 | 0.064057 | 0.847818 |
| BadClipMargin | base | 0.178863 | 0.111123 | 0.652303 | 0.387788 | 0.842068 |
| BadClipMargin | new | 0.184317 | 0.101899 | 0.620665 | 0.376623 | 0.850769 |

BadClipMargin only slightly increases image-side shift magnitude, while it substantially increases target attraction and text-side prompt shift. This indicates that the gain mainly comes from stronger target-oriented cross-modal alignment rather than simply enlarging the image perturbation.

## Cross-split Shared Direction

| Method | cos(base_image_mean_dir,new_image_mean_dir) | new_delta_i to base_mean | Top10 overlap |
|---|---:|---:|---:|
| BadCLIP | 0.989556 | 0.838697 | 0.650964 |
| BadClipMargin | 0.989634 | 0.841672 | 0.635514 |

The shared image-side backdoor direction remains highly consistent across base and new classes for both methods. BadClipMargin does not create a new backdoor subspace.

## Subspace Removal on New Classes

| Method | original ASR | remove_mean ASR | remove_pca10 ASR | remove_random10 ASR |
|---|---:|---:|---:|---:|
| BadCLIP | 87.2271 | 2.6201 | 29.9127 | 86.4629 |
| BadClipMargin | 92.1397 | 12.3362 | 47.3799 | 91.3755 |

Removing the shared mean direction causes a severe ASR drop, while removing random directions has little effect. This confirms that the shared mean direction is necessary for the attack.

## Subspace Keeping on New Classes

| Method | original ASR | keep_mean ASR | keep_mean_pca10 ASR | keep_random10 ASR |
|---|---:|---:|---:|---:|
| BadCLIP | 87.2271 | 79.4760 | 81.0044 | 2.2926 |
| BadClipMargin | 92.1397 | 89.1921 | 88.8646 | 12.9913 |

Keeping only the shared mean direction preserves most of the attack effect, showing that the mean direction is largely sufficient for cross-class backdoor transfer.

## Prompt Ablation on New Classes

| Method | bd_img_bd_prompt | bd_img_clean_prompt | clean_img_bd_prompt | keep_mean_bd_prompt | keep_mean_clean_prompt |
|---|---:|---:|---:|---:|---:|
| BadCLIP | 87.2271 | 82.9694 | 2.1834 | 79.4760 | 73.7991 |
| BadClipMargin | 92.1397 | 17.3581 | 9.9345 | 89.1921 | 13.3188 |

For BadCLIP, the image-side trigger alone remains highly effective even with clean prompts. In contrast, BadClipMargin becomes more dependent on the backdoored prompt: the attack remains strong when the shared mean direction is combined with the backdoored prompt, but drops sharply with clean prompts.

## Conclusion

BadClipMargin improves 1-shot backdoor generalization not by learning a new backdoor direction, but by preserving the original shared image-side direction while strengthening target attraction, target margin, and the coupling between the shared image direction and the target-oriented backdoored prompt.

This supports the central hypothesis that low-shot BadCLIP already contains a transferable shared backdoor direction, but its target-boundary crossing is insufficient. Target-margin amplification improves the attack by making this shared direction more target-discriminative.
