# [P2] Disable debug mode for deployed web applications

## Severity

P2 - security/reliability

## Evidence

- `app/settings.py:23`: `DEBUG = True`
- `app/settings.py:25`: `TEMPLATE_DEBUG = True`

## Problem

Debug mode is enabled in application startup code. In deployed web apps, debug mode can expose detailed stack traces, configuration details, or development-only behavior to users when an error occurs.

## Suggested fix

Default debug mode to false, enable it only through an explicit local development setting, and keep deployed WSGI or Flask entry points in production mode.

## Review metadata

- Repository: `garethpaul/playlist`
- Reviewed commit: `27ffc6be3079151d20a7dc75f991587f5e483dff`
- Labels: `bug`, `codex-review`, `severity:P2`
- Codex review fingerprint: `0de2f07d35e177f3`
