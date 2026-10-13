# Contributing to CampusFix

Read this guide before editing code.

## Setup
1. Install Python 3.10+ and Git.
2. Fork the repository.
3. Clone your fork to your computer.
4. Install development dependencies: `python -m pip install -r requirements-dev.txt`.
5. Run the starter tests: `python -m pytest -q`.
6. Run the application: `python -m campusfix.cli`.

## Branch names
Use one focused branch per issue or feature:
- Bug fix: `fix/issue-<number>-<short-description>`
- Core feature: `feature/search-and-filters`
- Extra feature: `feature/<short-feature-name>`

Examples:
- `fix/issue-12-status-update`
- `fix/issue-13-case-insensitive-search`
- `feature/search-and-filters`
- `feature/request-summary`

## Commit messages
Use: `type(scope): short description`
Examples:
- `fix(requests): persist status updates`
- `feat(search): combine title query and filters`
- `test(service): cover empty search results`
- `docs(architecture): explain request flow`

## Pull requests
Open a separate pull request for each bug or feature. Include:
- What changed and why.
- Which issue it addresses.
- Tests/checks run and their results.
- Known limitations.
- Screenshots or a short recording if useful.

## Quality and conduct
- Keep changes focused and readable.
- Do not remove, weaken or bypass tests or automated checks.
- Never commit passwords, API keys, credentials or private personal data.
- Be respectful in discussions and credit external sources.
- Declare AI use in `AI_USAGE.md`.
