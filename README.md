# CampusFix — Open-Source Evaluation

**Zenith School of AI | Individual Build Challenge**

## Official student package

The complete student starter project lives in the [student-starter folder](student-starter/). Work from that folder; it contains the intentionally imperfect app, the 110-test behaviour contract, project templates, and the problem statement.

## Getting started

Requirements: Python 3.10 or newer and Git.

From the repository root, enter the student package:

```bash
cd student-starter
python -m pip install -e .
python -m pip install -r requirements-dev.txt
python -m pytest -q
python -m campusfix.cli
```

The starter tests include deliberate failures. At the start, **86 tests pass and 24 fail**; students should fix the underlying behaviours rather than remove or weaken tests. On GitHub, the Actions run reports exact pass/fail/error/skipped counts and fails the check until the suite is passing.

## Read before coding

1. [Student problem statement](student-starter/STUDENT_PROBLEM_STATEMENT.md)
2. [Contribution instructions](student-starter/CONTRIBUTING.md)
3. [Architecture template](student-starter/ARCHITECTURE_TEMPLATE.md)
4. [Testing template](student-starter/TESTING_TEMPLATE.md)
5. [AI-use declaration template](student-starter/AI_USAGE_TEMPLATE.md)

At the announced kick-off, the organisers will share the issues to reproduce and fix. Create focused branches and pull requests; follow the integrity and AI-use requirements in the problem statement.

## For organisers and reviewers

- Public student-facing files: in the student-starter folder.
- Automated test reporting: [.github/workflows/tests.yml](.github/workflows/tests.yml).
- The private corrected reference solution must **not** be committed to this public repository.
