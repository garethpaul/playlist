# Hosted Security Validation

Status: Complete

## Context

The legacy Django sample has dependency-free checks for production settings,
exact integration routes, POST input normalization, logout method safety, and
malformed provider results, but no hosted validation runs them.

## Changes

- Added a commit-pinned, credential-free, read-only hosted Linux matrix for
  Python 3.10 and Python 3.12.
- Made local and hosted Make gates bytecode-free and guarded leftover caches.
- Kept `make check` independent of the obsolete Django and social API packages.
- Kept Twitter, Beats, Spotify, and production Django credentials out of CI.
- Enforced the complete workflow contract from the static baseline.

## Verification

- `make lint`
- `make test`
- `make build`
- `make check`
- Python 3.10 container `make check`
- workflow YAML parse
- `git diff --check`
- successful hosted Linux `Check` workflow for both Python versions

## Boundaries

- Do not install or call legacy third-party integrations in hosted validation.
- Do not add credentials, deployment, or database services.
- Do not upgrade Django or integration dependencies in this pass.
