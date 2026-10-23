# Buổi 1 - Xử lý văn bản

## Mục tiêu

Buổi thực hành này tập trung vào các thao tác nền tảng trong xử lý văn bản:

1. Tách từ và stemming tiếng Anh.
2. Tách từ tiếng Việt và kiểm tra từ xuất hiện trong văn bản.
3. Đếm tần số từ trong một tài liệu.
4. Đếm số tài liệu chứa từng từ.
5. Tìm giao và hợp của hai danh sách số nguyên đã sắp xếp.
6. Xây dựng chỉ mục từ và tìm kiếm trên 10 tài liệu tiếng Việt.

## Cấu trúc thư mục

```text
lab01-xu-ly-van-ban/
├── README.md
├── src/       # Mã nguồn của 6 bài tập
├── data/      # Dữ liệu đầu vào, gồm các tài liệu văn bản
└── tests/     # Kiểm thử
```

## Chuẩn bị môi trường

Từ thư mục gốc repository, chạy:

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -c "import nltk; nltk.download('popular')"
```

Phase 1 sử dụng `underthesea` để tách từ tiếng Việt. Kiểm tra nhanh:

```powershell
.\.venv\Scripts\python.exe -c "from underthesea import word_tokenize; print(word_tokenize('Xử lý văn bản tiếng Việt.'))"
```

Các resource NLTK cần cho Bài 1, trong đó có `punkt` và `punkt_tab`, phải được tải thành công trước khi chạy chương trình.

## Hàm dùng chung - Phase 2

Module [`src/text_utils.py`](src/text_utils.py) cung cấp các hàm nền tảng:

| Hàm | Quy ước |
|---|---|
| `normalize_text(text)` | Chuẩn hóa Unicode NFKC, chuyển chữ thường, gom khoảng trắng; giữ dấu câu |
| `remove_punctuation(text)` | Thay dấu câu bằng khoảng trắng để không làm dính hai từ |
| `get_unique_words(words)` | Loại token rỗng, giữ thứ tự xuất hiện đầu tiên |
| `count_words(words)` | Đếm tần số từng token, giữ thứ tự key đầu tiên |
| `count_document_frequency(documents)` | Đếm số tài liệu chứa mỗi token, mỗi tài liệu chỉ tính một lần |

Các hàm xử lý token không tự động chuyển chữ thường. Hãy gọi `normalize_text()` trước khi tách từ nếu bài tập cần coi chữ hoa và chữ thường là cùng một từ.

## Chạy kiểm thử

Từ thư mục gốc repository:

```powershell
Set-Location lab01-xu-ly-van-ban
..\.venv\Scripts\python.exe -m unittest discover -s tests -p "test_*.py" -v
```

Phase 2 hiện có 8 test cho chuẩn hóa văn bản, xử lý dấu câu, loại từ trùng, tần số từ, tần số tài liệu và kiểm tra kiểu dữ liệu đầu vào.

## Bài 1 - Tách từ tiếng Anh và Porter stemming

Mã nguồn nằm ở [`src/bai01_tach_tu_tieng_anh.py`](src/bai01_tach_tu_tieng_anh.py).

Luồng xử lý:

```text
Văn bản tiếng Anh
        ↓
nltk.word_tokenize()
        ↓
Danh sách token (bao gồm cả dấu câu)
        ↓
nltk.PorterStemmer().stem()
        ↓
Danh sách stem tương ứng theo từng token
```

Các hàm chính:

| Hàm | Vai trò |
|---|---|
| `tokenize_english(text)` | Tách văn bản bằng NLTK, giữ cả token dấu câu |
| `stem_tokens(tokens)` | Áp dụng Porter stemmer cho từng token |
| `analyze_english_text(text)` | Trả về cặp `(tokens, stems)` có cùng độ dài |
| `format_analysis(text)` | Tạo bảng kết quả để hiển thị |

Chạy Bài 1 từ thư mục `lab01-xu-ly-van-ban`:

```powershell
..\.venv\Scripts\python.exe src\bai01_tach_tu_tieng_anh.py
```

Nếu để trống phần nhập, chương trình sẽ dùng văn bản tiếng Anh mẫu. Kết quả có dạng:

```text
Token                    | Stem
-------------------------+--------------------------
Information              | inform
retrieval                | retriev
is                       | is
useful                   | use
.                        | .
```

Việc giữ dấu câu trong danh sách token là chủ ý để phản ánh trực tiếp kết quả của `nltk.word_tokenize()`. Khi các bài sau cần danh sách từ thuần túy, có thể lọc dấu câu ở bước xử lý riêng.

## Bài 2 - Tách từ tiếng Việt và kiểm tra từ

Mã nguồn nằm ở [`src/bai02_tach_tu_tieng_viet.py`](src/bai02_tach_tu_tieng_viet.py). Bài này sử dụng `underthesea.word_tokenize(..., format="list")`.

Luồng xử lý:

```text
Văn bản tiếng Việt
        ↓
