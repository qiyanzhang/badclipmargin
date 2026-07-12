import argparse
import os
import sys
from pathlib import Path
from types import SimpleNamespace

import torch
from PIL import Image

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import backdoor_attack
from dassl.engine import build_trainer
from dassl.utils import set_random_seed, setup_logger


DATA_ROOT = "/mnt/disk3/zhuangrenwei/zqy/badclip_exp/data"
CFG_NAME = "vit_b16_c4_ep10_batch1_ctxv1_init"
LOAD_EPOCH = 10
SHOTS = 2
SUBSAMPLE = "new"

VIS_DIR = Path("analysis_notes/preprocess_strength_sweep/visual_check")

DEFAULT_DATASETS = ["caltech101", "food101"]
DEFAULT_METHODS = ["badclipmargin"]
DEFAULT_PREPROCESSES = [
    "none",
    "color0.95",
    "jpeg98",
    "jpeg95",
    "jpeg90",
    "blur0.3",
    "blur0.5",
    "resize0.95",
    "resize0.90",
]


CLIP_MEAN = torch.tensor([0.48145466, 0.4578275, 0.40821073]).view(1, 3, 1, 1)
CLIP_STD = torch.tensor([0.26862954, 0.26130258, 0.27577711]).view(1, 3, 1, 1)


def build_args(dataset, trainer_name, seed, output_dir):
    return SimpleNamespace(
        root=DATA_ROOT,
        output_dir=str(output_dir),
        resume="",
        seed=seed,
        source_domains=None,
        target_domains=None,
        transforms=None,
        config_file=f"configs/trainers/BadClip/{CFG_NAME}.yaml",
        dataset_config_file=f"configs/datasets/{dataset}.yaml",
        trainer=trainer_name,
        backbone="",
        head="",
        opts=[
            "DATASET.NUM_SHOTS", str(SHOTS),
            "DATASET.SUBSAMPLE_CLASSES", SUBSAMPLE,
            "BACKDOOR.TARGET", "0",
        ],
    )


def get_method_spec(dataset, method, seed):
    method = method.lower()

    if method == "badclip":
        return {
            "trainer": "BadClip",
            "tag": "badclip",
            "model_dir": Path(
                f"output/train_seen/{dataset}/shots_{SHOTS}/BadClip/{CFG_NAME}/seed{seed}"
            ),
            "extra_env": {},
        }

    if method == "badclipmargin":
        lambda_margin = "0.2" if dataset == "caltech101" else "0.1"
        return {
            "trainer": "BadClipMargin",
            "tag": f"badclipmargin_lm{lambda_margin}_m5",
            "model_dir": Path(
                f"output/train_seen/{dataset}/shots_{SHOTS}/BadClipMargin/{CFG_NAME}_lm{lambda_margin}_m5/seed{seed}"
            ),
            "extra_env": {
                "BADCLIP_MARGIN_LAMBDA": lambda_margin,
                "BADCLIP_MARGIN_M": "5.0",
            },
        }

    raise ValueError(f"Unsupported method: {method}")


def denormalize_to_01(x):
    mean = CLIP_MEAN.to(device=x.device, dtype=x.dtype)
    std = CLIP_STD.to(device=x.device, dtype=x.dtype)
    return (x * std + mean).clamp(0.0, 1.0)


def save_rgb_tensor(image_chw_01, path):
    path.parent.mkdir(parents=True, exist_ok=True)
    array = (
        image_chw_01.detach()
        .clamp(0.0, 1.0)
        .mul(255.0)
        .round()
        .to(torch.uint8)
        .permute(1, 2, 0)
        .cpu()
        .numpy()
    )
    Image.fromarray(array).save(path)


def apply_preprocess(trainer, image, mode):
    old_mode = os.environ.get("BADCLIP_PREPROCESS")
    os.environ["BADCLIP_PREPROCESS"] = mode

    try:
        try:
            return trainer.apply_input_preprocess(image, mode=mode)
        except TypeError:
            return trainer.apply_input_preprocess(image)
    finally:
        if old_mode is None:
            os.environ.pop("BADCLIP_PREPROCESS", None)
        else:
            os.environ["BADCLIP_PREPROCESS"] = old_mode


