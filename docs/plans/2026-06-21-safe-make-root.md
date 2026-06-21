# Safe Makefile Root Resolution

status: completed

## Context

The existing absolute Makefile contract ignored `REPO_ROOT` overrides, but a
caller could replace Make's automatic `MAKEFILE_LIST` variable and redirect
the checker plus all three dependency-free test scripts to another directory.
The first verifier only inspected dry-run text, so caller-controlled `SHELL`
still executed before the assertions and double quotes or backticks in a
checkout path remained unsafe at recipe execution time.

## Scope Boundaries

- Do not install or execute the obsolete Django and social-service dependency
  set.
- Do not change application, authentication, provider, template, URL,
  credential, database, or network behavior.
- Preserve every existing dependency-free security and normalization test.

## Work Completed

- Reject command-line and environment overrides of `MAKEFILE_LIST`.
- Reject non-empty `MAKEFILES` preload configuration.
- Freeze the recipe shell, shell flags, and Python command against Make
  command-line and environment overrides.
- Canonicalize and shell-quote the trusted Makefile directory while preserving
  spaces, apostrophes, double quotes, and backticks.
- Ignore caller-controlled `REPO_ROOT` values for every public target.
- Replace dry-run text checks with executable stub gates for all nine public
  Make targets, including an earlier explicit Makefile.

## Verification Completed

- `make lint`, `make settings-test`, `make url-test`, `make test`, `make build`,
  `make static-check`, `make root-test`, `make verify`, and `make check` passed.
- All 27 dependency-free settings, view-normalization, and URL tests passed.
- 81 executable target and authority-override combinations passed from a
  temporary path containing repeated spaces, brackets, apostrophes, double
  quotes, and backticks.
- Command-line and environment `MAKEFILE_LIST` overrides failed closed.
- Command-line and environment `MAKEFILES` preload attempts failed closed.
- An earlier explicit Makefile preserved the trusted repository root.

## Trust Boundary

GNU Make parses caller-supplied preload and explicit Makefiles before this
repository can reject them. Those files, the host `PATH`, and the `python3`
executable selected from it remain caller/runner trust inputs rather than code
this repository can sandbox.
