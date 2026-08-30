import unittest

from linux_browser import __version__


class PackageTest(unittest.TestCase):
    def test_package_has_version(self) -> None:
        self.assertEqual(__version__, "0.1.2")
