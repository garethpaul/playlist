---
title: Local Repository Metadata Ignore
date: 2026-06-25
type: implementation-plan
status: completed
---

# Local Repository Metadata Ignore

## Summary

Keep `.explore/` maintainer intelligence out of fresh-checkout status and the
tracked legacy Django source set.

## Problem Frame

This clone hid `.explore/` only through `.git/info/exclude`. That private file
does not protect contributors or CI. The baseline also used raw substring
checks, which did not prove an ignore rule was active, effective after ordered
negations, or separate from tracked index state.

## Requirements

- R1. Add the exact active `.explore/` repository ignore rule.
- R2. Preserve exact active cache, environment, database, and log rules.
- R3. Validate `.explore/` and a representative file with pinned
  `/usr/bin/git check-ignore`.
- R4. Reject every tracked `.explore` path using `git ls-files`.
- R5. Preserve settings, routes, providers, templates, tests, and package data.

## Work Completed

- Added the repository-owned `.explore/` rule.
- Replaced raw ignore substring checks with active-pattern checks.
- Added effective Git behavior and tracked-index contracts.
- Added repository guidance and this required completed plan.

## Verification Completed

- The red-first baseline rejected the absent active `.explore/` rule.
- The focused baseline, 9 settings tests, and 2 URL tests passed.
- Root and external `make check` each passed 29 dependency-free tests plus 81
  executable Make target/override cases.
- Isolated Python compilation, generated-bytecode, and `git diff --check`
  gates passed.

## Merge Gates

- Exact-head Codex review reported no actionable findings.
- Duplicate hosted Python 3.10/3.12 lanes and CodeQL passed on PR #13.
