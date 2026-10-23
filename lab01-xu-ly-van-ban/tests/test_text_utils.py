"""Unit tests for the shared Lab 01 text utilities."""

from __future__ import annotations

import unittest

from src.text_utils import (
    count_document_frequency,
    count_words,
    get_unique_words,
    normalize_text,
    remove_punctuation,
)


class TextUtilsTests(unittest.TestCase):
    def test_normalize_text_unicode_case_and_whitespace(self) -> None:
        self.assertEqual(
            normalize_text("  HỌC\t  máy\nViệt Nam  "),
            "học máy việt nam",
        )

    def test_normalize_text_can_preserve_case(self) -> None:
        self.assertEqual(
            normalize_text("  Python\tViệt Nam ", lowercase=False),
            "Python Việt Nam",
        )

    def test_remove_punctuation_keeps_words_separate(self) -> None:
        self.assertEqual(
            remove_punctuation("Xin-chào, Việt Nam!"),
            "Xin chào Việt Nam",
        )

    def test_remove_punctuation_can_delete_punctuation(self) -> None:
        self.assertEqual(remove_punctuation("a,b!", replacement=""), "ab")

    def test_get_unique_words_preserves_order_and_ignores_empty_tokens(self) -> None:
        self.assertEqual(
            get_unique_words(["python", "", "data", "python", " data "]),
            ["python", "data"],
        )

    def test_count_words(self) -> None:
        self.assertEqual(
            count_words(["python", "data", "python", "", " data "]),
            {"python": 2, "data": 2},
        )

    def test_count_document_frequency_counts_once_per_document(self) -> None:
        documents = [
            ["python", "python", "data"],
            ["data", "search"],
            ["python", "search"],
        ]
        self.assertEqual(
            count_document_frequency(documents),
            {"python": 2, "data": 2, "search": 2},
        )

    def test_text_arguments_are_validated(self) -> None:
        with self.assertRaises(TypeError):
            normalize_text(None)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            remove_punctuation(123)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            get_unique_words("python")
        with self.assertRaises(TypeError):
            count_words(["python", 1])  # type: ignore[list-item]
        with self.assertRaises(TypeError):
            count_document_frequency(["python"])  # type: ignore[list-item]


if __name__ == "__main__":
    unittest.main()
