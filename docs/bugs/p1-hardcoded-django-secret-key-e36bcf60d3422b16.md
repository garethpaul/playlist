# [P1] Move Django SECRET_KEY out of source control

## Severity

P1 - security/session-integrity

## Evidence

- `app/settings.py:20`: `SECRET_KEY = ')e-_u9#$xfu5(uw!izbq!yu+dtf1*ce5@7w42p^ro*i-+)$yy%'`

## Problem

The Django `SECRET_KEY` is committed as a literal value. Anyone with the repository can reuse the signing key, which can invalidate assumptions around signed cookies, password reset tokens, and other cryptographic signatures if this key is used in a deployed environment.

## Suggested fix

Read `SECRET_KEY` from an environment variable or deployment secret store, provide a safe development default only outside production, and rotate the deployed key after removing the committed value.

## Review metadata

- Repository: `garethpaul/playlist`
- Reviewed commit: `bba33fc8384f0741746d5ee709718337544c663b`
- Labels: `bug`, `codex-review`, `severity:P1`
- Codex review fingerprint: `e36bcf60d3422b16`
