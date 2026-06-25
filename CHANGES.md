# Changelog

## 2026-06-25T15:28:19-07:00 — P2 local repository metadata

- Cycle: inspected the MIT-licensed legacy Django sample, disabled issue state,
  recent auth/security work, settings, routes, templates, provider boundaries,
  dependency-free tests, and hosted lanes.
- Threads: started portable local intelligence enforcement; continued
  dependency-free security and repository-contract hardening; stopped none.
- Bug: `.explore/` was hidden only by this clone's private `.git/info/exclude`,
  so fresh checkouts could report maintainer notes as untracked source or stage
  them accidentally.
- Work: added the active rule; replaced raw ignore substring checks with exact
  active patterns, effective `git check-ignore`, and `git ls-files` index state.
- Files: changed `.gitignore`, `scripts/check-baseline.py`, `README.md`,
  `SECURITY.md`, `VISION.md`, `AGENTS.md`, and
  `docs/plans/2026-06-25-local-repository-metadata-ignore.md`.
- Validation: the red-first baseline failed on the absent active `.explore/`
  rule. The focused baseline, 9 settings tests, and 2 URL tests pass. Root and
  external `make check` each pass 29 dependency-free tests plus 81 executable
  Make target/override cases; isolated Python compilation, generated-bytecode,
  and `git diff --check` gates also pass. Exact-head Codex review reported no
  actionable findings, and duplicate hosted Python 3.10/3.12 lanes plus CodeQL
  passed on PR #13.
- Findings: clone-local excludes are not portable repository policy, and raw
  text cannot prove ordered ignore behavior or an empty tracked source set.
- Blockers: retired provider SDKs and unbounded legacy requirements remain
  intentionally uninstalled; validation protects source/security boundaries.
- Next: merge PR #13, persist the repository map and evidence, then continue
  the licensed public-repository loop.

## 2026-06-25T13:22:43-07:00 — P1 social-auth failure recovery

- Cycle: inspected the MIT-licensed legacy Django sample, disabled issue state,
  recent security work, settings, URL patterns, auth routing, provider response
  boundaries, templates, dependency-free tests, and hosted verification.
- Threads: prioritized authentication recovery over provider modernization
  because `SOCIAL_AUTH_LOGIN_ERROR_URL` pointed at `/login-error/` even though
  the application registers no route for that path.
- Bug: Twitter/social-auth failures could redirect users to an application 404
  instead of the existing root login and reconnection flow.
- Files: changed `app/settings.py`, `test_settings_security.py`,
  `test_url_patterns.py`, `scripts/check-baseline.py`, repository guidance, and
  `docs/plans/2026-06-25-social-auth-error-route.md`.
- Validation: the pre-fix focused settings regression failed on
  `/login-error/`; focused settings and URL-source tests pass with the root
  target and exact registered login pattern. Six isolated mutations were
  rejected. Root and external `make check` each passed 29 dependency-free
  tests plus 81 executable Make target/override cases, and isolated Python
  compilation plus generated-bytecode checks passed.
- Blockers: retired provider SDKs and unbounded legacy requirements remain
  intentionally uninstalled; verification protects local source boundaries,
  not live Twitter/Beats/social-auth deployability.
- Next: run hostile mutations, root and external full gates, exact-head Codex
  review, and hosted Python 3.10/3.12 checks before merge.

## 2026-06-21

- Hardened every public Make quality gate against `MAKEFILE_LIST`, `MAKEFILES`,
  `REPO_ROOT`, `SHELL`, shell-flag, and `PYTHON` redirection. Executable
  regressions cover temporary paths containing spaces, apostrophes, double
  quotes, and backticks.

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
