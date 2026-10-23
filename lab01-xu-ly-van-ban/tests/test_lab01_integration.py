"""End-to-end tests for the Lab 01 exercises and document-query workflow."""

from __future__ import annotations

from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path
from unittest.mock import patch
import unittest

from src.bai01_tach_tu_tieng_anh import format_analysis as format_english_analysis
from src.bai02_tach_tu_tieng_viet import format_analysis as format_vietnamese_analysis
from src.bai03_tan_so_tu import format_frequency_table
from src.bai04_tan_so_tai_lieu import format_document_frequency_table
from src.bai05_giao_hop import format_set_operations
from src.bai06_truy_van import (
    build_inverted_index,
    get_document,
    load_documents,
    main as query_main,
    search_index,
)


DATA_DIRECTORY = Path(__file__).resolve().parents[1] / "data" / "documents"


class Lab01IntegrationTests(unittest.TestCase):
    def test_all_exercise_formatters_produce_readable_output(self) -> None:
        english_output = format_english_analysis("Information retrieval.")
        vietnamese_output = format_vietnamese_analysis(
            "Sinh viên học xử lý văn bản.", "xử lý"
        )
        frequency_output = format_frequency_table("Python học Python.")
        document_frequency_output = format_document_frequency_table(
            ["Python xử lý dữ liệu.", "Python tìm kiếm dữ liệu."]
        )
        set_output = format_set_operations([1, 3, 5], [2, 3, 5])

        self.assertIn("inform", english_output)
        self.assertIn("Result: FOUND", vietnamese_output)
        self.assertIn("python", frequency_output)
        self.assertIn("Number of documents", document_frequency_output)
        self.assertIn("Giao: [3, 5]", set_output)
        self.assertIn("Hợp: [1, 2, 3, 5]", set_output)

    def test_real_dataset_query_pipeline_is_consistent(self) -> None:
        documents = load_documents(DATA_DIRECTORY)
        index = build_inverted_index(documents)

        self.assertEqual(len(documents), 10)
        self.assertEqual(search_index(index, "python"), [1, 2, 10])
        self.assertEqual(search_index(index, "dữ liệu"), [1, 2, 4, 5, 6, 7, 8, 9, 10])
        self.assertIn("ngôn ngữ lập trình", get_document(documents, 1))

        for postings in index.values():
            self.assertEqual(postings, sorted(set(postings)))
            self.assertTrue(all(document_id in documents for document_id in postings))

    def test_query_cli_can_search_select_and_exit(self) -> None:
        output = StringIO()
        with patch("builtins.input", side_effect=["python", "1", "q"]):
            with redirect_stdout(output):
                query_main(DATA_DIRECTORY)

        rendered = output.getvalue()
        self.assertIn("Đã nạp 10 tài liệu.", rendered)
        self.assertIn("Documents: 1, 2, 10", rendered)
        self.assertIn("Toàn văn tài liệu 1:", rendered)
        self.assertIn("Python là ngôn ngữ lập trình", rendered)


if __name__ == "__main__":
    unittest.main()
