.PHONY: build check lint settings-test static-check test url-test verify

check: verify

verify: lint test build

lint: static-check

test: settings-test url-test

build: static-check

static-check:
	PYTHONDONTWRITEBYTECODE=1 python3 scripts/check-baseline.py

settings-test:
	PYTHONDONTWRITEBYTECODE=1 python3 test_settings_security.py -v
	PYTHONDONTWRITEBYTECODE=1 python3 test_views_normalization.py -v

url-test:
	PYTHONDONTWRITEBYTECODE=1 python3 test_url_patterns.py -v
