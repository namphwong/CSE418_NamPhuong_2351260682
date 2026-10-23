"""Bài 1: English tokenization and Porter stemming with NLTK.

This module keeps tokenization and stemming as separate operations so the
intermediate token list can be inspected, tested, and reused in later labs.
"""

from __future__ import annotations

from collections.abc import Iterable

from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize


DEFAULT_ENGLISH_TEXT = (
    "Information retrieval systems process documents. "
    "The systems retrieve relevant information quickly."
)


def tokenize_english(text: str) -> list[str]:
    """Split an English document into NLTK word and punctuation tokens.

    ``word_tokenize`` intentionally returns punctuation as tokens too. This
    mirrors the assignment requirement and makes the tokenization result
    visible instead of silently discarding information.

    Args:
        text: English document to tokenize.

    Returns:
        Tokens returned by NLTK's Punkt tokenizer.

    Raises:
        TypeError: If ``text`` is not a string.
        RuntimeError: If the required NLTK tokenizer data is unavailable.
    """

    if not isinstance(text, str):
        raise TypeError(f"text must be a string, got {type(text).__name__}")

    try:
        return word_tokenize(text, language="english")
    except LookupError as error:
        raise RuntimeError(
            "NLTK tokenizer data is missing. Run "
            "python -c \"import nltk; nltk.download('popular')\" "
            "inside the project environment."
        ) from error


def stem_tokens(tokens: Iterable[str]) -> list[str]:
    """Apply the Porter stemming algorithm to each token.

    The output has exactly the same length and order as the input. Punctuation
    tokens are passed to the stemmer as returned by NLTK, so the relationship
    between every token and its stem remains explicit.
    """

    if isinstance(tokens, (str, bytes)):
        raise TypeError("tokens must be an iterable of tokens, not a string")

    stemmer = PorterStemmer()
    stems: list[str] = []
    for index, token in enumerate(tokens):
        if not isinstance(token, str):
            raise TypeError(
                f"tokens[{index}] must be a string, got {type(token).__name__}"
            )
        stems.append(stemmer.stem(token))
    return stems


def analyze_english_text(text: str) -> tuple[list[str], list[str]]:
    """Tokenize an English document and stem its tokens.

    Returns:
        A pair ``(tokens, stems)``. ``tokens[i]`` corresponds to
        ``stems[i]`` for every valid index ``i``.
    """

    tokens = tokenize_english(text)
    return tokens, stem_tokens(tokens)


def format_analysis(text: str) -> str:
    """Format a readable token/stem table for the command-line program."""

    tokens, stems = analyze_english_text(text)
    lines = [
        "Document:",
        text,
        "",
        "Tokenization and Porter stemming:",
        "No. | Token                    | Stem",
        "----+--------------------------+--------------------------",
    ]
    lines.extend(
        f"{index:>3} | {token:<24} | {stem}"
        for index, (token, stem) in enumerate(zip(tokens, stems), start=1)
    )
    return "\n".join(lines)


def main() -> None:
    """Run the interactive demonstration for Bài 1."""

    print("Bài 1 - Tách từ tiếng Anh và Porter stemming")
    print("Nhập một đoạn văn tiếng Anh; để trống để dùng văn bản mẫu.")
    try:
        user_text = input("Text: ").strip()
    except EOFError:
        user_text = ""

    text = user_text or DEFAULT_ENGLISH_TEXT
    print()
    print(format_analysis(text))


if __name__ == "__main__":
    main()
