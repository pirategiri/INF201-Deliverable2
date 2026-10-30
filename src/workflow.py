"""Task 5: the full workflow. Run from the repo root with: python -m src.workflow"""
import json
from pathlib import Path

from src.ingestion import read_file, parse_log
from src.recursion import find_log_files, find_active_registers
from src.numeric import remove_outliers
from src.analysis import (build_dataframe, hourly_revenue,
                          status_pivot, item_refund_ratios)

DATA_DIR = Path("data")
OUT_DIR = Path("outputs")


def main():
    # 1. find log files and active registers
    log_files = find_log_files(DATA_DIR / "2026")
    config = json.loads((DATA_DIR / "store_config.json").read_text(encoding="utf-8"))
    active = find_active_registers(config)
    print(f"Found {len(log_files)} log files, active registers: {sorted(active)}")

    # 2. read and parse
    records = []
    for file in log_files:
        text, encoding = read_file(file)
        file_records = parse_log(text)
        print(f"{file.parent.parent.name}/{file.parent.name}: "
              f"{len(file_records)} records ({encoding})")
        records.extend(file_records)
    records = [r for r in records if r["register_id"] in active]

    # 3. dataframe
    df = build_dataframe(records)

    # 4. remove price outliers
    df["price"] = remove_outliers(df["price"].to_numpy())

    # 5. fix NOK prices
    df.loc[df["currency"] == "NOK", "price"] *= 10.0

    # 6. reports
    hourly = hourly_revenue(df)
    pivot = status_pivot(df)
    ratios = item_refund_ratios(df)

    # 7. save
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUT_DIR / "cleaned_transactions.csv")

    hourly_dict = {}
    for (item, hour), total in hourly.items():
        hourly_dict.setdefault(item, {})[str(hour)] = float(total)
    with open(OUT_DIR / "hourly_revenue.json", "w", encoding="utf-8") as f:
        json.dump(hourly_dict, f, indent=2)

    pivot.to_csv(OUT_DIR / "status_pivot_table.csv")
    ratios.to_csv(OUT_DIR / "item_refund_ratios.csv", index=False)

    print(pivot)
    print(ratios)


if __name__ == "__main__":
    main()