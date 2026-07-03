import argparse
import numpy as np


def unit(x):
    return x / (np.linalg.norm(x, axis=-1, keepdims=True) + 1e-12)


def mean_dir(x):
    m = x.mean(axis=0)
    return m / (np.linalg.norm(m) + 1e-12)


def pca_basis(x, k):
    x_center = x - x.mean(axis=0, keepdims=True)
    _, _, vh = np.linalg.svd(x_center, full_matrices=False)
    return vh[:k].T


def energy_in_subspace(x, basis):
    x_center = x - x.mean(axis=0, keepdims=True)
    proj = x_center @ basis @ basis.T
    return np.sum(proj ** 2) / (np.sum(x_center ** 2) + 1e-12)


def subspace_overlap(a, b):
    k = a.shape[1]
    return np.linalg.norm(a.T @ b, ord="fro") ** 2 / k


def shuffled_alignment(di, dt, n=100, seed=1):
    rng = np.random.default_rng(seed)
    di_u = unit(di)
    dt_u = unit(dt)
    vals = []
    for _ in range(n):
        perm = rng.permutation(len(dt_u))
        vals.append(np.sum(di_u * dt_u[perm], axis=1).mean())
    return float(np.mean(vals)), float(np.std(vals))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--base", required=True)
    parser.add_argument("--new", required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()

    base = np.load(args.base, allow_pickle=True)
    new = np.load(args.new, allow_pickle=True)

    base_di = base["delta_i"]
    new_di = new["delta_i"]
    base_dt = base["delta_t"]
    new_dt = new["delta_t"]

    base_mean_i = mean_dir(base_di)
    new_mean_i = mean_dir(new_di)
    base_mean_t = mean_dir(base_dt)
    new_mean_t = mean_dir(new_dt)

    cos_base_new_image_mean = float(base_mean_i @ new_mean_i)
    cos_base_new_text_mean = float(base_mean_t @ new_mean_t)

    new_to_base_mean = unit(new_di) @ base_mean_i
    base_to_new_mean = unit(base_di) @ new_mean_i

    base_align_shuffle_mean, base_align_shuffle_std = shuffled_alignment(base_di, base_dt)
    new_align_shuffle_mean, new_align_shuffle_std = shuffled_alignment(new_di, new_dt)

    lines = []
    lines.append("# Cross-split Backdoor Subspace Analysis")
    lines.append("")
    lines.append("## Mean direction similarity")
    lines.append(f"cos(base_image_mean_dir, new_image_mean_dir): {cos_base_new_image_mean:.6f}")
    lines.append(f"cos(base_text_mean_dir, new_text_mean_dir): {cos_base_new_text_mean:.6f}")
    lines.append("")
    lines.append("## New shifts projected to base mean direction")
    lines.append(f"new_delta_i cosine to base_image_mean_dir mean: {new_to_base_mean.mean():.6f}")
    lines.append(f"new_delta_i cosine to base_image_mean_dir std: {new_to_base_mean.std():.6f}")
    lines.append(f"base_delta_i cosine to new_image_mean_dir mean: {base_to_new_mean.mean():.6f}")
    lines.append(f"base_delta_i cosine to new_image_mean_dir std: {base_to_new_mean.std():.6f}")
    lines.append("")
    lines.append("## Pairwise alignment vs shuffled baseline")
    lines.append(f"base actual align mean: {base['align'].mean():.6f}")
    lines.append(f"base shuffled align mean: {base_align_shuffle_mean:.6f}")
    lines.append(f"base shuffled align std: {base_align_shuffle_std:.6f}")
    lines.append(f"new actual align mean: {new['align'].mean():.6f}")
    lines.append(f"new shuffled align mean: {new_align_shuffle_mean:.6f}")
    lines.append(f"new shuffled align std: {new_align_shuffle_std:.6f}")
    lines.append("")
    lines.append("## PCA subspace transfer and overlap")

    for k in [1, 3, 5, 10]:
        base_basis = pca_basis(base_di, k)
        new_basis = pca_basis(new_di, k)

        base_energy_in_base = energy_in_subspace(base_di, base_basis)
        new_energy_in_new = energy_in_subspace(new_di, new_basis)
        new_energy_in_base = energy_in_subspace(new_di, base_basis)
        base_energy_in_new = energy_in_subspace(base_di, new_basis)
        overlap = subspace_overlap(base_basis, new_basis)

        lines.append(f"Top-{k}:")
        lines.append(f"  base energy in base PCs: {base_energy_in_base:.6f}")
        lines.append(f"  new energy in new PCs: {new_energy_in_new:.6f}")
        lines.append(f"  new energy in base PCs: {new_energy_in_base:.6f}")
        lines.append(f"  base energy in new PCs: {base_energy_in_new:.6f}")
        lines.append(f"  base-new subspace overlap: {overlap:.6f}")

    with open(args.out, "w") as f:
        f.write("\n".join(lines))

    print("\n".join(lines))
    print(f"\nSaved to: {args.out}")


if __name__ == "__main__":
    main()
