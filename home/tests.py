try:
    from django.test import TestCase
except ImportError:
    import unittest

    class TestCase(unittest.TestCase):
        pass

# Create your tests here.
