"""Shared utilities for the Lab 01 text-processing exercises.

The functions in this module deliberately do not perform tokenization with a
language-specific library. They provide small, predictable building blocks
that can be reused by the English, Vietnamese, and document-indexing tasks.
"""

from __future__ import annotations

from collections.abc import Iterable
import unicodedata

__all__ = [
    "normalize_text",
    "remove_punctuation",
    "get_unique_words",
    "count_words",
    "count_document_frequency",
]


def _require_text(value: object, argument_name: str) -> str:
    """Validate and return a text argument."""

    if not isinstance(value, str):
        raise TypeError(
            f"{argument_name} must be a string, got {type(value).__name__}"
        )
    return value


def _clean_token(token: object, argument_name: str = "token") -> str:
    """Validate a token and remove surrounding whitespace."""

    return _require_text(token, argument_name).strip()


def normalize_text(text: str, *, lowercase: bool = True) -> str:
    """Normalize Unicode text and whitespace.

    The function applies Unicode NFKC normalization, optionally converts the
    text to lowercase, collapses consecutive whitespace characters to one
    space, and strips leading/trailing whitespace. Punctuation is preserved.

    Args:
        text: Source text to normalize.
        lowercase: Convert text to lowercase when ``True`` (the default).

    Returns:
        A normalized string.

    Raises:
        TypeError: If ``text`` is not a string or ``lowercase`` is not boolean.
    """

    value = _require_text(text, "text")
    if not isinstance(lowercase, bool):
        raise TypeError("lowercase must be a boolean")

    value = unicodedata.normalize("NFKC", value)
    if lowercase:
        value = value.lower()
    return " ".join(value.split())


def remove_punctuation(text: str, *, replacement: str = " ") -> str:
    """Replace Unicode punctuation with a replacement string.

    A space is used by default instead of deleting punctuation. This prevents
    text such as ``"information-retrieval"`` from becoming the single token
    ``"informationretrieval"``. Whitespace is normalized in the returned
    value. Set ``replacement=""`` when literal deletion is desired.

    Args:
        text: Source text.
        replacement: Text used for each punctuation character.

    Returns:
        Text with punctuation replaced and whitespace normalized.

    Raises:
        TypeError: If an argument has the wrong type.
    """

    value = _require_text(text, "text")
    replacement = _require_text(replacement, "replacement")
    value = unicodedata.normalize("NFKC", value)

    without_punctuation = "".join(
        replacement if unicodedata.category(character).startswith("P") else character
        for character in value
    )
    return " ".join(without_punctuation.split())


def get_unique_words(words: Iterable[str]) -> list[str]:
    """Return unique non-empty words in first-seen order.

    The function does not lowercase or otherwise normalize tokens. Callers
    should normalize the source text before tokenization when that behavior is
    required.
    """

    if isinstance(words, (str, bytes)):
        raise TypeError("words must be an iterable of tokens, not a string")

    unique_words: list[str] = []
    seen: set[str] = set()
    for index, word in enumerate(words):
        token = _clean_token(word, f"words[{index}]")
        if token and token not in seen:
            seen.add(token)
            unique_words.append(token)
    return unique_words


def count_words(words: Iterable[str]) -> dict[str, int]:
    """Count non-empty words while preserving first-seen key order.

    Tokens are stripped of surrounding whitespace but are otherwise kept as
    provided. In particular, this function does not change capitalization or
    punctuation by itself.
    """

    if isinstance(words, (str, bytes)):
        raise TypeError("words must be an iterable of tokens, not a string")

    frequencies: dict[str, int] = {}
    for index, word in enumerate(words):
        token = _clean_token(word, f"words[{index}]")
        if token:
            frequencies[token] = frequencies.get(token, 0) + 1
    return frequencies


def count_document_frequency(documents: Iterable[Iterable[str]]) -> dict[str, int]:
    """Count the number of distinct documents containing each word.

    A repeated word contributes at most one count per document. For example,
    ``[["python", "python"], ["python"]]`` returns ``{"python": 2}``.
    Keys retain the order in which they first appear across the documents.
    """

    if isinstance(documents, (str, bytes)):
        raise TypeError("documents must be an iterable of token iterables")

    document_frequencies: dict[str, int] = {}
    for document_index, document in enumerate(documents):
        if isinstance(document, (str, bytes)):
            raise TypeError(
                f"documents[{document_index}] must be an iterable of tokens, "
                "not a string"
            )

        for word in get_unique_words(document):
            document_frequencies[word] = document_frequencies.get(word, 0) + 1

    return document_frequencies
