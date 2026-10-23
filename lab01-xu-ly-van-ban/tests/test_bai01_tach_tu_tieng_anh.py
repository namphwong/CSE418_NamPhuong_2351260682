"""Tests for Bài 1 English tokenization and stemming."""

from __future__ import annotations

import unittest

from src.bai01_tach_tu_tieng_anh import (
    analyze_english_text,
    stem_tokens,
    tokenize_english,
)


class EnglishTextTests(unittest.TestCase):
    def test_tokenize_english_uses_words_and_punctuation(self) -> None:
        self.assertEqual(
            tokenize_english("Information retrieval is useful."),
            ["Information", "retrieval", "is", "useful", "."],
        )

    def test_stem_tokens_uses_porter_algorithm(self) -> None:
        self.assertEqual(
            stem_tokens(["caresses", "ponies", "relational", "."]),
            ["caress", "poni", "relat", "."],
        )

    def test_analysis_preserves_token_stem_alignment(self) -> None:
        tokens, stems = analyze_english_text(
            "The cats are running quickly."
        )
        self.assertEqual(len(tokens), len(stems))
        self.assertEqual(tokens[0], "The")
        self.assertEqual(stems[0], "the")
        self.assertEqual(tokens[-1], ".")
        self.assertEqual(stems[-1], ".")

    def test_tokenize_rejects_non_string_input(self) -> None:
        with self.assertRaises(TypeError):
            tokenize_english(None)  # type: ignore[arg-type]

    def test_stem_tokens_rejects_string_as_token_collection(self) -> None:
        with self.assertRaises(TypeError):
            stem_tokens("running")

    def test_stem_tokens_rejects_non_string_token(self) -> None:
        with self.assertRaises(TypeError):
            stem_tokens(["running", 1])  # type: ignore[list-item]


if __name__ == "__main__":
    unittest.main()
