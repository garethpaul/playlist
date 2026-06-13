# Social Token Metadata Normalization

status: pending

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

Pending implementation.

## Verification Completed

Pending implementation and validation.
