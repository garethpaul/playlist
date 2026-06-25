---
title: Social-Auth Error Route
date: 2026-06-25
type: implementation-plan
status: completed
---

# Social-Auth Error Route

## Summary

Route legacy social-auth failures to the registered root login rather than an
unregistered `/login-error/` path.

## Problem Frame

The root login view is the application's existing integration recovery screen,
but `SOCIAL_AUTH_LOGIN_ERROR_URL` pointed at a path absent from `urlpatterns`.
Provider authentication failures therefore ended in an application 404.

## Requirements

- R1. Set the social-auth error URL to `/`.
- R2. Keep the exact root pattern registered to `home.views.login`.
- R3. Reject reintroduction of `/login-error/`.
- R4. Preserve login success, integration auth-state, logout, credentials,
  provider API, template, and database behavior.
- R5. Add dependency-free settings, route-source, static, guidance, and plan
  contracts.

## Work Completed

- Aligned `SOCIAL_AUTH_LOGIN_ERROR_URL` with the root login route.
- Added settings and URL-source regressions that bind the target to the exact
  registered root pattern.
- Extended the baseline and public guidance with the recovery boundary.

## Verification Completed

- The pre-fix settings regression failed on the unregistered `/login-error/`
  value; focused settings and URL tests passed after using the registered root
  login. The recovery target is the registered root login.
- 29 dependency-free tests passed through `make check` from the repository and
  an external working directory.
- Six isolated hostile mutations were rejected across the error target, root
  route, settings regression, URL regression, guidance, and completed plan.
- `git diff --check`, artifact, credential, captured-identifier, conflict,
  binary, size, mode, and generated-bytecode scans passed.
- Exact diff review, hosted Python 3.10/3.12 checks, and exact-head Codex review
  remain required before merge.
