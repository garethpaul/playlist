# AGENTS.md

## Repository purpose

`garethpaul/playlist` is a legacy Django social/music integration sample for connecting Twitter authentication, Beats, and Spotify-era playlist flows.

## Project structure

- `Makefile` - repository verification targets
- `scripts` - baseline checks and helper scripts
- `docs` - plans, notes, and generated README assets
- `app` - application source or app module
- `templates` - server-rendered templates
- `manage.py` - Django management entry point
- `requirements.txt` - Python runtime dependencies

## Development commands

- Install dependencies: `python3 -m pip install -r requirements.txt`
- Full baseline: `make check`
- Combined verification: `make verify`
- Lint/static checks: `make lint`
- Tests: `make test`
- Build: `make build`
- Make root regression tests: `make root-test`
- If a command above skips because a platform toolchain is missing, verify on a machine with that SDK before claiming platform behavior is tested.

## Coding conventions

- Language mix noted in the README: Python (11).
- Django commands should run through `python3 manage.py ...` with environment variables set locally.
- Prefer dependency-free tests or stdlib checks when legacy packages are unavailable.

## Testing guidance

- Test-related files detected: `home/tests.py`, `test_settings_security.py`, `test_url_patterns.py`, `test_views_normalization.py`
- Start with the narrowest relevant test or Make target, then run `make check` before handing off if the change is not documentation-only.
- Keep README verification notes in sync when commands, fixtures, or supported toolchains change.

## PR / change guidance

- Keep diffs focused on the requested repository and avoid unrelated modernization or formatting churn.
- Preserve public APIs, sample behavior, file formats, and documented environment variables unless the task explicitly changes them.
- Update tests, README notes, or docs/plans when behavior, security posture, or validation commands change.
- Call out skipped platform validation, legacy toolchain assumptions, and any risky files touched in the final summary.

## Safety and gotchas

- Detected references to Twitter. Keep API keys, OAuth credentials, tokens, and account-specific values in local configuration only.
- Required outside local debug: `DJANGO_SECRET_KEY`.
- Blank `DJANGO_SECRET_KEY` values are rejected outside local debug mode.
- Production `DJANGO_SECRET_KEY` values must be at least 32 characters after trimming.
- `DJANGO_ALLOWED_HOSTS` is required outside local debug mode.
- `DJANGO_ALLOWED_HOSTS=*` wildcard allowed hosts are rejected outside local debug.
- Optional runtime controls: `DJANGO_DEBUG`, `DJANGO_ALLOWED_HOSTS`.
- `.explore/` is local maintainer intelligence; keep it ignored and move durable
  decisions into tracked plans, changes, policies, tests, or source.
- `SOCIAL_AUTH_LOGIN_ERROR_URL` must remain the registered root login path;
  do not restore the unregistered `/login-error/` target.
- The playlist template must use the provider's HTTPS avatar field and HTTPS,
  opener-isolated Twitter links; do not restore third-party service-label art.

## Agent workflow

1. Inspect the README, Makefile, manifests, and the files directly related to the request.
2. Make the smallest source or docs change that satisfies the task; avoid generated, vendored, or local-environment files unless required.
3. Run the narrowest useful validation first, then `make check` or the documented package/platform gate when available.
4. If a required SDK, service credential, or external runtime is unavailable, record the skipped command and why.
5. Summarize changed files, commands run, and remaining risks or follow-up validation.
