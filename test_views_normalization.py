import importlib.util
import pathlib
import sys
import types
import unittest


ROOT = pathlib.Path(__file__).resolve().parent
VIEWS = ROOT / "home" / "views.py"
BEATS_TEMPLATE = ROOT / "templates" / "beats.html"


def decorator(function):
    return function


def install_import_stubs():
    django = types.ModuleType("django")
    django_conf = types.ModuleType("django.conf")
    django_conf.settings = types.SimpleNamespace()

    django_shortcuts = types.ModuleType("django.shortcuts")
    django_shortcuts.__all__ = [
        "HttpResponseRedirect",
        "RequestContext",
        "redirect",
        "render_to_response",
    ]
    django_shortcuts.HttpResponseRedirect = lambda path: path
    django_shortcuts.RequestContext = lambda request: request
    django_shortcuts.redirect = lambda path: path
    django_shortcuts.render_to_response = lambda *args, **kwargs: args

    django_contrib = types.ModuleType("django.contrib")
    django_auth = types.ModuleType("django.contrib.auth")
    django_auth.logout = lambda request: None
    django_auth_decorators = types.ModuleType("django.contrib.auth.decorators")
    django_auth_decorators.login_required = decorator
    django_auth_decorators.user_passes_test = lambda test: decorator
    django_auth_models = types.ModuleType("django.contrib.auth.models")
    django_auth_models.User = object

    django_views = types.ModuleType("django.views")
    django_views_decorators = types.ModuleType("django.views.decorators")
    django_views_http = types.ModuleType("django.views.decorators.http")
    django_views_http.require_POST = decorator

    social = types.ModuleType("social")
    social_apps = types.ModuleType("social.apps")
    social_django = types.ModuleType("social.apps.django_app")
    social_default = types.ModuleType("social.apps.django_app.default")
    social_models = types.ModuleType("social.apps.django_app.default.models")
    social_models.UserSocialAuth = type("UserSocialAuth", (), {})

    twitter = types.ModuleType("twitter")
    twitter.api = types.SimpleNamespace(Api=lambda **kwargs: object())

    spotipy = types.ModuleType("spotipy")
    pybeats = types.ModuleType("pybeats")
    pybeats_api = types.ModuleType("pybeats.api")
    pybeats_api.BeatsAPI = lambda **kwargs: types.SimpleNamespace(access_token=None)

    modules = {
        "django": django,
        "django.conf": django_conf,
        "django.shortcuts": django_shortcuts,
        "django.contrib": django_contrib,
        "django.contrib.auth": django_auth,
        "django.contrib.auth.decorators": django_auth_decorators,
        "django.contrib.auth.models": django_auth_models,
        "django.views": django_views,
        "django.views.decorators": django_views_decorators,
        "django.views.decorators.http": django_views_http,
        "social": social,
        "social.apps": social_apps,
        "social.apps.django_app": social_django,
        "social.apps.django_app.default": social_default,
        "social.apps.django_app.default.models": social_models,
        "twitter": twitter,
        "spotipy": spotipy,
        "pybeats": pybeats,
        "pybeats.api": pybeats_api,
    }
    sys.modules.update(modules)


