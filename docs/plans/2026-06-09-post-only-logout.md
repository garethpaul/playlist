# Post-Only Logout Plan

Status: Complete

Date: 2026-06-09

## Context

The logout route deleted social-auth rows and ended the Django session through a
GET link in the base template. Logout is a state-changing action, so it should
require an authenticated POST with CSRF protection like the tweet and favorite
actions.

## Goals

- Require authentication before running logout cleanup.
- Require POST for the logout view.
- Replace the base-template logout link with a CSRF-protected POST form.
- Extend the static baseline and docs so GET logout links do not return.

## Verification

- `make check`
- `python3 scripts/check-baseline.py`
- `python3 test_settings_security.py -v`
- `git diff --check`
