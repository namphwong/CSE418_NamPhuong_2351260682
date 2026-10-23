"""Tìm kiếm tài liệu bằng câu truy vấn Whoosh.

Chương trình hỗ trợ hai chế độ:

* Chế độ thân thiện: nhập ba nhóm từ bắt buộc, tùy chọn và bị cấm. Chương
  trình tự sinh cú pháp AND/OR/NOT.
* Chế độ nâng cao (``python search.py --advanced``): nhập trực tiếp cú pháp
  Whoosh để thử phrase, proximity và wildcard query theo tài liệu bài tập.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path
from typing import Callable, Iterable, Mapping, Sequence

from whoosh import scoring
from whoosh.index import FileIndex, exists_in
from whoosh.qparser import QueryParser, QueryParserError

try:
    from .index import DEFAULT_INDEX_DIR, build_index, open_index
except ImportError:  # Chạy trực tiếp bằng ``python search.py``.
    from index import DEFAULT_INDEX_DIR, build_index, open_index


EXIT_COMMANDS = {"q", "quit", "exit"}

# Giữ nguyên dấu ngoặc kép và hậu tố proximity, ví dụ:
#   "machine learning"
#   "whoosh library"~5
TERM_PATTERN = re.compile(r'"(?:[^"\\]|\\.)*"(?:~\d+)?|\S+')


def is_exit_command(value: str) -> bool:
    """Kiểm tra lệnh thoát dùng trong các ô nhập liệu."""

    return value.strip().lower() in EXIT_COMMANDS


def split_terms(text: str) -> list[str]:
    """Tách một nhóm từ nhưng vẫn giữ phrase/proximity query nguyên vẹn.

    Ví dụ ``machine "learning model"`` trở thành hai toán hạng, còn
    ``"whoosh library"~5`` trở thành một toán hạng.
    """

    if not isinstance(text, str):
        raise TypeError("text phải là chuỗi")

    stripped = text.strip()
    if not stripped:
        return []
    if stripped.count('"') % 2:
        raise ValueError("Dấu ngoặc kép trong phrase chưa được đóng.")

    tokens = TERM_PATTERN.findall(stripped)
    remainder = TERM_PATTERN.sub("", stripped).strip()
    if remainder:
        raise ValueError(
            "Không phân tích được nhóm từ. Hãy đóng dấu ngoặc kép cho phrase."
        )
    return tokens


def build_friendly_query(
    required_text: str,
    optional_text: str,
    forbidden_text: str,
) -> str:
    """Sinh câu truy vấn Whoosh từ ba nhóm nhập liệu thân thiện.

    * required: các từ phải cùng xuất hiện, nối ngầm định bằng AND;
    * optional: chỉ cần một từ xuất hiện, đặt trong nhóm OR;
    * forbidden: mỗi từ được thêm một mệnh đề NOT.

    Phải có ít nhất một từ ở nhóm required hoặc optional; truy vấn chỉ có
    NOT không hữu ích khi dùng QueryParser trên trường content.
    """

    required = split_terms(required_text)
    optional = split_terms(optional_text)
    forbidden = split_terms(forbidden_text)

    positive_parts: list[str] = []
    if required:
        positive_parts.append(" ".join(required))
    if optional:
        positive_parts.append(f"({' OR '.join(optional)})")

    if not positive_parts:
        raise ValueError("Hãy nhập ít nhất một từ bắt buộc hoặc tùy chọn.")

    parts = positive_parts + [f"NOT {term}" for term in forbidden]
    return " ".join(parts)


def index_is_available(index_dir: str | Path = DEFAULT_INDEX_DIR) -> bool:
    """Kiểm tra thư mục có chứa một Whoosh index hợp lệ hay không."""

    path = Path(index_dir)
    return path.is_dir() and exists_in(str(path))


def parse_query(query_text: str, index: FileIndex):
    """Phân tích câu truy vấn trên trường ``content``."""

    if not query_text.strip():
        raise ValueError("Câu truy vấn không được rỗng.")
    parser = QueryParser("content", schema=index.schema)
    try:
        return parser.parse(query_text)
    except QueryParserError as exc:
        raise ValueError(f"Câu truy vấn không hợp lệ: {exc}") from exc


def search_documents(
    query_text: str,
    index_dir: str | Path = DEFAULT_INDEX_DIR,
) -> list[dict[str, object]]:
    """Tìm tài liệu và trả về các stored fields cùng điểm số.

    Hàm này nhận trực tiếp cú pháp Whoosh nên được dùng để thử AND, OR, NOT,
    phrase, proximity và wildcard query.
    """

    if not isinstance(query_text, str):
        raise TypeError("query_text phải là chuỗi")
    if not query_text.strip():
        return []

    path = Path(index_dir)
    if not index_is_available(path):
        raise FileNotFoundError(
            f"Chưa có chỉ mục tại {path}. Hãy chạy index.py trước."
        )

    index = open_index(path)
    try:
        query = parse_query(query_text, index)
        with index.searcher(weighting=scoring.Frequency) as searcher:
            results = searcher.search(query, limit=None)
            output: list[dict[str, object]] = []
            for result in results:
                item = dict(result)
                item["score"] = float(result.score)
                output.append(item)
            return output
    finally:
        index.close()


def format_results(results: Sequence[Mapping[str, object]]) -> list[str]:
    """Định dạng danh sách kết quả, đánh số từ 1."""

    lines = [f"Số kết quả: {len(results)}"]
    for number, result in enumerate(results, start=1):
        score = result.get("score", 0.0)
        lines.append(
            f"{number}. {result.get('title', '<không có tiêu đề>')} "
            f"(điểm: {float(score):.4f})"
        )
    return lines


def read_result_content(result: Mapping[str, object]) -> str:
    """Đọc toàn văn tài liệu được lưu trong trường ``path``."""

    raw_path = result.get("path")
    if not raw_path:
        raise KeyError("Kết quả không có đường dẫn tài liệu.")
    path = Path(str(raw_path))
    if not path.is_file():
        raise FileNotFoundError(f"Không tìm thấy tài liệu: {path}")
    return path.read_text(encoding="utf-8")


def _choose_result(
    results: Sequence[Mapping[str, object]],
    input_fn: Callable[[str], str],
    output_fn: Callable[[str], None],
) -> bool:
    """Cho chọn kết quả; trả về False nếu người dùng muốn thoát."""

    while True:
        raw_selection = input_fn(
            "Nhập số thứ tự để xem nội dung, hoặc q để thoát: "
        ).strip()
        if is_exit_command(raw_selection):
            return False

        try:
            selection = int(raw_selection)
        except ValueError:
            output_fn("Số thứ tự phải là một số nguyên.")
            continue

        if not 1 <= selection <= len(results):
            output_fn(f"Số thứ tự phải nằm trong khoảng 1 đến {len(results)}.")
            continue

        try:
            content = read_result_content(results[selection - 1])
        except (FileNotFoundError, KeyError) as exc:
            output_fn(f"Không thể đọc tài liệu: {exc}")
            return True

        output_fn("\n--- Nội dung tài liệu ---")
        output_fn(content)
        return True


def run_friendly_cli(
    index_dir: str | Path = DEFAULT_INDEX_DIR,
    *,
    input_fn: Callable[[str], str] = input,
    output_fn: Callable[[str], None] = print,
    auto_build: bool = True,
) -> None:
    """Chạy giao diện ba nhóm từ khóa theo yêu cầu bài thực hành."""

    if auto_build and not index_is_available(index_dir):
        output_fn("Chưa có chỉ mục; đang tạo chỉ mục từ CS-Docs...")
        build_index(index_dir=index_dir)

    output_fn("\n=== TÌM KIẾM THÂN THIỆN ===")
    output_fn("Nhập q, quit hoặc exit ở bất kỳ bước nào để kết thúc.")

    while True:
        required = input_fn(
            "Các từ bắt buộc phải xuất hiện (required): "
        ).strip()
        if is_exit_command(required):
            output_fn("Đã kết thúc chương trình.")
            return

        optional = input_fn(
            "Các từ tùy chọn, chỉ cần một từ xuất hiện (optional): "
        ).strip()
        if is_exit_command(optional):
            output_fn("Đã kết thúc chương trình.")
            return

        forbidden = input_fn(
            "Các từ không được xuất hiện (forbidden): "
        ).strip()
        if is_exit_command(forbidden):
            output_fn("Đã kết thúc chương trình.")
            return

        try:
            generated_query = build_friendly_query(required, optional, forbidden)
            results = search_documents(generated_query, index_dir)
        except (ValueError, FileNotFoundError) as exc:
            output_fn(f"Lỗi: {exc}")
            continue

        output_fn(f"Câu truy vấn được tạo: {generated_query}")
        for line in format_results(results):
            output_fn(line)

        if not results:
            output_fn("Không có tài liệu phù hợp.")
            continue

        if not _choose_result(results, input_fn, output_fn):
            output_fn("Đã kết thúc chương trình.")
            return


def run_advanced_cli(
    index_dir: str | Path = DEFAULT_INDEX_DIR,
    *,
    input_fn: Callable[[str], str] = input,
    output_fn: Callable[[str], None] = print,
    auto_build: bool = True,
) -> None:
    """Chạy chế độ nhập trực tiếp cú pháp truy vấn Whoosh."""

    if auto_build and not index_is_available(index_dir):
        output_fn("Chưa có chỉ mục; đang tạo chỉ mục từ CS-Docs...")
        build_index(index_dir=index_dir)

    output_fn("\n=== TÌM KIẾM NÂNG CAO WHOOSH ===")
    output_fn('Ví dụ: learning AND data, "machine learning", learn*')
    output_fn("Nhập q, quit hoặc exit để kết thúc.")

    while True:
        query_text = input_fn("Nhập câu truy vấn: ").strip()
        if is_exit_command(query_text):
            output_fn("Đã kết thúc chương trình.")
            return
        if not query_text:
            output_fn("Câu truy vấn không được rỗng.")
            continue

        try:
            results = search_documents(query_text, index_dir)
        except (ValueError, FileNotFoundError) as exc:
            output_fn(f"Lỗi truy vấn: {exc}")
            continue

        for line in format_results(results):
            output_fn(line)
        if not results:
            output_fn("Không có tài liệu phù hợp.")
            continue

        if not _choose_result(results, input_fn, output_fn):
            output_fn("Đã kết thúc chương trình.")
            return


def main(argv: Iterable[str] | None = None) -> None:
    """Điểm vào cho cả chế độ thân thiện và nâng cao."""

    parser = argparse.ArgumentParser(description="Tìm kiếm tài liệu bằng Whoosh")
    parser.add_argument(
        "--advanced",
        action="store_true",
        help="nhập trực tiếp cú pháp truy vấn Whoosh",
    )
    parser.add_argument(
        "--no-build",
        action="store_true",
        help="không tự tạo index nếu indexdir chưa tồn tại",
    )
    args = parser.parse_args(list(argv) if argv is not None else None)

    if args.no_build and not index_is_available(DEFAULT_INDEX_DIR):
        raise SystemExit("Chưa có indexdir; hãy chạy index.py trước.")

    runner = run_advanced_cli if args.advanced else run_friendly_cli
    runner(auto_build=not args.no_build)


if __name__ == "__main__":
    main()
