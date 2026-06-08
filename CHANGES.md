# Changelog

## 2026-06-08

- Removed checked-in Django and service credential placeholders from runtime configuration.
- Made `DJANGO_DEBUG` opt-in, required `DJANGO_SECRET_KEY` outside local debug mode, and documented `DJANGO_ALLOWED_HOSTS`.
- Moved tweet posting and favorite actions onto POST-backed request handling.
- Aligned the tweet form with the `/twttr` POST route.
- Added `make check` with dependency-free static baseline and settings tests
  for this legacy Django sample.
