# Zenith School of AI — Open-Source Evaluation

## CampusFix: Improve an Existing Community Helpdesk
**Individual Build Challenge | 100 marks**

## 1. The Challenge
A campus community receives everyday requests: Wi-Fi is not working, a classroom projector needs attention, a lab resource is missing, or a student cannot access an account. If requests are not recorded, prioritised and updated properly, some get missed.

CampusFix is an existing application that helps a team record and manage these requests. It has basic functionality, reported issues to fix and user-requested improvements. You are joining the project as a new open-source contributor.

Your mission: understand the existing code, fix reported problems, add useful improvements, test your changes and contribute using GitHub. You are improving an existing project—not starting from a blank page.

## 2. Technology and Setup
The supplied starter repository uses Python 3.10+ so all students can use the same project and comparable checks. Keep the supplied language for this overnight evaluation; do not rebuild the whole app in another framework. The challenge assesses problem-solving and contribution practices, not language popularity.

Install Python 3.10 or newer and Git before the event, if possible. Fork and clone the repository as described in `README.md`.

Run the application:
```bash
python -m campusfix.cli
```

Install development dependencies and run starter checks:
```bash
python -m pip install -r requirements-dev.txt
python -m pytest -q
```

Read `CONTRIBUTING.md` before making changes.

## 3. Understand the Existing Project — Mandatory
- Run the starter application and inspect the supplied files.
- Explain how a request is represented, loaded, listed, searched and updated.
- Trace the flow from input to result.
- Create `ARCHITECTURE.md` using `ARCHITECTURE_TEMPLATE.md`. Include the project map, numbered request flow, data structure/storage and a simple diagram. Excalidraw is available at https://excalidraw.com/.
- Suggest three concrete improvements based on the code you inspected.

## 4. Fix Reported Issues — Mandatory
The organisers will share three separate GitHub issues at kick-off. Each describes the observed behaviour and expected behaviour. Reproduce each issue, identify its root cause, fix it, and verify that existing behaviour still works.

Create a separate branch and pull request for each bug fix. Use the branch and commit naming conventions in `CONTRIBUTING.md`. Do not combine unrelated fixes into one pull request.

## 5. Add the Core Feature — Mandatory
### Request Search and Filtering
- Search request titles without being affected by uppercase/lowercase differences.
- Filter by status: Open, In Progress or Resolved.
- Filter by priority: Low, Medium or High.
- Allow search and filters to work together.
- Show a clear message when no requests match.
- Handle empty search text and invalid filter values safely.
- Explain the logic/data structure you used and any performance trade-off.

## 6. Choose One Additional Feature
Complete at least one option.

**Option A — Request Summary**
- Display total requests.
- Count requests by status and priority.
- Identify the category with the most requests.
- Handle an empty list.

**Option B — Duplicate Request Warning**
- Find titles matching after extra spaces are removed and case is ignored.
- Show IDs/references of possible duplicates.
- Flag for human review; never delete automatically.
- Handle no duplicates.

**Option C — Priority View**
- Display unresolved High-priority requests before Medium and Low.
- Keep requests of the same priority in a consistent order.
- Do not unintentionally change stored data.
- Explain the sorting approach.

## 7. Code Quality and Testing
Use clear names, sensible functions/modules and the existing project conventions. Handle empty lists, missing fields and unexpected input gracefully.

Run the provided automated tests and check the GitHub Actions result on your pull requests. Add/update relevant tests and document at least five cases with expected and actual results in `TESTING.md`.

The agreed test target will be published with the repository. A passing percentage alone does not guarantee a high score; mentors also assess the relevant behaviour and your explanation. Do not remove, weaken or bypass tests/checks.

## 8. GitHub Contribution Workflow
Read `CONTRIBUTING.md`. Use these branch naming patterns:
- Bug fix: `fix/issue-<number>-<short-description>` (example: `fix/issue-12-status-update`).
- Core feature: `feature/search-and-filters`.
- Additional feature: `feature/<short-feature-name>` (example: `feature/request-summary`).

Commit format: `type(scope): short description` (example: `fix(requests): persist status updates`).

Open focused pull requests with a summary, reasoning, issue reference, tests run and known limitations.

Keep a short handover/knowledge base in `PROJECT_NOTES.md`: requirements completed, files changed, decisions, assumptions, tests and next steps. Credit external resources.

## 9. Submission Requirements
- Public repository fork URL and pull-request links.
- `README.md` with setup/run/usage instructions.
- `ARCHITECTURE.md`.
- `TESTING.md` with at least five test cases and expected/actual results.
- `PROJECT_NOTES.md`.
- Summary of bugs fixed and features completed.
- AI-use declaration in `AI_USAGE.md`, if applicable.
- Two-minute demo video.
- Live application/demo URL if deployment is feasible; otherwise explain why and provide reliable run instructions.

## 10. AI Tool Use and Credit Reporting
AI tools are permitted. You are responsible for understanding, testing and explaining every submitted change. Using AI is not itself a penalty or an advantage.

In `AI_USAGE.md`, record each tool/model, what you used it for, what you verified or changed yourself, and approximate credits/tokens if the tool shows them. If usage is not displayed, write “not available”; do not guess.

Give one example of a suggestion you accepted, modified or rejected and explain why. Do not share secrets, credentials or private personal data with AI tools.

Credit usage is an exploratory efficiency metric only, not a standalone score. Different tools use different credit systems, so raw amounts are not directly comparable.

## 11. Schedule
- **Day 1, 9:00 PM** — Kick-off; repository and issues shared.
- **Day 2, 8:00 AM** — Code freeze; later commits are not counted.
- **Day 2, 9:00 AM** — Submission deadline.
- **Day 2, from 11:00 AM** — Evaluation: 10-minute demo and 5-minute viva.

## 12. Evaluation Parameters
| Parameter | Weight | What mentors assess |
|---|---:|---|
| Codebase Understanding | 15 | Explains project structure, request flow and where changes belong. |
| Problem Solving | 25 | Finds root causes, chooses appropriate logic/data structures and handles edge cases. |
| Working Prototype | 20 | Bug fixes, search/filter feature and one additional feature work. |
| Code Quality | 10 | Readable, maintainable code that follows project conventions. |
| Testing | 10 | Runs checks, adds relevant tests and explains results/limitations. |
| Demo & Communication | 20 | Clear demo, explains decisions/trade-offs, answers questions and acknowledges limitations. |
| **TOTAL** | **100** | |

## 13. Demo and Viva
Be prepared to:
- Explain how a request moves through the project.
- Demonstrate a bug fix and explain why it works.
- Run search/filtering on new request data.
- Explain a data structure or algorithm used.
- Make or describe a small change to a function you wrote.
- Show branches, commits, pull requests and automated test results.
- Explain one limitation and how you used/verified AI assistance.

## 14. Rules and Integrity
This is an individual evaluation; your work must be your own. Copying another student's code or submitting a pre-written solution is prohibited.

- No commits before kick-off; commits after code freeze do not count.
- Online learning resources are permitted with credit.
- AI tools are permitted but must be declared; you must understand every change.
- Do not remove or bypass tests or automated checks.
- Mentors may provide unseen input or a small change request to verify understanding.

## 15. Shortlisting
All 300 students will be assessed using the same six-parameter rubric. The top 170 will be shortlisted by final score, subject to any minimum competency criteria announced before the event. Ties at the cutoff: Problem Solving, Demo & Communication, Working Prototype, Codebase Understanding, then Testing.

**Understand the project. Fix a real issue. Make a focused improvement. Test it. Explain your contribution.**
