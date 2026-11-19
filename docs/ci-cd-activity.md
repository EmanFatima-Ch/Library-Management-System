# CI/CD Pipeline Activity

## Pipeline Diagram

```text
Feature Branch / Pull Request
             |
             v
      [1. Commit & Push]
             |
             v
      [2. Build / Dependencies]
      checkout@v4, setup-python@v5 (Python 3.12),
      pip install -r requirements.txt
             |
             v
      [3. Lint & Tests]
      flake8 . + pytest; stop the pipeline on failure
             |
             v
      [4. Artifact]
      Package the tested source and dependencies;
      identify the build with its commit SHA
             |
             v
      [5. Staging]
      Deploy and verify authentication/2FA, books,
      members, borrowing, search, and persistence
             |
             v
      [6. Approval Gate]
      Manual review / approval for production release
             |
             v
      [7. Production]
      Deploy the approved artifact and run smoke tests;
      use a rollback and database recovery plan if unhealthy
             |
             v
      [8. Monitoring]
      Review application logs, errors, availability,
      authentication events, and database health
```

## Part A — Source & CI

Changes to the Python library system are committed to a branch and proposed
through a pull request. The GitHub Actions workflow runs for pushes to `main`
and pull requests targeting `main`. It checks out the source, configures Python
3.12, installs `requirements.txt`, then runs `flake8 .` and `pytest`. A lint or
test failure blocks the workflow from reporting a successful CI run.

The tests cover book and member management, borrowing and returns, title/author
search, SQLite persistence, and password plus time-based one-time-password
(2FA) authentication. This helps catch regressions in the operations that
library staff and members rely on before a change is delivered.

## Part B — Delivery

After CI succeeds, the delivery activity is to package the exact tested source
and its dependency instructions as an artifact identified by the commit SHA.
The artifact can then be deployed to staging for end-to-end checks of sign-in
and 2FA, adding and searching books, registering members, borrowing and
returning books, and persisted data.

Production promotion should require an explicit approval gate. Deploy the same
artifact that passed staging, then run smoke tests. If checks fail, roll back
to the previous known-good version and restore or recover the SQLite database
from a verified backup when needed.

## Part C — Operations

After release, monitor service availability, exceptions, authentication and
2FA failures, book/member/borrowing operations, and SQLite read/write health.
Use actionable logs and health checks to identify failures quickly. Back up
the database securely, verify that backups can be restored, and investigate
repeated failed logins or unusual borrowing activity without logging
passwords, one-time codes, or authenticator secrets.

## Current Workflow Scope

The checked-in GitHub Actions workflow currently implements the source/CI
stages: checkout, Python setup, dependency installation, linting, and tests.
Artifact creation, staging and production deployments, manual environment
approval, and ongoing monitoring are delivery/operations steps in this
activity; they are not currently automated by the workflow.
