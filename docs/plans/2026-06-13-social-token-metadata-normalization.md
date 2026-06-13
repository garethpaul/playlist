# Social Token Metadata Normalization

status: completed

## Context

The routing boundary checks for Twitter and Beats auth records, but API client
construction directly indexes each record's `extra_data`. Missing dictionaries,
missing keys, non-string values, or blank tokens can raise raw metadata errors
before the existing missing-token failure boundary.

## Requirements

- Extract Twitter OAuth token pairs only from the expected nested dictionary
  shape and require two nonblank strings.
- Extract the Beats access token only from a dictionary and require a nonblank
  string.
- Preserve configured Twitter token fallbacks when social metadata is malformed
  or incomplete.
- Preserve the existing explicit missing-token failures and API construction.
- Add dependency-free malformed-shape tests and mutation-sensitive contracts.

## Scope Boundaries

- Do not change auth routing, redirects, templates, external API calls,
  credentials, dependencies, settings, database behavior, or deployment.

## Work Completed

- Added pure Twitter token-pair and Beats token extractors that require expected
  dictionary shapes and trimmed nonblank strings.
- Routed API client construction through the extractors, preserving configured
  Twitter fallbacks when social metadata is malformed or incomplete and the
  existing explicit missing-token failures.
- Added dependency-free malformed-shape fixtures plus current guidance and
  mutation-sensitive source, test, documentation, and completed-plan contracts.

## Verification Completed

- `python3 test_views_normalization.py -v`
- `make lint`, `make test`, `make build`, `make verify`, and `make check`
- Ran the checker from an external working directory and parsed workflow YAML
  and the `README SVG`.
- Confirmed focused hostile mutations to pair atomicity, Beats normalization,
  live helper wiring, fixtures, documentation, and completed-plan evidence are
  rejected.
- `git diff --check`
- The intended-path secret, captured-identifier, and generated-bytecode scan
  passed; routes, redirects, templates, settings, dependencies, database,
  external API call shapes, and deployment behavior had no diff.
