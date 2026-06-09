import importlib.util
import os
import pathlib
import unittest
from unittest import mock


ROOT = pathlib.Path(__file__).resolve().parent
SETTINGS = ROOT / "app" / "settings.py"


class SettingsSecurityTest(unittest.TestCase):
    def load_settings(self, env):
        with mock.patch.dict(os.environ, env, clear=True):
            spec = importlib.util.spec_from_file_location("playlist_settings_under_test", str(SETTINGS))
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            return module

    def test_secret_key_required_when_debug_disabled(self):
        with mock.patch.dict(os.environ, {}, clear=True):
            spec = importlib.util.spec_from_file_location("playlist_settings_missing_secret", str(SETTINGS))
            module = importlib.util.module_from_spec(spec)
            with self.assertRaisesRegex(RuntimeError, "DJANGO_SECRET_KEY"):
                spec.loader.exec_module(module)

    def test_blank_secret_key_rejected_when_debug_disabled(self):
        with mock.patch.dict(os.environ, {"DJANGO_SECRET_KEY": "   ", "DJANGO_DEBUG": "0"}, clear=True):
            spec = importlib.util.spec_from_file_location("playlist_settings_blank_secret", str(SETTINGS))
            module = importlib.util.module_from_spec(spec)
            with self.assertRaisesRegex(RuntimeError, "DJANGO_SECRET_KEY"):
                spec.loader.exec_module(module)

    def test_local_debug_uses_explicit_development_fallback(self):
        settings = self.load_settings({"DJANGO_DEBUG": "1"})

        self.assertTrue(settings.DEBUG)
        self.assertTrue(settings.TEMPLATE_DEBUG)
        self.assertEqual("unsafe-development-secret-key", settings.SECRET_KEY)

    def test_production_settings_come_from_environment(self):
        settings = self.load_settings({
            "DJANGO_SECRET_KEY": "  test-production-secret  ",
            "DJANGO_DEBUG": "0",
            "DJANGO_ALLOWED_HOSTS": "playlist.example.com, api.example.com",
            "SOCIAL_AUTH_TWITTER_KEY": "twitter-key",
            "SOCIAL_AUTH_TWITTER_SECRET": "twitter-secret",
            "TWITTER_ACCESS_TOKEN": "twitter-token",
            "TWITTER_ACCESS_TOKEN_SECRET": "twitter-token-secret",
            "SOCIAL_AUTH_BEATS_KEY": "beats-key",
            "SOCIAL_AUTH_BEATS_SECRET": "beats-secret",
            "SOCIAL_AUTH_SPOTIFY_KEY": "spotify-key",
            "SOCIAL_AUTH_SPOTIFY_SECRET": "spotify-secret",
        })

        self.assertFalse(settings.DEBUG)
        self.assertFalse(settings.TEMPLATE_DEBUG)
        self.assertEqual("test-production-secret", settings.SECRET_KEY)
        self.assertEqual(["playlist.example.com", "api.example.com"], settings.ALLOWED_HOSTS)
        self.assertEqual("twitter-key", settings.SOCIAL_AUTH_TWITTER_KEY)
        self.assertEqual("twitter-token", settings.TWITTER_ACCESS_TOKEN)
        self.assertEqual("beats-key", settings.SOCIAL_AUTH_BEATS_KEY)
        self.assertEqual("spotify-key", settings.SOCIAL_AUTH_SPOTIFY_KEY)


if __name__ == "__main__":
    unittest.main()
