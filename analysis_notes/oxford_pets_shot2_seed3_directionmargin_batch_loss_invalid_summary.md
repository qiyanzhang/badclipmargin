# OxfordPets 2-shot ep10 BadClipDirectionMargin Batch-level Direction Loss Summary

## Setting

- Dataset: OxfordPets
- Shots: 2-shot
- Epochs: 10
- Seed: 3
- Method: BadClipDirectionMargin
- lambda_margin: 0.1
- margin_m: 5.0
- lambda_dir: 0.05

## Result

| Method | Base Clean ACC | Base ASR | New Clean ACC | New ASR |
|---|---:|---:|---:|---:|
| Fixed BadClipMargin lambda=0.1,m=5.0 | 88.2% | 97.2% | 93.7% | 94.2% |
| BadClipDirectionMargin | 86.8% | 98.6% | 80.4% | 96.8% |

## Observation

Although BadClipDirectionMargin increases ASR, new clean accuracy drops significantly.

More importantly, the logged direction loss is almost zero during training. This is likely because the current training configuration uses batch size 1. With batch size 1, the batch mean direction is identical to the current sample direction, making the direction consistency loss nearly zero.

Therefore, the current batch-level direction loss is ineffective under the batch1 setting.

## Next Step

Replace the batch-level shared direction with an EMA-based global shared direction.

The new method should maintain an EMA direction across batches and align each current image-shift direction to this historical shared direction.