Underthesea word_tokenize(format="list")
        ↓
Danh sách token tiếng Việt
        ↓
Chuẩn hóa chữ hoa, chữ thường và khoảng trắng
        ↓
Kiểm tra query có phải một token đầy đủ hay không
```

Các hàm chính:

| Hàm | Vai trò |
|---|---|
| `tokenize_vietnamese(text)` | Tách văn bản thành danh sách token tiếng Việt |
| `contains_token(tokens, query)` | Kiểm tra query trong danh sách token đã có |
| `contains_word(document, query)` | Tách văn bản rồi kiểm tra query |
| `analyze_vietnamese_text(document, query)` | Trả về token list và kết quả tìm kiếm |
| `format_analysis(document, query)` | Tạo kết quả hiển thị cho CLI |

Underthesea giữ các từ nhiều âm tiết thành một token, ví dụ `"sinh viên"`, `"xử lý"` và `"văn bản"`. Vì vậy `"xử lý"` được tìm thấy nhưng `"xử"` không được coi là một token riêng trong văn bản đó. Việc so khớp không phân biệt hoa thường và không làm mất dấu tiếng Việt.

Chạy Bài 2 từ thư mục `lab01-xu-ly-van-ban`:

```powershell
..\.venv\Scripts\python.exe src\bai02_tach_tu_tieng_viet.py
```

Chương trình yêu cầu nhập văn bản rồi nhập query. Ví dụ:

```text
Document: Sinh viên học xử lý văn bản tiếng Việt.
Query: xử lý
Result: FOUND
```

Nếu query rỗng, chương trình báo lỗi và dừng để tránh kết luận sai rằng chuỗi rỗng là một từ hợp lệ.

## Bài 3 - Tần số từ

Mã nguồn nằm ở [`src/bai03_tan_so_tu.py`](src/bai03_tan_so_tu.py).

Pipeline của bài:

```text
Tài liệu đầu vào
        ↓
Chuẩn hóa Unicode, chữ thường và dấu câu
        ↓
Tách token bằng Underthesea
        ↓
Loại token chỉ chứa dấu câu
        ↓
Đếm bằng dict: từ → số lần xuất hiện
        ↓
Sắp xếp giảm dần theo tần số
```

Các hàm chính:

| Hàm | Vai trò |
|---|---|
| `tokenize_document(text)` | Chuẩn hóa và tách token để đếm |
| `count_word_frequency(text)` | Trả về dictionary `từ -> số lần xuất hiện` |
| `sort_frequencies(frequencies)` | Sắp xếp giảm dần theo tần số, sau đó theo alphabet |
| `format_frequency_table(text)` | Hiển thị token và bảng tần số |

Mặc định, bài sử dụng tokenizer tiếng Việt để giữ các từ nhiều âm tiết như `"xử lý"`, `"văn bản"` và `"tìm kiếm"` thành một token. Có thêm chế độ `language="whitespace"` cho dữ liệu đơn giản cần tách theo khoảng trắng.

Chạy Bài 3:

```powershell
..\.venv\Scripts\python.exe src\bai03_tan_so_tu.py
```

Ví dụ kết quả:

```text
Unique words (9):
Word                         | Frequency
-----------------------------+----------
văn bản                       | 2
xử lý                         | 2
bước                          | 1
```

Dictionary tần số được trả về riêng bởi `count_word_frequency()` để có thể tái sử dụng trong Bài 4 và các bài xây dựng chỉ mục sau này.

## Bài 4 - Từ vựng và tần số tài liệu

Mã nguồn nằm ở [`src/bai04_tan_so_tai_lieu.py`](src/bai04_tan_so_tai_lieu.py). Tập tài liệu được khai báo trực tiếp trong biến `DEFAULT_DOCUMENTS`, gồm 4 tài liệu tiếng Việt, mỗi tài liệu là một câu.

Điểm khác biệt với Bài 3:

| Bài | Đại lượng đếm | Ví dụ |
|---|---|---|
| Bài 3 | Số lần từ xuất hiện trong một tài liệu | `python: 3` |
| Bài 4 | Số tài liệu khác nhau chứa từ đó | `python: 2` |

Luồng xử lý Bài 4:

```text
Tập tài liệu D
        ↓
