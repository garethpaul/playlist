# Preview Seconds Validation

status: completed

## Summary

Validate the request-controlled Beats preview duration before it reaches the
template's JavaScript numeric expression. Preserve the existing preview flow
for bounded decimal seconds while rejecting malformed or executable text.

## Problem Frame

The `/beats` view currently forwards `preview` directly from POST or GET data
into `templates/beats.html`. The template renders that value both into a hidden
field and as an unquoted JavaScript comparison operand. Django HTML escaping is
not a JavaScript numeric validator, so punctuation-only payloads can alter the
script without requiring quotes.

## Requirements

- **R1:** Accept preview durations only as trimmed nonnegative decimal-second
  strings.
- **R2:** Reject signs, exponent notation, non-string values, overlong numeric
  text, non-finite values, and durations above one hour.
- **R3:** Preserve POST precedence over GET and preserve the existing hidden
  field and elapsed-time behavior for valid preview values.
- **R4:** Ensure rejected values are absent from the render context rather than
  interpolated into JavaScript.
- **R5:** Add dependency-free behavioral tests, mutation-sensitive static
  contracts, and completed verification evidence.

## Key Technical Decisions

- Keep validation in a pure helper beside the existing POST and track-search
  normalizers so it remains testable without installing the obsolete Django
  dependency graph.
- Use a strict decimal grammar and the standard-library decimal type for the
  range check. Do not coerce arbitrary Python values or accept exponent syntax.
- Return the trimmed validated string so the existing template emits a numeric
  literal without changing its playback control flow.
- Cap accepted preview durations at 3,600 seconds and bound input length before
  numeric parsing.

## Scope Boundaries

### In Scope

- Preview request normalization and view wiring.
- Dependency-free helper and view-source regression coverage.
- Static checker, README, security, vision, changelog, and completed-plan
  evidence.

### Deferred to Follow-Up Work

- Installing or modernizing the historical Django, Twitter, Beats, Spotify,
  database, or deployment dependency graph.
- Rewriting the inline player JavaScript or changing preview UX semantics.
- Exercising live provider credentials, network calls, browser playback, or
  service-backed authentication.

## Implementation Units

### U1. Validate Preview Durations

**Goal:** Prevent request-controlled script expressions while retaining valid
bounded preview durations.

**Requirements:** R1, R2, R3, R4

**Dependencies:** None

**Files:** `home/views.py`, `test_views_normalization.py`

**Approach:** Add a pure preview-seconds normalizer with strict shape, grammar,
length, finiteness, and range checks. Route the current POST-first/GET-fallback
request value through it before constructing the render context.

**Execution note:** Add malformed and valid characterization cases before
changing the live view assignment.

**Patterns to follow:** `clean_post_text`, `clean_tweet_id`,
`clean_track_search`, and the dependency-free import stubs in
`test_views_normalization.py`.

**Test scenarios:**

- Accept trimmed integer and decimal values at zero and the one-hour boundary.
- Reject JavaScript punctuation, signs, exponent notation, blank text,
  non-string values, overlong numeric text, and values above one hour.
- Verify the `/beats` source routes the POST-first/GET-fallback value through
  the helper and does not retain the direct context assignment.

**Verification:** Valid values remain numeric strings and every malformed value
returns `None`; the complete dependency-free test suite remains green.

### U2. Enforce the Security Contract

**Goal:** Make the preview boundary resistant to accidental regression.

**Requirements:** R5

**Dependencies:** U1

**Files:** `scripts/check-baseline.py`, `README.md`, `SECURITY.md`, `VISION.md`,
`CHANGES.md`, `docs/plans/2026-06-15-preview-seconds-validation.md`

**Approach:** Extend the static checker with source, test, guidance, and plan
contracts that reject direct request-to-template wiring, weakened grammar or
range checks, missing malicious fixtures, and incomplete plan evidence.

**Test scenarios:**

- The checker rejects removal or weakening of the helper and live view wiring.
- The checker rejects removal of malicious punctuation and range-boundary
  fixtures.
- The checker rejects missing guidance or an unfinished plan status.

**Verification:** Root and external Make gates pass, isolated hostile mutations
fail, and the exact intended diff passes artifact, credential, whitespace,
mode, and large-file audits.

## Risks And Dependencies

- Existing callers using negative, exponent-form, or greater-than-one-hour
  preview values will now receive the normal non-preview behavior.
- The historical dependency graph remains intentionally uninstalled; tests
  validate pure normalization and source wiring rather than live Django
  rendering or Beats playback.
- This change must remain stacked on PR #6 and follow base-first merge order.

## Work Completed

- Added strict preview-second normalization for trimmed nonnegative decimal
  strings with input-length and one-hour bounds.
- Routed the existing POST-first/GET-fallback preview value through the helper
  before it enters the render context.
- Added dependency-free valid, boundary, malformed, executable-punctuation,
  and source-wiring regressions plus synchronized guidance and static contracts.

## Verification Completed

- `python3 test_views_normalization.py -v` passed all focused normalization
  cases, and the complete dependency-free suites passed 21 tests.
- `make lint`, `make test`, `make build`, `make verify`, and `make check` passed.
- The complete gate passed from an external working directory through the
  absolute Makefile path.
- The workflow YAML and README SVG parsed successfully.
- Browser execution was not available because `agent-browser` and the legacy
  Django/social/provider runtime are absent; template source and render-context
  wiring were covered by dependency-free tests and static contracts instead.
- Six isolated hostile mutations were rejected for direct request wiring,
  weakened grammar, a raised range cap, removed executable punctuation
  coverage, missing guidance, and reopened plan status.
- `git diff --check` and artifact, credential, and generated-bytecode audits
  passed for the exact intended paths.
