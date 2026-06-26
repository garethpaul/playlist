# Playlist Selection Helper

Status: completed

## Context

The Beats view builds up to five valid tweet/track pairs and contains the
current-track ordering decision inline with provider calls. The repository
roadmap calls for focused playlist-selection tests, but that decision cannot be
tested independently today.

## Goals

- Extract the current-track ordering decision into a dependency-free helper.
- Preserve provider result order when no requested track matches.
- Move the requested track to the front without mutating the collected list.
- Normalize request-controlled track identifiers before comparison.
- Cover empty, unmatched, matched, and non-string inputs.

## Work Completed

- Added `select_playlist_track` as the dependency-free ordering boundary.
- Preserved collected provider order when no requested track matches.
- Promoted the first normalized requested match in a copied list.
- Replaced the inline Beats-view branch with the tested helper.
- Added focused helper and integration tests plus static documentation contracts.

## Verification Completed

- `python3 test_views_normalization.py -v` passed all 22 dependency-free view tests.
- `make lint`, `make test`, `make build`, `make verify`, and
  `make check` passed; the complete test gate ran 33 dependency-free tests.
- Absolute-Makefile `make check` passed from an external working directory.
- Eight focused hostile mutations were rejected across helper delegation,
  copied-list behavior, normalized selection, stable ordering, tests, vision,
  changelog, and completed-plan evidence.
- The isolated Python bytecode scan compiled every tracked Python source, then
  confirmed cleanup left no `__pycache__`, `.pyc`, or `.pyo` output.
- `git diff --check` passed.
