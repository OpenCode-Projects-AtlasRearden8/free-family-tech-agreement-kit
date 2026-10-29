# Free Family Tech Agreement Kit

Free printables for calmer family screen rules. Plain HTML/CSS sources print
to clean PDFs with one local build script — no signups, no accounts, no
telemetry, nothing to install beyond Python.

## What's inside

| Printable | File | What it does |
| --- | --- | --- |
| Family Screen-Time Agreement | `family-screen-agreement` | One-page agreement kids and grown-ups both sign, with fill-in-the-blank "our numbers" and a shared screen-down call |
| My First Phone — a Contract to Sign Together | `first-phone-contract` | Read-aloud-together contract covering app installs, charging spot, privacy expectations for kids *and* grown-ups, plus a consequences ladder |
| Evening Device-Curfew Menus | `evening-curfew-menus` | Five pick-one "menus" (A–E) that turn nightly screen negotiations into choices, with a fill-in week planner |
| Grandparent-Visit Screen Rules | `grandparent-visit-rules` | Pre-agreed rules so visiting parents/grandparents aren't improvising screen policy mid-visit |
| Guest WiFi House Rule Cards | `guest-wifi-cards` | Six cut-out cards with the network, password, and the house's quiet rules |
| Review Date Page — Rules That Grow With You | `rules-review-page` | A standing review meeting with logs for kid and grown-up amendments, so rules evolve without fights |

The PDFs are **unbranded** — no company name, logo, or promotional copy — so
you can print and use them anywhere.

## How to build

Requirements: Python 3.10+ with `weasyprint` and `pypdf`
(`pip install weasyprint pypdf`):

```bash
python3 build.py                 # renders every source into printables/
python3 build.py --list          # just list the sheets
python3 build.py --out /somewhere
```

Each PDF is rendered with WeasyPrint and validated on the spot (valid PDF
header, readable by pypdf, expected content present). The build fails loudly
if anything is off.

## How to test

```bash
python3 -m unittest discover -s tests
```

Tests build every sheet into a temporary directory and verify that each PDF
is valid, contains the expected text, and contains no branding.

## Design notes

- US Letter (8.5×11") page size, print margins tuned for home printers.
- Web-safe fonts only (Georgia + Helvetica), no web fonts, so the build works
  fully offline.
- Sources are plain HTML/CSS in `sources/`; shared styling lives in
  `sources/css/print.css`.
- Pick a matching companion for AI-era questions at home: this kit pairs
  naturally with the *Talking to Kids About AI* guide.

## Credit

Created by **Asdale Dynamics, LLC** — beginner-friendly AI education, books,
and practical local-first tools. Licensed under the MIT License (see
`LICENSE`).
