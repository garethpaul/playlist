# Status Template Link Security Implementation Plan

Status: Completed

> **For Claude:** REQUIRED SUB-SKILL: Use executing-plans to implement this plan task-by-task.

**Goal:** Make every tracked Twitter status link use HTTPS and opener isolation without changing the rendered status content.

**Architecture:** Keep the templates and Django view flow intact. Enforce one exact safe anchor contract in both `twitter.html` and the dormant duplicate `spotify.html` through dependency-free source tests and the repository baseline checker.

**Tech Stack:** Django templates, Python stdlib `unittest`, repository static checker, GNU Make.

---

### Task 1: Prove the unsafe duplicate links

**Files:**
- Modify: `test_views_normalization.py`

**Step 1: Write the failing test**

Add both template paths and assert each contains the exact HTTPS, `_blank`,
`noopener noreferrer` status anchor while rejecting plaintext Twitter URLs and
the custom `_target` browsing context.

**Step 2: Run test to verify it fails**

Run: `PYTHONDONTWRITEBYTECODE=1 python3 test_views_normalization.py -v`

Expected: FAIL against the existing plaintext links.

### Task 2: Apply the minimal template correction

**Files:**
- Modify: `templates/twitter.html`
- Modify: `templates/spotify.html`

**Step 1: Replace only link attributes**

Use `https://twitter.com`, `target="_blank"`, and
`rel="noopener noreferrer"` while preserving interpolations and visible text.

**Step 2: Run the focused test**

Run: `PYTHONDONTWRITEBYTECODE=1 python3 test_views_normalization.py -v`

Expected: all view/template tests pass.

### Task 3: Preserve contracts and maintenance evidence

**Files:**
- Modify: `scripts/check-baseline.py`
- Modify: `README.md`
- Modify: `SECURITY.md`
- Modify: `VISION.md`
- Modify: `CHANGES.md`
- Modify: `docs/plans/2026-06-26-status-template-links.md`

**Step 1: Add static and documentation contracts**

Require both exact anchors, the focused test name, completed plan, and current
security guidance.

**Step 2: Run full validation**

Run root and external-directory `/usr/bin/make check`, isolated Python
compilation, `git diff --check`, current-tree gitleaks, and history scanning.

Expected: all gates pass or any pre-existing history-only finding is recorded.

### Task 4: Review and merge the exact head

**Files:**
- No additional source files.

Commit and push the focused branch, open a PR, invoke Codex branch review, wait
for hosted Python and CodeQL checks, verify local/remote/PR SHA equality, and
merge only that exact green head.

## Work Completed

- Updated `twitter.html` and `spotify.html` to the exact reviewed HTTPS status
  link with `_blank` and `noopener noreferrer`.
- Added one dependency-free test covering both tracked copies.
- Added baseline, documentation, plan, and changelog contracts.

## Verification Completed

- RED: the focused test failed independently for both plaintext status links.
- GREEN: all 24 dependency-free view tests passed after the two attribute-only
  template changes.
- Root and external-directory `make check` each passed the complete 35-test
  dependency-free suite and all 81 executable Make authority cases.
- Isolated Python compilation, `git diff --check`, current-tree gitleaks, and
  the 70-commit history scan passed with no leaks.
- The first final baseline rerun rejected bytecode left by the explicit
  compilation probe. An attempted `make clean` confirmed that the repository
  has no clean target, so the generated `.pyc` files and `__pycache__`
  directories were removed explicitly before the baseline passed.
- Hosted Python and CodeQL checks remain exact-head merge gates.
