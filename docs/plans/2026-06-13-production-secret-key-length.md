# Production secret key length

status: planned

## Context

Production settings reject a missing or blank `DJANGO_SECRET_KEY`, but accept
trivially short values. Django uses this secret for cryptographic signing, so a
weak configured value can undermine signed data even though no key is checked
into source control.

## Requirements

- Require at least 32 characters after trimming a production
  `DJANGO_SECRET_KEY`.
- Preserve the explicit debug-only development fallback and existing
  environment-only credential handling.
- Add standard-library tests, mutation-sensitive static contracts,
  documentation, and completed verification.
- Do not install or modernize the obsolete Django/social dependency graph or
  make live service calls.

## Verification

- Run focused settings tests, every Make gate, checker compilation, hostile
  mutations, diff checks, artifact scans, and secret scans.
