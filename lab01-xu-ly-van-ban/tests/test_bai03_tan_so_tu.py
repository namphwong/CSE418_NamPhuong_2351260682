"""Tests for Bài 3 word-frequency counting."""

from __future__ import annotations

import unittest

from src.bai03_tan_so_tu import (
    count_word_frequency,
    sort_frequencies,
    tokenize_document,
)


class WordFrequencyTests(unittest.TestCase):
    def test_tokenize_document_removes_punctuation_and_lowercases(self) -> None:
        self.assertEqual(
            tokenize_document("Python, PYTHON học."),
            ["python", "python", "học"],
        )

    def test_tokenize_document_keeps_vietnamese_multi_syllable_words(self) -> None:
        self.assertEqual(
            tokenize_document("Xử lý văn bản. Xử lý tốt."),
            ["xử lý", "văn bản", "xử lý", "tốt"],
        )

    def test_count_word_frequency_uses_a_dictionary(self) -> None:
        self.assertEqual(
            count_word_frequency("Python học Python. Python!"),
            {"python": 3, "học": 1},
        )

    def test_whitespace_mode_is_available_for_simple_input(self) -> None:
        self.assertEqual(
            tokenize_document(
                "Data data search.", language="whitespace"
            ),
            ["data", "data", "search"],
        )

    def test_empty_document_returns_empty_frequency_dictionary(self) -> None:
        self.assertEqual(count_word_frequency("   "), {})

    def test_sort_frequencies_is_deterministic(self) -> None:
        self.assertEqual(
            sort_frequencies({"z": 1, "b": 2, "a": 2}),
            [("a", 2), ("b", 2), ("z", 1)],
        )

    def test_invalid_inputs_are_rejected(self) -> None:
        with self.assertRaises(TypeError):
            tokenize_document(None)  # type: ignore[arg-type]
        with self.assertRaises(ValueError):
            tokenize_document("text", language="unknown")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            sort_frequencies([])  # type: ignore[arg-type]
        with self.assertRaises(ValueError):
            sort_frequencies({"word": -1})


if __name__ == "__main__":
    unittest.main()