Tách từng tài liệu thành token
        ↓
Loại từ trùng bên trong từng tài liệu
        ↓
Đếm số tài liệu chứa từng từ
        ↓
Sắp xếp và hiển thị document frequency
```

Các hàm chính:

| Hàm | Vai trò |
|---|---|
| `tokenize_documents(documents)` | Tách toàn bộ tài liệu, giữ thứ tự tài liệu |
| `count_document_frequencies(documents)` | Trả về dictionary `từ -> số tài liệu chứa từ` |
| `sort_document_frequencies(frequencies)` | Sắp xếp giảm dần theo document frequency |
| `format_document_frequency_table(documents)` | Hiển thị tập tài liệu và bảng kết quả |

Ví dụ, nếu từ `dữ liệu` xuất hiện nhiều lần trong tài liệu 1 nhưng chỉ xuất hiện trong tài liệu 1, 2 và 4 thì kết quả là `dữ liệu: 3`, không phải tổng số lần xuất hiện.

Chạy Bài 4:

```powershell
..\.venv\Scripts\python.exe src\bai04_tan_so_tai_lieu.py
```

Kết quả mẫu có dạng:

```text
Word                         | Number of documents
-----------------------------+--------------------
dữ liệu                       | 3
giúp                          | 2
python                        | 2
```

## Bài 5 - Giao và hợp danh sách thẻ định vị

Mã nguồn nằm ở [`src/bai05_giao_hop.py`](src/bai05_giao_hop.py).

Bài này sử dụng thuật toán hai con trỏ trên hai danh sách số nguyên đã sắp xếp:

```text
Danh sách 1: [1, 3, 5, 7, 9]
Danh sách 2: [2, 3, 5, 8, 9]
                    ↓
Giao: [3, 5, 9]
Hợp: [1, 2, 3, 5, 7, 8, 9]
```

Các hàm chính:

| Hàm | Vai trò |
|---|---|
| `intersection_sorted(first, second)` | Tìm các số xuất hiện trong cả hai danh sách |
| `union_sorted(first, second)` | Gộp các số từ hai danh sách và loại phần tử trùng |
| `parse_integer_list(raw_text)` | Đọc số nguyên cách nhau bằng dấu cách hoặc dấu phẩy |
| `format_set_operations(first, second)` | Hiển thị hai danh sách, giao và hợp |

Quy ước xử lý:

- Danh sách phải được sắp xếp không giảm dần.
- Kết quả giao và hợp không chứa phần tử trùng lặp.
- Danh sách rỗng, số âm và số 0 đều được hỗ trợ.
- Danh sách không sắp xếp hoặc chứa dữ liệu không phải số nguyên sẽ bị từ chối.
- Hai danh sách đầu vào không bị sửa đổi.
- Thuật toán có độ phức tạp thời gian `O(n + m)` và không dùng `set`.

Chạy Bài 5:

```powershell
..\.venv\Scripts\python.exe src\bai05_giao_hop.py
```

Khi nhập dữ liệu, có thể dùng một trong hai dạng:

```text
1 3 5 7 9
2 3 5 8 9
```

hoặc:

```text
1, 3, 5, 7, 9
2, 3, 5, 8, 9
```

## Phase 8 - Bộ dữ liệu cho Bài 6

Thư mục [`data/documents/`](data/documents/) hiện có 10 tài liệu tiếng Việt nguyên bản. Tên file được đánh số từ `01` đến `10`, vì vậy chương trình Bài 6 có thể dùng thứ tự tên file để gán ID tài liệu ổn định.

Danh sách chủ đề và quy ước ID được ghi trong [`data/documents/README.md`](data/documents/README.md). Tất cả file văn bản đều được lưu bằng UTF-8 và đã được kiểm tra bằng tokenizer hiện tại:

```text
10 tài liệu được đọc thành công
10/10 tài liệu có token
Tổng số token: 388
```

Không đưa nội dung tài liệu vào biến trong chương trình Bài 6; chương trình cần đọc các file từ thư mục này để thực hành đúng yêu cầu mở file, lưu tài liệu trong bộ nhớ và xây dựng chỉ mục.

## Phase 9 - Chỉ mục ngược và truy vấn

Mã nguồn nằm ở [`src/bai06_truy_van.py`](src/bai06_truy_van.py). Chương trình thực hiện đầy đủ quy trình Bài 6:

```text
Đọc 10 file .txt bằng encoding="utf-8"
        ↓