def collect_images(trainer, num_images):
    images = []
    with torch.no_grad():
        for batch in trainer.test_loader:
            batch_images = batch["img"].to(trainer.device)
            for image in batch_images:
                images.append(image.unsqueeze(0))
                if len(images) >= num_images:
                    return images
    return images


def build_trainer_for_visual_check(dataset, method, seed):
    spec = get_method_spec(dataset, method, seed)
    model_dir = spec["model_dir"]

    if not model_dir.exists():
        print(f"[WARN] Missing checkpoint directory: {model_dir}")
        print("[INFO] Candidate directories:")
        cmd = (
            f'find output/train_seen -type d | grep -i "{dataset}" '
            f'| grep -i "{spec["trainer"]}" | grep "seed{seed}"'
        )
        print(os.popen(cmd).read().strip())
        return None, None

    for key, value in spec.get("extra_env", {}).items():
        os.environ[key] = value

    os.environ.setdefault("BADCLIP_PREPROCESS", "none")

    output_dir = Path("output/preprocess_strength_sweep_visual") / dataset / method / f"seed{seed}"
    args = build_args(dataset, spec["trainer"], seed, output_dir)
    cfg = backdoor_attack.setup_cfg(args)

    if cfg.SEED >= 0:
        set_random_seed(cfg.SEED)

    setup_logger(cfg.OUTPUT_DIR)

    if torch.cuda.is_available() and cfg.USE_CUDA:
        torch.backends.cudnn.benchmark = True

    trainer = build_trainer(cfg)
    trainer.load_model(str(model_dir), epoch=LOAD_EPOCH)

    return trainer, spec


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--datasets", nargs="+", default=DEFAULT_DATASETS)
    parser.add_argument("--methods", nargs="+", default=DEFAULT_METHODS)
    parser.add_argument("--seed", type=int, default=1)
    parser.add_argument("--num-images", type=int, default=3)
    parser.add_argument("--preprocesses", nargs="+", default=DEFAULT_PREPROCESSES)
    args = parser.parse_args()

    VIS_DIR.mkdir(parents=True, exist_ok=True)

    for dataset in args.datasets:
        for method in args.methods:
            trainer, spec = build_trainer_for_visual_check(dataset, method, args.seed)
            if trainer is None:
                continue

            trainer.set_model_mode("eval")
            model_core = trainer.model.module if isinstance(trainer.model, torch.nn.DataParallel) else trainer.model

            images = collect_images(trainer, args.num_images)
            print(f"[VisualCheck] dataset={dataset} method={method} images={len(images)}")

            with torch.no_grad():
                for preprocess in args.preprocesses:
                    print(f"[VisualCheck] preprocess={preprocess}")

                    for idx, image in enumerate(images):
                        clean_original = denormalize_to_01(image)[0]

                        clean_preprocessed_norm = apply_preprocess(
                            trainer, image.clone(), preprocess
                        )
                        clean_preprocessed = denormalize_to_01(clean_preprocessed_norm)[0]

                        bd_original_norm = model_core.trigger(image.clone())
                        bd_original = denormalize_to_01(bd_original_norm)[0]

                        bd_preprocessed_norm = apply_preprocess(
                            trainer, bd_original_norm.clone(), preprocess
                        )
                        bd_preprocessed = denormalize_to_01(bd_preprocessed_norm)[0]

                        stem = f"{dataset}_{method}_{preprocess}_{idx}"
                        save_rgb_tensor(clean_original, VIS_DIR / f"{stem}_clean_original.png")
                        save_rgb_tensor(clean_preprocessed, VIS_DIR / f"{stem}_clean_preprocessed.png")
                        save_rgb_tensor(bd_original, VIS_DIR / f"{stem}_bd_original.png")
                        save_rgb_tensor(bd_preprocessed, VIS_DIR / f"{stem}_bd_preprocessed.png")

    print(f"[VisualCheck] Saved images to: {VIS_DIR}")


if __name__ == "__main__":
    main()
