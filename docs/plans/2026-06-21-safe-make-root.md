# Safe Makefile Root Resolution

status: completed

## Context

The existing absolute Makefile contract ignored `REPO_ROOT` overrides, but a
caller could replace Make's automatic `MAKEFILE_LIST` variable and redirect
the checker plus all three dependency-free test scripts to another directory.

## Scope Boundaries

- Do not install or execute the obsolete Django and social-service dependency
  set.
- Do not change application, authentication, provider, template, URL,
  credential, database, or network behavior.
- Preserve every existing dependency-free security and normalization test.

## Work Completed

- Reject command-line and environment overrides of `MAKEFILE_LIST`.
- Canonicalize the trusted Makefile directory while preserving paths with
  spaces and apostrophes.
- Ignore caller-controlled `REPO_ROOT` values for every public target.
- Add deterministic regression coverage for all nine public Make targets.

## Verification Completed

- `make lint`, `make settings-test`, `make url-test`, `make test`, `make build`,
  `make static-check`, `make root-test`, `make verify`, and `make check` passed.
- All 27 dependency-free settings, view-normalization, and URL tests passed.
- 27 target and `REPO_ROOT` override combinations passed from a temporary path
  containing spaces and an apostrophe.
- Command-line and environment `MAKEFILE_LIST` overrides failed closed.
