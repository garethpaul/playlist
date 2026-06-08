## Playlist Vision

Playlist is a legacy Django sample for a Music Hack Day project that connects
Twitter authentication, music-service authentication, mentions, and playlist
creation into a small web app.

The repository is useful as a compact integration demo for social login,
service API clients, Django views, Fabric startup, and template-driven pages.

The goal is to preserve the hackathon learning value while making legacy
service dependencies, credential handling, and upgrade risks explicit.

The current focus is:

Priority:

- Preserve the Django sample flow from login to generated playlist
- Keep service credentials out of source and documented as local configuration
- Treat Django 1.6-era code and API clients as legacy
- Keep template and view behavior easy to trace

Next priorities:

- Move placeholder credentials into environment-based configuration
- Add setup notes for currently unavailable or changed third-party services
- Add tests around auth-state routing and playlist selection logic
- Modernize Django only in a separate compatibility pass

Contribution rules:

- One PR = one focused auth, API, view, template, or documentation change.
- Do not commit real access tokens or user data.
- Include local setup and migration notes for dependency changes.
- Keep hackathon-specific behavior visible rather than abstracting it away.

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
