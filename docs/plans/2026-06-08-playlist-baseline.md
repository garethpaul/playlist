# Playlist Baseline Plan

Status: Complete

Date: 2026-06-08

## Context

`playlist` is a legacy Django 1.6-era Music Hack Day sample. The useful behavior is the small integration flow across Twitter login, Beats login, mentions, and playlist playback, but the repository still needs safe defaults and repeatable checks before future modernization.

## Goals

- Keep the hackathon app shape intact.
- Remove committed secret and token placeholders from runtime settings.
- Default debug mode off and require explicit local opt-in.
- Stop using `request.REQUEST` for side-effecting Twitter actions.
- Add a verification path that works without installing unavailable legacy service clients.

## Work Completed

- Settings now read `DJANGO_SECRET_KEY`, `DJANGO_DEBUG`, `DJANGO_ALLOWED_HOSTS`, `DJANGO_SQLITE_PATH`, and social-service credentials from environment variables.
- Production-style startup fails closed when `DJANGO_SECRET_KEY` is absent and debug mode is not explicitly enabled.
- Tweet posting and favorite creation read from POST data; preview and track routing can still preserve UI state.
- The Beats template submits favorite actions through a CSRF-protected POST form.
- `make check` runs `scripts/check-baseline.py` and `test_settings_security.py`, which validate Python syntax, security guardrails, docs, SVG parseability, and environment-driven settings behavior.

## Verification

- `make check`
- `python3 test_settings_security.py -v`
- `git diff --check`

## Follow-Up

- Add narrow unit tests around auth routing and playlist selection after the legacy dependency set is pinned or replaced.
- Modernize Django and retired service integrations in a separate compatibility pass.
