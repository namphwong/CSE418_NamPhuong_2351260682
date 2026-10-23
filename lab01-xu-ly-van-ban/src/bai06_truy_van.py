"""Bài 6: Build an inverted index and search a Vietnamese document set.

The program reads UTF-8 text files, keeps their full contents in memory, and
builds an index with the shape ``word -> sorted list of document IDs``.
"""

from __future__ import annotations

from collections.abc import Mapping
from pathlib import Path
import re

try:
    from .bai03_tan_so_tu import tokenize_document
    from .text_utils import get_unique_words, normalize_text
except ImportError:  # Allow running this file directly as a script.
    from bai03_tan_so_tu import tokenize_document
    from text_utils import get_unique_words, normalize_text


DEFAULT_DOCUMENT_DIRECTORY = (
    Path(__file__).resolve().parents[1] / "data" / "documents"
)
DOCUMENT_ID_PATTERN = re.compile(r"^(\d+)_")


def _document_id_from_path(path: Path) -> int:
    """Extract a positive numeric ID from a document filename."""

    match = DOCUMENT_ID_PATTERN.match(path.stem)
    if match is None:
        raise ValueError(
            f"document filename must start with '<id>_': {path.name}"
        )

    document_id = int(match.group(1))
    if document_id <= 0:
        raise ValueError(f"document ID must be positive: {path.name}")
    return document_id


def load_documents(folder_path: str | Path) -> dict[int, str]:
    """Read all numbered UTF-8 text documents from a directory.

    Files are sorted by their numeric filename prefix and returned as an
    insertion-ordered dictionary mapping document ID to full document text.
    """

    folder = Path(folder_path)
    if not folder.exists():
        raise FileNotFoundError(f"document directory does not exist: {folder}")
    if not folder.is_dir():
        raise NotADirectoryError(f"document path is not a directory: {folder}")

    paths = list(folder.glob("*.txt"))
    if not paths:
        raise ValueError(f"no .txt documents found in: {folder}")

    paths.sort(key=lambda path: (_document_id_from_path(path), path.name))
    documents: dict[int, str] = {}
    for path in paths:
        document_id = _document_id_from_path(path)
        if document_id in documents:
            raise ValueError(f"duplicate document ID {document_id}: {path.name}")
        documents[document_id] = path.read_text(encoding="utf-8")
    return documents


def build_inverted_index(documents: Mapping[int, str]) -> dict[str, list[int]]:
    """Build ``token -> sorted document IDs`` from in-memory documents.

    Each token is added at most once for a document. The document-frequency
    list is therefore also a postings list suitable for later query work.
    """

    if not isinstance(documents, Mapping):
        raise TypeError("documents must be a mapping of integer IDs to text")

    index: dict[str, list[int]] = {}
    for document_id in sorted(documents):
        if isinstance(document_id, bool) or not isinstance(document_id, int):
            raise TypeError("document IDs must be integers")
        if document_id <= 0:
            raise ValueError("document IDs must be positive")

        text = documents[document_id]
        if not isinstance(text, str):
            raise TypeError(
                f"documents[{document_id}] must be a string, "
                f"got {type(text).__name__}"
            )

        tokens = tokenize_document(text)
        for token in get_unique_words(tokens):
            index.setdefault(token, []).append(document_id)

    return index


def search_index(index: Mapping[str, list[int]], query: str) -> list[int]:
    """Return document IDs containing an exact normalized query token."""

    if not isinstance(index, Mapping):
        raise TypeError("index must be a mapping of tokens to document IDs")
    if not isinstance(query, str):
        raise TypeError(f"query must be a string, got {type(query).__name__}")

    normalized_query = normalize_text(query)
    if not normalized_query:
        raise ValueError("query must not be empty")

    postings = index.get(normalized_query, [])
    return list(postings)


def get_document(documents: Mapping[int, str], document_id: int) -> str:
    """Return the full text for a document ID."""

    if isinstance(document_id, bool) or not isinstance(document_id, int):
        raise TypeError("document_id must be an integer")
    try:
        return documents[document_id]
    except KeyError as error:
        raise KeyError(f"document ID not found: {document_id}") from error


def format_query_result(
    query: str, document_ids: list[int], documents: Mapping[int, str]
) -> str:
    """Format query results and optionally the selected full document."""

    lines = [f"Query: {query}"]
    if not document_ids:
        lines.append("Documents: (none)")
        return "\n".join(lines)

    lines.append(
        "Documents: " + ", ".join(str(document_id) for document_id in document_ids)
    )
    return "\n".join(lines)


def _read_document_id(raw_value: str) -> int | None:
    """Parse an optional document ID entered at the CLI."""

    if not raw_value.strip():
        return None
    try:
        return int(raw_value.strip())
    except ValueError as error:
        raise ValueError("document ID must be an integer") from error


def main(folder_path: str | Path = DEFAULT_DOCUMENT_DIRECTORY) -> None:
    """Run the interactive query program."""

    print("Bài 6 - Truy vấn tài liệu")
    try:
        documents = load_documents(folder_path)
        index = build_inverted_index(documents)
    except (FileNotFoundError, NotADirectoryError, ValueError, OSError) as error:
        print(f"Không thể nạp tài liệu: {error}")
        return

    print(f"Đã nạp {len(documents)} tài liệu.")
    print(f"Từ điển chỉ mục có {len(index)} token.")
    print("Nhập q để thoát.")

    while True:
        try:
            query = input("\nTừ truy vấn: ").strip()
        except EOFError:
            break
        if query.lower() in {"q", "quit", "exit"}:
            break
        if not query:
            print("Từ truy vấn không được để trống.")
            continue

        document_ids = search_index(index, query)
        print(format_query_result(query, document_ids, documents))
        if not document_ids:
            continue

        try:
            raw_document_id = input(
                "Chọn ID tài liệu để xem toàn văn (Enter để bỏ qua): "
            )
            selected_id = _read_document_id(raw_document_id)
            if selected_id is None:
                continue
            print(f"\nToàn văn tài liệu {selected_id}:")
            print(get_document(documents, selected_id))
        except (EOFError, TypeError, ValueError, KeyError) as error:
            print(f"Lựa chọn không hợp lệ: {error}")


if __name__ == "__main__":
    main()
