from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from src.bai01_whoosh_co_ban import build_demo_index, search_demo


class Bai01WhooshTest(unittest.TestCase):
    def test_build_and_search_demo_index(self) -> None:
        with TemporaryDirectory() as temporary:
            index_dir = Path(temporary) / "index"
            build_demo_index(index_dir)
            results = search_demo("first", index_dir)

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["title"], "First document")
        self.assertEqual(results[0]["path"], "/a")

    def test_empty_query_returns_no_results(self) -> None:
        with TemporaryDirectory() as temporary:
            index_dir = Path(temporary) / "index"
            build_demo_index(index_dir)
            self.assertEqual(search_demo("", index_dir), [])


if __name__ == "__main__":
    unittest.main()

