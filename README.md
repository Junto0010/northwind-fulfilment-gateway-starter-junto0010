# Capstone — Northwind Fulfilment Gateway

You have joined Northwind's platform team. Build a small, production-minded
service which accepts fulfilment requests, stores them safely, quotes shipping
through a downstream provider, and exposes a fast operations view.

This is an engineering assessment, not a pixel-perfect API exercise. Your
implementation must keep its layers separate, be safe with untrusted input,
remain responsive under downstream latency, and be measurably efficient at
scale.

## What to build

Complete the `fulfilment/` package without changing the public function and
route signatures. The acceptance criteria are deliberately expressed as
behaviours rather than prescribed implementations:

| Area | Required behaviour | Course links |
|---|---|---|
| API | `POST /shipments` validates requests, rejects empty/invalid lines, and returns `201`; `GET /shipments/{id}` permits only the owning customer. | 01, 12 |
| Persistence & security | Store shipments in SQLite; queries must be parameterised; an attempted SQL injection must never disclose another customer's shipment. | 05, 11 |
| Design | Select a carrier through the `Carrier` protocol / registry, so an additional carrier can be added without editing the service orchestration. | 02, 03 |
| Async resilience | Quote every package with bounded async concurrency, preserve package order, and use the supplied circuit breaker to fail fast after repeated carrier failures. | 07, 13 |
| Performance | Produce one summary per customer from 100,000 shipment rows in linear time. | 04, 10 |
| Delivery | Make the list endpoint return a slim payload; compress large responses and cache the immutable asset route correctly. | 08 |
| Testing | Add meaningful tests of your own, including one failure path. | 09 |

## Step 1 — Create your private submission repository

Do this once, before writing any code.

1. Open the starter repository:
   `https://github.com/dondonMD/northwind-fulfilment-gateway-starter`
2. Click **Use this template** and then **Create a new repository**.
3. Set **Owner** to your own GitHub account.
4. Name the repository exactly: `northwind-fulfilment-YOUR-GITHUB-USERNAME`.
   For example, GitHub user `jane-smith` creates
   `northwind-fulfilment-jane-smith`.
5. Select **Private** visibility, then click **Create repository from template**.
6. In the new repository, open **Settings** → **Collaborators** → **Add people**.
   Invite `dondonMD` and grant write access. Accept any GitHub confirmation.
7. Clone **your new private repository** to your computer. Do not work directly
   in the public starter repository.

Your repository must remain private. Your instructor must have collaborator
access before the deadline, otherwise the submission cannot be graded.

## Before you start

You need Python 3.12 and Git. Work only in your assigned repository. From the
project folder, create and activate a virtual environment, then install:

```bash
# Windows PowerShell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1

# macOS/Linux
python3.12 -m venv .venv
source .venv/bin/activate

python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

If PowerShell refuses activation, run `Set-ExecutionPolicy -Scope Process
Bypass` once and try again.

## Contract

The exact data contract and TODOs are in the docstrings in `fulfilment/`.
The public checks in `tests/` are intentionally representative, not complete.
Run everything locally before every push:

```bash
python -m pip install -r requirements.txt
python -m pytest -q
python grading/grade.py
```

`pytest` is the pass/fail check. `grade.py` prints public feedback and writes
`grading/grade.json`. Do not edit tests, `grading/`, workflow files,
requirements, or public function/route signatures; final checks rely on them.

## Required submission checklist

Before the deadline, you must:

1. Implement the TODOs in `fulfilment/`.
2. Add at least two useful tests in `student_tests/`; one must cover a failure,
   validation, security, or resilience path.
3. Complete `DECISIONS.md` and `AI_USAGE.md`.
4. Make at least three meaningful commits: design/tests, core implementation,
   then hardening/performance.
5. Confirm the latest GitHub Actions run is green, then submit your repository
   URL and final commit SHA through the course submission channel.

Do not submit screenshots in place of code. In `DECISIONS.md`, record the
command, input size, elapsed time, and conclusion from one measurement. That
written evidence is sufficient; you do not send performance pictures.

## Submission

Push to your assigned repository. GitHub Actions repeats the public checks on
every push and publishes `grading/grade.json` as an artifact. The instructor
grader then runs additional edge, security, and performance tests against the
same public contract.

GitHub normally starts the check within about a minute. If it fails, read the
log, reproduce the problem locally, fix it, and push again. A green run means
the visible checks passed; it does not reveal or replace instructor-only tests.

Commit in at least three meaningful stages: design/tests, core implementation,
and production/performance hardening. Include `DECISIONS.md` (maximum 500
words) explaining your carrier extension point, bounded-concurrency choice,
and one performance measurement made on your machine.

## Marking

Automated checks are worth **70 points**: correctness/API 20, security and
persistence 15, async resilience 15, performance 10, delivery optimisation
5, and student-written tests 5. `grading/grade.py` reports the public portion
locally; the final automated score uses additional instructor-only cases.

The remaining **30 points** are assessed during a short individual review:

- 10: explain a trade-off in your implementation using your `DECISIONS.md`.
- 10: make a small live change (for example, add a carrier surcharge or alter
  the concurrency limit) and explain the test that protects it.
- 10: test quality, naming, boundaries, and commit history.

You may use AI and documentation, but you must cite material assistance in
`AI_USAGE.md` and be able to explain and adapt every submitted line. Undeclared
or unverifiable work is not awarded the individual-review marks. This makes AI
use transparent without trying to play an unwinnable "detect the AI" game.

## Frequently asked questions

**Can I use AI, Stack Overflow, or documentation?** Yes, unless your instructor
says otherwise. Declare meaningful assistance in `AI_USAGE.md` and be ready to
explain and adapt your work.

**Will I get the same timing locally and in CI?** Not exactly. Machines differ.
The threshold is deliberately generous: design a linear algorithm rather than
optimising tiny timing differences.

**May I change the API or the public tests?** No. You may extend behind the
documented boundaries, but preserve the published contract.

**My CI is red but local tests pass.** Use the CI error log, recreate a clean
virtual environment, then push a fix. Ask for help with the error and command,
not a screenshot alone.

**How do I submit?** Push your final code, confirm the latest Actions run is
green, then submit your private repository URL and final commit SHA. Do not
email ZIP files or screenshots.

**Why must I invite `dondonMD`?** The repository is private. Your instructor
needs collaborator access to view the code, run final tests, and grade it.
