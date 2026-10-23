"""Xây dựng chỉ mục Whoosh cho bài thực hành 3.

Mỗi file trong ``CS-Docs`` có dạng:

    Dòng đầu tiên: tiêu đề
    Các dòng còn lại: nội dung tài liệu

Chỉ mục lưu ``title`` và ``path`` để hiển thị/truy xuất kết quả; trường
``content`` được lập chỉ mục để tìm kiếm nhưng không cần lưu toàn văn.
"""

from __future__ import annotations

from pathlib import Path
from whoosh.fields import ID, TEXT, Schema
from whoosh.filedb.filestore import FileStorage
from whoosh.index import FileIndex, create_in


PROJECT_DIR = Path(__file__).resolve().parent
DEFAULT_DOCS_DIR = PROJECT_DIR / "CS-Docs"
DEFAULT_INDEX_DIR = PROJECT_DIR / "indexdir"


def make_schema() -> Schema:
    """Tạo schema theo cấu trúc được yêu cầu trong tài liệu bài tập."""

    return Schema(
        title=TEXT(stored=True),
        path=ID(stored=True),
        content=TEXT,
    )


def document_paths(root: str | Path = DEFAULT_DOCS_DIR) -> list[Path]:
    """Trả về các file ``.txt`` trong thư mục dữ liệu theo thứ tự ổn định."""

    docs_dir = Path(root)
    if not docs_dir.is_dir():
        raise FileNotFoundError(f"Không tìm thấy thư mục tài liệu: {docs_dir}")

    paths = sorted(
        path
        for path in docs_dir.iterdir()
        if path.is_file() and path.suffix.lower() == ".txt"
    )
    if not paths:
        raise FileNotFoundError(f"Không có file .txt trong thư mục: {docs_dir}")
    return paths


def read_document(path: str | Path) -> tuple[str, str]:
    """Đọc một tài liệu và tách thành ``(title, content)``.

    File được đọc bằng UTF-8 để không phụ thuộc vào encoding mặc định của
    hệ điều hành.
    """

    document_path = Path(path)
    lines = document_path.read_text(encoding="utf-8").splitlines()
    if not lines or not lines[0].strip():
        raise ValueError(f"Tài liệu không có tiêu đề: {document_path}")

    title = lines[0].strip()
    content = "\n".join(lines[1:]).strip()
    if not content:
        raise ValueError(f"Tài liệu không có nội dung: {document_path}")
    return title, content


def build_index(
    root: str | Path = DEFAULT_DOCS_DIR,
    index_dir: str | Path = DEFAULT_INDEX_DIR,
) -> Path:
    """Tạo mới chỉ mục từ toàn bộ tài liệu trong ``root``.

    Hàm có thể gọi nhiều lần để xây dựng lại chỉ mục sau khi dữ liệu thay
    đổi. Writer được hủy nếu quá trình ghi gặp lỗi.
    """

    docs_dir = Path(root).resolve()
    target_dir = Path(index_dir).resolve()
    target_dir.mkdir(parents=True, exist_ok=True)

    index: FileIndex = create_in(str(target_dir), make_schema())
    writer = index.writer()
    paths = document_paths(docs_dir)
    try:
        for path in paths:
            title, content = read_document(path)
            writer.add_document(
                # Giữ cả tên file và tiêu đề, giống chương trình mẫu.
                title=f"{path.name} - {title}",
                path=str(path),
                content=content,
            )
        writer.commit()
    except Exception:
        writer.cancel()
        raise
    finally:
        index.close()

    return target_dir


def open_index(index_dir: str | Path = DEFAULT_INDEX_DIR) -> FileIndex:
    """Mở index với mmap tắt để giải phóng file sạch trên Windows."""

    storage = FileStorage(str(Path(index_dir)), supports_mmap=False)
    return FileIndex(storage)


def main() -> None:
    """Điểm vào khi chạy ``python index.py``."""

    index_dir = build_index()
    paths = document_paths()
    print(f"Đã lập chỉ mục {len(paths)} tài liệu.")
    print(f"Thư mục chỉ mục: {index_dir}")
    for path in paths:
        print(f"- {path.name}")


if __name__ == "__main__":
    main()
