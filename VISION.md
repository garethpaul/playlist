## Playlist Vision

This document explains the current state and direction of the project.
Project overview and developer docs: [`README.md`](README.md)

Playlist is a legacy Django sample for a Music Hack Day project that connects
Twitter authentication, music-service authentication, mentions, and playlist
creation into a small web app.

The repository is useful as a compact integration demo for social login,
service API clients, Django views, Fabric startup, and template-driven pages.

The goal is to preserve the hackathon learning value while making legacy
service dependencies, credential handling, and upgrade risks explicit.

Current baseline: `make lint`, `make test`, `make build`, `make verify`, and
`make check` verify Python 3 syntax, environment-based Django secret/debug
configuration, static security guardrails, and the documented fixes for the
hardcoded `SECRET_KEY` and default debug-mode bugs.

The current focus is:

Priority:

- Preserve the Django sample flow from login to generated playlist
- Keep environment-based configuration as the baseline for secrets and service
  credentials
- Keep service credentials out of source and documented as local configuration
- Treat Django 1.6-era code and API clients as legacy
- Keep template and view behavior easy to trace
- Keep state-changing tweet, favorite, and playlist actions on POST paths
- Keep logout as a POST-only logout action with CSRF protection
- Keep post input normalization close to outbound Twitter side effects
- Keep non-string post inputs out of Twitter service calls
- Keep malformed Beats search results out of the playlist queue
- Keep malformed Twitter mention text out of outbound track searches
- Keep login and playlist routing aligned on the same required Twitter and
  Beats auth-state predicate
- Keep `DJANGO_SECRET_KEY` and social API credentials environment-driven
- Keep blank `DJANGO_SECRET_KEY` values from satisfying production settings
- Keep production `DJANGO_SECRET_KEY` values at least 32 characters long
- Keep allowed hosts required outside local debug mode
- Keep wildcard allowed hosts rejected outside local debug mode
- Keep Twitter and Beats URL patterns as exact-match integration routes
- Keep user-linked playlist data out of debug print output
- Keep standard Make gate aliases available for local verification
- Keep the dependency-free security baseline running in pinned,
  credential-free, read-only GitHub Actions with Python 3.10 and 3.12
- Keep local and hosted verification free of generated Python bytecode

Next priorities:

- Add setup notes for currently unavailable or changed third-party services
- Add tests around playlist selection logic
- Add focused tests around log-safe playlist selection once dependencies are
  pinned or replaced
- Modernize Django only in a separate compatibility pass
- Replace deprecated Django rendering and request APIs in a compatibility pass

Contribution rules:

- One PR = one focused auth, API, view, template, or documentation change.
- Do not commit real access tokens or user data.
- Include local setup and migration notes for dependency changes.
- Keep hackathon-specific behavior visible rather than abstracting it away.
- Keep `make lint`, `make test`, `make build`, `make verify`, and `make check`
  passing for settings and credential guardrails.

## Security And Responsible Use

Canonical security policy and reporting:

- [`SECURITY.md`](SECURITY.md)

The app touches social identities, access tokens, and music-service data.
Credentials must remain local, token revocation should be respected, and sample
data should be fake or user-provided.

## What We Will Not Merge (For Now)

- Production credentials or captured user data
- Silent posting, favoriting, or playlist changes
- Framework upgrades mixed with feature work
- Opaque background jobs that call user-linked services

This list is a roadmap guardrail, not a permanent rule.
Strong user demand and strong technical rationale can change it.
