# BadClipMargin Hyperparameter Ablation

## Per-seed Results

| Dataset | Param | Seed | Base Clean | Base ASR | New Clean | New ASR |
|---|---|---:|---:|---:|---:|---:|
| Caltech101 | λ=0.2,m=5 | 1 | 96.3 | 99.7 | 93.3 | 98.3 |
| Caltech101 | λ=0.2,m=5 | 2 | 97.2 | 99.7 | 94.3 | 98.9 |
| Caltech101 | λ=0.2,m=5 | 3 | 96.8 | 99.7 | 94.8 | 98.9 |
| Caltech101 | λ=0.5,m=5 | 1 | 96.7 | 99.8 | 92.0 | 98.6 |
| Caltech101 | λ=0.5,m=5 | 2 | 95.8 | 99.7 | 90.9 | 99.0 |
| Caltech101 | λ=0.5,m=5 | 3 | 95.0 | 99.9 | 94.0 | 99.5 |
| Caltech101 | λ=0.5,m=4 | 1 | 96.8 | 99.8 | 92.1 | 97.8 |
| OxfordPets | λ=0.1,m=5 | 1 | 80.2 | 97.0 | 90.4 | 94.6 |
| OxfordPets | λ=0.1,m=5 | 2 | 83.1 | 96.9 | 90.5 | 95.1 |
| OxfordPets | λ=0.1,m=5 | 3 | 88.2 | 97.2 | 93.7 | 94.2 |
| OxfordPets | λ=0.2,m=5 | 1 | 75.7 | 97.4 | 90.3 | 95.2 |
| OxfordPets | λ=0.2,m=5 | 2 | 66.2 | 99.0 | 46.9 | 89.8 |
| OxfordPets | λ=0.2,m=5 | 3 | 82.2 | 98.7 | 55.8 | 98.9 |

## Mean Results

| Dataset | Param | Seeds | Base Clean | Base ASR | New Clean | New ASR |
|---|---|---:|---:|---:|---:|---:|
| Caltech101 | λ=0.2,m=5 | 3 | 96.77 | 99.70 | 94.13 | 98.70 |
| Caltech101 | λ=0.5,m=4 | 1 | 96.80 | 99.80 | 92.10 | 97.80 |
| Caltech101 | λ=0.5,m=5 | 3 | 95.83 | 99.80 | 92.30 | 99.03 |
| OxfordPets | λ=0.1,m=5 | 3 | 83.83 | 97.03 | 91.53 | 94.63 |
| OxfordPets | λ=0.2,m=5 | 3 | 74.70 | 98.37 | 64.33 | 94.63 |

## Notes

- Caltech101 contains λ=0.2,m=5 and λ=0.5,m=5 with three seeds.
- Caltech101 λ=0.5,m=4 is only available for seed1, so it should be treated as a pilot setting rather than a formal three-seed result.
- OxfordPets contains λ=0.1,m=5 and λ=0.2,m=5 with three seeds.
