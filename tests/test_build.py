"""Tests for the family screen-rules printable kit.

Run with:  python3 -m unittest discover -s tests -v
(or:  python3 -m pytest tests  if pytest is installed)

Every test builds into a temporary directory so the committed printables/
are never disturbed by test runs.
"""

import sys
import tempfile
import unittest
from pathlib import Path

# Make build.py importable when tests are run from anywhere.
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "sources"))

import build  # noqa: E402  (import after sys.path setup above)

SOURCES = PROJECT_ROOT / "sources"


class BuildTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls._tmp = tempfile.TemporaryDirectory()
        cls.out_dir = Path(cls._tmp.name) / "printables"
        sheets = build.discover_sheets(SOURCES)
        cls.problems: dict[str, list[str]] = {}
        for sheet in sheets:
            cls.problems[sheet.stem] = build.build_sheet(
                sheet, cls.out_dir, silent=True
            )
        cls.built = sorted(p.stem for p in cls.out_dir.glob("*.pdf"))

    @classmethod
    def tearDownClass(cls):
        cls._tmp.cleanup()

    def test_six_sheets_exist(self):
        self.assertEqual(len(list(SOURCES.glob("*.html"))), 6,
                         "expected exactly six HTML source sheets")

    def test_every_sheet_builds_without_problems(self):
        for sheet in build.discover_sheets(SOURCES):
            with self.subTest(sheet=sheet.name):
                self.assertEqual(self.problems[sheet.stem], [])

    def test_every_pdf_is_generated(self):
        for stem in build.REQUIRED_PHRASES:
            with self.subTest(pdf=stem):
                self.assertIn(stem, self.built)

    def test_pdfs_start_with_pdf_header(self):
        for pdf in (self.out_dir / f"{stem}.pdf" for stem in self.built):
            with self.subTest(pdf=pdf.name):
                self.assertTrue(pdf.read_bytes().startswith(b"%PDF"))

    def test_pdfs_are_readable_with_at_least_one_page(self):
        from pypdf import PdfReader

        for pdf in self.out_dir.glob("*.pdf"):
            with self.subTest(pdf=pdf.name):
                reader = PdfReader(str(pdf))
                self.assertGreaterEqual(len(reader.pages), 1)

    def test_every_pdf_has_expected_text(self):
        """Independent of build.py's own validation: re-check phrases here."""
        for stem, phrases in build.REQUIRED_PHRASES.items():
            pdf = self.out_dir / f"{stem}.pdf"
            with self.subTest(pdf=pdf.name):
                self.assertEqual(
                    build.validate_pdf(pdf, phrases), [],
                    f"{pdf.name}: required text missing",
                )

    def test_pdfs_contain_no_branding_keywords(self):
        """Unbranded requirement: no LLC/author name should appear in PDFs."""
        banned = ["asdale", "dylan", "massive ai manual"]
        from pypdf import PdfReader

        for pdf in self.out_dir.glob("*.pdf"):
            with self.subTest(pdf=pdf.name):
                text = " ".join(
                    (p.extract_text() or "")
                    for p in PdfReader(str(pdf)).pages
                )
                lowered = " ".join(text.lower().split())
                for word in banned:
                    self.assertNotIn(word, lowered)

    def test_validate_pdf_reports_missing_file(self):
        missing = self.out_dir / "does-not-exist.pdf"
        problems = build.validate_pdf(missing)
        self.assertTrue(problems)

    def test_list_flag_lists_sheets(self):
        import subprocess

        result = subprocess.run(
            [sys.executable, str(PROJECT_ROOT / "build.py"), "--list"],
            capture_output=True, text=True,
        )
        self.assertEqual(result.returncode, 0)
        self.assertEqual(len(result.stdout.strip().splitlines()), 6)


if __name__ == "__main__":
    unittest.main()
