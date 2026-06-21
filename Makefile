.PHONY: build check lint root-test settings-test static-check test url-test verify

override SHELL := /bin/sh
override .SHELLFLAGS := -c
ifneq ($(strip $(MAKEFILES)),)
$(error MAKEFILES must not be set)
endif
override MAKEFILES :=
ifneq ($(origin MAKEFILE_LIST),file)
$(error MAKEFILE_LIST must not be overridden)
endif
override REPO_ROOT := $(shell MAKEFILE_LIST_RAW='$(subst ','"'"',$(MAKEFILE_LIST))' python3 -c "import os, shlex; raw = os.environ['MAKEFILE_LIST_RAW']; candidates = [raw] + [raw[index + 1:] for index, char in enumerate(raw) if char == ' ']; path = next((candidate for candidate in candidates if (candidate == 'Makefile' or candidate.endswith('/Makefile')) and os.path.isfile(os.path.abspath(candidate))), None); assert path is not None, 'trusted Makefile path not found'; print(shlex.quote(os.path.dirname(os.path.realpath(path))))")
override PYTHON := python3
build check lint root-test settings-test static-check test url-test verify: override REPO_ROOT := $(REPO_ROOT)
build check lint root-test settings-test static-check test url-test verify: override PYTHON := $(PYTHON)

check: verify

verify: lint test build root-test

lint: static-check

test: settings-test url-test

build: static-check

root-test:
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) $(REPO_ROOT)/scripts/test-makefile-root.py

static-check:
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) $(REPO_ROOT)/scripts/check-baseline.py

settings-test:
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) $(REPO_ROOT)/test_settings_security.py -v
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) $(REPO_ROOT)/test_views_normalization.py -v

url-test:
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) $(REPO_ROOT)/test_url_patterns.py -v
