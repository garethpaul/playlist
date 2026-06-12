# Playlist CI Baseline

## Status: Complete

## Context

`playlist` has dependency-free Django settings, URL, and view-normalization
checks behind `make check`. The repository needs a lightweight GitHub Actions
gate so credential, host, POST-only, and routing guardrails run before review.

## Objectives

- Run the existing static and dependency-free tests in GitHub Actions.
- Keep the workflow independent of legacy Django runtime dependencies.
- Make the CI workflow presence part of the static baseline contract.

## Work Completed

- Added `.github/workflows/check.yml` to run `make check` on pushes, pull
  requests, and manual dispatches.
- Set up Python 3.12 in CI for the dependency-free baseline checker and tests.
- Extended `scripts/check-baseline.py` to require the CI workflow and this
  completed plan.
- Updated README, VISION, SECURITY, and CHANGES with the CI baseline.

## Verification

- `make check`
- `python3 scripts/check-baseline.py`
- `git diff --check`

## Follow-Up Candidates

- Add a pinned legacy Django dependency test job after the old runtime and
  third-party service assumptions are documented.
