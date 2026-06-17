# Security Policy

## Supported Versions

The supported security scope for `playlist` is the current default branch, `master`. Older commits, tags, branches, forks, demos, and generated artifacts are not actively supported unless the repository explicitly marks them as maintained.

Project summary: No GitHub description is currently set.

## Reporting a Vulnerability

Please report suspected vulnerabilities through GitHub's private vulnerability reporting or by opening a draft GitHub Security Advisory for `garethpaul/playlist` when that option is available. If GitHub does not show a private reporting option for this repository, contact the repository owner through GitHub and avoid posting exploit details publicly until the issue can be assessed.

Do not open a public issue that includes exploit code, secrets, personal data, or detailed reproduction steps for an unpatched vulnerability.

## What to Include

Helpful reports include:

- the affected file, endpoint, permission, dependency, or workflow
- a concise impact statement explaining what an attacker could do
- reproduction steps using test data and accounts you control
- the branch, commit SHA, platform version, device, runtime, or dependency versions used
- logs, screenshots, or proof-of-concept snippets that demonstrate impact without exposing private data

## Project Security Posture

- This repository appears to be a Python web API or service project. The active security scope is the code and documentation on the default branch.
- Review found authentication, token, or session-related code paths; changes in those areas should receive security-focused review before merge.
- Review found external API integrations or credential-adjacent configuration; changes in those areas should receive security-focused review before merge.
- Review found network clients, sockets, web APIs, or service endpoints; changes in those areas should receive security-focused review before merge.
- Review found mobile permission or privacy-sensitive data handling; changes in those areas should receive security-focused review before merge.
- Review found file, document, data, or media parsing flows; changes in those areas should receive security-focused review before merge.
- Dependency manifests detected: requirements.txt. Dependency updates should preserve lockfiles when present and avoid introducing packages without a clear maintenance reason.
- Pinned, credential-free, read-only GitHub Actions validation runs the
  dependency-free settings, route, and input-normalization baseline without
  installing legacy packages or using Twitter, Beats, Spotify, or Django
  production credentials.
- Keep verification bytecode-free so generated Python caches do not enter
  commits or obscure the reviewed source tree.
- Current baseline reads Django `SECRET_KEY`, `DJANGO_DEBUG`,
  `DJANGO_ALLOWED_HOSTS`, Twitter, Beats, and Spotify credentials from
  environment variables. `DJANGO_DEBUG` defaults to off, and
  `DJANGO_SECRET_KEY` is required unless local debug mode is explicitly enabled.
  A blank `DJANGO_SECRET_KEY` value is rejected in non-debug mode, and wildcard
  allowed hosts are rejected outside local debug.
  Production secret keys must be at least 32 characters after trimming.

## Service and API Notes

For web services, APIs, sockets, or scraping workflows, prioritize reports involving authentication bypass, authorization errors, injection, server-side request forgery, unsafe deserialization, credential leakage, data exposure, or denial-of-service conditions. Use test accounts and minimal proof-of-concept traffic only.

Do not commit `.env` files, local settings modules, OAuth tokens, API secrets,
SQLite databases, session data, playlist data from real users, or captured
Twitter/Beats/Spotify responses. Run `make lint`, `make test`, `make build`,
`make verify`, and `make check` before changing settings, authentication, or
credential handling.

Keep state-changing tweet, favorite, playlist, and playback actions on POST
paths with CSRF protection.
Keep logout as a CSRF-protected POST logout action so session and social-auth
cleanup are not triggered by a link visit.
Keep post input normalization close to outbound Twitter side effects so blank
status text, non-string post inputs, and malformed favorite IDs do not reach
service clients.
Keep malformed Twitter mention text out of Beats searches, and bound cleaned
search queries before outbound provider calls.
Skip malformed Beats search results before playlist entries are
queued.
Require expected dictionary shapes and nonblank strings for Twitter and Beats
token metadata before API client construction. Malformed Twitter metadata must
preserve configured token fallbacks rather than expose raw key errors.
Accept player preview durations only as bounded nonnegative decimal seconds
before rendering them into JavaScript. Reject signs, exponents, executable
punctuation, overlong values, and durations above one hour.
Render player metadata and timing fields with `textContent` so provider SDK
callback values cannot become executable DOM markup.
Keep OAuth access tokens out of visible player controls. The legacy SDK may
retain its token in memory, but the UI must not display or edit it.
Keep Twitter and Beats view URL patterns as exact-match integration routes so
prefix paths cannot reach those authenticated service views.
Keep `DJANGO_ALLOWED_HOSTS` required outside local debug so production host
validation cannot be omitted accidentally.
Reject wildcard allowed hosts outside local debug so production host validation
stays explicit.

Do not add debug print statements that expose OAuth tokens, mention text, track
search terms, track results, playlist choices, or other user-linked service
data.

## Dependency and Supply Chain Security

Dependency updates should come from trusted package managers and should keep lockfiles in sync when lockfiles exist. Do not commit credentials, private keys, tokens, generated secrets, or machine-local configuration. If a vulnerability depends on a compromised package, typosquatting risk, insecure transitive dependency, or unsafe build step, include the package name, affected version, and the path through which it is used.

## Safe Research Guidelines

Good-faith research is welcome when it stays within these boundaries:

- use only accounts, devices, data, and infrastructure that you own or have explicit permission to test
- avoid destructive actions, persistence, spam, phishing, social engineering, or denial-of-service testing
- minimize access to personal data and stop testing immediately if private data is exposed
- do not exfiltrate secrets or third-party data; report the minimum evidence needed to verify impact
- keep vulnerability details confidential until the maintainer has assessed the report

## Maintainer Response

The maintainer will review complete reports as availability allows, prioritize issues by exploitability and impact, and coordinate a fix or mitigation when the affected code is still maintained. For sample, archived, or educational repositories, the likely remediation may be documentation, dependency updates, or clearly marking unsupported code rather than a production-style patch release.
