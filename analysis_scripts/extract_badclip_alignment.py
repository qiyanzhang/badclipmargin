import argparse
import os
import sys
from types import SimpleNamespace

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

import numpy as np
import torch
import torch.nn.functional as F

from backdoor_attack import setup_cfg
from trainers.badclip import BadClip


def build_args(cli_args):
    opts = [
        "DATASET.NUM_SHOTS", str(cli_args.num_shots),
        "DATASET.SUBSAMPLE_CLASSES", cli_args.subsample,
    ]

    return SimpleNamespace(
        root=cli_args.root,
        output_dir=cli_args.output_dir,
        resume="",
        seed=cli_args.seed,
        source_domains=None,
        target_domains=None,
        transforms=None,
        trainer="BadClip",
        backbone="",
        head="",
        dataset_config_file=cli_args.dataset_config_file,
        config_file=cli_args.config_file,
        model_dir=cli_args.model_dir,
        load_epoch=cli_args.load_epoch,
        eval_only=False,
        no_train=False,
        opts=opts,
    )


def unwrap_model(model):
    return model.module if hasattr(model, "module") else model


def parse_batch(trainer, batch):
    if hasattr(trainer, "parse_batch_test"):
        return trainer.parse_batch_test(batch)

    if isinstance(batch, dict):
        image = batch["img"].to(trainer.device)
        label = batch["label"].to(trainer.device)
        return image, label

    image, label = batch[0].to(trainer.device), batch[1].to(trainer.device)
    return image, label


