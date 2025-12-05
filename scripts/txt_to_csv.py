from pathlib import Path
import csv

DATA_DIR = Path(__file__).resolve().parent.parent / "data"


def convert_txt_to_csv(txt_path: Path) -> Path:
    """Stream a whitespace-separated .txt file into a comma-separated .csv."""
    csv_path = txt_path.with_suffix(".csv")
    csv_path.parent.mkdir(parents=True, exist_ok=True)

    with txt_path.open("r", encoding="utf-8") as txt_file, csv_path.open(
        "w", newline="", encoding="utf-8"
    ) as csv_file:
        writer = csv.writer(csv_file)
        for line in txt_file:
            cells = line.strip().split()
            if cells:
                writer.writerow(cells)

    return csv_path


def main() -> None:
    txt_files = sorted(DATA_DIR.rglob("*.txt"))
    if not txt_files:
        print(f"No .txt files found under {DATA_DIR}")
        return

    for txt_path in txt_files:
        csv_path = convert_txt_to_csv(txt_path)
        print(f"Converted {txt_path} -> {csv_path}")


if __name__ == "__main__":
    main()
