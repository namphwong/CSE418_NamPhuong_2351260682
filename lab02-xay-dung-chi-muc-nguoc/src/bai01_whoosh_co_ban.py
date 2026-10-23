"""Bài 1: tạo index, thêm tài liệu và tìm kiếm bằng Whoosh."""

from __future__ import annotations

from pathlib import Path

try:  # Cho phép chạy bằng cả `python -m src...` và `python src\...py`.
    from .whoosh_common import basic_schema, commit_documents, create_index, open_index, search_index
except ImportError:  # pragma: no cover
    from whoosh_common import basic_schema, commit_documents, create_index, open_index, search_index


DEMO_DOCUMENTS = (
    {
        "title": "First document",
        "path": "/a",
        "content": "This is the first document we've added!",
    },
    {
        "title": "Second document",
        "path": "/b",
        "content": "The second one is even more interesting!",
    },
)

DEFAULT_INDEX_DIR = Path(__file__).resolve().parents[1] / "indexdir-bai01"


def build_demo_index(index_dir: str | Path = DEFAULT_INDEX_DIR) -> Path:
    """Tạo lại index mẫu và trả về đường dẫn index."""

    index = create_index(index_dir, basic_schema())
    commit_documents(index, DEMO_DOCUMENTS)
    return Path(index_dir)


def search_demo(query_text: str, index_dir: str | Path = DEFAULT_INDEX_DIR) -> list[dict[str, str]]:
    """Tìm trong index mẫu đã được tạo."""

    index = open_index(index_dir)
    try:
        return search_index(index, query_text)
    finally:
        index.close()


def main() -> None:
    index_dir = build_demo_index()
    query = input("Nhập câu truy vấn (mặc định: first): ").strip() or "first"
    results = search_demo(query, index_dir)
    print(f"Số kết quả: {len(results)}")
    for number, result in enumerate(results, start=1):
        print(f"{number}. {result['title']} ({result['path']})")


if __name__ == "__main__":
    main()

