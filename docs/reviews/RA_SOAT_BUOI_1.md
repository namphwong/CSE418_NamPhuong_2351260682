> Cập nhật sau sửa ngày 23/10/2026: các lỗi trong báo cáo lịch sử dưới đây đã được xử lý. Buổi 1 đạt 56/56 test, tổng token dữ liệu vẫn là 388. Xem KET_QUA_HOAN_THIEN_BUOI_1_2_3.md.

# Rà soát bài thực hành Buổi 1

Ngày kiểm tra: 23/10/2026.

## Kết luận

Đã có đủ mã nguồn cho 6 bài, 10 tài liệu UTF-8, hướng dẫn chạy và bộ kiểm thử. Tuy nhiên, cần sửa lỗi xử lý ranh giới câu trong hàm tách từ dùng chung trước khi kết luận bài hoàn chỉnh. Lỗi này ảnh hưởng Bài 3, Bài 4 và Bài 6.

Đây là báo cáo rà soát và danh sách công việc; chưa sửa mã nguồn chương trình.

## Căn cứ và kết quả kiểm tra

- Đối chiếu cả hai trang của `../TH01-Thuc hanh xu ly van ban.pdf`.
- Đọc mã nguồn trong `src/`, các test, dữ liệu và README.
- Chạy `..\.venv\Scripts\python.exe -m compileall -q src tests`: thành công.
- Chạy `..\.venv\Scripts\python.exe -m unittest discover -s tests -p "test_*.py" -v`: 54/54 test thành công.
- Chạy thêm ví dụ nhiều câu ngoài bộ test: phát hiện lỗi ghép từ qua dấu chấm.
- Các kết quả trên được kiểm tra trong môi trường `.venv` hiện có; chưa xác nhận cài đặt mới trên máy khác hoặc kết quả chạy GitHub Actions.

## Đối chiếu từng bài với đề

| Bài | Kết quả rà soát |
|---|---|
| 1 | Đã dùng NLTK word_tokenize và PorterStemmer, hiển thị token và stem tương ứng; chưa thấy lỗi trong phạm vi đã kiểm tra. |
| 2 | Đã nhập văn bản, tách từ bằng Underthesea và kiểm tra từ đầy đủ; có điểm nên cải thiện về query chỉ chứa dấu câu. |
| 3 | Đã đếm bằng dictionary; cần sửa thứ tự xử lý dấu câu và tách từ. |
| 4 | Có 4 tài liệu một câu khai báo trong code, mỗi từ chỉ được tính một lần trong mỗi tài liệu; chịu ảnh hưởng hàm tách từ của Bài 3 khi dùng dữ liệu khác. |
| 5 | Có nhập hai danh sách, giao và hợp bằng hai con trỏ; hỗ trợ danh sách rỗng, phần tử trùng và từ chối dữ liệu chưa sắp xếp; chưa thấy lỗi trong phạm vi đã kiểm tra. |
| 6 | Có đủ 10 file, đọc UTF-8, lưu toàn văn, chỉ mục từ sang ID, truy vấn và xem toàn văn; chịu ảnh hưởng lỗi tách từ khi tài liệu có ranh giới câu phù hợp để tái hiện. |

## Công việc cần làm

### 1. Cần sửa: bảo toàn ranh giới câu khi tách từ tiếng Việt

Vị trí: `src/bai03_tan_so_tu.py`, hàm `tokenize_document()`, dòng 60-66 tại thời điểm rà soát.

Hiện tại chương trình gọi `normalize_text(remove_punctuation(text))` trước khi gọi Underthesea. Dấu chấm bị thay bằng khoảng trắng khiến tokenizer có thể ghép các âm tiết nằm ở hai câu khác nhau.

Ví dụ đã chạy:

```text
Đầu vào: Tôi thích học. Sinh viên thích Python.
Token hiện tại: ['tôi', 'thích', 'học sinh viên', 'thích', 'python']
Token mong đợi: ['tôi', 'thích', 'học', 'sinh viên', 'thích', 'python']
```

Ảnh hưởng đã xác nhận:

- Bài 3: đếm nhầm `học sinh viên`, làm mất các từ `học` và `sinh viên`.
- Bài 4: với một tài liệu là câu trên, kết quả chứa `học sinh viên: 1`, thiếu hai từ thực tế.
- Bài 6: với `{1: văn_bản_trên}`, query `học` và `sinh viên` đều trả `[]`; query `học sinh viên` lại trả `[1]`.
- Ví dụ khác: `Máy tính. Toán học.` đang thành `['máy tính toán', 'học']`.

