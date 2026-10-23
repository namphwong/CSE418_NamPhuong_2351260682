"""Bài 2: Vietnamese word segmentation and membership checking.

Underthesea is used for Vietnamese word segmentation. Its list format keeps
multi-syllable words such as ``"sinh viên"`` and ``"xử lý"`` together, which
is the form used when matching a query against the token list.
"""

from __future__ import annotations

from collections.abc import Iterable

from underthesea import word_tokenize

try:
    from .text_utils import normalize_text
except ImportError:  # Allow running this file directly as a script.
    from text_utils import normalize_text


DEFAULT_VIETNAMESE_TEXT = (
    "Sinh viên học xử lý văn bản tiếng Việt. "
    "Bài thực hành giúp sinh viên hiểu cách tách từ."
)


def tokenize_vietnamese(text: str) -> list[str]:
    """Segment Vietnamese text into Underthesea tokens.

    The explicit ``format="list"`` option is used so the function returns a
    list suitable for membership checks. Multi-syllable words remain one token
    represented with an internal space, for example ``"văn bản"``.

    Args:
        text: Vietnamese document containing one or more sentences.

    Returns:
        A list of Vietnamese word and punctuation tokens.

    Raises:
        TypeError: If ``text`` is not a string.
    """

    if not isinstance(text, str):
        raise TypeError(f"text must be a string, got {type(text).__name__}")
    return word_tokenize(text, format="list")


def contains_token(tokens: Iterable[str], query: str) -> bool:
    """Check whether a normalized query is an exact token in ``tokens``.

    Matching is case-insensitive and collapses whitespace through
    :func:`normalize_text`. The query must match a complete token; for
    example, ``"xử lý"`` matches the token ``"xử lý"``, while ``"xử"`` does
    not match that multi-syllable token.

    Args:
        tokens: Iterable of tokens produced by the tokenizer.
        query: Word or multi-syllable word to find.

    Returns:
        ``True`` if the query is present, otherwise ``False``.

    Raises:
        TypeError: If ``tokens``, a token, or ``query`` has the wrong type.
        ValueError: If ``query`` is empty after normalization.
    """

    if isinstance(tokens, (str, bytes)):
        raise TypeError("tokens must be an iterable of tokens, not a string")

    normalized_query = normalize_text(query)
    if not normalized_query:
        raise ValueError("query must not be empty")

    normalized_tokens: list[str] = []
    for index, token in enumerate(tokens):
        if not isinstance(token, str):
            raise TypeError(
                f"tokens[{index}] must be a string, got {type(token).__name__}"
            )
        normalized_tokens.append(normalize_text(token))

    return normalized_query in normalized_tokens


def contains_word(document: str, query: str) -> bool:
    """Tokenize a Vietnamese document and check whether ``query`` is present."""

    return contains_token(tokenize_vietnamese(document), query)


def analyze_vietnamese_text(
    document: str, query: str
) -> tuple[list[str], bool]:
    """Return the token list and query-membership result for a document."""

    tokens = tokenize_vietnamese(document)
    return tokens, contains_token(tokens, query)


def format_analysis(document: str, query: str) -> str:
    """Format tokenization and membership results for the CLI."""

    tokens, found = analyze_vietnamese_text(document, query)
    lines = [
        "Document:",
        document,
        "",
        "Vietnamese tokens:",
        "No. | Token",
        "----+--------------------------",
    ]
    lines.extend(
        f"{index:>3} | {token}"
        for index, token in enumerate(tokens, start=1)
    )
    lines.extend(
        [
            "",
            f"Query: {query}",
            f"Result: {'FOUND' if found else 'NOT FOUND'}",
        ]
    )
    return "\n".join(lines)


def main() -> None:
    """Run the interactive demonstration for Bài 2."""

    print("Bài 2 - Tách từ tiếng Việt và kiểm tra từ")
    print("Để trống văn bản để dùng văn bản mẫu.")
    try:
        user_document = input("Document: ").strip()
    except EOFError:
        user_document = ""

    document = user_document or DEFAULT_VIETNAMESE_TEXT
    try:
        query = input("Query: ").strip()
    except EOFError:
        query = ""
    if not query:
        print("Query không được để trống.")
        return

    print()
    print(format_analysis(document, query))


if __name__ == "__main__":
    main()
