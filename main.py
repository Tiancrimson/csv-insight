import argparse
import csv
from pathlib import Path


def summarize_csv(file_path: Path) -> dict:
    with file_path.open("r", encoding="utf-8-sig", newline="") as csv_file:
        reader = csv.DictReader(csv_file)
        rows = list(reader)
        fieldnames = reader.fieldnames or []

    missing_counts = {
        field: sum(1 for row in rows if not (row.get(field) or "").strip())
        for field in fieldnames
    }

    return {
        "file": str(file_path),
        "rows": len(rows),
        "columns": len(fieldnames),
        "fieldnames": fieldnames,
        "missing_counts": missing_counts,
    }


def print_summary(summary: dict) -> None:
    print(f"文件：{summary['file']}")
    print(f"行数：{summary['rows']}")
    print(f"列数：{summary['columns']}")
    print(f"列名：{', '.join(summary['fieldnames'])}")
    print()
    print("缺失值统计：")

    for field, count in summary["missing_counts"].items():
        print(f"- {field}: {count}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Summarize a local CSV file.")
    parser.add_argument("csv_file", type=Path, help="Path to the CSV file")
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    if not args.csv_file.exists():
        raise SystemExit(f"找不到文件：{args.csv_file}")

    summary = summarize_csv(args.csv_file)
    print_summary(summary)


if __name__ == "__main__":
    main()
