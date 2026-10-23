"""Bài 3: Count word frequency in a document.

The default pipeline is Vietnamese-aware and uses Underthesea so multi-
syllable words remain one token. Punctuation-only tokens are removed before
the frequency dictionary is built.
"""

from __future__ import annotations

from collections.abc import Iterable
from typing import Literal

from underthesea import word_tokenize as vietnamese_word_tokenize

try:
    from .text_utils import count_words, normalize_text, remove_punctuation
except ImportError:  # Allow running this file directly as a script.
    from text_utils import count_words, normalize_text, remove_punctuation

Language = Literal["vietnamese", "whitespace"]

DEFAULT_DOCUMENT = (
    "Xử lý văn bản là bước quan trọng. "
    "Xử lý văn bản giúp máy tính tìm kiếm thông tin."
)


def _is_word_token(token: str) -> bool:
    """Return whether a token contains at least one letter or digit."""

    return any(character.isalpha() or character.isdigit() for character in token)


def tokenize_document(
    text: str, *, language: Language = "vietnamese"
) -> list[str]:
    """Normalize and tokenize a document for frequency counting.

    Args:
        text: Document to tokenize.
        language: ``"vietnamese"`` uses Underthesea and keeps multi-syllable
            words together. ``"whitespace"`` uses normalized whitespace
            splitting for language-independent simple input.

    Returns:
        Lowercase, non-empty word tokens. Punctuation-only tokens are removed.

    Raises:
        TypeError: If ``text`` is not a string.
        ValueError: If ``language`` is unsupported.
    """

    if not isinstance(text, str):
        raise TypeError(f"text must be a string, got {type(text).__name__}")
    if language not in ("vietnamese", "whitespace"):
        raise ValueError(
            f"unsupported language {language!r}; use 'vietnamese' or 'whitespace'"
        )

    normalized_text = normalize_text(remove_punctuation(text))
    if not normalized_text:
        return []

    if language == "vietnamese":
        raw_tokens: Iterable[str] = vietnamese_word_tokenize(
            normalized_text, format="list"
        )
    else:
        raw_tokens = normalized_text.split()

    tokens: list[str] = []
    for token in raw_tokens:
        normalized_token = normalize_text(token)
        if normalized_token and _is_word_token(normalized_token):
            tokens.append(normalized_token)
    return tokens


def count_word_frequency(
    text: str, *, language: Language = "vietnamese"
) -> dict[str, int]:
    """Return a dictionary mapping each word to its occurrence count."""

    return count_words(tokenize_document(text, language=language))


def sort_frequencies(frequencies: dict[str, int]) -> list[tuple[str, int]]:
    """Sort frequency pairs by descending count, then alphabetically.

    Deterministic sorting makes command-line output and future tests easier to
    compare. The input dictionary is not modified.
    """

    if not isinstance(frequencies, dict):
        raise TypeError(
            f"frequencies must be a dictionary, got {type(frequencies).__name__}"
        )
    for word, frequency in frequencies.items():
        if not isinstance(word, str):
            raise TypeError("frequency dictionary keys must be strings")
        if not isinstance(frequency, int):
            raise TypeError("frequency dictionary values must be integers")
        if frequency < 0:
            raise ValueError("frequency values must not be negative")

    return sorted(frequencies.items(), key=lambda item: (-item[1], item[0]))


def format_frequency_table(
    text: str, *, language: Language = "vietnamese"
) -> str:
    """Format the token list and word-frequency dictionary for the CLI."""

    tokens = tokenize_document(text, language=language)
    frequencies = count_words(tokens)
    lines = [
        "Document:",
        text,
        "",
        f"Tokens ({len(tokens)}):",
        ", ".join(tokens) if tokens else "(none)",
        "",
        f"Unique words ({len(frequencies)}):",
        "Word                         | Frequency",
        "-----------------------------+----------",
    ]
    lines.extend(
        f"{word:<29} | {frequency}"
        for word, frequency in sort_frequencies(frequencies)
    )
    return "\n".join(lines)


def main() -> None:
    """Run the interactive demonstration for Bài 3."""

    print("Bài 3 - Tần số từ")
    print("Nhập một tài liệu; để trống để dùng văn bản mẫu.")
    try:
        user_text = input("Document: ").strip()
    except EOFError:
        user_text = ""

    text = user_text or DEFAULT_DOCUMENT
    print()
    print(format_frequency_table(text))


if __name__ == "__main__":
    main()
