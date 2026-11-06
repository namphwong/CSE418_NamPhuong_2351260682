# CSE418 - Truy hồi thông tin

Repository lưu trữ đề bài và bài thực hành môn **CSE418 - Truy hồi thông tin**.

## Thông tin sinh viên

- Họ và tên: Nam Phương
- Mã sinh viên: 2351260682

## Cấu trúc repository

```text
.
|-- DeBai/   # Đề bài thực hành
|-- TH1/     # Xử lý văn bản
|-- TH2/     # Xây dựng chỉ mục ngược
|-- TH3/     # Xử lý câu truy vấn
`-- TH4/     # Đánh giá hệ thống truy hồi thông tin
```

### TH1 - Xử lý văn bản

Gồm 6 bài tập về tách từ, tách gốc từ tiếng Anh, xử lý tiếng Việt, thống kê tần suất từ, phép toán trên tập hợp và xây dựng chỉ mục ngược đơn giản. Thư mục `documents/` chứa 10 tài liệu mẫu dùng cho `bai6.py`.

### TH2 - Xây dựng chỉ mục ngược

Gồm 3 bài tập sử dụng Whoosh để tạo chỉ mục, thêm tài liệu và thực hiện truy vấn trên dữ liệu tiếng Anh và tiếng Việt.

### TH3 - Xử lý câu truy vấn

- `index.py`: tạo chỉ mục cho các tài liệu trong `CS-Docs/`.
- `search.py`: thực hiện truy vấn với nhóm từ bắt buộc, tùy chọn và loại trừ; kết quả được xếp hạng theo tần suất.

### TH4 - Đánh giá truy hồi thông tin

`ir-eval.py` xây dựng tập tài liệu và truy vấn mẫu, sau đó đánh giá kết quả bằng các độ đo:

- Precision@5
- Recall
- F1-score
- R-Precision

## Yêu cầu môi trường

- Python 3.10 trở lên
- Các thư viện: `nltk`, `pyvi`, `Whoosh`

Cài đặt thư viện:

```bash
python -m pip install nltk pyvi Whoosh
```

Riêng bài 1 của TH1 cần dữ liệu tokenizer của NLTK. Có thể cài bằng lệnh:

```bash
python -m nltk.downloader punkt punkt_tab
```

## Cách chạy

Các chương trình sử dụng đường dẫn tương đối, vì vậy nên chuyển vào đúng thư mục bài thực hành trước khi chạy.

### TH1

```bash
cd TH1
python bai1.py
python bai2.py
python bai3.py
python bai4.py
python bai5.py
python bai6.py
```

### TH2

```bash
cd TH2
python bai1.py
python bai2.py
python bai3.py
```

Mỗi chương trình sẽ tạo thư mục `indexdir/` để lưu chỉ mục Whoosh.

### TH3

```bash
cd TH3
python index.py
python search.py
```

Chạy `index.py` trước để tạo chỉ mục, sau đó mới chạy `search.py`.

### TH4

```bash
cd TH4
python ir-eval.py
```

Kết quả đánh giá từng truy vấn và giá trị trung bình sẽ được in ra màn hình.
