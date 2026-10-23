"""Tests for Bài 5 sorted-list set operations."""

from __future__ import annotations

import unittest

from src.bai05_giao_hop import (
    intersection_sorted,
    parse_integer_list,
    union_sorted,
)


class SortedListOperationsTests(unittest.TestCase):
    def test_intersection_and_union_basic_case(self) -> None:
        first = [1, 3, 5, 7, 9]
        second = [2, 3, 5, 8, 9]
        self.assertEqual(intersection_sorted(first, second), [3, 5, 9])
        self.assertEqual(union_sorted(first, second), [1, 2, 3, 5, 7, 8, 9])

    def test_empty_lists(self) -> None:
        self.assertEqual(intersection_sorted([], [1, 2]), [])
        self.assertEqual(union_sorted([], [1, 2]), [1, 2])
        self.assertEqual(union_sorted([], []), [])

    def test_disjoint_lists(self) -> None:
        self.assertEqual(intersection_sorted([1, 3], [2, 4]), [])
        self.assertEqual(union_sorted([1, 3], [2, 4]), [1, 2, 3, 4])

    def test_duplicate_values_are_deduplicated_in_results(self) -> None:
        first = [1, 1, 2, 4, 4]
        second = [1, 2, 2, 3, 4]
        self.assertEqual(intersection_sorted(first, second), [1, 2, 4])
        self.assertEqual(union_sorted(first, second), [1, 2, 3, 4])

    def test_negative_and_zero_values(self) -> None:
        first = [-5, -1, 0, 4]
        second = [-3, -1, 0, 8]
        self.assertEqual(intersection_sorted(first, second), [-1, 0])
        self.assertEqual(union_sorted(first, second), [-5, -3, -1, 0, 4, 8])

    def test_input_iterables_are_supported_without_mutation(self) -> None:
        first = [1, 2, 5]
        second = [2, 3, 5]
        first_snapshot = first.copy()
        second_snapshot = second.copy()
        self.assertEqual(union_sorted(iter(first), iter(second)), [1, 2, 3, 5])
        self.assertEqual(first, first_snapshot)
        self.assertEqual(second, second_snapshot)

    def test_parser_accepts_spaces_and_commas(self) -> None:
        self.assertEqual(parse_integer_list("1, 3 5,7"), [1, 3, 5, 7])
        self.assertEqual(parse_integer_list("   "), [])
        self.assertEqual(parse_integer_list("-2, 0, 8"), [-2, 0, 8])

    def test_invalid_input_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            intersection_sorted([1, 4, 3], [1, 2])
        with self.assertRaises(ValueError):
            union_sorted([1, 2], [3, 1])
        with self.assertRaises(TypeError):
            intersection_sorted("1 2", [1, 2])
        with self.assertRaises(TypeError):
            union_sorted([1, True], [1, 2])
        with self.assertRaises(ValueError):
            parse_integer_list("1, two, 3")


if __name__ == "__main__":
    unittest.main()
