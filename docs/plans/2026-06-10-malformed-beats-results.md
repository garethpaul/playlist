# Malformed Beats Search Results

Status: Complete

Date: 2026-06-10

## Context

`home.views.beats` expected Beats search responses to be dictionaries with a
non-empty `data` list and a track dictionary containing an `id`. Malformed
responses could raise while building the playlist instead of being skipped like
other invalid integration inputs.

## Goals

- Add a small `first_track_result` helper for Beats result validation.
- Skip malformed Beats search results before queueing playlist entries.
- Add dependency-free view normalization tests for malformed and valid Beats
  result payloads.
- Extend static checks and docs for the malformed-result guardrail.

## Verification

- `python3 test_views_normalization.py -v`
- `make check`
- `python3 scripts/check-baseline.py`
- `git diff --check`
