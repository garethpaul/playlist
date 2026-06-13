# Production secret key length

status: completed

## Context

Production settings reject a missing or blank `DJANGO_SECRET_KEY`, but accept
trivially short values. Django uses this secret for cryptographic signing, so a
weak configured value can undermine signed data even though no key is checked
into source control.

## Requirements

- Require at least 32 characters after trimming a production
  `DJANGO_SECRET_KEY`.
- Preserve the explicit debug-only development fallback and existing
  environment-only credential handling.
- Add standard-library tests, mutation-sensitive static contracts,
  documentation, and completed verification.
- Do not install or modernize the obsolete Django/social dependency graph or
  make live service calls.

## Verification

## Work completed

- Added a 32-character production minimum after whitespace normalization.
- Preserved the explicit debug-only development fallback and environment-only
  production configuration.
- Added standard-library settings coverage and mutation-sensitive checker and
  documentation contracts.

## Verification completed

- `python3 test_settings_security.py -v`, `make lint`, `make test`,
  `make build`, `make verify`, and `make check` passed without installing the
  legacy dependency graph.
- Checker compilation, `git diff --check`, artifact scans, and secret scans
  passed.
- The checker rejected six hostile mutations covering removal or weakening of
  the length guard, debug-mode coupling, missing short-key coverage, an unsafe
  production fixture, and incomplete plan evidence.
