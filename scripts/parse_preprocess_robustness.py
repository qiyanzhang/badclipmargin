import csv
import re
from pathlib import Path


LOG_DIR = Path("analysis_notes/preprocess_robustness")
CSV_PATH = LOG_DIR / "robustness_seed1_summary.csv"
MD_PATH = LOG_DIR / "robustness_seed1_summary.md"

FILENAME_RE = re.compile(
    r"^(?P<dataset>[a-z0-9_]+)_shot(?P<shots>\d+)_seed(?P<seed>\d+)_(?P<method>.+)_(?P<preprocess>none|jpeg90|jpeg70|blur|resize|colorjitter)_test_unseen\.run\.log$"
)
ACC_RE = re.compile(r"\* accuracy:\s*([0-9.]+)%")


def parse_log(path):
    text = path.read_text(encoding="utf-8", errors="ignore")
    matches = ACC_RE.findall(text)
    if len(matches) < 2:
        raise ValueError(f"Expected at least two accuracy values in {path}")

    clean = float(matches[-2])
    asr = float(matches[-1])
    meta = FILENAME_RE.match(path.name)
    if meta is None:
        raise ValueError(f"Unexpected log filename: {path.name}")

    row = meta.groupdict()
    row["seed"] = int(row["seed"])
    row["shots"] = int(row["shots"])
    row["new_clean"] = clean
    row["new_asr"] = asr
    return row


def fmt(value):
    return f"{value:.2f}"


def main():
    rows = []
    for path in sorted(LOG_DIR.glob("*.run.log")):
        rows.append(parse_log(path))

    rows.sort(key=lambda x: (x["dataset"], x["method"], x["seed"], x["preprocess"]))

    LOG_DIR.mkdir(parents=True, exist_ok=True)

    with CSV_PATH.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Dataset", "Method", "Seed", "Preprocess", "New Clean", "New ASR"])
        for row in rows:
            writer.writerow(
                [
                    row["dataset"],
                    row["method"],
                    row["seed"],
                    row["preprocess"],
                    fmt(row["new_clean"]),
                    fmt(row["new_asr"]),
                ]
            )

    baseline = {}
    for row in rows:
        if row["preprocess"] == "none":
            baseline[(row["dataset"], row["method"], row["seed"])] = row

    delta_rows = []
    for row in rows:
        if row["preprocess"] == "none":
            continue
        key = (row["dataset"], row["method"], row["seed"])
        if key not in baseline:
            continue
        base = baseline[key]
        delta_rows.append(
            {
                "dataset": row["dataset"],
                "method": row["method"],
                "seed": row["seed"],
                "preprocess": row["preprocess"],
                "delta_clean": row["new_clean"] - base["new_clean"],
                "delta_asr": row["new_asr"] - base["new_asr"],
            }
        )

    delta_rows.sort(key=lambda x: (x["dataset"], x["method"], x["seed"], x["preprocess"]))

    lines = []
    lines.append("| Dataset | Method | Seed | Preprocess | New Clean | New ASR |")
    lines.append("|---|---|---:|---|---:|---:|")
    for row in rows:
        lines.append(
            f"| {row['dataset']} | {row['method']} | {row['seed']} | {row['preprocess']} | {fmt(row['new_clean'])} | {fmt(row['new_asr'])} |"
        )

    lines.append("")
    lines.append("| Dataset | Method | Preprocess | Δ New Clean | Δ New ASR |")
    lines.append("|---|---|---|---:|---:|")
    for row in delta_rows:
        lines.append(
            f"| {row['dataset']} | {row['method']} | {row['preprocess']} | {fmt(row['delta_clean'])} | {fmt(row['delta_asr'])} |"
        )

    MD_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
