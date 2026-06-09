.PHONY: build check lint settings-test static-check test verify

check: verify

verify: lint test build

lint: static-check

test: settings-test

build: static-check

static-check:
	python3 scripts/check-baseline.py

settings-test:
	python3 test_settings_security.py -v
