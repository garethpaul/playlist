.PHONY: build check lint settings-test static-check test url-test verify

override REPO_ROOT := $(abspath $(dir $(lastword $(MAKEFILE_LIST))))

check: verify

verify: lint test build

lint: static-check

test: settings-test url-test

build: static-check

static-check:
	PYTHONDONTWRITEBYTECODE=1 python3 "$(REPO_ROOT)/scripts/check-baseline.py"

settings-test:
	PYTHONDONTWRITEBYTECODE=1 python3 "$(REPO_ROOT)/test_settings_security.py" -v
	PYTHONDONTWRITEBYTECODE=1 python3 "$(REPO_ROOT)/test_views_normalization.py" -v

url-test:
	PYTHONDONTWRITEBYTECODE=1 python3 "$(REPO_ROOT)/test_url_patterns.py" -v
