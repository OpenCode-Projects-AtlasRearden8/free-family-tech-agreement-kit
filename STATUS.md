# STATUS

## What was built

The Free Family Tech Agreement Kit: six home-printable PDF sheets for calmer
family screen rules, generated from plain HTML/CSS sources by a single local
build script. All PDFs are unbranded (no company name, logo, or promo text)
and US Letter sized.

| Sheet | Source | PDF output |
| --- | --- | --- |
| Family Screen-Time Agreement | `sources/family-screen-agreement.html` | `printables/family-screen-agreement.pdf` (2 pp) |
| My First Phone Contract | `sources/first-phone-contract.html` | `printables/first-phone-contract.pdf` (2 pp) |
| Evening Device-Curfew Menus | `sources/evening-curfew-menus.html` | `printables/evening-curfew-menus.pdf` (2 pp) |
| Grandparent-Visit Screen Rules | `sources/grandparent-visit-rules.html` | `printables/grandparent-visit-rules.pdf` (2 pp) |
| Guest WiFi House Rule Cards | `sources/guest-wifi-cards.html` | `printables/guest-wifi-cards.pdf` (2 pp, 6 cut-out cards) |
| Review Date Page | `sources/rules-review-page.html` | `printables/rules-review-page.pdf` (2 pp) |

Supporting files:
- `sources/css/print.css` — shared print styling (US Letter @page rules,
  running titles, checkboxes, signature lines, fill-in blanks).
- `build.py` — renders every `sources/*.html` with WeasyPrint into
  `printables/`, then validates each PDF (pypdf: valid header, at least one
  page, required sheet-specific text present). Exits non-zero if anything
  fails.
- `tests/test_build.py` — unittest suite that builds every sheet into a temp
  directory and verifies: sheet count, per-sheet build success, PDF header,
  readability/page counts, expected content per sheet, no branding keywords
  in any PDF, `--list` flag behavior.
- `README.md` (credits Asdale Dynamics, LLC), `LICENSE` (MIT,
  `Copyright (c) 2026 Asdale Dynamics, LLC`), `.gitignore`.

## How to run it

```bash
pip install weasyprint pypdf     # one-time
python3 build.py                 # build all six printables/
python3 build.py --list          # list sheets
python3 -m unittest discover -s tests   # run tests
```

Local-only: no network access, accounts, or signups are used at build or
print time. Fonts are web-safe (Georgia/Helvetica), so the build works fully
offline.

## Verification results

- `python3 build.py` → 6/6 sheets built and validated OK
  (each reported "built ... OK" with page counts).
- `python3 -m unittest discover -s tests` → **9 tests, all passing (OK)**,
  including the unbranded-content check.
- Visual check: rendered every PDF to PNG (pdftoppm) and reviewed every page
  for layout problems; fixed along the way (split tables made
  page-break-safe, sparse second pages filled with purposeful content,
  WiFi cards re-set in a 2-up cut-out grid).
- `printables/` is gitignored (generated artifacts); the committed PDFs on
  disk are current with the sources as of this commit.

## Known gaps / notes

- Connection to the companion *Talking to Kids About AI* guide is mentioned
  in the README; the guide itself lives in a separate repository and is not
  linked programmatically here.
- No A4 variant: pages areLetter-only. A future `--size a4` option could
  add an alternate `@page` rule.
- No PDF metadata branding pass: WeasyPrint's default PDF title is the HTML
  `<title>`; unbranded-ness is verified by test.
- Tests duplicate rule content as literal phrases (e.g., "first phone");
  renaming a sheet without updating `build.py:REQUIRED_PHRASES` would fail
  the build loudly, which is intended.

## License & credit

MIT — `Copyright (c) 2026 Asdale Dynamics, LLC` (see `LICENSE`).
Built for beginner-friendly, local-first AI education by Asdale Dynamics, LLC.
