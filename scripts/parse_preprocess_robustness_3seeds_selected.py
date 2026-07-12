import csv
import re
import statistics
from pathlib import Path
from collections import defaultdict

LOG_DIR = Path("analysis_notes/preprocess_robustness_3seeds_selected")
OUT_MD = LOG_DIR / "robustness_3seeds_selected_summary.md"
OUT_CSV = LOG_DIR / "robustness_3seeds_selected_summary.csv"
OUT_TEX = LOG_DIR / "robustness_3seeds_selected_latex_table.tex"

PREPROCESS_ORDER = [
    "none",
    "color0.90",
    "blur0.5",
    "jpeg70",
    "resize0.95",
    "color0.98",
    "color0.95",
    "jpeg99",
    "jpeg98",
    "jpeg95",
    "jpeg90",
    "jpeg80",
    "blur0.1",
    "blur0.3",
    "blur1.0",
    "resize0.98",
    "resize0.90",
    "resize0.75",
]

DATASET_ORDER = ["caltech101", "food101"]
METHOD_ORDER = ["BadCLIP", "BadClipMargin"]

METHOD_NAME = {
    "badclip": "BadCLIP",
    "badclipmargin_lm0.2_m5": "BadClipMargin",
    "badclipmargin_lm0.1_m5": "BadClipMargin",
}


def parse_filename(path):
    name = path.name
    suffix = "_test_unseen.run.log"

    if not name.endswith(suffix):
        raise ValueError("Unexpected suffix: {}".format(name))

    stem = name[:-len(suffix)]

    m = re.match(r"^(?P<dataset>.+)_shot(?P<shot>\d+)_seed(?P<seed>\d+)_(?P<rest>.+)$", stem)
    if m is None:
        raise ValueError("Unexpected filename structure: {}".format(name))

    dataset = m.group("dataset")
    shot = int(m.group("shot"))
    seed = int(m.group("seed"))
    rest = m.group("rest")

    method_tag = None
    preprocess = None

    for pp in sorted(PREPROCESS_ORDER, key=len, reverse=True):
        marker = "_" + pp
        if rest.endswith(marker):
            method_tag = rest[:-len(marker)]
            preprocess = pp
            break

    if method_tag is None or preprocess is None:
        raise ValueError("Cannot split method/preprocess: {}".format(name))

    method = METHOD_NAME.get(method_tag, method_tag)

    return {
        "dataset": dataset,
        "shot": shot,
        "seed": seed,
        "method": method,
        "method_tag": method_tag,
        "preprocess": preprocess,
    }


def parse_log(path):
    meta = parse_filename(path)
    text = path.read_text(errors="ignore")

    accs = [float(x) for x in re.findall(r"\* accuracy:\s*([0-9.]+)%", text)]
    if len(accs) < 2:
        raise ValueError("Less than two accuracy values: {}".format(path.name))

    meta["new_clean"] = accs[-2]
    meta["new_asr"] = accs[-1]
    meta["path"] = str(path)
    return meta


def mean_std(values):
    mean = statistics.mean(values)
    std = statistics.stdev(values) if len(values) > 1 else 0.0
    return mean, std


def fmt_mean_std(values):
    mean, std = mean_std(values)
    return "{:.2f}±{:.2f}".format(mean, std)


def latex_mean_std(values):
    return fmt_mean_std(values).replace("±", r"$\pm$")


def dataset_rank(dataset):
    return DATASET_ORDER.index(dataset) if dataset in DATASET_ORDER else 999


def method_rank(method):
    return METHOD_ORDER.index(method) if method in METHOD_ORDER else 999


def preprocess_rank(preprocess):
    return PREPROCESS_ORDER.index(preprocess) if preprocess in PREPROCESS_ORDER else 999


def sort_key(row):
    return (
        dataset_rank(row["dataset"]),
        method_rank(row["method"]),
        row["seed"],
        preprocess_rank(row["preprocess"]),
    )


def group_key_sort(key):
    dataset, method, preprocess = key
    return (
        dataset_rank(dataset),
        method_rank(method),
        preprocess_rank(preprocess),
    )


