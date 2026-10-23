"""Bài 2: lập chỉ mục và tìm kiếm sau khi tách từ tiếng Việt bằng PyVI."""

from __future__ import annotations

from pathlib import Path

try:
    from .whoosh_common import (
        basic_schema,
        commit_documents,
        create_index,
        open_index,
        search_index,
        tokenize_vietnamese,
    )
except ImportError:  # pragma: no cover
    from whoosh_common import (
        basic_schema,
        commit_documents,
        create_index,
        open_index,
        search_index,
        tokenize_vietnamese,
    )


VIETNAMESE_DOCUMENTS = (
    {
        "title": "Đại học Thủy Lợi",
        "path": "/vn/1",
        "content": "Đại học Thủy Lợi đào tạo kỹ thuật, công nghệ thông tin và quản lý tài nguyên nước.",
    },
    {
        "title": "Tìm kiếm thông tin",
        "path": "/vn/2",
        "content": "Tìm kiếm thông tin cần có dữ liệu phù hợp, chỉ mục ngược và câu truy vấn rõ ràng.",
    },
    {
        "title": "Xử lý văn bản",
        "path": "/vn/3",
        "content": "Xử lý văn bản tiếng Việt cần tách từ ghép trước khi lập chỉ mục và tìm kiếm.",
    },
)

DEFAULT_INDEX_DIR = Path(__file__).resolve().parents[1] / "indexdir-bai02"


def build_vietnamese_index(index_dir: str | Path = DEFAULT_INDEX_DIR) -> Path:
    """Tách từ toàn bộ tài liệu rồi ghi bản đã tách vào Whoosh."""

    index = create_index(index_dir, basic_schema())
    indexed_documents = []
    for document in VIETNAMESE_DOCUMENTS:
        indexed_documents.append(
            {
                "title": document["title"],
                "path": document["path"],
                "content": tokenize_vietnamese(document["content"]),
            }
        )
    commit_documents(index, indexed_documents)
    return Path(index_dir)


def search_vietnamese(
    query_text: str,
    index_dir: str | Path = DEFAULT_INDEX_DIR,
) -> list[dict[str, str]]:
    """Tách từ câu truy vấn rồi tìm trong index đã tách từ."""

    index = open_index(index_dir)
    try:
        return search_index(index, tokenize_vietnamese(query_text))
    finally:
        index.close()


def main() -> None:
    index_dir = build_vietnamese_index()
    query = input("Nhập câu truy vấn tiếng Việt (mặc định: Đại học Thủy Lợi): ").strip()
    query = query or "Đại học Thủy Lợi"
    print(f"Truy vấn sau khi tách từ: {tokenize_vietnamese(query)}")
    results = search_vietnamese(query, index_dir)
    print(f"Số kết quả: {len(results)}")
    for number, result in enumerate(results, start=1):
        print(f"{number}. {result['title']} ({result['path']})")


if __name__ == "__main__":
    main()

