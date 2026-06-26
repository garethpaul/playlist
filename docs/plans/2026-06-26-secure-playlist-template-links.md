# Secure Playlist Template Resources

Status: completed

## Context

The rendered playlist used an unrelated plain-HTTP image for its Twitter
label, the provider's non-HTTPS avatar field, HTTP profile and status links,
and a reusable named browsing target without opener isolation.

## Goals

- Remove the unrelated remote service-label image.
- Use the provider's HTTPS avatar field.
- Keep Twitter profile and status navigation on HTTPS.
- Isolate newly opened external tabs from the playlist window.
- Preserve the legacy playlist layout and provider behavior.

## Work Completed

- Replaced the remote icon with a local text service label.
- Switched playlist avatars to `profile_image_url_https`.
- Upgraded Twitter profile and status links to HTTPS.
- Added `_blank` plus `noopener noreferrer` to external Twitter links.
- Added a focused source regression and durable static repository contracts.
- Updated maintainer, security, vision, README, and changelog guidance.

## Verification Completed

- The red-first focused regression failed on the unrelated HTTP image before
  the template change, then `python3 test_views_normalization.py -v` passed all
  23 dependency-free view tests.
- `make lint`, `make test`, `make build`, `make verify`, and `make check`
  passed from the repository root.
- Absolute-Makefile `make check` passed from an external working directory.
- Focused hostile mutations restoring the remote icon, HTTP links,
  non-HTTPS avatar field, named target, or missing opener relation were
  rejected by tests or the static baseline.
- Isolated Python compilation and the generated-bytecode cleanup check passed.
- `git diff --check` passed.
