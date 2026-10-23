from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from index import build_index, document_paths, open_index, read_document


PROJECT_DIR = Path(__file__).resolve().parents[1]
DOCS_DIR = PROJECT_DIR / "CS-Docs"


class IndexTest(unittest.TestCase):
    def test_document_dataset_has_five_files(self) -> None:
        paths = document_paths(DOCS_DIR)
        self.assertEqual([path.name for path in paths], ["AI.txt", "DM.txt", "ML.txt", "OS.txt", "SE.txt"])

    def test_read_document_uses_first_line_as_title(self) -> None:
        title, content = read_document(DOCS_DIR / "ML.txt")
        self.assertEqual(title, "Machine Learning")
        self.assertIn("learn from data", content)

    def test_build_index_stores_title_and_path(self) -> None:
        with TemporaryDirectory() as temporary:
            index_dir = Path(temporary) / "index"
            build_index(DOCS_DIR, index_dir)
            index = open_index(index_dir)
            try:
                with index.searcher() as searcher:
                    self.assertEqual(searcher.doc_count_all(), 5)
                    hit = searcher.document(path=str(DOCS_DIR / "AI.txt"))
            finally:
                index.close()

        self.assertEqual(hit["title"], "AI.txt - Artificial Intelligence")
        self.assertEqual(hit["path"], str(DOCS_DIR / "AI.txt"))


if __name__ == "__main__":
    unittest.main()
