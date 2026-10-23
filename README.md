# CSE418 - Truy hồi thông tin và tìm kiếm web

Repository thực hành của sinh viên **Nam Phuong (2351260682)**.

## Nội dung thực hành

| Buổi | Chủ đề | Trạng thái |
|---|---|---|
| 1 | Xử lý văn bản | Hoàn thành - Phase 11 |
| 2 | Xây dựng chỉ mục ngược | Hoàn thành - Phase 11 |
| 3 | Xử lý câu truy vấn | Chưa thực hiện |
| 4 | Đánh giá truy hồi thông tin | Chưa thực hiện |
| 5 | Phân loại văn bản | Chưa thực hiện |

## Cấu trúc repository

Mỗi buổi thực hành được tổ chức trong một thư mục riêng. Code, dữ liệu, test và hướng dẫn chạy của từng buổi sẽ được đặt cùng khu vực để dễ theo dõi và đưa lên GitHub.

Buổi 1 đã hoàn thành tại [`lab01-xu-ly-van-ban/`](lab01-xu-ly-van-ban/). Buổi 2 đã hoàn thành tại [`lab02-xay-dung-chi-muc-nguoc/`](lab02-xay-dung-chi-muc-nguoc/). Các file PDF `TH01` đến `TH05` ở thư mục gốc là tài liệu đề bài; phần cài đặt của các buổi 3 đến 5 sẽ được bổ sung sau.

## Cấu trúc chính

```text
.
├── .github/workflows/ci.yml       # Kiểm tra tự động trên GitHub Actions
├── lab01-xu-ly-van-ban/
│   ├── data/documents/             # 10 tài liệu tiếng Việt mẫu, mã hóa UTF-8
│   ├── src/                        # Mã nguồn 6 bài và module dùng chung
│   ├── tests/                      # Unit test và integration test
│   └── README.md                   # Hướng dẫn chi tiết Buổi 1
├── lab02-xay-dung-chi-muc-nguoc/
│   ├── src/                        # Bài 1-3 và module Whoosh dùng chung
│   ├── tests/                      # Unit test và integration test
│   └── README.md                   # Hướng dẫn chi tiết Buổi 2
├── requirements.txt                # Dependency dùng chung
└── README.md
```

## Cài đặt môi trường

Repository đã được kiểm tra với Python 3.11.9 trên Windows. Tạo môi trường ảo và cài các thư viện runtime bằng PowerShell:

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -c "import nltk; nltk.download('popular')"
```

Có thể kích hoạt môi trường ảo trước khi làm việc:

```powershell
.\.venv\Scripts\Activate.ps1
```

Nếu PowerShell chặn việc activate, vẫn có thể chạy trực tiếp bằng đường dẫn `.\.venv\Scripts\python.exe` như các lệnh ở trên. Dữ liệu NLTK được tải ở thư mục dữ liệu người dùng và không đưa vào Git repository.

Các phiên bản đã xác minh trong Phase 1:

- Python 3.11.9
- NLTK 3.10.4
- Underthesea 6.8.4
- Whoosh 2.7.4
- PyVI 0.1.1

## Chạy nhanh Buổi 1

Sau khi cài đặt môi trường, chạy từ thư mục gốc repository:

```powershell
Set-Location lab01-xu-ly-van-ban
..\.venv\Scripts\python.exe -m compileall -q src tests
..\.venv\Scripts\python.exe -m unittest discover -s tests -p "test_*.py" -v
```

Để chạy chương trình truy vấn và xem toàn văn tài liệu:

```powershell
..\.venv\Scripts\python.exe src\bai06_truy_van.py
```

Xem [`lab01-xu-ly-van-ban/README.md`](lab01-xu-ly-van-ban/README.md) để biết lệnh chạy riêng từng bài, mô tả đầu vào/đầu ra và quy ước dữ liệu.

## Tiến độ

- [x] Khởi tạo cấu trúc cho Buổi 1
- [x] Cài đặt môi trường và thư viện (Phase 1)
- [x] Hoàn thành các bài tập Buổi 1 (Phase 2-9)
- [x] Hoàn thiện kiểm thử và tài liệu Buổi 1 (Phase 10-11)
- [x] Hoàn thành Buổi 2: xây dựng chỉ mục ngược (Phase 1-11)

## Tiêu chí bàn giao Buổi 1

- Sáu bài thực hành có mã nguồn độc lập trong `lab01-xu-ly-van-ban/src/`.
- Mười tài liệu tiếng Việt mẫu được lưu trong `data/documents/` và có bảng ánh xạ ID.
- Có 54 unit test/integration test và kiểm tra cú pháp bằng `compileall`.
- Có workflow GitHub Actions tại [`.github/workflows/ci.yml`](.github/workflows/ci.yml).
- Có hướng dẫn cài đặt, chạy, kiểm thử và cấu trúc dữ liệu trong [README Buổi 1](lab01-xu-ly-van-ban/README.md).

**Trạng thái hiện tại:** Buổi 1 và Buổi 2 hoàn thành; các buổi 3-5 chưa bắt đầu triển khai.
