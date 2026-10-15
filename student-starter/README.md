# CampusFix — Expanded Open-Source Evaluation Starter

CampusFix is a small community helpdesk used for the Zenith School of AI open-source evaluation. Students must understand the existing code, fix reported issues, implement combined search/filtering, add regression tests, and explain their contribution.

## Setup

```bash
python -m venv .venv
# macOS/Linux: source .venv/bin/activate
# Windows: .venv\\Scripts\\activate
python -m pip install -e .
python -m pip install -r requirements-dev.txt
python -m pytest -q
python -m campusfix.cli
```

## Project map

- `campusfix/models.py` — request model and domain constants.
- `campusfix/storage.py` — JSON loading, saving and lookup helpers.
- `campusfix/service.py` — status updates, title search, combined filters, summaries and priority view.
- `campusfix/cli.py` — command-line demonstration.
- `data/requests.json` — sample helpdesk records.
- `tests/` — automated behaviour checks.
- `.github/workflows/tests.yml` — runs tests on pushes and pull requests and reports pass/fail counts.

## CI on pull requests

Open a pull request to `main`. GitHub Actions runs the automated suite against the proposed changes. The Actions summary reports total, passed, failed, error and skipped test counts. A failing run makes the check fail; do not remove or weaken tests to obtain a green check.

Some service functions contain deliberate defects or incomplete behaviour for the evaluation. Read the problem statement and GitHub issues before editing. The test suite represents the published contract and may initially fail on the starter branch.
