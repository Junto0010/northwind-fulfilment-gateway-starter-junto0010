# Instructor setup guide

## The workflow in one page

1. Give every student their own copy of this starter repository.
2. They work locally and push; the included GitHub Action reruns public tests.
3. At the deadline, record each final commit SHA and stop accepting changes.
4. Run private checks against that exact SHA, then conduct the short review.
5. Record automated marks out of 70 and review marks out of 30.

Students do **not** send performance screenshots. Their code, commit history,
green CI result, `DECISIONS.md`, and individual review are the evidence.

## Distribution

Use this directory as a GitHub template repository or GitHub Classroom starter.
Students receive the same files, run `python -m pytest -q` locally, and see the
same check in Actions after every push. The generated `grading/grade.json`
artifact gives quick, understandable feedback; it is not the final score.

### Recommended: GitHub Classroom

Create an **individual assignment**, use this project as its starter template,
set the deadline, and send students the Classroom invitation link. Classroom
creates a separate private repository for each student. The workflow is copied
into each repository and runs on every push.

### Without GitHub Classroom

Create one private repository per student from this template, grant access only
to the relevant student, and send its URL. They clone, code, and push; they
submit the URL plus final commit SHA through your LMS. Before releasing the
assignment, make one test push to a copy and confirm the **Capstone checks**
Action appears and can install dependencies.

## Final automated grading (keep separate)

Keep additional tests in a **private instructor repository**, never in the
starter repository or its Actions workflow. In your grading job:

1. Check out the student's submitted commit into a clean container.
2. Install `capstone-fulfilment-gateway/requirements.txt`.
3. Mount or copy your private `hidden_tests/` directory beside the project.
4. Run `pytest -q tests hidden_tests` with a fixed CPU/memory limit and record
   the result.
5. Record the score outside the student-controlled repository.

Do not place hidden tests in student repositories, Actions artifacts, or public
workflows. The included `grade.py` is deliberately only a feedback reporter;
it is not a secure final grader. If you have no separate CI system yet, clone
each submitted repository at its final SHA into a clean folder, copy in your
private tests, and run the command above manually.

The private suite should exercise the documented interface, not inspect source
for a particular implementation. Recommended extra cases: multiple ownership
attacks, duplicate/empty data, a carrier that fails then recovers, invalid
concurrency limits, 250,000 rows with skewed customers, and a deliberately
large list response that must gzip.

## Fair performance testing

Use a relative or comfortably loose threshold on a pinned runner, warm up once,
and enforce a timeout. Do not grade microseconds: the aim is to distinguish a
linear lookup/indexing design from an accidental O(n²) design. Preserve an
absolute correctness check alongside every timing check.

## Recommended rubric and review

Award 70 automated points as described in the student README and 30 points in a
6–8 minute individual review. Give each student one small, randomised change
card (new carrier rule, temporary carrier outage, changed quote formula, or a
new validation rule). They must make the change and identify the relevant test.

This is a much stronger integrity control than trying to detect AI output. It
rewards explainable, adaptable work, permits declared AI use, and gives a
student who built their work honestly a clear way to demonstrate it.

## What to record for every mark

Keep the repository URL, final SHA, public CI outcome, private automated score
out of 70, the three review scores out of 30, and short feedback. Grade the
recorded final SHA only, not a later correction. This gives you an audit trail
for any mark query.

## Free-plan workflow (no Classroom 50 required)

You do not need an organisation, GitHub Education, or a paid plan to run this
assessment. Make the starter repository **public** and mark it as a **template
repository**. Each student creates their own **private** repository from the
template and invites the instructor (`dondonMD`) as a collaborator.

Give students one template URL and require this repository name:
`northwind-fulfilment-<github-username>`. They must choose private visibility
and invite the instructor with write access immediately after creation. The
student owns the repository, so their GitHub Free account supplies its Actions
allowance; the provided workflow runs automatically whenever they push.

This does not provision repositories from a roster automatically. GitHub's
free plan has no native replacement for that feature. It avoids creating
repositories one by one, keeps submissions private, and costs nothing. Collect
the private repository URL and final commit SHA through your LMS or a simple
Google Form at the deadline.
