from collections import defaultdict
from pathlib import Path
import csv


REQUIRED_COLUMNS = [
    "Use Case",
    "Business Rule",
    "Formula Type",
    "Required Columns",
    "Example Formula",
    "Notes",
]

PROJECT_ROOT = Path(__file__).resolve().parents[1]
INPUT_FILE = PROJECT_ROOT / "data" / "formula_requests.csv"
OUTPUT_FILE = PROJECT_ROOT / "output" / "formula_reference.md"


def read_formula_requests(input_file=INPUT_FILE):
    """Read formula request examples from CSV and validate required columns."""
    input_file = Path(input_file)

    if not input_file.exists():
        raise FileNotFoundError(f"Input file not found: {input_file}")

    with input_file.open("r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)

        missing_columns = [
            column for column in REQUIRED_COLUMNS
            if column not in (reader.fieldnames or [])
        ]

        if missing_columns:
            raise ValueError(
                "Missing required columns: " + ", ".join(missing_columns)
            )

        rows = []

        for line_number, row in enumerate(reader, start=2):
            if not any((value or "").strip() for value in row.values()):
                continue

            cleaned_row = {
                column: (row.get(column) or "").strip()
                for column in REQUIRED_COLUMNS
            }

            if not cleaned_row["Use Case"]:
                raise ValueError(f"Row {line_number} is missing Use Case.")

            if not cleaned_row["Formula Type"]:
                raise ValueError(f"Row {line_number} is missing Formula Type.")

            if not cleaned_row["Example Formula"]:
                raise ValueError(f"Row {line_number} is missing Example Formula.")

            rows.append(cleaned_row)

    if not rows:
        raise ValueError("No formula examples found in the input file.")

    return rows


def build_markdown(rows):
    """Build a Markdown formula reference guide from formula request rows."""
    grouped_rows = defaultdict(list)

    for row in rows:
        grouped_rows[row["Formula Type"]].append(row)

    lines = [
        "# Smartsheet Formula Reference",
        "",
        "Generated from `data/formula_requests.csv`.",
        "",
        f"Total formula patterns: {len(rows)}",
        "",
    ]

    for formula_type in sorted(grouped_rows):
        lines.append(f"## {formula_type}")
        lines.append("")

        for row in grouped_rows[formula_type]:
            lines.extend(
                [
                    f"### {row['Use Case']}",
                    "",
                    f"**Business rule:** {row['Business Rule']}",
                    "",
                    f"**Required columns:** {row['Required Columns']}",
                    "",
                    "**Example formula:**",
                    "",
                    "```text",
                    row["Example Formula"],
                    "```",
                    "",
                    f"**Notes:** {row['Notes']}",
                    "",
                ]
            )

    return "\n".join(lines).rstrip() + "\n"


def main():
    """Generate the Smartsheet formula reference guide."""
    try:
        rows = read_formula_requests()
        markdown = build_markdown(rows)

        OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
        OUTPUT_FILE.write_text(markdown, encoding="utf-8")

        formula_types = sorted({row["Formula Type"] for row in rows})

        print("Formula reference generated successfully.")
        print(f"Input file: {INPUT_FILE}")
        print(f"Output file: {OUTPUT_FILE}")
        print(f"Formula patterns: {len(rows)}")
        print(f"Formula types: {len(formula_types)}")

        for formula_type in formula_types:
            print(f" - {formula_type}")

    except (FileNotFoundError, ValueError) as error:
        print(f"Error: {error}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