def main():
    LOG_DIR.mkdir(parents=True, exist_ok=True)

    log_paths = sorted(LOG_DIR.glob("*.run.log"))
    if not log_paths:
        raise RuntimeError("No .run.log files found under {}".format(LOG_DIR))

    rows = []
    failed = []

    for path in log_paths:
        try:
            rows.append(parse_log(path))
        except Exception as e:
            failed.append((path.name, str(e)))

    if failed:
        print("[WARN] Failed logs:")
        for name, err in failed:
            print("  - {}: {}".format(name, err))

    if not rows:
        raise RuntimeError("No valid logs parsed.")

    rows = sorted(rows, key=sort_key)

    with OUT_CSV.open("w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Dataset", "Method", "Seed", "Preprocess", "New Clean", "New ASR", "Log Path"])
        for r in rows:
            writer.writerow([
                r["dataset"],
                r["method"],
                r["seed"],
                r["preprocess"],
                "{:.2f}".format(r["new_clean"]),
                "{:.2f}".format(r["new_asr"]),
                r["path"],
            ])

    grouped = defaultdict(list)
    for r in rows:
        grouped[(r["dataset"], r["method"], r["preprocess"])].append(r)

    grouped_keys = sorted(grouped.keys(), key=group_key_sort)

    none_mean = {}
    for key in grouped_keys:
        dataset, method, preprocess = key
        vals = grouped[key]
        clean_vals = [x["new_clean"] for x in vals]
        asr_vals = [x["new_asr"] for x in vals]
        clean_mean, _ = mean_std(clean_vals)
        asr_mean, _ = mean_std(asr_vals)
        if preprocess == "none":
            none_mean[(dataset, method)] = (clean_mean, asr_mean)

    with OUT_MD.open("w") as f:
        f.write("# Robustness under Selected Input Preprocessing Settings\n\n")
        f.write("- Setting: 2-shot base-to-new evaluation\n")
        f.write("- Seeds: 1, 2, 3\n")
        f.write("- Parsed logs: {}\n".format(len(rows)))
        f.write("- Failed logs: {}\n\n".format(len(failed)))

        f.write("## Per-seed Results\n\n")
        f.write("| Dataset | Method | Seed | Preprocess | New Clean | New ASR |\n")
        f.write("|---|---|---:|---|---:|---:|\n")
        for r in rows:
            f.write(
                "| {} | {} | {} | {} | {:.2f} | {:.2f} |\n".format(
                    r["dataset"],
                    r["method"],
                    r["seed"],
                    r["preprocess"],
                    r["new_clean"],
                    r["new_asr"],
                )
            )

        f.write("\n## Mean ± Std Results\n\n")
        f.write("| Dataset | Method | Preprocess | New Clean | New ASR |\n")
        f.write("|---|---|---|---:|---:|\n")
        for key in grouped_keys:
            dataset, method, preprocess = key
            vals = grouped[key]
            clean_vals = [x["new_clean"] for x in vals]
            asr_vals = [x["new_asr"] for x in vals]
            f.write(
                "| {} | {} | {} | {} | {} |\n".format(
                    dataset,
                    method,
                    preprocess,
                    fmt_mean_std(clean_vals),
                    fmt_mean_std(asr_vals),
                )
            )

        f.write("\n## Mean Changes Relative to None\n\n")
        f.write("| Dataset | Method | Preprocess | Δ New Clean | Δ New ASR |\n")
        f.write("|---|---|---|---:|---:|\n")
        for key in grouped_keys:
            dataset, method, preprocess = key
            if preprocess == "none":
                continue

            if (dataset, method) not in none_mean:
                continue

            vals = grouped[key]
            clean_vals = [x["new_clean"] for x in vals]
            asr_vals = [x["new_asr"] for x in vals]
            clean_mean, _ = mean_std(clean_vals)
            asr_mean, _ = mean_std(asr_vals)
            clean_none, asr_none = none_mean[(dataset, method)]

            f.write(
                "| {} | {} | {} | {:+.2f} | {:+.2f} |\n".format(
                    dataset,
                    method,
                    preprocess,
                    clean_mean - clean_none,
                    asr_mean - asr_none,
                )
            )

    with OUT_TEX.open("w") as f:
        f.write("\\begin{table*}[t]\n")
        f.write("\\centering\n")
        f.write("\\caption{Robustness under selected input preprocessing settings. Results are averaged over three random seeds.}\n")
        f.write("\\label{tab:preprocess_robustness_selected}\n")
        f.write("\\begin{tabular}{lllcc}\n")
        f.write("\\toprule\n")
        f.write("Dataset & Method & Preprocess & New Clean (\\%) & New ASR (\\%) \\\\\n")
        f.write("\\midrule\n")

        last_dataset = None
        for key in grouped_keys:
            dataset, method, preprocess = key
            vals = grouped[key]
            clean_vals = [x["new_clean"] for x in vals]
            asr_vals = [x["new_asr"] for x in vals]

            if last_dataset is not None and dataset != last_dataset:
                f.write("\\midrule\n")
            last_dataset = dataset

            clean_tex = latex_mean_std(clean_vals)
            asr_tex = latex_mean_std(asr_vals)

            f.write("{} & {} & {} & {} & {} \\\\\n".format(
                dataset,
                method,
                preprocess,
                clean_tex,
                asr_tex,
            ))

        f.write("\\bottomrule\n")
        f.write("\\end{tabular}\n")
        f.write("\\end{table*}\n")

    print("[OK] Parsed logs: {}".format(len(rows)))
    print("[OK] Failed logs: {}".format(len(failed)))
    print("[OK] Wrote: {}".format(OUT_MD))
    print("[OK] Wrote: {}".format(OUT_CSV))
    print("[OK] Wrote: {}".format(OUT_TEX))


if __name__ == "__main__":
    main()
