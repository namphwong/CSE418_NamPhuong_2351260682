from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from src.bai02_tieng_viet import build_vietnamese_index, search_vietnamese
from src.whoosh_common import tokenize_vietnamese


class Bai02TiengVietTest(unittest.TestCase):
    def test_pyvi_segments_compound_words(self) -> None:
        self.assertEqual(tokenize_vietnamese("Đại học Thủy Lợi"), "Đại_học Thủy_Lợi")

    def test_search_segments_query_consistently(self) -> None:
        with TemporaryDirectory() as temporary:
            index_dir = Path(temporary) / "index"
            build_vietnamese_index(index_dir)
            results = search_vietnamese("đại học thủy lợi", index_dir)

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["title"], "Đại học Thủy Lợi")

    def test_multiword_query_finds_vietnamese_document(self) -> None:
        with TemporaryDirectory() as temporary:
            index_dir = Path(temporary) / "index"
            build_vietnamese_index(index_dir)
            results = search_vietnamese("tách từ ghép", index_dir)

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["title"], "Xử lý văn bản")


if __name__ == "__main__":
    unittest.main()