@torch.no_grad()
def extract_image_and_target_text_features(model, image):
    """
    Return:
      image_features: [B, D]
      target_text_features: [B, D]

    For each image, BadCLIP/CoCoOp generates instance-conditioned prompts.
    We take the target-class text feature for each instance.
    """
    tokenized_prompts = model.tokenized_prompts
    target = int(model.trigger.target)

    image_features = model.image_encoder(image.type(model.dtype))
    image_features = image_features / image_features.norm(dim=-1, keepdim=True)

    prompts = model.prompt_learner(image_features)

    target_text_features = []
    for pts_i in prompts:
        text_features = model.text_encoder(pts_i, tokenized_prompts)
        text_features = text_features / text_features.norm(dim=-1, keepdim=True)
        target_text_features.append(text_features[target])

    target_text_features = torch.stack(target_text_features, dim=0)

    return image_features.float(), target_text_features.float()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", required=True)
    parser.add_argument("--model-dir", required=True)
    parser.add_argument("--load-epoch", type=int, default=10)
    parser.add_argument("--subsample", default="base", choices=["base", "new", "all"])
    parser.add_argument("--num-shots", type=int, default=16)
    parser.add_argument("--seed", type=int, default=1)
    parser.add_argument("--max-batches", type=int, default=0)
    parser.add_argument("--out", required=True)

    parser.add_argument(
        "--dataset-config-file",
        default="configs/datasets/caltech101.yaml",
    )
    parser.add_argument(
        "--config-file",
        default="configs/trainers/BadClip/vit_b16_c4_ep10_batch1_ctxv1_init.yaml",
    )
    parser.add_argument(
        "--output-dir",
        default="output/analysis_extract",
    )

    cli_args = parser.parse_args()

    os.makedirs(os.path.dirname(cli_args.out), exist_ok=True)

    args = build_args(cli_args)
    cfg = setup_cfg(args)

    print("Building BadClip trainer...")
    trainer = BadClip(cfg)

    print(f"Loading model from: {cli_args.model_dir}")
    trainer.load_model(cli_args.model_dir, epoch=cli_args.load_epoch)

    model = unwrap_model(trainer.model)
    model.eval()

    target = int(model.trigger.target)
    target_name = model.prompt_learner.classnames[target]
    print(f"Target index: {target}")
    print(f"Target name: {target_name}")

    all_labels = []
    all_align = []
    all_target_attract = []
    all_delta_i_norm = []
    all_delta_t_norm = []
    all_delta_i = []
    all_delta_t = []

    loader = trainer.test_loader

    for batch_idx, batch in enumerate(loader):
        if cli_args.max_batches > 0 and batch_idx >= cli_args.max_batches:
            break

        image, label = parse_batch(trainer, batch)
        image = image.to(trainer.device)
        label = label.to(trainer.device)

        clean_image = image
        bd_image = model.trigger(image.clone())

        clean_img_feat, clean_txt_feat = extract_image_and_target_text_features(
            model, clean_image
        )
        bd_img_feat, bd_txt_feat = extract_image_and_target_text_features(
            model, bd_image
        )

        delta_i = bd_img_feat - clean_img_feat
        delta_t = bd_txt_feat - clean_txt_feat

        delta_i_norm = delta_i.norm(dim=-1)
        delta_t_norm = delta_t.norm(dim=-1)

        delta_i_unit = F.normalize(delta_i, dim=-1, eps=1e-8)
        delta_t_unit = F.normalize(delta_t, dim=-1, eps=1e-8)

        align = (delta_i_unit * delta_t_unit).sum(dim=-1)

        clean_sim = (clean_img_feat * clean_txt_feat).sum(dim=-1)
        bd_sim = (bd_img_feat * bd_txt_feat).sum(dim=-1)
        target_attract = bd_sim - clean_sim

        all_labels.append(label.detach().cpu())
        all_align.append(align.detach().cpu())
        all_target_attract.append(target_attract.detach().cpu())
        all_delta_i_norm.append(delta_i_norm.detach().cpu())
        all_delta_t_norm.append(delta_t_norm.detach().cpu())
        all_delta_i.append(delta_i.detach().cpu())
        all_delta_t.append(delta_t.detach().cpu())

        if (batch_idx + 1) % 10 == 0:
            print(f"Processed batches: {batch_idx + 1}")

    labels = torch.cat(all_labels).numpy()
    align = torch.cat(all_align).numpy()
    target_attract = torch.cat(all_target_attract).numpy()
    delta_i_norm = torch.cat(all_delta_i_norm).numpy()
    delta_t_norm = torch.cat(all_delta_t_norm).numpy()
    delta_i = torch.cat(all_delta_i).numpy()
    delta_t = torch.cat(all_delta_t).numpy()

    # PCA/SVD on image shift
    x = delta_i - delta_i.mean(axis=0, keepdims=True)
    _, s, _ = np.linalg.svd(x, full_matrices=False)
    var = s ** 2
    explained = var / (var.sum() + 1e-12)
    pca_top10 = explained[:10]

    # Direction consistency: cosine to mean direction
    mean_dir = delta_i.mean(axis=0)
    mean_dir = mean_dir / (np.linalg.norm(mean_dir) + 1e-12)
    delta_i_unit_np = delta_i / (np.linalg.norm(delta_i, axis=1, keepdims=True) + 1e-12)
    consistency_to_mean = delta_i_unit_np @ mean_dir

    np.savez(
        cli_args.out,
        labels=labels,
        align=align,
        target_attract=target_attract,
        delta_i_norm=delta_i_norm,
        delta_t_norm=delta_t_norm,
        delta_i=delta_i,
        delta_t=delta_t,
        pca_explained_top10=pca_top10,
        consistency_to_mean=consistency_to_mean,
        target_index=target,
        target_name=np.array([target_name]),
    )

    summary_path = cli_args.out.replace(".npz", ".summary.txt")
    with open(summary_path, "w") as f:
        f.write("# BadCLIP Alignment Analysis\n\n")
        f.write(f"subsample: {cli_args.subsample}\n")
        f.write(f"num_samples: {len(labels)}\n")
        f.write(f"target_index: {target}\n")
        f.write(f"target_name: {target_name}\n\n")

        f.write("## Cross-modal alignment\n")
        f.write(f"align_mean: {align.mean():.6f}\n")
        f.write(f"align_std: {align.std():.6f}\n")
        f.write(f"align_median: {np.median(align):.6f}\n\n")

        f.write("## Target attraction\n")
        f.write(f"target_attract_mean: {target_attract.mean():.6f}\n")
        f.write(f"target_attract_std: {target_attract.std():.6f}\n")
        f.write(f"target_attract_median: {np.median(target_attract):.6f}\n\n")

        f.write("## Shift norm\n")
        f.write(f"delta_i_norm_mean: {delta_i_norm.mean():.6f}\n")
        f.write(f"delta_t_norm_mean: {delta_t_norm.mean():.6f}\n\n")

        f.write("## Image-shift PCA explained ratio top10\n")
        for i, v in enumerate(pca_top10, start=1):
            f.write(f"PC{i}: {v:.6f}\n")
        f.write(f"Top1 cumulative: {pca_top10[:1].sum():.6f}\n")
        f.write(f"Top3 cumulative: {pca_top10[:3].sum():.6f}\n")
        f.write(f"Top5 cumulative: {pca_top10[:5].sum():.6f}\n\n")

        f.write("## Image-shift consistency to mean direction\n")
        f.write(f"consistency_mean: {consistency_to_mean.mean():.6f}\n")
        f.write(f"consistency_std: {consistency_to_mean.std():.6f}\n")

    csv_path = cli_args.out.replace(".npz", ".csv")
    table = np.stack(
        [labels, align, target_attract, delta_i_norm, delta_t_norm, consistency_to_mean],
        axis=1,
    )
    header = "label,align,target_attract,delta_i_norm,delta_t_norm,consistency_to_mean"
    np.savetxt(csv_path, table, delimiter=",", header=header, comments="")

    print("Saved:")
    print(cli_args.out)
    print(summary_path)
    print(csv_path)

    print("\n===== Summary =====")
    print(f"subsample: {cli_args.subsample}")
    print(f"num_samples: {len(labels)}")
    print(f"target_name: {target_name}")
    print(f"align_mean: {align.mean():.6f}")
    print(f"target_attract_mean: {target_attract.mean():.6f}")
    print(f"delta_i_norm_mean: {delta_i_norm.mean():.6f}")
    print(f"delta_t_norm_mean: {delta_t_norm.mean():.6f}")
    print(f"PCA top1: {pca_top10[:1].sum():.6f}")
    print(f"PCA top3: {pca_top10[:3].sum():.6f}")
    print(f"PCA top5: {pca_top10[:5].sum():.6f}")
    print(f"consistency_mean: {consistency_to_mean.mean():.6f}")


if __name__ == "__main__":
    main()
