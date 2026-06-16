---
title: Text-Only Player Metadata
type: security
status: planned
date: 2026-06-16
---

# Text-Only Player Metadata

## Problem

The authenticated Beats playback page writes provider-controlled track metadata
to `innerHTML`. A malicious or compromised provider response could therefore be
interpreted as markup instead of displayed as text. Timing values use the same
unnecessary HTML sink, widening the surface that future SDK changes could make
unsafe.

## Priority

1. Remove the executable DOM sink from provider-controlled metadata.
2. Keep all player status fields on one explicit text-only rendering contract.
3. Make the dependency-free baseline and mutations reject any regression to
   HTML interpretation.

## Approach

- Replace player title and timing/status `innerHTML` writes with `textContent`.
- Preserve field labels, event handlers, arithmetic, playback sequencing, and
  the existing provider SDK integration.
- Add source-level regressions proving the title field receives `data.display`
  only through `textContent` and that the player template contains no
  `innerHTML` assignment.
- Extend project guidance and completed verification evidence around the
  text-only player metadata boundary.

## Files

- `templates/beats.html`
- `test_views_normalization.py`
- `scripts/check-baseline.py`
- `README.md`
- `SECURITY.md`
- `VISION.md`
- `CHANGES.md`
- `docs/plans/2026-06-16-text-only-player-metadata.md`

## Acceptance Criteria

- Provider-controlled `data.display` is written with `textContent`.
- Every existing player status DOM write uses `textContent`; no `innerHTML`
  assignment remains in `templates/beats.html`.
- Existing labels and values remain unchanged.
- The focused tests, complete Make gates, external-directory gate, template
  syntax/structure checks, and hostile mutations pass.
- Exact diff, generated-artifact, credential, conflict-marker, binary,
  large-file, mode, and whitespace audits pass.

## Risks And Boundaries

- The obsolete Django, Beats, Twitter, and browser dependency graph remains
  intentionally uninstalled and requires a separate modernization plan.
- Live provider authorization, SDK callbacks, playback, and browser rendering
  cannot be exercised in the dependency-free Linux baseline.
- This change prevents HTML interpretation at the identified DOM sinks; it does
  not make provider data trustworthy for other contexts.

## Verification Planned

- Run focused normalization/static tests and all repository Make gates from the
  repository root and an external directory.
- Reject isolated mutations for the title sink, timing sinks, global
  `innerHTML` absence, tests, guidance, and plan completion evidence.
- Run final intended-path, artifact, credential, conflict-marker, binary,
  size, mode, and whitespace audits.
