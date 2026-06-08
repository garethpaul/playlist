.PHONY: check static-check settings-test

check: static-check settings-test

static-check:
	python3 scripts/check-baseline.py

settings-test:
	python3 test_settings_security.py -v
