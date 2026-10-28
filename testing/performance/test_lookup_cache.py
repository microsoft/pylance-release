import tempfile
import unittest
from pathlib import Path

from testing.performance.lookup_cache import clear_module_cache, resolve_module_path


class ResolveModulePathTests(unittest.TestCase):
    def setUp(self) -> None:
        clear_module_cache()

    def test_reuses_cached_lookup(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "module.py").touch()
            roots = (directory,)

            first = resolve_module_path("module", roots)
            second = resolve_module_path("module", roots)

            self.assertEqual(first, str(root / "module.py"))
            self.assertEqual(second, first)
            self.assertEqual(resolve_module_path.cache_info().hits, 1)

    def test_clears_cached_miss_after_filesystem_change(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            roots = (directory,)
            self.assertIsNone(resolve_module_path("module", roots))

            (Path(directory) / "module.py").touch()
            self.assertIsNone(resolve_module_path("module", roots))

            clear_module_cache()

            self.assertEqual(
                resolve_module_path("module", roots),
                str(Path(directory) / "module.py"),
            )


if __name__ == "__main__":
    unittest.main()
