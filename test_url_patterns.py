import pathlib
import re
import unittest


ROOT = pathlib.Path(__file__).resolve().parent
URLS = ROOT / "app" / "urls.py"


class UrlPatternTest(unittest.TestCase):
    def test_social_auth_error_target_is_registered_root_login(self):
        settings = (ROOT / "app" / "settings.py").read_text(encoding="utf-8")
        urls = URLS.read_text(encoding="utf-8")

        self.assertIn("SOCIAL_AUTH_LOGIN_ERROR_URL    = '/'", settings)
        self.assertNotIn("/login-error/", settings)
        self.assertRegex(
            urls,
            re.compile(r"url\(r'\^\$'\s*,\s*'home\.views\.login'"),
        )

    def test_integration_routes_are_exact_matches(self):
        source = URLS.read_text(encoding="utf-8")

        self.assertRegex(
            source,
            re.compile(r"url\(r'\^twttr\$'\s*,\s*'home\.views\.twttr'"),
        )
        self.assertRegex(
            source,
            re.compile(r"url\(r'\^beats\$'\s*,\s*'home\.views\.beats'"),
        )
        self.assertNotRegex(
            source,
            re.compile(r"url\(r'\^(?:twttr|beats)'"),
        )


if __name__ == "__main__":
    unittest.main()
