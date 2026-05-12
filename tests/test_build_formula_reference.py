from pathlib import Path
import csv
import sys
import tempfile
import unittest


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"
sys.path.insert(0, str(SRC_DIR))

from build_formula_reference import (  # noqa: E402
    REQUIRED_COLUMNS,
    build_markdown,
    read_formula_requests,
)


class FormulaReferenceTests(unittest.TestCase):
    def temporary_folder(self):
        return tempfile.TemporaryDirectory(dir=PROJECT_ROOT)

    def write_csv(self, folder, rows, fieldnames=None):
        csv_path = Path(folder) / "formula_requests.csv"

        with csv_path.open("w", encoding="utf-8", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames or REQUIRED_COLUMNS)
            writer.writeheader()
            writer.writerows(rows)

        return csv_path

    def test_read_formula_requests_reads_valid_csv_and_cleans_rows(self):
        row = {
            "Use Case": "  Count Complete Tasks  ",
            "Business Rule": " Count checked rows ",
            "Formula Type": " Summary Formula ",
            "Required Columns": " Complete ",
            "Example Formula": " =COUNTIF(Complete:Complete, 1) ",
            "Notes": " Use for status summaries. ",
        }

        with self.temporary_folder() as folder:
            csv_path = self.write_csv(folder, [row])

            rows = read_formula_requests(csv_path)

        self.assertEqual(len(rows), 1)
        self.assertEqual(
            rows[0],
            {
                "Use Case": "Count Complete Tasks",
                "Business Rule": "Count checked rows",
                "Formula Type": "Summary Formula",
                "Required Columns": "Complete",
                "Example Formula": "=COUNTIF(Complete:Complete, 1)",
                "Notes": "Use for status summaries.",
            },
        )

    def test_read_formula_requests_raises_value_error_for_missing_header(self):
        fieldnames = [
            column for column in REQUIRED_COLUMNS
            if column != "Notes"
        ]
        row = {
            "Use Case": "Count Complete Tasks",
            "Business Rule": "Count checked rows",
            "Formula Type": "Summary Formula",
            "Required Columns": "Complete",
            "Example Formula": "=COUNTIF(Complete:Complete, 1)",
        }

        with self.temporary_folder() as folder:
            csv_path = self.write_csv(folder, [row], fieldnames=fieldnames)

            with self.assertRaises(ValueError) as error:
                read_formula_requests(csv_path)

        self.assertIn("Missing required columns: Notes", str(error.exception))

    def test_read_formula_requests_skips_blank_rows(self):
        first_row = {
            "Use Case": "Milestone ID Builder",
            "Business Rule": "Build a readable ID",
            "Formula Type": "Text Formula",
            "Required Columns": "Milestone; Task",
            "Example Formula": '=Milestone@row + " " + Task@row',
            "Notes": "Useful for labels.",
        }
        blank_row = {column: "   " for column in REQUIRED_COLUMNS}
        second_row = {
            "Use Case": "Kickoff Complete Count",
            "Business Rule": "Count checked items",
            "Formula Type": "Summary Formula",
            "Required Columns": "Hold Kick-off",
            "Example Formula": "=COUNTIF({Hold Kick-off}, 1)",
            "Notes": "Counts checked values.",
        }

        with self.temporary_folder() as folder:
            csv_path = self.write_csv(folder, [first_row, blank_row, second_row])

            rows = read_formula_requests(csv_path)

        self.assertEqual(len(rows), 2)
        self.assertEqual(
            [row["Use Case"] for row in rows],
            ["Milestone ID Builder", "Kickoff Complete Count"],
        )

    def test_build_markdown_groups_by_formula_type_and_includes_content(self):
        rows = [
            {
                "Use Case": "Schedule Moved in Workdays",
                "Business Rule": "Calculate schedule movement",
                "Formula Type": "Date Formula",
                "Required Columns": "Original Date; New Date",
                "Example Formula": "=NETDAYS([Original Date]@row, [New Date]@row)",
                "Notes": "Shows workday movement.",
            },
            {
                "Use Case": "Milestone ID Builder",
                "Business Rule": "Build a readable ID",
                "Formula Type": "Text Formula",
                "Required Columns": "Milestone; Task",
                "Example Formula": '=Milestone@row + " " + Task@row',
                "Notes": "Useful for labels.",
            },
        ]

        markdown = build_markdown(rows)

        self.assertIn("## Date Formula", markdown)
        self.assertIn("## Text Formula", markdown)
        self.assertIn("### Schedule Moved in Workdays", markdown)
        self.assertIn("### Milestone ID Builder", markdown)
        self.assertIn(
            "=NETDAYS([Original Date]@row, [New Date]@row)",
            markdown,
        )
        self.assertIn('=Milestone@row + " " + Task@row', markdown)
        self.assertLess(
            markdown.index("## Date Formula"),
            markdown.index("## Text Formula"),
        )


if __name__ == "__main__":
    unittest.main()
