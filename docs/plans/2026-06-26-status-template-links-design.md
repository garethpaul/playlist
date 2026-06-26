# Status Template Link Security Design

## Evidence

- The registered `/twttr` route renders `templates/twitter.html`.
- Both `twitter.html` and the tracked legacy `spotify.html` duplicate a
  plaintext `http://twitter.com/.../status/...` link with `target="_target"`
  and no opener isolation.
- The recently hardened playlist template establishes the repository pattern:
  HTTPS Twitter links, `target="_blank"`, and `rel="noopener noreferrer"`.
- No provider SDK or runtime dependency is needed to validate template source.

## Options

1. Harden only `twitter.html`. This fixes the active route but leaves an unsafe
   tracked duplicate ready to regress if the legacy template is restored.
2. **Harden both duplicate status templates (recommended).** Small, consistent,
   and removes the full bug class without changing provider behavior.
3. Delete `spotify.html`. Its ownership and historical purpose are not clear
   enough to justify removal in this focused security patch.

## Decision

Preserve the URL path interpolation and displayed status ID. Change both links
to `https://twitter.com`, open them in a real new browsing context, and isolate
the opener with `noopener noreferrer`.

## Validation

- Add a dependency-free test covering both tracked templates.
- Add static contracts for exact link shape and completed plan evidence.
- Run root/external `make check`, Python compilation, diff hygiene, and secret
  scans before exact-head review and hosted merge gates.
