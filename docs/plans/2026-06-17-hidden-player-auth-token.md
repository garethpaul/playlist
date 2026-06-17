---
title: Hidden Player Authentication Token
type: security
status: planned
date: 2026-06-17
---

# Hidden Player Authentication Token

## Problem

The authenticated Beats player copies its OAuth access token into a visible,
editable text input and reads that field back when a stream is loaded. The SDK
requires the token in browser memory, but exposing it as a UI control makes
accidental shoulder-surfing, screenshots, and user edits unnecessary risks.

## Prioritized Requirements

- P0. Remove the visible access-token input and token-to-control assignment.
- P0. Keep reload behavior using the existing `bam.authentication` object.
- P1. Preserve track selection, playback controls, provider callbacks, and the
  existing text-only metadata boundary.
- P1. Add mutation-sensitive static tests, checker contracts, synchronized
  guidance, and truthful completed verification evidence.

## Implementation Units

### U1. Token UI removal

**File:** `templates/beats.html`

Remove the authentication input and the two JavaScript paths that copy the
token into and back out of that visible control. Leave the initial SDK
authentication object unchanged.

### U2. Regression contracts

**Files:** `test_views_normalization.py`, `scripts/check-baseline.py`

Require the initial token assignment while rejecting the access-token control,
its visible assignment, and reads from that control. Protect the contract with
isolated hostile mutations.

### U3. Guidance and evidence

**Files:** `README.md`, `SECURITY.md`, `VISION.md`, `CHANGES.md`, this plan

Document the no-visible-token boundary and record actual bounded validation.

## Validation

- Run focused tests, every Make alias, and the absolute Makefile gate from an
  external working directory.
- Reject isolated mutations of the visible token control, token assignment,
  token readback, regression, guidance, and completed plan status.
- Audit the exact diff, artifacts, credentials, conflict markers, file modes,
  binaries, large files, and whitespace before committing.

## Scope Boundaries

- Do not replace or modernize the obsolete Beats SDK or provider integration.
- Do not change token acquisition, session storage, routes, playback controls,
  or provider callback behavior.
- Do not claim live provider authorization or browser playback coverage from
  dependency-free Linux validation.
- Do not merge or close any stacked pull request.

## Risks

- The provider token remains present in JavaScript memory because the legacy
  client-side SDK requires it; this change removes only unnecessary UI exposure.
- Live provider behavior remains dependent on an obsolete external service.
- This change is stacked on PR #8, which must remain open and merge first.
