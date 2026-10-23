"""Bài 3: chương trình tìm kiếm hoàn chỉnh trên 10 tài liệu tiếng Việt."""

from __future__ import annotations

from pathlib import Path
from typing import Callable, Iterable

try:
    from .data import DEFAULT_DOCUMENTS, Document, get_document
    from .whoosh_common import create_index, document_schema, open_index, search_index, tokenize_vietnamese
except ImportError:  # pragma: no cover
    from data import DEFAULT_DOCUMENTS, Document, get_document
    from whoosh_common import create_index, document_schema, open_index, search_index, tokenize_vietnamese


DEFAULT_INDEX_DIR = Path(__file__).resolve().parents[1] / "indexdir-bai03"


def build_index(
    index_dir: str | Path = DEFAULT_INDEX_DIR,
    documents: Iterable[Document] = DEFAULT_DOCUMENTS,
) -> Path:
    """Xây dựng inverted index cho tập tài liệu D.

    Chỉ ``doc_id`` và ``title`` được lưu. ``content`` chỉ được phân tích để
    tạo postings và không được lưu trong stored fields.
    """

    index = create_index(index_dir, document_schema())
    writer = index.writer()
    try:
        for document in documents:
            writer.add_document(
                doc_id=str(document.document_id),
                title=document.title,
                content=tokenize_vietnamese(document.content),
            )
        writer.commit()
    except Exception:
        writer.cancel()
        raise
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


def run_cli(
    index_dir: str | Path = DEFAULT_INDEX_DIR,
    *,
    input_fn: Callable[[str], str] = input,
    output_fn: Callable[[str], None] = print,
    documents: tuple[Document, ...] = DEFAULT_DOCUMENTS,
) -> None:
    """Chạy vòng lặp nhập truy vấn, chọn kết quả và xem toàn văn."""

    build_index(index_dir, documents)
    output_fn("Đã xây dựng chỉ mục ngược cho 10 tài liệu.")
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

        raw_selection = input_fn("Nhập số thứ tự kết quả để xem nội dung: ").strip()
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


def main() -> None:
    run_cli()


if __name__ == "__main__":
    main()

