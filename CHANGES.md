# Changelog

## 2026-06-09

- Added stable Make aliases for lint, test, build, verify, and check gates.

## 2026-06-08

- Removed checked-in Django and service credential placeholders from runtime configuration.
- Made `DJANGO_DEBUG` opt-in, required `DJANGO_SECRET_KEY` outside local debug mode, and documented `DJANGO_ALLOWED_HOSTS`.
- Moved tweet posting and favorite actions onto POST-backed request handling.
- Aligned the tweet form with the `/twttr` POST route.
- Removed a playlist debug print that exposed mention search text and track
  results.
- Rejected blank `DJANGO_SECRET_KEY` values outside local debug mode.
- Added post input normalization for Twitter status text and favorite IDs.
- Required `DJANGO_ALLOWED_HOSTS` outside local debug mode.
- Moved logout to a CSRF-protected POST form and required authenticated POST
  before social-auth cleanup.
- Added `make check` with dependency-free static baseline and settings tests
  for this legacy Django sample.
