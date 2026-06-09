# Make Gate Aliases

Status: Complete

## Context

The repository had a single `make check` entry point that combined the static
security baseline with dependency-free settings tests. The shared maintenance
workflow also expects root lint, test, build, verify, and check commands.

## Completed Scope

- Added `make lint` for the static security baseline.
- Added `make test` for `test_settings_security.py`.
- Added `make build` as the local static build gate.
- Added `make verify` to combine lint, test, and build.
- Extended README, VISION, SECURITY, CHANGES, and the baseline checker so the
  gate contract stays visible.

## Verification

- `make lint`
- `make test`
- `make build`
- `make verify`
- `make check`
- `python3 scripts/check-baseline.py`
- `python3 test_settings_security.py -v`
- `git diff --check`
