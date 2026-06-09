# Exact Integration Routes

Status: Complete
Date: 2026-06-09

## Context

The legacy Django URL patterns for `twttr` and `beats` used prefix-matching
regular expressions. That let paths beginning with those names reach the
authenticated Twitter and Beats integration views even when the path was not
the canonical endpoint.

## Changes

- Anchored the `twttr` and `beats` URL regexes so only `/twttr` and `/beats`
  resolve to those views.
- Added `test_url_patterns.py` as a dependency-free guard for the exact-match
  route contract.
- Added the URL-pattern test to `make test` and the static baseline checker.

## Verification

- `make lint`
- `make test`
- `make build`
- `make check`
