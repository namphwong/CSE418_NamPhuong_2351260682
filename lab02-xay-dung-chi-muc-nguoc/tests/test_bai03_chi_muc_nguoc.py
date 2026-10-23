from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from src.bai03_chi_muc_nguoc import (
    build_index,
    format_results,
    result_document,
    run_cli,
    search_documents,
)
from src.data import DEFAULT_DOCUMENTS
from src.whoosh_common import open_index


class Bai03ChiMucNguocTest(unittest.TestCase):
    def test_dataset_has_ten_documents(self) -> None:
        self.assertEqual(len(DEFAULT_DOCUMENTS), 10)
        self.assertEqual(
            [document.document_id for document in DEFAULT_DOCUMENTS],
            list(range(1, 11)),
        )

    def test_index_stores_id_and_title_but_not_content(self) -> None:
        with TemporaryDirectory() as temporary:
            index_dir = Path(temporary) / "index"
            build_index(index_dir)
            index = open_index(index_dir)
            try:
                with index.searcher() as searcher:
                    hit = searcher.document(doc_id="10")
            finally:
                index.close()

        self.assertEqual(hit["title"], "Học máy")
        self.assertEqual(hit["doc_id"], "10")
        self.assertNotIn("content", hit)

    def test_query_returns_titles_and_content_can_be_retrieved(self) -> None:
        with TemporaryDirectory() as temporary:
            index_dir = Path(temporary) / "index"
            build_index(index_dir)
            results = search_documents("học máy", index_dir)

        self.assertTrue(results)
        self.assertEqual(results[0]["doc_id"], "10")
        self.assertEqual(result_document(results[0]).title, "Học máy")
        self.assertIn("dự đoán", result_document(results[0]).content)

    def test_format_results_numbers_from_one(self) -> None:
        lines = format_results(
            [
                {"doc_id": "2", "title": "Xử lý dữ liệu"},
                {"doc_id": "3", "title": "Tìm kiếm thông tin"},
            ]
        )
        self.assertEqual(lines[0], "Số kết quả: 2")
        self.assertTrue(lines[1].startswith("1. "))
        self.assertTrue(lines[2].startswith("2. "))

    def test_cli_query_selection_and_exit(self) -> None:
        with TemporaryDirectory() as temporary:
            index_dir = Path(temporary) / "index"
            answers = iter(["học máy", "1", "q"])
            output: list[str] = []
            run_cli(index_dir, input_fn=lambda _: next(answers), output_fn=output.append)

        joined_output = "\n".join(output)
        self.assertIn("Số kết quả:", joined_output)
        self.assertIn("Nội dung tài liệu 10 - Học máy:", joined_output)
        self.assertIn("Đã kết thúc chương trình.", joined_output)

    def test_cli_handles_invalid_selection(self) -> None:
        with TemporaryDirectory() as temporary:
            index_dir = Path(temporary) / "index"
            answers = iter(["học máy", "99", "q"])
            output: list[str] = []
            run_cli(index_dir, input_fn=lambda _: next(answers), output_fn=output.append)

        self.assertTrue(any("phải nằm trong khoảng" in line for line in output))


if __name__ == "__main__":
    unittest.main()

