from __future__ import annotations

import argparse
import csv
import logging
from pathlib import Path


DEFAULT_INPUT_FILE = Path("data/freshbasket_daily_orders.csv")
REQUIRED_COLUMNS = {
    "order_id",
    "customer_id",
    "order_total",
    "order_date",
}


def configure_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate the FreshBasket daily orders input file before processing."
    )
    parser.add_argument(
        "--input",
        type=Path,
        default=DEFAULT_INPUT_FILE,
        help="Path to the daily input CSV file.",
    )
    return parser.parse_args()


def check_input_file(file_path: Path) -> Path:
    logging.info("Checking input file: %s", file_path)

    if not file_path.exists():
        message = f"Input file not found: {file_path}"
        logging.error(message)
        raise FileNotFoundError(message)

    if file_path.stat().st_size == 0:
        message = f"Input file is empty: {file_path}"
        logging.error(message)
        raise ValueError(message)

    logging.info("Input file is available and not empty: %s", file_path)
    return file_path


def read_csv_header(file_path: Path) -> list[str]:
    with file_path.open(mode="r", encoding="utf-8", newline="") as csv_file:
        reader = csv.DictReader(csv_file)

        if reader.fieldnames is None:
            message = f"Could not read CSV header from file: {file_path}"
            logging.error(message)
            raise ValueError(message)

        return [column.strip() for column in reader.fieldnames]


def build_missing_columns_message(
    file_path: Path,
    actual_columns: set[str],
    missing_columns: set[str],
) -> str:
    return (
        f"Missing required columns in {file_path}. "
        f"Expected at least: {sorted(REQUIRED_COLUMNS)}. "
        f"Found: {sorted(actual_columns)}. "
        f"Missing: {sorted(missing_columns)}."
    )


def validate_required_columns(file_path: Path, required_columns: set[str]) -> None:
    actual_columns = read_csv_header(file_path)
    actual_column_set = set(actual_columns)

    logging.info("Actual columns found: %s", actual_columns)

    missing_columns = required_columns - actual_column_set

    if missing_columns:
        message = build_missing_columns_message(
            file_path=file_path,
            actual_columns=actual_column_set,
            missing_columns=missing_columns,
        )
        logging.error(message)
        raise ValueError(message)

    logging.info("Schema validation passed for file: %s", file_path)


def main() -> None:
    configure_logging()
    args = parse_args()

    checked_file = check_input_file(args.input)
    validate_required_columns(checked_file, REQUIRED_COLUMNS)

    logging.info("Pipeline can continue with validated file: %s", checked_file)


if __name__ == "__main__":
    main()