def load_views():
    install_import_stubs()
    spec = importlib.util.spec_from_file_location("playlist_views_under_test", str(VIEWS))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class ViewsNormalizationTest(unittest.TestCase):
    def test_provider_values_are_escaped_for_javascript_string_literals(self):
        template = BEATS_TEMPLATE.read_text()

        for interpolation in [
            "{{ pair.1.id|escapejs }}",
            "{{ beats_me.result.client_id|escapejs }}",
            "{{ beats.access_token|escapejs }}",
            "{{ beats_me.result.user_context|escapejs }}",
            "{{ track.1.id|escapejs }}",
            "{{ track.0.id|escapejs }}",
        ]:
            with self.subTest(interpolation=interpolation):
                self.assertIn(interpolation, template)

        for unsafe_interpolation in [
            "playNext('{{pair.1.id}}')",
            "'{{ beats_me.result.client_id }}'",
            "'{{ beats.access_token }}'",
            "'{{ beats_me.result.user_context }}'",
            "'{{ track.1.id }}'",
            '"{{ track.0.id }}"',
        ]:
            with self.subTest(unsafe_interpolation=unsafe_interpolation):
                self.assertNotIn(unsafe_interpolation, template)

    def test_player_sdk_is_loaded_over_https(self):
        template = BEATS_TEMPLATE.read_text()

        self.assertIn(
            'src="https://bam.cdn.beatsmusic.com/bam-1.0.2.min.js"',
            template,
        )
        self.assertNotIn('src="http://bam.cdn.beatsmusic.com/', template)

    def test_player_auth_token_is_not_exposed_as_control(self):
        template = BEATS_TEMPLATE.read_text()

        self.assertIn("access_token: '{{ beats.access_token|escapejs }}'", template)
        self.assertNotIn('id="accessToken"', template)
        self.assertNotIn("accessToken.value", template)

    def test_player_metadata_and_timing_use_text_only_dom_sinks(self):
        template = BEATS_TEMPLATE.read_text()

        self.assertNotIn(".innerHTML", template)
        self.assertIn(
            'trackName.textContent = "Title:" + data.display;',
            template,
        )
        for assignment in [
            'timeDuration.textContent = "Duration: " + value;',
            'timeElapsed.textContent = "Elapsed: " + elapsed;',
            'timeRemaining.textContent = "Remaining: " + remaining;',
            'timeBufferedStart.textContent = "Start: " + buffered.start;',
            'timeBufferedEnd.textContent = "End: " + buffered.end;',
            'timeBufferedLength.textContent = "Length: " + buffered.length;',
            'timeSeekableStart.textContent = "Start: " + seekable.start;',
            'timeSeekableEnd.textContent = "End: " + seekable.end;',
            'timeSeekableLength.textContent = "Length: " + seekable.length;',
        ]:
            with self.subTest(assignment=assignment):
                self.assertIn(assignment, template)

    def test_clean_preview_seconds_accepts_bounded_decimal_strings(self):
        views = load_views()

        for value, expected in [
            ("0", "0"),
            (" 30 ", "30"),
            ("0.5", "0.5"),
            ("3600", "3600"),
            ("3600.0", "3600.0"),
        ]:
            with self.subTest(value=value):
                self.assertEqual(expected, views.clean_preview_seconds(value))

    def test_clean_preview_seconds_rejects_non_numeric_or_unsafe_values(self):
        views = load_views()

        for value in [
            None,
            30,
            b"30",
            [],
            {},
            "",
            "  ",
            "-1",
            "+1",
            "01",
            "1.",
            ".5",
            "1e2",
            "3600.1",
            "9" * 17,
            "0);alert(1);//",
        ]:
            with self.subTest(value=value):
                self.assertIsNone(views.clean_preview_seconds(value))

    def test_beats_view_normalizes_preview_before_rendering(self):
        source = VIEWS.read_text()

        self.assertIn(
            'preview = clean_preview_seconds(request.POST.get("preview", '
            'request.GET.get("preview", None)))',
            source,
        )
        self.assertNotIn(
            'preview = request.POST.get("preview", request.GET.get("preview", None))',
            source,
        )

    def test_incomplete_integration_auth_returns_to_registered_login_page(self):
        source = VIEWS.read_text()

        self.assertIn('if not has_required_auths(auths):\n        return redirect("/")', source)
        self.assertNotIn('return redirect("/login")', source)

    def test_has_required_auths_accepts_both_integrations(self):
        views = load_views()

        self.assertTrue(views.has_required_auths({"twitter": object(), "beats": object()}))

    def test_has_required_auths_rejects_incomplete_or_malformed_state(self):
        views = load_views()

        for value in [
            {"twitter": object()},
            {"beats": object()},
            {"twitter": object(), "beats": None},
            {},
            None,
            [],
            "twitter,beats",
        ]:
            with self.subTest(value=value):
                self.assertFalse(views.has_required_auths(value))

    def test_twitter_access_tokens_require_complete_nested_string_pair(self):
        views = load_views()

        malformed_values = [
            None,
            [],
            "token",
            {},
            {"access_token": None},
            {"access_token": "token"},
            {"access_token": {}},
            {"access_token": {"oauth_token": "key"}},
            {"access_token": {"oauth_token": "key", "oauth_token_secret": "  "}},
            {"access_token": {"oauth_token": 123, "oauth_token_secret": "secret"}},
        ]
        for value in malformed_values:
            with self.subTest(value=value):
                self.assertEqual((None, None), views.twitter_access_tokens(value))

        self.assertEqual(
            ("key", "secret"),
            views.twitter_access_tokens({
                "access_token": {
                    "oauth_token": " key ",
                    "oauth_token_secret": " secret ",
                },
            }),
        )

    def test_beats_access_token_requires_nonblank_string(self):
        views = load_views()

        malformed_values = [
            None,
            [],
            "token",
            {},
            {"access_token": None},
            {"access_token": 123},
            {"access_token": "  "},
        ]
        for value in malformed_values:
            with self.subTest(value=value):
                self.assertIsNone(views.beats_access_token(value))

        self.assertEqual(
            "beats-token",
            views.beats_access_token({"access_token": " beats-token "}),
        )

    def test_clean_post_text_rejects_non_string_values(self):
        views = load_views()

        for value in [123, b"hello", [], {}]:
            with self.subTest(value=value):
                self.assertIsNone(views.clean_post_text(value))

    def test_clean_tweet_id_rejects_non_string_values(self):
        views = load_views()

        for value in [123, b"123", [], {}]:
            with self.subTest(value=value):
                self.assertIsNone(views.clean_tweet_id(value))

    def test_clean_track_search_rejects_malformed_twitter_mentions(self):
        views = load_views()

        for value in [None, 123, b"song", [], {}, "", "  ", "@listener", "@one @two"]:
            with self.subTest(value=value):
                self.assertIsNone(views.clean_track_search(value))

    def test_clean_track_search_removes_handles_and_bounds_queries(self):
        views = load_views()

        self.assertEqual("Song Name", views.clean_track_search(" @listener  Song Name "))
        query = views.clean_track_search("x" * (views.MAX_TRACK_SEARCH_LENGTH + 1))
        self.assertEqual(views.MAX_TRACK_SEARCH_LENGTH, len(query))

    def test_first_track_result_rejects_malformed_beats_results(self):
        views = load_views()

        for value in [
            None,
            [],
            {"data": None},
            {"data": []},
            {"data": ["track"]},
            {"data": [{}]},
            {"data": [{"id": "  "}]},
        ]:
            with self.subTest(value=value):
                self.assertIsNone(views.first_track_result(value))

    def test_first_track_result_accepts_first_identified_track(self):
        views = load_views()
        track = {"id": " track-1 ", "title": "Example"}

        self.assertEqual(track, views.first_track_result({"data": [track]}))


if __name__ == "__main__":
    unittest.main()
