# Location-Independent Make Gates

status: completed

## Context

The standard Make aliases pass from the repository root, but an absolute
Makefile invocation from another directory resolves the baseline checker and
all three dependency-free test scripts against the caller. Shared automation
should run the same security, normalization, and URL contracts without first
changing directories.

## Requirements

- Derive an override-protected repository root from the Makefile location.
- Invoke the baseline checker and each existing test script by rooted path.
- Preserve bytecode suppression, verbose test output, alias dependencies, and
  the existing Python command behavior.
- Preserve all 18 dependency-free tests, auth-state and token normalization
  contracts, credential boundaries, workflow, and obsolete-integration scope.
- Statically reject caller-relative or caller-overridable gate execution.

## Scope Boundaries

- Do not change Django, Twitter, Beats, Spotify, OAuth, URL, view, settings,
  dependency, credential, template, integration, or network behavior.
- Do not add obsolete dependencies or live service calls.
- Do not weaken the checker, tests, or bytecode-free gate.

## Implementation Units

1. Root checker and test-script execution while preserving every existing
   alias and command option.
2. Extend `scripts/check-baseline.py` to require rooted recipes, this plan,
   completed evidence, and maintenance documentation.
3. Document the external invocation contract in `README.md` and `CHANGES.md`.

## Verification Plan

- Run all standard aliases from the repository root and through the absolute
  Makefile path from `/tmp`, including a caller-supplied root override.
- Compile the checker outside the repository and parse workflow YAML and the
  README SVG.
- Run isolated hostile mutations over each rooted recipe and plan evidence.
- Audit intended paths, unchanged integration surfaces, whitespace, generated
  bytecode, captured identifiers, and secret-like data.

## Work Completed

The Makefile now derives an override-protected absolute repository root from
its own location and invokes the checker plus all three dependency-free test
scripts through rooted paths. Existing aliases, bytecode suppression, verbose
output, Python command behavior, integration code, and credentials remain
unchanged.

## Verification Completed

- `make lint`, `make test`, `make build`, `make verify`, `make check`,
  `make static-check`, `make settings-test`, and `make url-test` passed from the
  repository root; test-bearing targets ran all 18 dependency-free tests.
- Every target passed from `/tmp` through the repository's absolute Makefile
  path.
- External `make check` passed with caller-supplied `REPO_ROOT=/tmp`, confirming
  command-line variables cannot redirect any script.
- `python3 -m py_compile` passed for the checker and all three test scripts with
  bytecode routed outside the repository; workflow YAML and README SVG parsed
  successfully.
- Twelve isolated hostile mutations were rejected across root derivation,
  override resistance, all four rooted scripts, completed evidence, README,
  and change-history contracts.
