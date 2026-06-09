# Required Allowed Hosts Plan

Status: Complete

## Context

The settings module required `DJANGO_SECRET_KEY` when `DJANGO_DEBUG` was off,
but still allowed non-debug startup with an empty `DJANGO_ALLOWED_HOSTS`. That
made production host validation easy to omit accidentally.

## Objectives

- Raise a `RuntimeError` when `DJANGO_ALLOWED_HOSTS` is empty outside local
  debug mode.
- Add a stdlib settings test named
  `test_allowed_hosts_required_when_debug_disabled`.
- Extend the static baseline and docs so the production allowed-hosts guard
  remains visible.

## Verification

- `python3 test_settings_security.py -v`
- `make check`
- `python3 scripts/check-baseline.py`
- `git diff --check`
