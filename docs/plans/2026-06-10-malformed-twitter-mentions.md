# Malformed Twitter Mentions

Status: Complete

## Context

The playlist loop applied the username regex directly to provider-owned
`status.text`. Missing or non-string text could raise `TypeError`, while
handle-only and oversized values could issue empty or excessive Beats queries.

## Objectives

- Add `clean_track_search` as the boundary for Twitter mention text.
- Reject missing, non-string, blank, and handle-only values.
- Bound outbound Beats search text to 200 characters.
- Treat missing status attributes defensively.
- Keep malformed Twitter mention text out of provider calls and playlist data.

## Verification

- `make lint`
- `make test`
- `make build`
- `make verify`
- `make check`
- Mutation: remove non-string rejection and confirm the tests fail.
- Mutation: remove the 200-character bound and confirm the tests fail.
- `git diff --check`
