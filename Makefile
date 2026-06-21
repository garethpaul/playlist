.PHONY: build check lint root-test settings-test static-check test url-test verify

ifneq ($(origin MAKEFILE_LIST),file)
$(error MAKEFILE_LIST must not be overridden)
endif
override REPO_ROOT := $(shell path='$(subst ','"'"',$(MAKEFILE_LIST))'; path=$$(printf '%s' "$$path" | /usr/bin/sed 's/^ //'); directory=$$(/usr/bin/dirname -- "$$path"); CDPATH= cd -- "$$directory" && /bin/pwd -P)

check: verify

verify: lint test build root-test

lint: static-check

test: settings-test url-test

build: static-check

root-test:
	PYTHONDONTWRITEBYTECODE=1 python3 "$(REPO_ROOT)/scripts/test-makefile-root.py"

static-check:
	PYTHONDONTWRITEBYTECODE=1 python3 "$(REPO_ROOT)/scripts/check-baseline.py"

settings-test:
	PYTHONDONTWRITEBYTECODE=1 python3 "$(REPO_ROOT)/test_settings_security.py" -v
	PYTHONDONTWRITEBYTECODE=1 python3 "$(REPO_ROOT)/test_views_normalization.py" -v

url-test:
	PYTHONDONTWRITEBYTECODE=1 python3 "$(REPO_ROOT)/test_url_patterns.py" -v
