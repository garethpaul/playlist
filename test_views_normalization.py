import importlib.util
import pathlib
import sys
import types
import unittest


ROOT = pathlib.Path(__file__).resolve().parent
VIEWS = ROOT / "home" / "views.py"


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
