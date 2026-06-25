#!/usr/bin/env python3
"""Static baseline checks for the legacy playlist Django sample."""

import ast
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

REQUIRED_FILES = [
    ".github/workflows/check.yml",
    ".gitignore",
    "CHANGES.md",
    "Makefile",
    "README.md",
    "SECURITY.md",
    "VISION.md",
    "app/settings.py",
    "app/urls.py",
    "app/wsgi.py",
    "docs/bugs/p1-hardcoded-django-secret-key-e36bcf60d3422b16.md",
    "docs/bugs/p2-production-debug-mode-0de2f07d35e177f3.md",
    "docs/plans/2026-06-08-playlist-baseline.md",
    "docs/plans/2026-06-09-remove-playlist-debug-print.md",
    "docs/plans/2026-06-09-blank-secret-key.md",
    "docs/plans/2026-06-09-post-input-normalization.md",
    "docs/plans/2026-06-09-required-allowed-hosts.md",
    "docs/plans/2026-06-09-post-only-logout.md",
    "docs/plans/2026-06-09-make-gate-aliases.md",
    "docs/plans/2026-06-09-wildcard-allowed-hosts.md",
    "docs/plans/2026-06-09-non-string-post-inputs.md",
    "docs/plans/2026-06-09-exact-integration-routes.md",
    "docs/plans/2026-06-10-ci-baseline.md",
    "docs/plans/2026-06-10-malformed-beats-results.md",
    "docs/plans/2026-06-10-malformed-twitter-mentions.md",
    "docs/plans/2026-06-10-hosted-security-validation.md",
    "docs/plans/2026-06-13-production-secret-key-length.md",
    "docs/plans/2026-06-13-auth-state-routing.md",
    "docs/plans/2026-06-13-social-token-metadata-normalization.md",
    "docs/plans/2026-06-14-location-independent-make-gates.md",
    "docs/plans/2026-06-15-preview-seconds-validation.md",
    "docs/plans/2026-06-16-text-only-player-metadata.md",
    "docs/plans/2026-06-17-hidden-player-auth-token.md",
    "docs/plans/2026-06-21-safe-make-root.md",
    "docs/readme-overview.svg",
    "fabfile.py",
    "home/views.py",
    "manage.py",
    "requirements.txt",
    "scripts/test-makefile-root.py",
    "templates/beats.html",
    "templates/twitter.html",
    "test_settings_security.py",
    "test_views_normalization.py",
    "test_url_patterns.py",
]

PYTHON_FILES = [
    "app/settings.py",
    "app/urls.py",
    "app/wsgi.py",
    "fabfile.py",
    "home/admin.py",
    "home/models.py",
    "home/tests.py",
    "home/views.py",
    "manage.py",
    "scripts/check-baseline.py",
    "scripts/test-makefile-root.py",
    "test_settings_security.py",
    "test_views_normalization.py",
    "test_url_patterns.py",
]

FORBIDDEN_SETTINGS_SNIPPETS = [
    ")e-_u9#$xfu5(uw!izbq!yu+dtf1*ce5@7w42p^ro*i-+)$yy%",
    "DEBUG = True",
    "TEMPLATE_DEBUG = True",
    "YOUR_TWITTER_API_KEY",
    "YOUR_TWITTER_API_SECRET",
    "YOUR_TWITTER_ACCESS_TOKEN",
    "YOUR_TWITTER_ACCESS_TOKEN_SECRET",
    "YOUR_BEATS_ACCESS_TOKEN",
    "YOUR_BEATS_ACCESS_TOKEN_SECRET",
    "YOUR_SPOTIFY_ACCESS_TOKEN",
    "YOUR_SPOTIFY_ACCESS_TOKEN_SECRET",
]


def fail(message):
    print("check-baseline: %s" % message, file=sys.stderr)
    return False


def read(path):
    return (ROOT / path).read_text(encoding="utf-8")


def markdown_section(text, heading):
    match = re.search(
        rf"(?ms)^## {re.escape(heading)}\s*$\n(.*?)(?=^## |\Z)",
        text,
    )
    return match.group(1).strip() if match else ""


def require(condition, message, errors):
    if not condition:
        errors.append(message)


