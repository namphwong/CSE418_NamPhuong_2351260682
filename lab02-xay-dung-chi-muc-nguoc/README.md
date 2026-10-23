# Buổi 2 - Xây dựng chỉ mục ngược

Buổi này triển khai các yêu cầu trong `TH02-Thuc hanh xay dung chi muc nguoc.pdf` bằng thư viện Whoosh và PyVI.

## Mục tiêu

- Khai báo schema cho tài liệu.
- Tạo, mở và commit chỉ mục Whoosh.
- Thêm tài liệu bằng `IndexWriter`.
- Phân tích truy vấn bằng `QueryParser`.
- Tách từ ghép tiếng Việt nhất quán bằng PyVI.
- Xây dựng chương trình tìm kiếm trên 10 tài liệu, hiển thị tiêu đề và truy xuất toàn văn theo mã tài liệu.

## Chuẩn bị môi trường

Từ thư mục gốc repository:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Kiểm tra nhanh:

```powershell
.\.venv\Scripts\python.exe -X utf8 -c "import whoosh, pyvi; from pyvi import ViTokenizer; print(whoosh.__version__); print(ViTokenizer.tokenize('Đại học Thủy Lợi'))"
```

Kết quả tách từ mong đợi là `Đại_học Thủy_Lợi`.

## Phase 2 - Schema và thao tác index

Các schema dùng chung nằm trong `src/whoosh_common.py`:

- `basic_schema()`: `title` và `path` được lưu; `content` chỉ lập chỉ mục.
- `document_schema()`: `doc_id` và `title` được lưu; `content` chỉ lập chỉ mục.

`create_index()` tạo mới index trong thư mục chỉ định. `open_index()` mở lại index sau khi đã commit.

## Phase 3-5 - Bài 1

Chạy:

```powershell
Set-Location lab02-xay-dung-chi-muc-nguoc
..\.venv\Scripts\python.exe src\bai01_whoosh_co_ban.py
```

Chương trình tạo hai tài liệu mẫu, commit, nhận câu truy vấn và in số kết quả cùng tiêu đề/đường dẫn.

## Phase 6 - Bài 2: tiếng Việt

Chạy:

```powershell
..\.venv\Scripts\python.exe src\bai02_tieng_viet.py
```

Tài liệu được tách bằng `ViTokenizer` trước khi ghi vào Whoosh. Câu truy vấn cũng được tách bằng chính hàm đó trước khi gọi `QueryParser`.

## Phase 7-10 - Bài 3

Chạy:

```powershell
..\.venv\Scripts\python.exe src\bai03_chi_muc_nguoc.py
```

Tập `D` gồm 10 tài liệu được khai báo trực tiếp trong `src/data.py`. Chỉ `doc_id` và `title` được lưu trong index. Nội dung vẫn nằm trong danh sách `DEFAULT_DOCUMENTS` để có thể truy xuất sau khi người dùng chọn số thứ tự kết quả.

Luồng chương trình:

```text
10 tài liệu D
    -> tách từ bằng PyVI
    -> ghi doc_id, title và nội dung đã tách vào index
    -> nhập truy vấn nhiều từ
    -> in số kết quả và tiêu đề, đánh số từ 1
    -> nhập số thứ tự
    -> tra doc_id trong D và in toàn văn
```

Nhập `q`, `quit` hoặc `exit` để kết thúc. Chương trình cũng xử lý truy vấn rỗng, số thứ tự không hợp lệ và truy vấn không có kết quả.

## Kiểm thử

Từ thư mục gốc:

```powershell
.\.venv\Scripts\python.exe -m compileall -q lab02-xay-dung-chi-muc-nguoc\src lab02-xay-dung-chi-muc-nguoc\tests
Set-Location lab02-xay-dung-chi-muc-nguoc
..\.venv\Scripts\python.exe -m unittest discover -s tests -p "test_*.py" -v
```

Các test kiểm tra:

- Tạo và tìm kiếm index mẫu.
- Truy vấn rỗng.
- Tách từ ghép tiếng Việt.
- Tìm kiếm câu truy vấn tiếng Việt nhiều từ.
- Tập dữ liệu đúng 10 tài liệu.
- Index có `doc_id`, `title` nhưng không lưu `content`.
- Truy xuất lại toàn văn từ danh sách ban đầu.
- Hiển thị số thứ tự kết quả bắt đầu từ 1.
- Luồng CLI hợp lệ và xử lý số thứ tự sai.