Các bước thực hiện:

- [ ] Với chế độ tiếng Việt, giữ dấu phân cách khi đưa văn bản vào tokenizer; lọc token dấu câu sau khi tách từ. Có thể tách theo câu trước nếu cần.
- [ ] Chuẩn hóa Unicode và chữ thường theo cách nhất quán; không làm mất ranh giới câu trước khi tokenizer xử lý.
- [ ] Duy trì hành vi của chế độ `language="whitespace"` và kiểm tra lại trường hợp từ ngăn cách bằng dấu phẩy, dấu gạch nối.
- [ ] Thêm test hồi quy cho hai ví dụ trên vào `tests/test_bai03_tan_so_tu.py`.
- [ ] Thêm test Bài 4 xác nhận `học` và `sinh viên` được đếm đúng theo số tài liệu.
- [ ] Thêm test Bài 6 với một tài liệu mẫu nhiều câu: hai query hợp lệ trả `[1]`, token ghép sai không được đưa vào chỉ mục.
- [ ] Chạy lại toàn bộ test. Nếu kết quả dữ liệu thật thay đổi, đối chiếu toàn văn và token trước khi sửa giá trị kỳ vọng trong test.

Tiêu chí hoàn thành: không tạo từ vượt qua dấu kết thúc câu; TF, DF và kết quả tìm kiếm đều đúng với ví dụ tái hiện; các chức năng hiện có vẫn chạy.

### 2. Cần cập nhật sau khi sửa: tài liệu và kết quả kiểm tra

Vị trí: `README.md` của Buổi 1 và phần bàn giao Buổi 1 trong README gốc.

- [ ] Cập nhật sơ đồ xử lý Bài 3 theo thứ tự xử lý thực tế sau khi sửa.
- [ ] Ghi thêm trường hợp nhiều câu vào mô tả kiểm thử.
- [ ] Cập nhật số test sau khi bổ sung; hiện tại con số 54 là đúng.
- [ ] Kiểm tra lại tổng token 388 nếu sửa tokenizer; chỉ cập nhật khi đã chạy đo lại.
- [ ] Chỉ xác nhận lại trạng thái hoàn thành sau khi kiểm tra hồi quy thành công.

### 3. Nên cải thiện: không coi dấu câu là một từ truy vấn ở Bài 2

Vị trí: `src/bai02_tach_tu_tieng_viet.py`, hàm `contains_token()`.

Đã tái hiện: `contains_word('Sinh viên học.', '.')` trả `True`. Nguyên nhân là danh sách token giữ dấu câu, còn query chỉ được kiểm tra khác rỗng. Đây là điểm cải thiện ngữ nghĩa của yêu cầu kiểm tra một từ; không cản trở các query từ thông thường.

- [ ] Quy định rõ query chỉ chứa dấu câu sẽ bị báo không hợp lệ hoặc trả `False`.
- [ ] Giữ danh sách token hiển thị nếu muốn minh họa kết quả tokenizer, nhưng loại dấu câu khỏi phần so khớp từ.
- [ ] Bổ sung test cho `.`, `!!!`, query chỉ có khoảng trắng và query từ tiếng Việt hợp lệ.
- [ ] Ghi quy ước này trong README.

## Lệnh nghiệm thu sau khi sửa

Chạy từ thư mục `lab01-xu-ly-van-ban`:

```powershell
..\.venv\Scripts\python.exe -m compileall -q src tests
..\.venv\Scripts\python.exe -m unittest discover -s tests -p "test_*.py" -v
..\.venv\Scripts\python.exe src\bai03_tan_so_tu.py
..\.venv\Scripts\python.exe src\bai06_truy_van.py
```

Khi chạy Bài 3, nhập ví dụ nhiều câu ở mục 1 để kiểm tra trực tiếp. Khi chạy Bài 6 với dữ liệu hiện có, kiểm tra `python` trả ID `1, 2, 10`, query không tồn tại trả rỗng, chọn ID `1` hiện đúng toàn văn, ID sai có thông báo và `q` thoát. Test với tài liệu nhiều câu mới cần kiểm tra riêng như mô tả ở mục 1.

Không cần bổ sung giao diện web, truy vấn Boolean hay xếp hạng TF-IDF để đáp ứng đề Buổi 1. PDF đề bài không yêu cầu nộp báo cáo hoặc ảnh chụp; nếu giảng viên có hướng dẫn riêng ngoài file này thì cần đối chiếu thêm.
