# Wildcard Allowed Hosts Plan

Status: Complete

## Context

`DJANGO_ALLOWED_HOSTS` was required when `DJANGO_DEBUG=0`, but a wildcard value
still allowed every host header through production configuration. The setting
should name explicit hosts outside local debug.

## Objectives

- Reject `DJANGO_ALLOWED_HOSTS=*` when debug is disabled.
- Preserve local debug behavior for development-only settings.
- Add no-Django settings coverage for wildcard allowed hosts.
- Extend static checks and docs so the host-header guardrail remains visible.

## Verification

- `python3 test_settings_security.py -v`
- `make check`
- `python3 scripts/check-baseline.py`
- `git diff --check`
