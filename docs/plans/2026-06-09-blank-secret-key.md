# Blank Secret Key Plan

Status: Complete

## Context

`DJANGO_SECRET_KEY` was required outside local debug mode, but a whitespace-only
environment value was still truthy and satisfied the check.

## Objectives

- Strip `DJANGO_SECRET_KEY` before validating it.
- Reject blank secret values when `DJANGO_DEBUG` is disabled.
- Extend settings tests, docs, and static checks for this guardrail.

## Verification

- `python3 test_settings_security.py -v`
- `make check`
- `python3 scripts/check-baseline.py`
- `python3 -m py_compile app/settings.py test_settings_security.py scripts/check-baseline.py`
- `git diff --check`
