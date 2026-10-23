"""Bài 4: Document frequency across a collection of documents.

Document frequency is different from word frequency: a word contributes at
most one count per document, even when it appears many times in that document.
"""

from __future__ import annotations

from collections.abc import Iterable

try:
    from .bai03_tan_so_tu import tokenize_document
    from .text_utils import count_document_frequency
except ImportError:  # Allow running this file directly as a script.
    from bai03_tan_so_tu import tokenize_document
    from text_utils import count_document_frequency


DEFAULT_DOCUMENTS = [
    "Python xử lý dữ liệu và văn bản.",
    "Python hỗ trợ tìm kiếm dữ liệu.",
    "Tìm kiếm thông tin giúp người dùng.",
    "Dữ liệu giúp xây dựng hệ thống thông tin.",
]


def tokenize_documents(documents: Iterable[str]) -> list[list[str]]:
    """Tokenize every document in a collection.

    The document order is preserved. Each item is passed through the same
    Vietnamese-aware tokenizer used by Bài 3.
    """

    if isinstance(documents, (str, bytes)):
        raise TypeError("documents must be an iterable of document strings")

    tokenized_documents: list[list[str]] = []
    for index, document in enumerate(documents, start=1):
        if not isinstance(document, str):
            raise TypeError(
                f"documents[{index}] must be a string, "
                f"got {type(document).__name__}"
            )
        tokenized_documents.append(tokenize_document(document))
    return tokenized_documents


def count_document_frequencies(documents: Iterable[str]) -> dict[str, int]:
    """Count the number of distinct documents containing each word.

    Repeated occurrences in one document count once. Empty documents are
    accepted and simply contribute no words.
    """

    tokenized_documents = tokenize_documents(documents)
    return count_document_frequency(tokenized_documents)


def sort_document_frequencies(
    frequencies: dict[str, int]
) -> list[tuple[str, int]]:
    """Sort document-frequency pairs by descending frequency and word."""

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


def format_document_frequency_table(documents: Iterable[str]) -> str:
    """Format documents and their document-frequency table for the CLI."""

    document_list = list(documents)
    tokenized_documents = tokenize_documents(document_list)
    frequencies = count_document_frequency(tokenized_documents)

    lines = ["Document collection:"]
    lines.extend(
        f"{index}. {document}" for index, document in enumerate(document_list, 1)
    )
    lines.extend(
        [
            "",
            "Document frequency:",
            "Word                         | Number of documents",
            "-----------------------------+--------------------",
        ]
    )
    lines.extend(
        f"{word:<29} | {frequency}"
        for word, frequency in sort_document_frequencies(frequencies)
    )
    return "\n".join(lines)


def main() -> None:
    """Run Bài 4 using the document collection defined in this file."""

    print("Bài 4 - Từ vựng và tần số tài liệu")
    print(format_document_frequency_table(DEFAULT_DOCUMENTS))


if __name__ == "__main__":
    main()
