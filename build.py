#!/usr/bin/env python3
"""Build printables/ PDFs from sources/ HTML sheets.

Local-only build: HTML + CSS in, PDFs out. No network, no signups.

Usage:
    python3 build.py                # build all sheets into printables/
    python3 build.py --out DIR      # build into a different directory
    python3 build.py --list         # list sheet names and exit
"""

import argparse
import sys
from pathlib import Path

from pypdf import PdfReader
from weasyprint import HTML

SOURCES_DIR = Path(__file__).resolve().parent / "sources"
DEFAULT_OUT_DIR = Path(__file__).resolve().parent / "printables"

# Key phrase expected (case-insensitive) in the text layer of each sheet.
# Used by tests to make sure the right content made it into the right PDF.
REQUIRED_PHRASES = {
    "family-screen-agreement": ["family screen-time agreement"],
    "first-phone-contract": ["first phone"],
    "evening-curfew-menus": ["evening device-curfew menus"],
    "grandparent-visit-rules": ["grandparent-visit screen rules"],
    "guest-wifi-cards": ["guest wifi house rule cards"],
    "rules-review-page": ["review date page"],
}


def discover_sheets(sources_dir: Path = SOURCES_DIR) -> list[Path]:
    """Return every HTML sheet in sources/, sorted."""
    return sorted(sources_dir.glob("*.html"))


def validate_pdf(path: Path, phrases: list[str] | None = None) -> list[str]:
    """Validate a PDF file; return a list of problems (empty means valid)."""
    problems: list[str] = []
    if not path.exists():
        return [f"{path.name}: file not found"]
    raw = path.read_bytes()
    if not raw.startswith(b"%PDF"):
        return [f"{path.name}: missing %PDF header"]
    try:
        reader = PdfReader(str(path))
        if len(reader.pages) < 1:
            return [f"{path.name}: has no pages"]
        if phrases:
            text = " ".join((page.extract_text() or "") for page in reader.pages)
            lowered = " ".join(text.lower().split())
            for phrase in phrases:
                if " ".join(phrase.split()).lower() not in lowered:
                    problems.append(f"{path.name}: expected phrase not found: {phrase!r}")
    except Exception as exc:  # noqa: BLE001 - surface any parse failure to the test
        return [f"{path.name}: unreadable PDF ({exc})"]
    return problems


def build_sheet(
    html_path: Path, out_dir: Path, silent: bool = False
) -> list[str]:
    """Render one HTML sheet to PDF in out_dir and validate it. Returns problems."""
    out_dir.mkdir(parents=True, exist_ok=True)
    pdf_path = out_dir / f"{html_path.stem}.pdf"
    try:
        HTML(filename=str(html_path)).write_pdf(target=str(pdf_path))
    except Exception as exc:  # noqa: BLE001 - report build failures as problems
        return [f"{html_path.name}: render failed ({exc})"]
    problems = validate_pdf(pdf_path, REQUIRED_PHRASES.get(html_path.stem))
    if not problems and not silent:
        pages = len(PdfReader(str(pdf_path)).pages)
        kb = pdf_path.stat().st_size / 1024
        print(f"  built {pdf_path.name} ({pages} page(s), {kb:.0f} KB) OK")
    return problems


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build family screen-rules printables.")
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT_DIR,
                        help="Output directory (default: printables/)")
    parser.add_argument("--sources", type=Path, default=SOURCES_DIR,
                        help="HTML sources directory (default: sources/)")
    parser.add_argument("--list", action="store_true", help="List sheets and exit")
    args = parser.parse_args(argv)

    sheets = discover_sheets(args.sources)
    if not sheets:
        print(f"No HTML sheets found in {args.sources}", file=sys.stderr)
        return 1

    if args.list:
        for sheet in sheets:
            print(sheet.name)
        return 0

    args.out.mkdir(parents=True, exist_ok=True)
    print("Building printables with WeasyPrint...")
    all_problems: list[str] = []
    for sheet in sheets:
        all_problems.extend(build_sheet(sheet, args.out))

    if all_problems:
        for problem in all_problems:
            print(f"ERROR {problem}", file=sys.stderr)
        print(f"Build finished with {len(all_problems)} problem(s).", file=sys.stderr)
        return 1
    print(f"Done: {len(sheets)} sheet(s) built and validated in {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