def main():
    errors = []

    for path in REQUIRED_FILES:
        require((ROOT / path).exists(), "missing required file: %s" % path, errors)

    for path in PYTHON_FILES:
        source = read(path)
        try:
            ast.parse(source, filename=path)
        except SyntaxError as exc:
            errors.append("%s is not Python 3 parseable: %s" % (path, exc))

    makefile = read("Makefile")
    for snippet in [
        "override SHELL := /bin/sh",
        "override .SHELLFLAGS := -c",
        "ifneq ($(strip $(MAKEFILES)),)",
        "$(error MAKEFILES must not be set)",
        "override MAKEFILES :=",
        "ifneq ($(origin MAKEFILE_LIST),file)",
        "$(error MAKEFILE_LIST must not be overridden)",
        "override REPO_ROOT := $(shell MAKEFILE_LIST_RAW=",
        "trusted Makefile path not found",
        "shlex.quote(os.path.dirname(os.path.realpath(path)))",
        "override PYTHON := python3",
        "verify: override REPO_ROOT := $(REPO_ROOT)",
        "verify: override PYTHON := $(PYTHON)",
        "check: verify",
        "verify: lint test build root-test",
        "lint: static-check",
        "test: settings-test url-test",
        "build: static-check",
        "root-test:",
        "PYTHONDONTWRITEBYTECODE=1 $(PYTHON) $(REPO_ROOT)/scripts/test-makefile-root.py",
        "PYTHONDONTWRITEBYTECODE=1 $(PYTHON) $(REPO_ROOT)/scripts/check-baseline.py",
        "PYTHONDONTWRITEBYTECODE=1 $(PYTHON) $(REPO_ROOT)/test_settings_security.py -v",
        "PYTHONDONTWRITEBYTECODE=1 $(PYTHON) $(REPO_ROOT)/test_views_normalization.py -v",
        "PYTHONDONTWRITEBYTECODE=1 $(PYTHON) $(REPO_ROOT)/test_url_patterns.py -v",
    ]:
        require(snippet in makefile, "Makefile missing guardrail: %s" % snippet, errors)

    root_test = read("scripts/test-makefile-root.py")
    for snippet in [
        "TARGETS = (",
        '"command ROOT override"',
        '"environment ROOT override"',
        '"command SHELL override"',
        '"environment SHELL override"',
        '"command shell flags override"',
        '"environment shell flags override"',
        '"command PYTHON override"',
        '"environment PYTHON override"',
        '"command MAKEFILE_LIST override"',
        '"environment MAKEFILE_LIST override"',
        '"command MAKEFILES override"',
        '"environment MAKEFILES override"',
        '"earlier explicit Makefile"',
        "caller-controlled shell or Python executed",
        "backticks in the checkout path executed",
        "MAKEFILE_LIST must not be overridden",
        "MAKEFILES must not be set",
        "81 executable target/override cases",
    ]:
        require(
            snippet in root_test,
            "Makefile root regression test missing: %s" % snippet,
            errors,
        )

    workflow = read(".github/workflows/check.yml")
    actions = re.findall(r"(?m)^\s*(?:-\s*)?uses:\s*(\S+)(?:\s+#.*)?$", workflow)
    checkout_step = re.search(
        r"(?m)^      - name: Check out repository\n"
        r"        uses: actions/checkout@df4cb1c069e1874edd31b4311f1884172cec0e10 # v6\.0\.3\n"
        r"        with:\n"
        r"          persist-credentials: false\n",
        workflow,
    )
    require(
        checkout_step is not None
        and actions == [
            "actions/checkout@df4cb1c069e1874edd31b4311f1884172cec0e10",
            "actions/setup-python@a309ff8b426b58ec0e2a45f0f869d46889d02405",
        ]
        and workflow.count("persist-credentials:") == 1
        and workflow.count("permissions:") == 1
        and re.search(r"(?m)^\s+[A-Za-z-]+:\s+write\s*$", workflow) is None
        and "permissions:\n  contents: read" in workflow
        and "cancel-in-progress: true" in workflow
        and "runs-on: ubuntu-24.04" in workflow
        and "timeout-minutes: 10" in workflow
        and 'python-version: ["3.10", "3.12"]' in workflow
        and 'PYTHONDONTWRITEBYTECODE: "1"' in workflow
        and "run: make check" in workflow,
        "Check workflow must stay singular, pinned, credential-free, read-only, matrixed, and bounded",
        errors,
    )

    bytecode_paths = sorted(
        str(path.relative_to(ROOT))
        for pattern in ("__pycache__", "*.pyc")
        for path in ROOT.rglob(pattern)
    )
    require(
        not bytecode_paths,
        "generated Python bytecode must not remain after gates: %s" % ", ".join(bytecode_paths[:5]),
        errors,
    )
    urls = read("app/urls.py")
    for snippet in [
        "url(r'^$', 'home.views.login', name='login')",
        "url(r'^twttr$', 'home.views.twttr', name='twttr')",
        "url(r'^beats$', 'home.views.beats', name='beats')",
    ]:
        require(snippet in urls, "urls missing exact route: %s" % snippet, errors)
    for snippet in [
        "url(r'^twttr', 'home.views.twttr', name='twttr')",
        "url(r'^beats', 'home.views.beats', name='beats')",
    ]:
        require(snippet not in urls, "urls still contains prefix route: %s" % snippet, errors)

    settings = read("app/settings.py")
    for snippet in FORBIDDEN_SETTINGS_SNIPPETS:
        require(snippet not in settings, "forbidden settings snippet remains: %s" % snippet, errors)

    for snippet in [
        "def env_bool(",
        "def env_list(",
        "DEBUG = env_bool('DJANGO_DEBUG', False)",
        "MIN_SECRET_KEY_LENGTH = 32",
        "SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')",
        "SECRET_KEY = SECRET_KEY.strip()",
        "if not DEBUG and len(SECRET_KEY) < MIN_SECRET_KEY_LENGTH:",
        "DJANGO_SECRET_KEY must be at least 32 characters",
        "raise RuntimeError(",
        "TEMPLATE_DEBUG = DEBUG",
        "SESSION_COOKIE_SECURE = not DEBUG",
        "CSRF_COOKIE_SECURE = not DEBUG",
        "ALLOWED_HOSTS = env_list(",
        "DJANGO_ALLOWED_HOSTS",
        "if not DEBUG and not ALLOWED_HOSTS:",
        "if not DEBUG and '*' in ALLOWED_HOSTS:",
        "DJANGO_SQLITE_PATH",
        "SOCIAL_AUTH_LOGIN_ERROR_URL    = '/'",
    ]:
        require(snippet in settings, "settings missing guardrail: %s" % snippet, errors)
    require(
        "/login-error/" not in settings,
        "social-auth failures must not target an unregistered login-error route",
        errors,
    )

    for name in [
        "SOCIAL_AUTH_TWITTER_KEY",
        "SOCIAL_AUTH_TWITTER_SECRET",
        "TWITTER_ACCESS_TOKEN",
        "TWITTER_ACCESS_TOKEN_SECRET",
        "SOCIAL_AUTH_BEATS_KEY",
        "SOCIAL_AUTH_BEATS_SECRET",
        "SOCIAL_AUTH_SPOTIFY_KEY",
        "SOCIAL_AUTH_SPOTIFY_SECRET",
    ]:
        require(
            "%s = os.environ.get('%s', '')" % (name, name) in settings,
            "settings should read %s from the environment" % name,
            errors,
        )

    settings_tests = read("test_settings_security.py")
    for snippet in [
        "test_short_secret_key_rejected_when_debug_disabled",
        '"short-production-secret"',
        '"at least 32 characters"',
        'production_secret = "x" * 32',
        "test_local_debug_does_not_require_secure_transport_cookies",
        "self.assertTrue(settings.SESSION_COOKIE_SECURE)",
        "self.assertTrue(settings.CSRF_COOKIE_SECURE)",
        "test_social_auth_errors_return_to_registered_root_login",
        'self.assertEqual("/", settings.SOCIAL_AUTH_LOGIN_ERROR_URL)',
    ]:
        require(snippet in settings_tests, "settings tests missing: %s" % snippet, errors)

    url_tests = read("test_url_patterns.py")
    for snippet in [
        "test_social_auth_error_target_is_registered_root_login",
        "SOCIAL_AUTH_LOGIN_ERROR_URL    = '/'",
        'self.assertNotIn("/login-error/", settings)',
        "home\\.views\\.login",
    ]:
        require(snippet in url_tests, "URL tests missing auth-error guard: %s" % snippet, errors)

    views = read("home/views.py")
    require("request.REQUEST" not in views, "legacy request.REQUEST access remains", errors)
    for snippet in [
        "def clean_post_text(",
        "if not isinstance(value, str):",
        "def clean_tweet_id(",
        "def clean_preview_seconds(",
        "def first_track_result(",
        "MAX_TRACK_SEARCH_LENGTH = 200",
        "MAX_PREVIEW_SECONDS_LENGTH = 16",
        "MAX_PREVIEW_SECONDS = Decimal('3600')",
        "preview_seconds_re = re.compile(r'^(?:0|[1-9][0-9]*)(?:\\.[0-9]+)?$')",
        "seconds = Decimal(value)",
        "if not seconds.is_finite() or seconds > MAX_PREVIEW_SECONDS:",
        "def clean_track_search(",
        "def has_required_auths(auths):",
        "if not isinstance(auths, dict):",
        'return bool(auths.get("twitter")) and bool(auths.get("beats"))',
        "def twitter_access_tokens(extra_data):",
        "def beats_access_token(extra_data):",
        "if not isinstance(access_token, dict):",
        "token_key = clean_post_text(access_token.get('oauth_token'))",
        "token_secret = clean_post_text(access_token.get('oauth_token_secret'))",
        "if not token_key or not token_secret:",
        "return token_key, token_secret",
        "clean_post_text(extra_data.get('access_token'))",
        "twitter_access_tokens(",
        "beats_access_token(getattr(usa, 'extra_data', None))",
        "if has_required_auths(auths):",
        "if not has_required_auths(auths):",
        "getattr(s, 'favorited', False)",
        "clean_track_search(getattr(s, 'text', None))",
        "if not search:",
        "not isinstance(results, dict)",
        "not isinstance(data, list) or not data",
        "not isinstance(track, dict) or not clean_post_text(track.get('id'))",
        "tweet_id_re = re.compile(r'^[0-9]+$')",
        'status = clean_post_text(request.POST.get("status", None))',
        'fav = clean_tweet_id(request.POST.get("fav", None))',
        'preview = clean_preview_seconds(request.POST.get("preview", request.GET.get("preview", None)))',
        'request.POST.get("track", request.GET.get("track", None))',
        "track = first_track_result(tracks)",
        "from django.views.decorators.http import require_POST",
        "@login_required\n@require_POST\ndef logout(request):",
        "except Exception:",
    ]:
        require(snippet in views, "views missing guardrail: %s" % snippet, errors)
    require("print(search, tracks)" not in views, "playlist debug print must not expose user-linked data", errors)
    require(
        'auths.get("twitter", None) and auths.get("beats", None)' not in views,
        "login must use the shared auth-state predicate",
        errors,
    )
    require(
        'not auths.get("twitter", None) or not auths.get("beats", None)' not in views,
        "beats must use the shared auth-state predicate",
        errors,
    )
    require(
        'if not has_required_auths(auths):\n        return redirect("/")' in views
        and 'return redirect("/login")' not in views,
        "incomplete integration auth must return to the registered login page",
        errors,
    )
    require(
        "usa.extra_data['access_token']" not in views,
        "social token extraction must not directly index extra_data",
        errors,
    )
    require(
        'preview = request.POST.get("preview", request.GET.get("preview", None))'
        not in views,
        "preview request values must not reach the template without normalization",
        errors,
    )

    view_tests = read("test_views_normalization.py")
    for snippet in [
        "test_has_required_auths_accepts_both_integrations",
        "test_has_required_auths_rejects_incomplete_or_malformed_state",
        'views.has_required_auths({"twitter": object(), "beats": object()})',
        "views.has_required_auths(value)",
        '"twitter,beats"',
        "test_twitter_access_tokens_require_complete_nested_string_pair",
        "test_beats_access_token_requires_nonblank_string",
        "views.twitter_access_tokens(value)",
        "views.beats_access_token(value)",
        'self.assertEqual((None, None), views.twitter_access_tokens(value))',
        'self.assertIsNone(views.beats_access_token(value))',
        "test_clean_preview_seconds_accepts_bounded_decimal_strings",
        "test_clean_preview_seconds_rejects_non_numeric_or_unsafe_values",
        "test_beats_view_normalizes_preview_before_rendering",
        "test_player_metadata_and_timing_use_text_only_dom_sinks",
        "test_provider_values_are_escaped_for_javascript_string_literals",
        "test_player_sdk_is_loaded_over_https",
        "test_player_auth_token_is_not_exposed_as_control",
        "test_incomplete_integration_auth_returns_to_registered_login_page",
        'self.assertNotIn(\'id="accessToken"\', template)',
        'self.assertNotIn("accessToken.value", template)',
        'trackName.textContent = "Title:" + data.display;',
        'self.assertNotIn(".innerHTML", template)',
        '"0);alert(1);//"',
        '"3600.1"',
        "views.clean_preview_seconds(value)",
    ]:
        require(snippet in view_tests, "view tests missing auth-state coverage: %s" % snippet, errors)

    beats_template = read("templates/beats.html")
    for snippet in [
        'id="play-next-form"',
        'method="post"',
        "{% csrf_token %}",
        'document.getElementById("play-next-fav").value',
        "form.submit();",
        "window.location.reload();",
        "}, 5000);",
    ]:
        require(snippet in beats_template, "beats template missing POST favorite path: %s" % snippet, errors)
    require('"/beats?fav=' not in beats_template, "favorite action still uses a query string", errors)
    require(
        "access_token: '{{ beats.access_token|escapejs }}'" in beats_template
        and 'id="accessToken"' not in beats_template
        and "accessToken.value" not in beats_template,
        "player authentication token must remain in the SDK object and out of visible controls",
        errors,
    )
    javascript_interpolations = [
        "{{ pair.1.id|escapejs }}",
        "{{ beats_me.result.client_id|escapejs }}",
        "{{ beats.access_token|escapejs }}",
        "{{ beats_me.result.user_context|escapejs }}",
        "{{ track.1.id|escapejs }}",
        "{{ track.0.id|escapejs }}",
    ]
    require(
        all(value in beats_template for value in javascript_interpolations),
        "provider-controlled JavaScript strings must use escapejs",
        errors,
    )
    require(
        'src="https://bam.cdn.beatsmusic.com/bam-1.0.2.min.js"' in beats_template
        and 'src="http://bam.cdn.beatsmusic.com/' not in beats_template,
        "player SDK must load over HTTPS",
        errors,
    )
    text_only_player_assignments = [
        'trackName.textContent = "Title:" + data.display;',
        'timeDuration.textContent = "Duration: " + value;',
        'timeElapsed.textContent = "Elapsed: " + elapsed;',
        'timeRemaining.textContent = "Remaining: " + remaining;',
        'timeBufferedStart.textContent = "Start: " + buffered.start;',
        'timeBufferedEnd.textContent = "End: " + buffered.end;',
        'timeBufferedLength.textContent = "Length: " + buffered.length;',
        'timeSeekableStart.textContent = "Start: " + seekable.start;',
        'timeSeekableEnd.textContent = "End: " + seekable.end;',
        'timeSeekableLength.textContent = "Length: " + seekable.length;',
    ]
    require(
        all(assignment in beats_template for assignment in text_only_player_assignments)
        and beats_template.count(".textContent =") == len(text_only_player_assignments)
        and ".innerHTML" not in beats_template,
        "player metadata and timing must use only the reviewed textContent sinks",
        errors,
    )

    twitter_template = read("templates/twitter.html")
    for snippet in ['action="/twttr"', 'method="post"', "{% csrf_token %}"]:
        require(snippet in twitter_template, "twitter template missing POST status path: %s" % snippet, errors)

    base_template = read("templates/base.html")
    for snippet in ['action="/logout"', 'method="post"', "{% csrf_token %}"]:
        require(snippet in base_template, "base template missing POST logout path: %s" % snippet, errors)
    require('href="/logout"' not in base_template, "logout action still uses a GET link", errors)

    view_tests = read("test_views_normalization.py")
    for snippet in [
        "test_first_track_result_rejects_malformed_beats_results",
        "test_first_track_result_accepts_first_identified_track",
        "test_clean_track_search_rejects_malformed_twitter_mentions",
        "test_clean_track_search_removes_handles_and_bounds_queries",
        "views.MAX_TRACK_SEARCH_LENGTH + 1",
    ]:
        require(snippet in view_tests, "view normalization tests missing: %s" % snippet, errors)

    gitignore = read(".gitignore")
    for snippet in [".env", "__pycache__/", "*.py[cod]", ".pytest_cache/", "db.sqlite3", "*.log"]:
        require(snippet in gitignore, ".gitignore missing: %s" % snippet, errors)

    readme = read("README.md")
    for snippet in [
        "make check",
        "make lint",
        "make test",
        "make build",
        "make verify",
        "DJANGO_SECRET_KEY",
        "DJANGO_DEBUG",
        "DJANGO_ALLOWED_HOSTS",
        "required outside local debug",
        "wildcard allowed hosts",
        "SOCIAL_AUTH_TWITTER_KEY",
        "TWITTER_ACCESS_TOKEN",
        "SOCIAL_AUTH_BEATS_KEY",
        "SOCIAL_AUTH_SPOTIFY_KEY",
        "debug print",
        "python3 test_settings_security.py -v",
        "python3 test_views_normalization.py -v",
        "python3 test_url_patterns.py -v",
        "blank",
        "at least 32 characters",
        "post input normalization",
        "non-string post inputs",
        "malformed Beats search results",
        "malformed Twitter mention text",
        "exact-match integration routes",
        "both Twitter and Beats connections are required",
        "social-auth failures return to the registered root login",
        "Shape-check and trim Twitter and Beats token metadata",
        "Validate preview durations as bounded decimal seconds",
        "provider-controlled player metadata",
        "visible player controls",
        "CSRF-protected POST logout",
        "GitHub Actions",
        "hosted Linux",
        "absolute Makefile path works from another directory",
    ]:
        require(snippet in readme, "README missing: %s" % snippet, errors)
    changes = " ".join(read("CHANGES.md").split())
    require(
        "external absolute-Makefile calls" in changes,
        "CHANGES missing external absolute-Makefile calls",
        errors,
    )
    require(
        "bounded decimal preview seconds" in changes,
        "CHANGES missing bounded preview validation",
        errors,
    )
    require(
        "text-only" in changes and "textContent" in changes,
        "CHANGES missing text-only player metadata hardening",
        errors,
    )
    require(
        "visible player control" in changes and "OAuth access token" in changes,
        "CHANGES missing player token visibility hardening",
        errors,
    )

    security = read("SECURITY.md")
    for snippet in ["DJANGO_SECRET_KEY", "DJANGO_DEBUG", "DJANGO_ALLOWED_HOSTS", "required outside local debug", "wildcard allowed hosts", "OAuth", "debug print", "blank", "at least 32 characters", "post input normalization", "non-string post inputs", "malformed Beats search results", "malformed Twitter mention text", "expected dictionary shapes and nonblank strings", "bounded nonnegative decimal seconds", "player metadata and timing fields with `textContent`", "visible player controls", "exact-match integration routes", "CSRF-protected POST logout", "social-auth failures"]:
        require(snippet in security, "SECURITY missing: %s" % snippet, errors)

    vision = read("VISION.md")
    for snippet in ["environment-based configuration", "POST", "make check", "make lint", "make test", "make build", "make verify", "debug print", "blank", "at least 32 characters", "post input normalization", "non-string post inputs", "malformed Beats search results", "malformed Twitter mention text", "normalized missing-token", "bounded preview seconds", "provider-controlled player metadata on text-only DOM sinks", "OAuth access tokens out of visible player controls", "allowed hosts", "wildcard allowed hosts", "exact-match integration routes", "POST-only logout", "social-auth failures"]:
        require(snippet in vision, "VISION missing: %s" % snippet, errors)

    plan = read("docs/plans/2026-06-08-playlist-baseline.md")
    for snippet in ["Status: Complete", "make check", "DJANGO_SECRET_KEY", "request.REQUEST", "test_settings_security.py", "/twttr"]:
        require(snippet in plan, "plan missing: %s" % snippet, errors)
    debug_plan = read("docs/plans/2026-06-09-remove-playlist-debug-print.md")
    for snippet in ["Status: Complete", "print(search, tracks)", "make check"]:
        require(snippet in debug_plan, "debug print plan missing: %s" % snippet, errors)
    blank_secret_plan = read("docs/plans/2026-06-09-blank-secret-key.md")
    for snippet in ["Status: Complete", "DJANGO_SECRET_KEY", "blank", "make check"]:
        require(snippet in blank_secret_plan, "blank secret plan missing: %s" % snippet, errors)
    post_input_plan = read("docs/plans/2026-06-09-post-input-normalization.md")
    for snippet in ["Status: Complete", "clean_post_text", "clean_tweet_id", "make check"]:
        require(snippet in post_input_plan, "post input plan missing: %s" % snippet, errors)
    allowed_hosts_plan = read("docs/plans/2026-06-09-required-allowed-hosts.md")
    for snippet in ["Status: Complete", "DJANGO_ALLOWED_HOSTS", "test_allowed_hosts_required_when_debug_disabled", "make check"]:
        require(snippet in allowed_hosts_plan, "allowed hosts plan missing: %s" % snippet, errors)
    post_logout_plan = read("docs/plans/2026-06-09-post-only-logout.md")
    for snippet in ["Status: Complete", "logout", "POST", "CSRF", "make check"]:
        require(snippet in post_logout_plan, "post-only logout plan missing: %s" % snippet, errors)
    make_gates_plan = read("docs/plans/2026-06-09-make-gate-aliases.md")
    for snippet in ["Status: Complete", "make lint", "make test", "make build", "make verify"]:
        require(snippet in make_gates_plan, "make gate aliases plan missing: %s" % snippet, errors)
    wildcard_hosts_plan = read("docs/plans/2026-06-09-wildcard-allowed-hosts.md")
    for snippet in ["Status: Complete", "DJANGO_ALLOWED_HOSTS", "wildcard", "make check"]:
        require(snippet in wildcard_hosts_plan, "wildcard allowed hosts plan missing: %s" % snippet, errors)
    non_string_post_plan = read("docs/plans/2026-06-09-non-string-post-inputs.md")
    for snippet in ["Status: Complete", "clean_post_text", "non-string post inputs", "test_views_normalization.py", "make check"]:
        require(snippet in non_string_post_plan, "non-string post input plan missing: %s" % snippet, errors)
    exact_routes_plan = read("docs/plans/2026-06-09-exact-integration-routes.md")
    for snippet in ["Status: Complete", "twttr", "beats", "exact-match", "test_url_patterns.py", "make check"]:
        require(snippet in exact_routes_plan, "exact integration routes plan missing: %s" % snippet, errors)
    ci_plan = read("docs/plans/2026-06-10-ci-baseline.md")
    for snippet in ["Status: Complete", "GitHub Actions", "make check"]:
        require(snippet in ci_plan, "CI baseline plan missing: %s" % snippet, errors)
    malformed_beats_plan = read("docs/plans/2026-06-10-malformed-beats-results.md")
    for snippet in ["Status: Complete", "first_track_result", "malformed Beats search results", "make check"]:
        require(snippet in malformed_beats_plan, "malformed Beats results plan missing: %s" % snippet, errors)
    malformed_twitter_plan = read("docs/plans/2026-06-10-malformed-twitter-mentions.md")
    for snippet in ["Status: Complete", "clean_track_search", "malformed Twitter mention text", "make check"]:
        require(snippet in malformed_twitter_plan, "malformed Twitter mention plan missing: %s" % snippet, errors)
    secret_length_plan = read("docs/plans/2026-06-13-production-secret-key-length.md")
    for snippet in ["status: completed", "make check", "six hostile mutations", "32 characters"]:
        require(snippet in secret_length_plan, "secret key length plan missing: %s" % snippet, errors)
    auth_state_plan = read("docs/plans/2026-06-13-auth-state-routing.md")
    for snippet in [
        "status: completed",
        "has_required_auths",
        "python3 test_views_normalization.py -v",
        "make check",
        "hostile mutations rejected",
        "external working directory",
        "git diff --check",
        "secret, captured-identifier, and generated-bytecode scan",
    ]:
        require(snippet in auth_state_plan, "auth-state routing plan missing: %s" % snippet, errors)
    social_token_plan = read(
        "docs/plans/2026-06-13-social-token-metadata-normalization.md"
    )
    social_token_status = re.findall(r"(?mi)^status:\s*(.+?)\s*$", social_token_plan)
    social_token_work = markdown_section(social_token_plan, "Work Completed")
    social_token_verification = markdown_section(
        social_token_plan, "Verification Completed"
    )
    require(
        social_token_status == ["completed"] and bool(social_token_work),
        "social token plan must record completed status and work",
        errors,
    )
    require(
        bool(social_token_verification)
        and not re.search(
            r"(?i)\b(?:pending|todo|tbd|not run)\b", social_token_verification
        ),
        "social token plan must record completed verification",
        errors,
    )
    for evidence in [
        "python3 test_views_normalization.py -v",
        "make lint",
        "make test",
        "make build",
        "make verify",
        "make check",
        "external working directory",
        "workflow YAML",
        "README SVG",
        "hostile mutations",
        "git diff --check",
        "secret, captured-identifier, and generated-bytecode scan",
    ]:
        require(
            evidence in social_token_verification,
            "social token verification missing: %s" % evidence,
            errors,
        )
    location_make_plan = read(
        "docs/plans/2026-06-14-location-independent-make-gates.md"
    )
    location_make_status = re.findall(
        r"(?mi)^status:\s*(.+?)\s*$", location_make_plan
    )
    location_make_work = markdown_section(location_make_plan, "Work Completed")
    location_make_verification = markdown_section(
        location_make_plan, "Verification Completed"
    )
    require(
        location_make_status == ["completed"] and bool(location_make_work),
        "location-independent Make plan must record completed status and work",
        errors,
    )
    require(
        bool(location_make_verification)
        and not re.search(
            r"(?i)\b(?:pending|todo|tbd|not run)\b", location_make_verification
        ),
        "location-independent Make plan must record completed verification",
        errors,
    )
    for evidence in [
        "make lint",
        "make test",
        "make build",
        "make verify",
        "make check",
        "make static-check",
        "make settings-test",
        "make url-test",
        "18 dependency-free tests",
        "from `/tmp`",
        "absolute",
        "caller-supplied `REPO_ROOT=/tmp`",
        "python3 -m py_compile",
        "workflow YAML",
        "README SVG",
        "Twelve isolated hostile mutations were rejected",
    ]:
        require(
            evidence in location_make_verification,
            "location-independent Make verification missing: %s" % evidence,
            errors,
        )
    preview_plan = read("docs/plans/2026-06-15-preview-seconds-validation.md")
    preview_status = re.findall(r"(?mi)^status:\s*(.+?)\s*$", preview_plan)
    preview_work = markdown_section(preview_plan, "Work Completed")
    preview_verification = markdown_section(preview_plan, "Verification Completed")
    require(
        preview_status == ["completed"] and bool(preview_work),
        "preview validation plan must record completed status and work",
        errors,
    )
    require(
        bool(preview_verification)
        and not re.search(
            r"(?i)\b(?:pending|todo|tbd|not run)\b", preview_verification
        ),
        "preview validation plan must record completed verification",
        errors,
    )
    for evidence in [
        "python3 test_views_normalization.py -v",
        "make lint",
        "make test",
        "make build",
        "make verify",
        "make check",
        "external working directory",
        "workflow YAML",
        "README SVG",
        "hostile mutations",
        "git diff --check",
        "artifact, credential, and generated-bytecode audits",
    ]:
        require(
            evidence in preview_verification,
            "preview validation verification missing: %s" % evidence,
            errors,
        )
    text_only_plan = read("docs/plans/2026-06-16-text-only-player-metadata.md")
    text_only_status = re.findall(r"(?mi)^status:\s*(.+?)\s*$", text_only_plan)
    text_only_work = markdown_section(text_only_plan, "Work Completed")
    text_only_verification = markdown_section(
        text_only_plan, "Verification Completed"
    )
    require(
        text_only_status == ["completed"] and bool(text_only_work),
        "text-only player metadata plan must record completed status and work",
        errors,
    )
    require(
        bool(text_only_verification)
        and not re.search(
            r"(?i)\b(?:pending|todo|tbd|not run)\b", text_only_verification
        ),
        "text-only player metadata plan must record completed verification",
        errors,
    )
    for evidence in [
        "python3 test_views_normalization.py -v",
        "make lint",
        "make test",
        "make build",
        "make verify",
        "make check",
        "external working directory",
        "template JavaScript syntax",
        "Seven isolated hostile mutations were rejected",
        "git diff --check",
        "artifact, credential, conflict-marker, binary, size, mode, and whitespace audits",
    ]:
        require(
            evidence in text_only_verification,
            "text-only player metadata verification missing: %s" % evidence,
            errors,
        )
    hidden_token_plan = read("docs/plans/2026-06-17-hidden-player-auth-token.md")
    hidden_token_status = re.findall(r"(?mi)^status:\s*(.+?)\s*$", hidden_token_plan)
    hidden_token_work = markdown_section(hidden_token_plan, "Work Completed")
    hidden_token_verification = markdown_section(
        hidden_token_plan, "Verification Completed"
    )
    require(
        hidden_token_status == ["completed"] and bool(hidden_token_work),
        "hidden player auth token plan must record completed status and work",
        errors,
    )
    require(
        bool(hidden_token_verification)
        and not re.search(
            r"(?i)\b(?:pending|todo|tbd|not run)\b", hidden_token_verification
        ),
        "hidden player auth token plan must record completed verification",
        errors,
    )
    for evidence in [
        "python3 test_views_normalization.py -v",
        "make lint",
        "make test",
        "make build",
        "make verify",
        "make check",
        "external working directory",
        "Six isolated hostile mutations were rejected",
        "git diff --check",
    ]:
        require(
            evidence in hidden_token_verification,
            "hidden player auth token verification missing: %s" % evidence,
            errors,
        )
    hosted_validation_plan = read("docs/plans/2026-06-10-hosted-security-validation.md")
    hosted_validation_status = re.findall(
        r"(?mi)^status:\s*(.+?)\s*$", hosted_validation_plan
    )
    hosted_validation_work = markdown_section(hosted_validation_plan, "Work Completed")
    hosted_validation_verification = markdown_section(
        hosted_validation_plan, "Verification Completed"
    )
    require(
        hosted_validation_status == ["Complete"] and bool(hosted_validation_work),
        "hosted validation plan must record one complete status and completed work",
        errors,
    )
    require(
        bool(hosted_validation_verification)
        and not re.search(
            r"(?i)\b(?:pending|todo|tbd|not run)\b", hosted_validation_verification
        ),
        "hosted validation plan must record finished verification without pending markers",
        errors,
    )
    for evidence in [
        "make lint",
        "make test",
        "make build",
        "make verify",
        "make check",
        "PYTHONDONTWRITEBYTECODE=1 python3 scripts/check-baseline.py",
        "git diff --check",
        "Six hostile workflow, normalization, and generated-bytecode mutations",
        "27390853154",
        "27390897822",
        "298b6814e6a0d4d88c63ec5672bea61d3281b1ca",
        "Python 3.10",
        "Python 3.12",
        "df4cb1c069e1874edd31b4311f1884172cec0e10",
        "a309ff8b426b58ec0e2a45f0f869d46889d02405",
        "persist-credentials: false",
        'PYTHONDONTWRITEBYTECODE: "1"',
        "test_secret_key_required_when_debug_disabled",
        "test_first_track_result_rejects_malformed_beats_results",
        "test_clean_track_search_rejects_malformed_twitter_mentions",
    ]:
        require(
            evidence in hosted_validation_verification,
            "hosted validation plan must preserve verification evidence: %s" % evidence,
            errors,
        )

    auth_error_plan = read("docs/plans/2026-06-25-social-auth-error-route.md")
    auth_error_status = re.findall(r"(?mi)^status:\s*(.+?)\s*$", auth_error_plan)
    auth_error_work = markdown_section(auth_error_plan, "Work Completed")
    auth_error_verification = markdown_section(auth_error_plan, "Verification Completed")
    require(
        auth_error_status == ["completed"] and bool(auth_error_work),
        "social-auth error route plan must record completed status and work",
        errors,
    )
    require(
        bool(auth_error_verification)
        and not re.search(r"(?i)\b(?:pending|todo|tbd|not run)\b", auth_error_verification),
        "social-auth error route plan must record completed verification",
        errors,
    )
    for evidence in [
        "registered root login",
        "29 dependency-free tests",
        "make check",
        "external working directory",
        "Six isolated hostile mutations were rejected",
        "git diff --check",
        "Exact diff",
    ]:
        require(
            evidence in auth_error_verification,
            "social-auth error route verification missing: %s" % evidence,
            errors,
        )

    try:
        ET.parse(ROOT / "docs/readme-overview.svg")
    except ET.ParseError as exc:
        errors.append("docs/readme-overview.svg is not parseable XML: %s" % exc)

    if errors:
        for error in errors:
            fail(error)
        return 1

    print("check-baseline: ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
