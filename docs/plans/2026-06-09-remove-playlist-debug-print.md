# Remove Playlist Debug Print

Status: Complete

Date: 2026-06-09

## Context

`home.views.beats` derived search text from Twitter mentions, queried Beats for
track results, and then printed `print(search, tracks)`. Those values can
contain user-linked social and music-service data and should not be exposed in
logs by default.

## Goals

- Preserve the existing playlist selection flow.
- Remove the debug print from the Beats view.
- Extend the static baseline so the debug print is forbidden.
- Document that mention text and track results should stay out of debug output.

## Verification

- `make check`
- `python3 scripts/check-baseline.py`
- `python3 test_settings_security.py -v`
- `git diff --check`
