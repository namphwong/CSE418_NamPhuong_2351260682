"""Các hàm dùng chung cho các bài thực hành Whoosh."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Iterable

from pyvi import ViTokenizer
from whoosh.fields import ID, TEXT, Schema
from whoosh.filedb.filestore import FileStorage
from whoosh.index import FileIndex, create_in
from whoosh.qparser import QueryParser


def basic_schema() -> Schema:
    """Tạo schema theo ví dụ của tài liệu thực hành."""

    return Schema(
        title=TEXT(stored=True),
        path=ID(stored=True),
        content=TEXT,
    )


def document_schema() -> Schema:
    """Tạo schema cho Bài 3.

    Chỉ mã tài liệu và tiêu đề được lưu. Nội dung được đưa vào inverted index
    để tìm kiếm nhưng không lưu trong index.
    """

    return Schema(
        doc_id=ID(stored=True),
        title=TEXT(stored=True),
        content=TEXT,
    )


def create_index(index_dir: str | Path, schema: Schema) -> FileIndex:
    """Tạo mới một index trong thư mục chỉ định."""

    path = Path(index_dir)
    path.mkdir(parents=True, exist_ok=True)
    return create_in(str(path), schema)


def open_index(index_dir: str | Path) -> FileIndex:
    """Mở một index đã tồn tại."""

    # Tắt mmap khi đọc để các file segment được giải phóng sạch trên Windows
    # sau khi Searcher đóng, nhất là trong các test dùng thư mục tạm.
    storage = FileStorage(str(Path(index_dir)), supports_mmap=False)
    return FileIndex(storage)


def tokenize_vietnamese(text: str) -> str:
    """Tách từ ghép tiếng Việt bằng PyVI.

    Ví dụ ``Đại học Thủy Lợi`` trở thành ``Đại_học Thủy_Lợi``.
    """

    if not isinstance(text, str):
        raise TypeError("text phải là chuỗi")
    stripped = text.strip()
    return ViTokenizer.tokenize(stripped) if stripped else ""


def search_index(
    index: FileIndex,
    query_text: str,
    *,
    field: str = "content",
) -> list[dict[str, Any]]:
    """Phân tích và thực thi một truy vấn, trả về các stored fields."""

    if not isinstance(query_text, str):
        raise TypeError("query_text phải là chuỗi")
    if not query_text.strip():
        return []

    parser = QueryParser(field, schema=index.schema)
    query = parser.parse(query_text)
    with index.searcher() as searcher:
        results = searcher.search(query, limit=None)
        return [dict(result) for result in results]


def commit_documents(index: FileIndex, documents: Iterable[dict[str, str]]) -> None:
    """Ghi các document có field phù hợp vào index và commit."""

    writer = index.writer()
    try:
        for document in documents:
            writer.add_document(**document)
        writer.commit()
    except Exception:
        writer.cancel()
        raise

