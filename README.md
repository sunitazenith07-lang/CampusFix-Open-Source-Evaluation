# CampusFix — Open-Source Evaluation

**Zenith School of AI | Individual Build Challenge**

CampusFix is a small existing Python application for managing campus helpdesk requests. This repository is the official starter code for the open-source evaluation.

## Your mission

Understand the existing codebase, fix the three issues shared by the organisers at kick-off, implement search and filtering, choose one additional feature, write tests, and explain your contribution.

## Getting started

- Python 3.10 or newer
- Git

Install dependencies and run the starter checks:

```bash
python -m pip install -r requirements-dev.txt
python -m pytest -q
```

Run the application:

```bash
python -m campusfix.cli
```

## Before you start

1. Read [CONTRIBUTING.md](CONTRIBUTING.md).
2. Inspect the `campusfix/`, `data/`, and `tests/` directories.
3. Create `ARCHITECTURE.md` from `ARCHITECTURE_TEMPLATE.md`.
4. Wait until kick-off to begin making challenge commits. Do not publish challenge solutions before the announced start time.
5. At kick-off, use the three official GitHub issues shared by the organisers and create a separate branch and pull request for each bug fix.

## Required work

- Fix all three organiser-reported issues.
- Add case-insensitive title search and combined status/priority filters.
- Complete one additional feature: request summary, duplicate request warning, or priority view.
- Add/update tests and document at least five cases in `TESTING.md`.
- Maintain `PROJECT_NOTES.md` and disclose AI use in `AI_USAGE.md` if applicable.
- Submit your repository and pull-request links and a two-minute demo video.

The detailed student problem statement and schedule will be shared by the organisers. Do not use a different repository for this evaluation.

## Project map

```text
campusfix/       Application code
  models.py      Request data model
  storage.py     JSON storage helpers
  service.py     Request-management logic
  cli.py         Command-line interface
data/            Sample request data
tests/           Starter automated tests
.github/         GitHub Actions test workflow
```

## Academic integrity and AI use

This is an individual evaluation. AI tools and online learning resources are permitted, but cite resources, declare AI use, test the changes, and be ready to explain every submitted change. Do not remove or bypass tests/checks, and do not share secrets or private personal data with AI tools.
