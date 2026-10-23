"""Tests for Bài 4 document-frequency counting."""

from __future__ import annotations

import unittest

from src.bai04_tan_so_tai_lieu import (
    count_document_frequencies,
    sort_document_frequencies,
    tokenize_documents,
)


class DocumentFrequencyTests(unittest.TestCase):
    def setUp(self) -> None:
        self.documents = [
            "Python Python xử lý dữ liệu.",
            "Python hỗ trợ tìm kiếm dữ liệu.",
            "Tìm kiếm thông tin.",
            "Dữ liệu giúp xây dựng hệ thống thông tin.",
        ]

    def test_tokenize_documents_preserves_document_order(self) -> None:
        tokenized = tokenize_documents(self.documents)
        self.assertEqual(tokenized[0], ["python", "python", "xử lý", "dữ liệu"])
        self.assertEqual(tokenized[2], ["tìm kiếm", "thông tin"])

    def test_repeated_word_in_one_document_counts_once(self) -> None:
        frequencies = count_document_frequencies(self.documents)
        self.assertEqual(frequencies["python"], 2)
        self.assertEqual(frequencies["dữ liệu"], 3)
        self.assertEqual(frequencies["tìm kiếm"], 2)
        self.assertEqual(frequencies["thông tin"], 2)

    def test_document_frequency_is_not_word_frequency(self) -> None:
        frequencies = count_document_frequencies(
            ["data data data.", "data.", "search."]
        )
        self.assertEqual(frequencies, {"data": 2, "search": 1})

    def test_empty_documents_are_allowed(self) -> None:
        self.assertEqual(
            count_document_frequencies(["", "   ", "Python."]),
            {"python": 1},
        )
        self.assertEqual(count_document_frequencies([]), {})

    def test_sort_document_frequencies_is_deterministic(self) -> None:
        self.assertEqual(
            sort_document_frequencies(
                {"z": 1, "b": 2, "a": 2, "c": 3}
            ),
            [("c", 3), ("a", 2), ("b", 2), ("z", 1)],
        )

    def test_invalid_inputs_are_rejected(self) -> None:
        with self.assertRaises(TypeError):
            tokenize_documents("not a collection")
        with self.assertRaises(TypeError):
            tokenize_documents(["valid", 123])  # type: ignore[list-item]
        with self.assertRaises(TypeError):
            sort_document_frequencies([])  # type: ignore[arg-type]
        with self.assertRaises(ValueError):
            sort_document_frequencies({"word": -1})


if __name__ == "__main__":
    unittest.main()