Lưu {document_id: toàn_văn_tài_liệu}
        ↓
Tách token và loại token trùng trong từng tài liệu
        ↓
Xây dựng {token: [document_id, ...]}
        ↓
Nhập query và trả về danh sách ID tài liệu
        ↓
Chọn ID để hiển thị toàn văn
```

Các hàm chính:

| Hàm | Vai trò |
|---|---|
| `load_documents(folder_path)` | Đọc các file được đánh số và lưu toàn văn trong bộ nhớ |
| `build_inverted_index(documents)` | Tạo ánh xạ `token -> danh sách ID tài liệu` |
| `search_index(index, query)` | Tìm các ID chứa query, không phân biệt hoa thường |
| `get_document(documents, document_id)` | Lấy toàn văn theo ID |
| `format_query_result(...)` | Định dạng kết quả truy vấn |

Chỉ mục được xây dựng với mỗi token tối đa một lần trong mỗi tài liệu. Vì vậy posting list luôn tăng dần và không có ID trùng lặp. Query được so khớp theo token đầy đủ; ví dụ `cơ sở dữ liệu` có thể tìm thấy, nhưng `cơ` không tự động tìm trong token nhiều âm tiết đó.

Chạy chương trình từ thư mục `lab01-xu-ly-van-ban`:

```powershell
..\.venv\Scripts\python.exe src\bai06_truy_van.py
```

Ví dụ phiên làm việc:

```text
Từ truy vấn: python
Documents: 1, 2, 10
Chọn ID tài liệu để xem toàn văn: 1
Toàn văn tài liệu 1:
Python là ngôn ngữ lập trình dễ đọc...
```

Nhập `q`, `quit` hoặc `exit` để kết thúc. Query không có kết quả trả về danh sách rỗng; ID tài liệu không tồn tại sẽ được báo lỗi thay vì hiển thị nhầm tài liệu.

## Phase 10 - Kiểm thử toàn bộ

Bộ test nằm trong thư mục [`tests/`](tests/) và sử dụng `unittest` có sẵn trong Python, nên không cần thêm dependency test.

Chạy kiểm tra cú pháp bytecode:

```powershell
..\.venv\Scripts\python.exe -m compileall -q src tests
```

Chạy toàn bộ unit test và integration test:

```powershell
..\.venv\Scripts\python.exe -m unittest discover -s tests -p "test_*.py" -v
```

Phase 10 kiểm tra 54 trường hợp, bao gồm:

- Các hàm dùng chung ở Phase 2.
- Tách từ tiếng Anh và Porter stemming.
- Tách từ tiếng Việt và kiểm tra query.
- Tần số từ và tần số tài liệu.
- Giao, hợp danh sách số nguyên.
- Đọc 10 file UTF-8 và xây dựng inverted index.
- Truy vấn dữ liệu thật, kiểm tra posting list và hiển thị toàn văn.
- Luồng CLI tìm kiếm, chọn ID tài liệu và thoát chương trình.
- Dữ liệu rỗng, ID sai, thư mục sai và kiểu dữ liệu không hợp lệ.

Repository cũng có workflow [`.github/workflows/ci.yml`](../.github/workflows/ci.yml) để tự chạy compile và test trên mỗi lần push hoặc pull request.

## Trạng thái thực hiện

- [x] Phase 0 - Khởi tạo cấu trúc Buổi 1
- [x] Phase 1 - Chuẩn bị môi trường Python
- [x] Phase 2 - Xây dựng hàm dùng chung
- [x] Phase 3 - Bài 1: Tách từ tiếng Anh
- [x] Phase 4 - Bài 2: Tách từ tiếng Việt
- [x] Phase 5 - Bài 3: Tần số từ
- [x] Phase 6 - Bài 4: Tần số tài liệu
- [x] Phase 7 - Bài 5: Giao và hợp danh sách
- [x] Phase 8 - Chuẩn bị dữ liệu cho Bài 6
- [x] Phase 9 - Xây dựng chỉ mục và truy vấn
- [x] Phase 10 - Kiểm thử
- [x] Phase 11 - Hoàn thiện tài liệu

## Bàn giao hoàn tất Buổi 1

Buổi thực hành 1 đã hoàn thiện toàn bộ sáu yêu cầu trong tài liệu `TH01-Thuc hanh xu ly van ban.pdf`:

| Hạng mục | Vị trí | Trạng thái |
|---|---|---|
| Hàm xử lý văn bản dùng chung | [`src/text_utils.py`](src/text_utils.py) | Hoàn thành |
| Bài 1: tách từ tiếng Anh và Porter stemming | [`src/bai01_tach_tu_tieng_anh.py`](src/bai01_tach_tu_tieng_anh.py) | Hoàn thành |
| Bài 2: tách từ tiếng Việt | [`src/bai02_tach_tu_tieng_viet.py`](src/bai02_tach_tu_tieng_viet.py) | Hoàn thành |
| Bài 3: tần số từ | [`src/bai03_tan_so_tu.py`](src/bai03_tan_so_tu.py) | Hoàn thành |
| Bài 4: tần số tài liệu | [`src/bai04_tan_so_tai_lieu.py`](src/bai04_tan_so_tai_lieu.py) | Hoàn thành |
| Bài 5: giao và hợp danh sách số nguyên | [`src/bai05_giao_hop.py`](src/bai05_giao_hop.py) | Hoàn thành |
| Bài 6: inverted index và truy vấn tài liệu | [`src/bai06_truy_van.py`](src/bai06_truy_van.py) | Hoàn thành |
| Dữ liệu đầu vào | [`data/documents/`](data/documents/) | 10 file UTF-8 |
| Kiểm thử | [`tests/`](tests/) | 54 test cases |
| CI | [`../.github/workflows/ci.yml`](../.github/workflows/ci.yml) | Đã cấu hình |

## Lệnh kiểm tra chuẩn

Các lệnh dưới đây được chạy từ thư mục `lab01-xu-ly-van-ban`:

```powershell
..\.venv\Scripts\python.exe -m compileall -q src tests
..\.venv\Scripts\python.exe -m unittest discover -s tests -p "test_*.py" -v
```

Để chạy chương trình tìm kiếm tương tác:

```powershell
..\.venv\Scripts\python.exe src\bai06_truy_van.py
```

Nếu đang đứng ở thư mục gốc repository, chuyển vào thư mục Buổi 1 trước:

```powershell
Set-Location lab01-xu-ly-van-ban
```

## Checklist hoàn thành

- [x] Mã nguồn bám sát sáu bài trong tài liệu đề bài.
- [x] Các hàm được tách thành module để có thể tái sử dụng và kiểm thử.
- [x] Dữ liệu mẫu có ID ổn định, nội dung UTF-8 và tài liệu mô tả riêng.
- [x] Có test cho trường hợp hợp lệ, dữ liệu rỗng, dữ liệu sai và luồng CLI.
- [x] Kiểm tra cú pháp và toàn bộ test chạy thành công.
- [x] README hướng dẫn được cập nhật để người khác có thể clone, cài đặt và chạy lại.

**Trạng thái:** Buổi 1 hoàn thành ở Phase 11. Không còn hạng mục bắt buộc nào trong phạm vi thực hành 1.
