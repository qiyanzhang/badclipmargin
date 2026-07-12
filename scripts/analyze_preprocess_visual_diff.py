from pathlib import Path
from PIL import Image, ImageChops
import numpy as np

VIS_DIR = Path("analysis_notes/preprocess_strength_sweep/visual_check")
OUT_DIR = Path("analysis_notes/preprocess_strength_sweep/visual_diff")
OUT_DIR.mkdir(parents=True, exist_ok=True)

def load_rgb(path):
    return Image.open(path).convert("RGB")

def save_diff(img_a, img_b, out_path, scale=10):
    a = np.asarray(img_a).astype(np.float32)
    b = np.asarray(img_b).astype(np.float32)
    diff = np.abs(a - b)
    diff_scaled = np.clip(diff * scale, 0, 255).astype(np.uint8)
    Image.fromarray(diff_scaled).save(out_path)

def save_auto_crop(img_a, img_b, out_prefix, pad=20, zoom=6):
    a = np.asarray(img_a).astype(np.float32)
    b = np.asarray(img_b).astype(np.float32)
    diff = np.abs(a - b).mean(axis=2)

    threshold = max(3.0, diff.max() * 0.25)
    ys, xs = np.where(diff >= threshold)

    if len(xs) == 0 or len(ys) == 0:
        # fallback: bottom-right crop, often trigger is near image corner
        w, h = img_a.size
        x1, y1 = int(w * 0.65), int(h * 0.65)
        x2, y2 = w, h
    else:
        x1, x2 = xs.min(), xs.max()
        y1, y2 = ys.min(), ys.max()
        w, h = img_a.size
        x1 = max(0, x1 - pad)
        y1 = max(0, y1 - pad)
        x2 = min(w, x2 + pad)
        y2 = min(h, y2 + pad)

    crop_a = img_a.crop((x1, y1, x2, y2)).resize(
        ((x2 - x1) * zoom, (y2 - y1) * zoom),
        Image.Resampling.NEAREST
    )
    crop_b = img_b.crop((x1, y1, x2, y2)).resize(
        ((x2 - x1) * zoom, (y2 - y1) * zoom),
        Image.Resampling.NEAREST
    )

    crop_a.save(f"{out_prefix}_crop_original.png")
    crop_b.save(f"{out_prefix}_crop_preprocessed.png")

def metrics(img_a, img_b):
    a = np.asarray(img_a).astype(np.float32) / 255.0
    b = np.asarray(img_b).astype(np.float32) / 255.0
    diff = np.abs(a - b)
    mse = np.mean((a - b) ** 2)
    psnr = 99.0 if mse == 0 else 10 * np.log10(1.0 / mse)
    return {
        "l1_mean": float(diff.mean()),
        "l1_max": float(diff.max()),
        "mse": float(mse),
        "psnr": float(psnr),
    }

rows = []

for bd_orig_path in sorted(VIS_DIR.glob("*_bd_original.png")):
    stem = bd_orig_path.name.replace("_bd_original.png", "")
    bd_pre_path = VIS_DIR / f"{stem}_bd_preprocessed.png"
    clean_orig_path = VIS_DIR / f"{stem}_clean_original.png"
    clean_pre_path = VIS_DIR / f"{stem}_clean_preprocessed.png"

    if not bd_pre_path.exists():
        continue

    bd_orig = load_rgb(bd_orig_path)
    bd_pre = load_rgb(bd_pre_path)

    save_diff(bd_orig, bd_pre, OUT_DIR / f"{stem}_bd_diff_x10.png", scale=10)
    save_diff(bd_orig, bd_pre, OUT_DIR / f"{stem}_bd_diff_x30.png", scale=30)
    save_auto_crop(bd_orig, bd_pre, OUT_DIR / f"{stem}_bd")

    bd_m = metrics(bd_orig, bd_pre)

    if clean_orig_path.exists() and clean_pre_path.exists():
        clean_orig = load_rgb(clean_orig_path)
        clean_pre = load_rgb(clean_pre_path)
        save_diff(clean_orig, clean_pre, OUT_DIR / f"{stem}_clean_diff_x10.png", scale=10)
        clean_m = metrics(clean_orig, clean_pre)
    else:
        clean_m = {"l1_mean": None, "l1_max": None, "mse": None, "psnr": None}

    parts = stem.split("_")
    # expected: dataset_method_preprocess_idx, but method may contain underscores
    dataset = parts[0]
    idx = parts[-1]
    preprocess = parts[-2]
    method = "_".join(parts[1:-2])

    rows.append([
        dataset,
        method,
        preprocess,
        idx,
        clean_m["l1_mean"],
        clean_m["l1_max"],
        clean_m["psnr"],
        bd_m["l1_mean"],
        bd_m["l1_max"],
        bd_m["psnr"],
    ])

summary = OUT_DIR / "visual_diff_metrics.md"
with summary.open("w") as f:
    f.write("| Dataset | Method | Preprocess | Idx | Clean L1 mean | Clean L1 max | Clean PSNR | BD L1 mean | BD L1 max | BD PSNR |\n")
    f.write("|---|---|---|---:|---:|---:|---:|---:|---:|---:|\n")
    for r in rows:
        f.write(
            f"| {r[0]} | {r[1]} | {r[2]} | {r[3]} | "
            f"{r[4]:.6f} | {r[5]:.3f} | {r[6]:.2f} | "
            f"{r[7]:.6f} | {r[8]:.3f} | {r[9]:.2f} |\n"
        )

print(f"Saved diff images to: {OUT_DIR}")
print(f"Saved metrics to: {summary}")
