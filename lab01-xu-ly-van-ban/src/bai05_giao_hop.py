"""Bài 5: Intersection and union of sorted integer lists.

The implementation uses the two-pointer technique. It therefore runs in
O(n + m) time for lists of lengths n and m and does not need to build sets.
"""

from __future__ import annotations

from collections.abc import Iterable


DEFAULT_FIRST_LIST = [1, 3, 5, 7, 9]
DEFAULT_SECOND_LIST = [2, 3, 5, 8, 9]


def _validate_sorted_integers(
    values: Iterable[int], name: str
) -> list[int]:
    """Materialize and validate a non-decreasing integer sequence."""

    if isinstance(values, (str, bytes)):
        raise TypeError(f"{name} must be an iterable of integers")

    result: list[int] = []
    for index, value in enumerate(values):
        if isinstance(value, bool) or not isinstance(value, int):
            raise TypeError(
                f"{name}[{index}] must be an integer, "
                f"got {type(value).__name__}"
            )
        if result and value < result[-1]:
            raise ValueError(f"{name} must be sorted in non-decreasing order")
        result.append(value)
    return result


def intersection_sorted(
    first: Iterable[int], second: Iterable[int]
) -> list[int]:
    """Return the unique sorted intersection of two integer sequences.

    Inputs may contain repeated values as long as they are non-decreasing. The
    result is set-like: every common integer appears once.
    """

    left = _validate_sorted_integers(first, "first")
    right = _validate_sorted_integers(second, "second")
    result: list[int] = []
    left_index = 0
    right_index = 0

    while left_index < len(left) and right_index < len(right):
        left_value = left[left_index]
        right_value = right[right_index]

        if left_value == right_value:
            if not result or result[-1] != left_value:
                result.append(left_value)
            left_index += 1
            right_index += 1
        elif left_value < right_value:
            left_index += 1
        else:
            right_index += 1

    return result


def union_sorted(first: Iterable[int], second: Iterable[int]) -> list[int]:
    """Return the unique sorted union of two integer sequences.

    Inputs may contain repeated values as long as they are non-decreasing. The
    result contains every value from either input exactly once.
    """

    left = _validate_sorted_integers(first, "first")
    right = _validate_sorted_integers(second, "second")
    result: list[int] = []
    left_index = 0
    right_index = 0

    def append_once(value: int) -> None:
        if not result or result[-1] != value:
            result.append(value)

    while left_index < len(left) and right_index < len(right):
        left_value = left[left_index]
        right_value = right[right_index]

        if left_value == right_value:
            append_once(left_value)
            left_index += 1
            right_index += 1
        elif left_value < right_value:
            append_once(left_value)
            left_index += 1
        else:
            append_once(right_value)
            right_index += 1

    while left_index < len(left):
        append_once(left[left_index])
        left_index += 1

    while right_index < len(right):
        append_once(right[right_index])
        right_index += 1

    return result


def parse_integer_list(raw_text: str) -> list[int]:
    """Parse integers separated by spaces, commas, or both.

    An empty input represents an empty list. This helper is used only by the
    command-line interface; the core algorithms accept iterable integers.
    """

    if not isinstance(raw_text, str):
        raise TypeError(
            f"raw_text must be a string, got {type(raw_text).__name__}"
        )

    normalized = raw_text.replace(",", " ")
    if not normalized.strip():
        return []

    values: list[int] = []
    for index, item in enumerate(normalized.split(), start=1):
        try:
            values.append(int(item))
        except ValueError as error:
            raise ValueError(
                f"item {index} ({item!r}) is not a valid integer"
            ) from error
    return values


def format_set_operations(
    first: Iterable[int], second: Iterable[int]
) -> str:
    """Format both set-like operations for display."""

    first_list = _validate_sorted_integers(first, "first")
    second_list = _validate_sorted_integers(second, "second")
    intersection = intersection_sorted(first_list, second_list)
    union = union_sorted(first_list, second_list)
    return "\n".join(
        [
            f"Danh sách 1: {first_list}",
            f"Danh sách 2: {second_list}",
            f"Giao: {intersection}",
            f"Hợp: {union}",
        ]
    )


def main() -> None:
    """Run the interactive demonstration for Bài 5."""

    print("Bài 5 - Giao và hợp hai danh sách số nguyên")
    print("Nhập số nguyên cách nhau bằng dấu cách hoặc dấu phẩy.")
    try:
        first_raw = input("Danh sách 1: ")
        second_raw = input("Danh sách 2: ")
    except EOFError:
        first_raw = ""
        second_raw = ""

    try:
        first = parse_integer_list(first_raw)
        second = parse_integer_list(second_raw)
        print()
        print(format_set_operations(first, second))
    except (TypeError, ValueError) as error:
        print(f"Dữ liệu không hợp lệ: {error}")


if __name__ == "__main__":
    main()
