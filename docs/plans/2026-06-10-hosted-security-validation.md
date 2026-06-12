# Hosted Security Validation

Status: Complete

## Context

The legacy Django sample has dependency-free checks for production settings,
exact integration routes, POST input normalization, logout method safety, and
malformed provider results, but no hosted validation runs them.

## Work Completed

- Added a commit-pinned, credential-free, read-only hosted Linux matrix for
  Python 3.10 and Python 3.12.
- Made local and hosted Make gates bytecode-free and guarded leftover caches.
- Kept `make check` independent of the obsolete Django and social API packages.
- Kept Twitter, Beats, Spotify, and production Django credentials out of CI.
- Enforced the complete workflow contract from the static baseline.

## Verification Completed

- Local `make lint`, `make test`, `make build`, `make verify`, and `make check`
  passed with 13 dependency-free tests and no generated Python bytecode.
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/check-baseline.py` and
  `git diff --check` passed.
- Six hostile workflow, normalization, and generated-bytecode mutations were
  rejected by the canonical baseline or focused tests.
- GitHub Actions push run `27390853154` and pull-request run `27390897822`
  completed successfully on exact implementation head
  `298b6814e6a0d4d88c63ec5672bea61d3281b1ca` for Python 3.10 and Python 3.12.
- The workflow preserves checkout commit
  `df4cb1c069e1874edd31b4311f1884172cec0e10`, setup-python commit
  `a309ff8b426b58ec0e2a45f0f869d46889d02405`,
  `persist-credentials: false`, and `PYTHONDONTWRITEBYTECODE: "1"`.
- Focused coverage includes `test_secret_key_required_when_debug_disabled`,
  `test_first_track_result_rejects_malformed_beats_results`, and
  `test_clean_track_search_rejects_malformed_twitter_mentions`.

## Boundaries

- Do not install or call legacy third-party integrations in hosted validation.
- Do not add credentials, deployment, or database services.
- Do not upgrade Django or integration dependencies in this pass.
