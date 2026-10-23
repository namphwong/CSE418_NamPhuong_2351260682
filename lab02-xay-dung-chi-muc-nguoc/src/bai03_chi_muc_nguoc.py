"""Bài 3: chương trình tìm kiếm hoàn chỉnh trên 10 tài liệu tiếng Việt."""

from __future__ import annotations

from pathlib import Path
from typing import Callable, Iterable

try:
    from .data import DEFAULT_DOCUMENTS, Document, get_document
    from .whoosh_common import rebuild_index, document_schema, open_index, search_index, tokenize_vietnamese
except ImportError:  # pragma: no cover
    from data import DEFAULT_DOCUMENTS, Document, get_document
    from whoosh_common import rebuild_index, document_schema, open_index, search_index, tokenize_vietnamese


DEFAULT_INDEX_DIR = Path(__file__).resolve().parents[1] / "indexdir-bai03"


def build_index(
    index_dir: str | Path = DEFAULT_INDEX_DIR,
    documents: Iterable[Document] = DEFAULT_DOCUMENTS,
) -> Path:
    """Xây dựng inverted index cho tập tài liệu D.

    Chỉ ``doc_id`` và ``title`` được lưu. ``content`` chỉ được phân tích để
    tạo postings và không được lưu trong stored fields.
    """

    documents = tuple(documents)
    ids = [d.document_id for d in documents]
    if any(type(i) is not int or i <= 0 for i in ids) or len(set(ids)) != len(ids):
        raise ValueError("Mã tài liệu phải là số nguyên dương và không trùng.")
    rebuild_index(index_dir, document_schema(), (
        dict(doc_id=str(d.document_id), title=d.title, content=tokenize_vietnamese(d.content))
        for d in documents
    ))
    return Path(index_dir)


def search_documents(
    query_text: str,
    index_dir: str | Path = DEFAULT_INDEX_DIR,
) -> list[dict[str, str]]:
    """Tách từ truy vấn và trả về các kết quả có mã, tiêu đề."""

    index = open_index(index_dir)
    try:
        return search_index(index, tokenize_vietnamese(query_text))
    finally:
        index.close()


def result_document(
    result: dict[str, str],
    documents: tuple[Document, ...] = DEFAULT_DOCUMENTS,
) -> Document:
    """Ánh xạ một kết quả Whoosh về toàn văn trong danh sách D."""

    return get_document(documents, int(result["doc_id"]))


def format_results(results: list[dict[str, str]]) -> list[str]:
    """Định dạng kết quả theo số thứ tự bắt đầu từ 1."""

    lines = [f"Số kết quả: {len(results)}"]
    lines.extend(
        f"{number}. {result['title']} [mã tài liệu: {result['doc_id']}]"
        for number, result in enumerate(results, start=1)
    )
    return lines


def _end_on_input_close(function):
    from functools import wraps
    @wraps(function)
    def wrapped(*args, **kwargs):
        try:
            return function(*args, **kwargs)
        except (EOFError, KeyboardInterrupt):
            kwargs.get("output_fn", print)("Đã kết thúc chương trình.")
    return wrapped


@_end_on_input_close
def run_cli(
    index_dir: str | Path = DEFAULT_INDEX_DIR,
    *,
    input_fn: Callable[[str], str] = input,
    output_fn: Callable[[str], None] = print,
    documents: tuple[Document, ...] = DEFAULT_DOCUMENTS,
) -> None:
    """Chạy vòng lặp nhập truy vấn, chọn kết quả và xem toàn văn."""

    build_index(index_dir, documents)
    output_fn(f"Đã xây dựng chỉ mục ngược cho {len(documents)} tài liệu.")
    output_fn("Nhập q, quit hoặc exit để kết thúc.")

    while True:
        raw_query = input_fn("Nhập câu truy vấn gồm nhiều từ: ").strip()
        if raw_query.lower() in {"q", "quit", "exit"}:
            output_fn("Đã kết thúc chương trình.")
            return
        if not raw_query:
            output_fn("Câu truy vấn không được rỗng.")
            continue

        results = search_documents(raw_query, index_dir)
        for line in format_results(results):
            output_fn(line)
        if not results:
            output_fn("Không có tài liệu phù hợp.")
            continue

        while True:
            raw_selection = input_fn("Nhập số thứ tự kết quả để xem nội dung: ").strip()
            if raw_selection.lower() in {"q", "quit", "exit"}:
                output_fn("Đã kết thúc chương trình.")
                return
            try:
                selection = int(raw_selection)
            except ValueError:
                output_fn("Số thứ tự phải là một số nguyên.")
                continue
            if not 1 <= selection <= len(results):
                output_fn(f"Số thứ tự phải nằm trong khoảng 1 đến {len(results)}.")
                continue

            selected = result_document(results[selection - 1], documents)
            output_fn(f"\nNội dung tài liệu {selected.document_id} - {selected.title}:")
            output_fn(selected.content)

            break


def main() -> None:
    run_cli()


if __name__ == "__main__":
    main()
