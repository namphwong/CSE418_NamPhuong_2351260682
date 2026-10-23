# Buổi 3 - Xử lý câu truy vấn

Bài làm triển khai yêu cầu trong tài liệu `TH03-Thuc hanh xu ly cau truy van.pdf` bằng Python và Whoosh.

## Mục tiêu

- Xây dựng chỉ mục cho 5 tài liệu trong `CS-Docs`.
- Thử nghiệm AND, OR, NOT, phrase, proximity và wildcard query.
- Cải tiến giao diện tìm kiếm để người dùng không cần tự viết cú pháp logic.
- Kiểm tra truy vấn rỗng, không có kết quả và lựa chọn kết quả không hợp lệ.

## Cấu trúc

```text
lab03-xu-ly-cau-truy-van/
├── CS-Docs/
├── index.py
├── search.py
├── README.md
└── tests/
```

## Chạy chương trình

Từ thư mục gốc repository:

```powershell
Set-Location lab03-xu-ly-cau-truy-van
..\.venv\Scripts\python.exe index.py
..\.venv\Scripts\python.exe search.py
```

`index.py` tạo thư mục `indexdir`. Có thể chạy `search.py` độc lập; chương trình sẽ tự tạo index nếu chưa có. Để bắt buộc chạy đúng quy trình `index.py` trước:

```powershell
..\.venv\Scripts\python.exe search.py --no-build
```

## Chế độ tìm kiếm thân thiện

Chương trình hỏi ba nhóm từ:

1. `required`: mọi từ đều phải có mặt, tương đương AND.
2. `optional`: chỉ cần một từ có mặt, được ghép bằng OR.
3. `forbidden`: các từ không được xuất hiện, mỗi từ được thêm NOT.

Ví dụ:

```text
required: learning data
optional: text image
forbidden: programming software
```

Chương trình sinh:

```text
learning data (text OR image) NOT programming NOT software
```

Có thể nhập phrase trong một nhóm bằng dấu ngoặc kép, ví dụ `"machine learning"`. Nhập `q`, `quit` hoặc `exit` để thoát.

## Chế độ truy vấn Whoosh nâng cao

Để thử trực tiếp cú pháp trong tài liệu:

```powershell
..\.venv\Scripts\python.exe search.py --advanced
```

Ví dụ:

```text
learning AND data
artificial OR operating
software NOT engineering
"machine learning"
"data mining"~5
learn*
mach?ne
```

## Kiểm thử

Từ thư mục gốc repository:

```powershell
.\.venv\Scripts\python.exe -m compileall -q lab03-xu-ly-cau-truy-van
Set-Location lab03-xu-ly-cau-truy-van
..\.venv\Scripts\python.exe -m unittest discover -s tests -p "test_*.py" -v
```

Bộ test kiểm tra:

- Đọc đúng 5 tài liệu và tiêu đề.
- Tạo index với `title`, `path`, `content`.
- Sinh đúng câu truy vấn mẫu của đề bài.
- AND, OR, NOT, phrase, proximity và wildcard.
- Truy vấn rỗng/không có kết quả.
- Đánh số kết quả từ 1.
- Xem nội dung tài liệu.
- Xử lý số thứ tự kết quả không hợp lệ.

## Quy tắc nhập và xây lại index

Nhóm optional vẫn yêu cầu ít nhất một từ xuất hiện khi được nhập, đúng ví dụ của đề. Chế độ thân thiện nhận từ đơn (Unicode), wildcard và phrase có thể kèm ~N; không nhận toán tử AND/OR/NOT, trường title:, dấu ngoặc hay boost. Dùng --advanced khi cần cú pháp Whoosh đầy đủ.

Sau khi sửa CS-Docs, chạy lại index.py. Index mới chỉ thay index cũ sau khi xây thành công. Lỗi nguồn hoặc lỗi ghi không xóa index cũ. Việc xây lại giả định một tiến trình ghi tại một thời điểm; đóng phiên tìm kiếm trước khi thay index trên Windows.

Kiểm thử bổ sung kiểm tra rebuild thất bại/khôi phục khi thay thư mục lỗi, EOF, phrase đúng thứ tự, proximity trong/ngoài giới hạn, wildcard * và ?, và logic của ba nhóm từ.

Bộ kiểm thử sau hoàn thiện: 22 test.
