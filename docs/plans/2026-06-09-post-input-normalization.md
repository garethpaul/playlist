# Post Input Normalization

Status: Complete

Date: 2026-06-09

## Context

The legacy Twitter routes already use POST for side-effecting actions, but the
submitted status and favorite ID values were passed through directly. Blank
status text could trigger an outbound Twitter call, and non-numeric favorite
IDs could reach the Twitter client before being swallowed by a broad exception.

## Goals

- Preserve the existing `/twttr` status-posting flow.
- Trim status text with `clean_post_text` and skip blank posts before calling
  Twitter.
- Only call `CreateFavorite` for numeric tweet IDs accepted by
  `clean_tweet_id`.
- Extend the static baseline so post input normalization remains in place.

## Verification

- `make check`
- `python3 scripts/check-baseline.py`
- `python3 test_settings_security.py -v`
- `git diff --check`
