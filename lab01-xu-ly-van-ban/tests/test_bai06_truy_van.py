"""Tests for Bài 6 document loading, indexing, and querying."""

from __future__ import annotations

from pathlib import Path
import tempfile
import unittest

from src.bai06_truy_van import (
    build_inverted_index,
    get_document,
    load_documents,
    search_index,
)


DATA_DIRECTORY = Path(__file__).resolve().parents[1] / "data" / "documents"


class DocumentQueryTests(unittest.TestCase):
    def setUp(self) -> None:
        self.documents = load_documents(DATA_DIRECTORY)
        self.index = build_inverted_index(self.documents)

    def test_load_documents_reads_all_ten_utf8_documents(self) -> None:
        self.assertEqual(list(self.documents), list(range(1, 11)))
        self.assertEqual(len(self.documents), 10)
        self.assertTrue(all(text.strip() for text in self.documents.values()))
        self.assertIn("Python", self.documents[1])

    def test_index_contains_sorted_unique_postings(self) -> None:
        self.assertTrue(self.index)
        for token, postings in self.index.items():
            self.assertEqual(postings, sorted(set(postings)), token)
            self.assertTrue(all(document_id in self.documents for document_id in postings))

    def test_query_returns_expected_document_ids(self) -> None:
        self.assertEqual(search_index(self.index, "python"), [1, 2, 10])
        self.assertEqual(search_index(self.index, "PYTHON"), [1, 2, 10])
        self.assertEqual(search_index(self.index, "tìm kiếm"), [1, 2, 3])

    def test_query_returns_empty_list_when_token_is_missing(self) -> None:
        self.assertEqual(search_index(self.index, "không tồn tại"), [])

    def test_query_does_not_match_a_partial_multi_syllable_token(self) -> None:
        self.assertEqual(search_index(self.index, "cơ"), [])
        self.assertEqual(search_index(self.index, "cơ sở dữ liệu"), [5, 8])

    def test_get_document_returns_full_text(self) -> None:
        self.assertEqual(get_document(self.documents, 1), self.documents[1])
        self.assertIn("ngôn ngữ lập trình", get_document(self.documents, 1))

    def test_invalid_query_and_document_id_are_rejected(self) -> None:
        with self.assertRaises(ValueError):
            search_index(self.index, "   ")
        with self.assertRaises(TypeError):
            search_index(self.index, 123)  # type: ignore[arg-type]
        with self.assertRaises(KeyError):
            get_document(self.documents, 999)
        with self.assertRaises(TypeError):
            get_document(self.documents, True)  # type: ignore[arg-type]

    def test_loader_rejects_missing_or_invalid_directories(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            empty_directory = Path(temporary_directory)
            with self.assertRaises(ValueError):
                load_documents(empty_directory)
            with self.assertRaises(FileNotFoundError):
                load_documents(empty_directory / "missing")

    def test_loader_reads_numeric_ids_in_numeric_order(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            folder = Path(temporary_directory)
            (folder / "10_last.txt").write_text("mười", encoding="utf-8")
            (folder / "2_second.txt").write_text("hai", encoding="utf-8")
            (folder / "1_first.txt").write_text("một", encoding="utf-8")
            self.assertEqual(load_documents(folder), {1: "một", 2: "hai", 10: "mười"})


if __name__ == "__main__":
    unittest.main()
