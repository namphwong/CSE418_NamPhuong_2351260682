import unittest
from src.bai03_tan_so_tu import tokenize_document, count_word_frequency
from src.bai04_tan_so_tai_lieu import count_document_frequencies
from src.bai06_truy_van import build_inverted_index, search_index
from src.bai02_tach_tu_tieng_viet import contains_word

class RegressionTests(unittest.TestCase):
    def test_sentence_boundaries(self):
        text = "Tôi thích học. Sinh viên thích Python."
        self.assertEqual(tokenize_document(text), ["tôi", "thích", "học", "sinh viên", "thích", "python"])
        self.assertEqual(tokenize_document("Máy tính. Toán học."), tokenize_document("Máy tính.") + tokenize_document("Toán học."))
        self.assertEqual(count_word_frequency(text)["thích"], 2)
        df = count_document_frequencies([text, "Sinh viên học."])
        self.assertEqual(df["sinh viên"], 2)
        index = build_inverted_index({1: text})
        for word in ["học", "sinh viên"]:
            self.assertEqual(search_index(index, word), [1])
        self.assertEqual(search_index(index, "học sinh viên"), [])
    def test_punctuation_is_not_a_word(self):
        for query in [".", "!!!"]:
            self.assertFalse(contains_word("Sinh viên học.", query))
