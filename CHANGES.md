# Changelog

## 2026-06-19

- Escaped provider-controlled values before placing them in JavaScript string
  literals and loaded the legacy Beats player SDK over HTTPS.
- Marked session and CSRF cookies secure outside local debug mode.
- Returned incomplete integration authentication to the registered root login
  page instead of the unregistered `/login` path.

## 2026-06-17

- Removed the OAuth access token from the visible player control while keeping
  the existing SDK authentication object for playback.

## 2026-06-16

- Replaced player metadata and timing `innerHTML` writes with `textContent` so
  provider SDK callback values remain text-only.

## 2026-06-15

- Restricted request-controlled player input to bounded decimal preview seconds
  before server-rendered JavaScript interpolation.

## 2026-06-14

- Made every standard Make gate resolve the checker and dependency-free test
  scripts from the repository root, including external absolute-Makefile calls.

## 2026-06-13

- Normalized Twitter and Beats social-auth token metadata before API client
  construction and added malformed nested-shape tests.
- Centralized the required Twitter-and-Beats auth-state decision used by login
  and playlist routing, with dependency-free complete and malformed-state tests.
- Required production `DJANGO_SECRET_KEY` values to contain at least 32
  characters after trimming, with standard-library regression coverage.

## 2026-06-10

- Added pinned, credential-free, read-only GitHub Actions validation on Python
  3.10 and 3.12 for the dependency-free Django security baseline.
- Made every Make gate bytecode-free and added a guard against leftover Python
  cache output.
- Extended the static baseline to require both completed hosted-validation
  plans and the exact least-privilege workflow contract.
## 2026-06-09

- Rejected non-string post inputs before Twitter status or favorite
  normalization.
- Rejected wildcard allowed hosts when debug is disabled.
- Added stable Make aliases for lint, test, build, verify, and check gates.
- Skipped malformed Beats search results before queueing playlist entries.
- Normalized malformed Twitter mention text and bounded outbound track search
  queries.

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
