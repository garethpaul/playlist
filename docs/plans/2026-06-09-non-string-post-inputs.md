# Non-String Post Inputs Plan

Status: Complete

## Context

`clean_post_text` trimmed strings and skipped blank values, but direct calls with
non-string post inputs could raise before the Twitter status and favorite ID
guards returned a safe no-op value.

## Objectives

- Make `clean_post_text` return `None` for non-string post inputs.
- Keep `clean_tweet_id` on the same normalization path for malformed favorite
  IDs.
- Add dependency-free view normalization tests using local import stubs.
- Include the new tests in `make test` and the static baseline.

## Verification

- `python3 test_views_normalization.py -v`
- `make lint`
- `make test`
- `make build`
- `make check`
- `git diff --check`
