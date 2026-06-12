#!/usr/bin/env python3
"""Static baseline checks for the legacy playlist Django sample."""

import ast
import sys
import xml.etree.ElementTree as ET
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

REQUIRED_FILES = [
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
    ".github/workflows/check.yml",
    "docs/readme-overview.svg",
    "fabfile.py",
    "home/views.py",
    "manage.py",
    "requirements.txt",
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
        "check: verify",
        "verify: lint test build",
        "lint: static-check",
        "test: settings-test url-test",
        "build: static-check",
        "python3 scripts/check-baseline.py",
        "python3 test_settings_security.py -v",
        "python3 test_views_normalization.py -v",
        "python3 test_url_patterns.py -v",
    ]:
        require(snippet in makefile, "Makefile missing guardrail: %s" % snippet, errors)

    workflow = read(".github/workflows/check.yml")
    for snippet in [
        "actions/checkout@v4",
        "actions/setup-python@v5",
        'python-version: "3.12"',
        "make check",
    ]:
        require(snippet in workflow, "GitHub Actions workflow missing: %s" % snippet, errors)

    urls = read("app/urls.py")
    for snippet in [
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
        "SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')",
        "SECRET_KEY = SECRET_KEY.strip()",
        "raise RuntimeError(",
        "TEMPLATE_DEBUG = DEBUG",
        "ALLOWED_HOSTS = env_list(",
        "DJANGO_ALLOWED_HOSTS",
        "if not DEBUG and not ALLOWED_HOSTS:",
        "if not DEBUG and '*' in ALLOWED_HOSTS:",
        "DJANGO_SQLITE_PATH",
    ]:
        require(snippet in settings, "settings missing guardrail: %s" % snippet, errors)

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

    views = read("home/views.py")
    require("request.REQUEST" not in views, "legacy request.REQUEST access remains", errors)
    for snippet in [
        "def clean_post_text(",
        "if not isinstance(value, str):",
        "def clean_tweet_id(",
        "tweet_id_re = re.compile(r'^[0-9]+$')",
        'status = clean_post_text(request.POST.get("status", None))',
        'fav = clean_tweet_id(request.POST.get("fav", None))',
        'request.POST.get("track", request.GET.get("track", None))',
        "from django.views.decorators.http import require_POST",
        "@login_required\n@require_POST\ndef logout(request):",
        "except Exception:",
    ]:
        require(snippet in views, "views missing guardrail: %s" % snippet, errors)
    require("print(search, tracks)" not in views, "playlist debug print must not expose user-linked data", errors)

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

    twitter_template = read("templates/twitter.html")
    for snippet in ['action="/twttr"', 'method="post"', "{% csrf_token %}"]:
        require(snippet in twitter_template, "twitter template missing POST status path: %s" % snippet, errors)

    base_template = read("templates/base.html")
    for snippet in ['action="/logout"', 'method="post"', "{% csrf_token %}"]:
        require(snippet in base_template, "base template missing POST logout path: %s" % snippet, errors)
    require('href="/logout"' not in base_template, "logout action still uses a GET link", errors)

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
        "post input normalization",
        "non-string post inputs",
        "exact-match integration routes",
        "CSRF-protected POST logout",
        "GitHub Actions",
    ]:
        require(snippet in readme, "README missing: %s" % snippet, errors)

    security = read("SECURITY.md")
    for snippet in ["DJANGO_SECRET_KEY", "DJANGO_DEBUG", "DJANGO_ALLOWED_HOSTS", "required outside local debug", "wildcard allowed hosts", "OAuth", "debug print", "blank", "post input normalization", "non-string post inputs", "exact-match integration routes", "CSRF-protected POST logout"]:
        require(snippet in security, "SECURITY missing: %s" % snippet, errors)

    vision = read("VISION.md")
    for snippet in ["environment-based configuration", "POST", "make check", "make lint", "make test", "make build", "make verify", "debug print", "blank", "post input normalization", "non-string post inputs", "allowed hosts", "wildcard allowed hosts", "exact-match integration routes", "POST-only logout"]:
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
