"""Tests for Bài 2 Vietnamese tokenization and membership checking."""

from __future__ import annotations

import unittest

from src.bai02_tach_tu_tieng_viet import (
    analyze_vietnamese_text,
    contains_token,
    contains_word,
    tokenize_vietnamese,
)


class VietnameseTextTests(unittest.TestCase):
    def test_tokenize_vietnamese_keeps_multi_syllable_words(self) -> None:
        self.assertEqual(
            tokenize_vietnamese("Sinh viên học xử lý văn bản tiếng Việt."),
            [
                "Sinh viên",
                "học",
                "xử lý",
                "văn bản",
                "tiếng",
                "Việt",
                ".",
            ],
        )

    def test_contains_word_is_case_insensitive(self) -> None:
        document = "Sinh viên học xử lý văn bản tiếng Việt."
        self.assertTrue(contains_word(document, "sinh viên"))
        self.assertTrue(contains_word(document, "SINH VIÊN"))
        self.assertTrue(contains_word(document, "Văn bản"))

    def test_contains_word_requires_a_complete_token(self) -> None:
        document = "Sinh viên học xử lý văn bản tiếng Việt."
        self.assertTrue(contains_word(document, "xử lý"))
        self.assertFalse(contains_word(document, "xử"))

    def test_contains_word_returns_false_for_missing_query(self) -> None:
        self.assertFalse(
            contains_word("Sinh viên học xử lý văn bản.", "cơ sở dữ liệu")
        )

    def test_analyze_returns_tokens_and_membership_result(self) -> None:
        tokens, found = analyze_vietnamese_text(
            "Tìm kiếm thông tin.", "tìm kiếm"
        )
        self.assertEqual(tokens, ["Tìm kiếm", "thông tin", "."])
        self.assertTrue(found)

    def test_contains_token_works_with_an_existing_token_list(self) -> None:
        tokens = ["Sinh viên", "học", "xử lý", "."]
        self.assertTrue(contains_token(tokens, "sinh viên"))
        self.assertFalse(contains_token(tokens, "sinh"))

    def test_invalid_inputs_are_rejected(self) -> None:
        with self.assertRaises(TypeError):
            tokenize_vietnamese(None)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            contains_token("sinh viên", "sinh viên")
        with self.assertRaises(TypeError):
            contains_token(["sinh viên", 1], "sinh viên")  # type: ignore[list-item]
        with self.assertRaises(ValueError):
            contains_word("Sinh viên học.", "   ")


if __name__ == "__main__":
    unittest.main()
