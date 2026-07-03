# BadCLIP Caltech101 Reproduction

## Setting

- Dataset: Caltech101
- Shot: 16
- Backbone: ViT-B/16
- Trainer: BadClip
- Seed: 1
- Target class: 0
- Trigger epsilon: 4
- Environment: PyTorch 2.0.1+cu118, NVIDIA GeForce RTX 4090

## Results

| Model | Dataset | Shot | Split | Clean ACC | ASR |
|---|---|---:|---|---:|---:|
| BadCLIP | Caltech101 | 16 | base/seen | 97.7% | 99.7% |
| BadCLIP | Caltech101 | 16 | new/unseen | 93.7% | 99.3% |

## Notes

The debug run with 1-shot and 1 epoch was only used to verify that the full pipeline works. The formal reproduction result is based on the 16-shot setting.

