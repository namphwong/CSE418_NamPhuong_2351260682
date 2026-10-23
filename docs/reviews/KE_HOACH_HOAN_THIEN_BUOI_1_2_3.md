> Đã thực hiện các phase sửa mã nguồn và tài liệu ngày 23/10/2026. Các phát hiện bên dưới là mốc trước khi sửa. Kết quả cuối và giới hạn kiểm chứng được ghi trong KET_QUA_HOAN_THIEN_BUOI_1_2_3.md.

# Kế hoạch hoàn thiện Buổi 1–3

Ngày rà soát: 23/10/2026. Phạm vi: mã nguồn, dữ liệu, test, README, requirements, CI và cấu trúc repository đến Buổi 3. Không triển khai hoặc sửa nội dung Buổi 4–5.

## Kết quả hiện tại

Đã đối chiếu đề TH01, TH02 và PDF TH03 trong ZIP gốc. Các chức năng chính của cả ba buổi đã có. Chưa thể coi việc tất cả test đạt là bằng chứng hoàn thiện, vì có lỗi ngoài các ca kiểm thử hiện tại.

| Phần | Kết quả chạy lại |
|---|---|
| Buổi 1 | 54/54 test đạt |
| Buổi 2 | 11/11 test đạt |
| Buổi 3 | 17/17 test đạt |
| Compile cả ba thư mục | Thành công |
| CI | Chỉ chạy Buổi 1 |

Tổng cộng 82 test đạt trong môi trường `.venv` hiện tại. Chưa kiểm chứng cài đặt sạch trên máy khác hay trạng thái GitHub Actions từ xa. Báo cáo này chỉ bổ sung kế hoạch, chưa sửa mã nguồn.

## Các phát hiện

### F01 — Cần sửa: tách từ vượt qua ranh giới câu ở Buổi 1

`lab01-xu-ly-van-ban/src/bai03_tan_so_tu.py`, hàm `tokenize_document()` xóa dấu câu trước khi gọi Underthesea. Đã tái hiện `Tôi thích học. Sinh viên thích Python.` bị tách thành `tôi, thích, học sinh viên, thích, python`. Bài 4 và Bài 6 dùng lại hàm này: query `học` hoặc `sinh viên` bỏ sót tài liệu, query ghép sai `học sinh viên` lại tìm thấy. Chi tiết bổ sung trong `docs/reviews/RA_SOAT_BUOI_1.md`.

### F02 — Ưu tiên cao: tạo lại index lỗi làm mất index đang dùng

`lab03-xu-ly-cau-truy-van/index.py`, `build_index()` gọi `create_in()` và mở writer trước khi kiểm tra thư mục dữ liệu. Đã kiểm tra bằng index tạm có 5 tài liệu: gọi lại với thư mục nguồn không tồn tại gây `FileNotFoundError`, sau đó mở index thấy 0 tài liệu. Đây là mất trạng thái chỉ mục, không phải mất file tài liệu gốc. `document_paths()` còn nằm ngoài `try`, nên nhánh lỗi đó không đi qua `writer.cancel()` và `index.close()`.

Buổi 2 cũng tạo mới index trước khi xử lý hết dữ liệu. Cần áp dụng cùng cơ chế bảo vệ khi bổ sung xử lý lỗi; chưa tái hiện riêng mọi dạng lỗi ghi ở Buổi 2.

### F03 — Cần sửa: nhóm từ bắt buộc ở Buổi 3 có thể bị đổi thành OR

`lab03-xu-ly-cau-truy-van/search.py`, `build_friendly_query()` ghép trực tiếp đầu vào vào chuỗi cú pháp. Đã xác nhận required=`learning OR software` được parse thành OR, trái quy ước mọi từ trong nhóm phải cùng xuất hiện. required=`title:software` chuyển sang tìm trường title. Cần quy định cú pháp được phép trong chế độ thân thiện và từ chối hoặc xử lý như dữ liệu các toán tử không được hỗ trợ.

Lưu ý: nhóm tên `optional` hiện được kết hợp AND với required và yêu cầu ít nhất một từ trong nhóm xuất hiện. Hành vi này đúng ví dụ của đề TH03; không đổi sang cách hiểu chỉ tăng điểm tùy chọn.

### F04 — Cần sửa: CI thiếu Buổi 2 và 3

`.github/workflows/ci.yml` chỉ compile/test trong Buổi 1. Lỗi ở hai buổi sau vẫn có thể đi qua CI. Tên workflow cũng chỉ ghi Lab 01.

### F05 — Cần sửa: lệnh kiểm tra Buổi 3 sai đường dẫn

README Buổi 3 ghi chạy từ gốc nhưng lệnh đầu dùng `..\.venv\Scripts\python.exe`, trỏ ra thư mục cha của repository. Phải dùng `.\.venv\Scripts\python.exe` khi đứng ở gốc; sau khi chuyển vào thư mục lab mới dùng `..\`.

### F06 — Nên bổ sung: độ bền của CLI và vòng đời tài nguyên

- CLI Buổi 2 và 3 chưa bắt EOFError ở các bước input; kết thúc luồng nhập có thể tạo traceback.
- Buổi 2 chưa đóng đối tượng index ở các hàm xây dựng sau commit; cần finally để đóng cả khi lỗi.
- Buổi 2 in cố định “10 tài liệu” dù `run_cli()` nhận tập dữ liệu tùy chỉnh.
- Buổi 3 bắt lỗi file không tồn tại khi xem toàn văn, nhưng chưa xử lý lỗi giải mã UTF-8 hoặc lỗi đọc khác bằng thông báo thân thiện.
- Bổ sung kiểm tra ID trùng/không hợp lệ khi xây dựng index Buổi 2 để tránh một hit ánh xạ về sai toàn văn với dữ liệu tùy chỉnh. Tập 10 tài liệu hiện tại có ID hợp lệ.

Đây là cải thiện độ bền ngoài các luồng mẫu đang chạy thành công, không phải kết luận toàn bộ bài chưa làm.

### F07 — Nên bổ sung: query dấu câu và độ mạnh của test

Bài 2 Buổi 1 trả True với `contains_word('Sinh viên học.', '.')`. Nên báo query không hợp lệ hoặc trả False nếu chỉ có dấu câu.

Test Buổi 3 phần lớn chỉ xác nhận có một kết quả mong đợi; test proximity dùng cụm sát nhau nên chưa chứng minh đúng giới hạn khoảng cách. Chưa có test riêng ký tự đại diện `?`, mặc dù đề yêu cầu thử cả `?` và `*`.

## Kế hoạch theo phase

### Phase 0 — Chốt phạm vi và lưu mốc ban đầu

- [x] Ghi lại trạng thái Git và các thay đổi đang có, gồm báo cáo rà soát Buổi 1.
- [x] Lưu kết quả 54 + 11 + 17 test làm mốc so sánh.
- [x] Dùng thư mục tạm cho các test tạo/xây dựng lại index.
- [x] Giữ Buổi 4–5 ở trạng thái chưa triển khai.

Đầu ra: mốc kiểm thử và danh sách file được sửa. Không xóa `.venv`, dữ liệu mẫu hoặc tài liệu đề bài để “dọn folder”.

### Phase 1 — Sửa tính đúng đắn Buổi 1 (F01, F07)

- [x] Giữ dấu phân cách câu trước bước tách từ; lọc token dấu câu sau khi tokenizer chạy.
- [x] Duy trì chuẩn hóa Unicode, hoa/thường và chế độ whitespace.
- [x] Thêm regression test cho `Tôi thích học. Sinh viên thích Python.` và `Máy tính. Toán học.`.
- [x] Kiểm tra TF, DF, và postings trên tài liệu nhiều câu; không chỉ kiểm tra chuỗi token.
- [x] Quy định query chỉ chứa dấu câu ở Bài 2 và bổ sung test.
- [x] Chạy lại test Buổi 1; đo lại tổng token trên 10 file. Nếu kết quả đổi, kiểm tra nội dung trước khi đổi kỳ vọng test.

Nghiệm thu: không có token ghép vượt qua dấu chấm; `học`, `sinh viên` tìm thấy tài liệu thử, `học sinh viên` không tìm thấy; test cũ và mới đạt.

### Phase 2 — Bảo vệ quá trình tạo index ở Buổi 2–3 (F02, F06)

- [x] Kiểm tra nguồn dữ liệu trước khi tạo index: thư mục tồn tại, có file, file UTF-8 hợp lệ, có tiêu đề và nội dung.
- [x] Xây index mới trong thư mục tạm riêng; chỉ thay index đích sau commit thành công. Thiết kế khôi phục index cũ nếu thao tác thay thế thất bại trên Windows.
- [x] Đặt toàn bộ vòng đời writer/index trong try/except/finally; cancel khi chưa commit và đóng tài nguyên ở mọi nhánh.
- [x] Áp dụng nguyên tắc tương tự cho các hàm build của Buổi 2; kiểm tra ID của dữ liệu tùy chỉnh.
- [x] Test rebuild thành công không nhân đôi tài liệu; rebuild thất bại với nguồn thiếu, rỗng, lỗi nội dung vẫn giữ kết quả tìm kiếm index cũ.
- [x] Test có thể mở và xây lại index sau lỗi, không còn khóa do writer bị bỏ quên.

Nghiệm thu: index 5 tài liệu của Buổi 3 vẫn có 5 tài liệu sau lần rebuild thất bại; dữ liệu gốc không đổi; tài nguyên được giải phóng.

### Phase 3 — Hoàn thiện truy vấn Buổi 3 (F03, F07)

- [x] Xác định cú pháp nhập ở chế độ thân thiện: từ đơn, phrase, proximity/wildcard nếu tiếp tục hỗ trợ.
- [x] Không để OR/NOT, ngoặc hoặc field selector trong ô nhập tự thay đổi logic của ba nhóm; chọn cách từ chối rõ ràng hoặc xây đối tượng Query từ các toán hạng đã kiểm tra.
- [x] Giữ đúng ý nghĩa ví dụ đề: required AND (ít nhất một optional) AND NOT forbidden.
- [x] Giữ chế độ `--advanced` cho người chủ động nhập cú pháp Whoosh.
- [x] Test kết quả thực thi, không chỉ so chuỗi sinh ra; kiểm tra required chứa OR, `title:`, ngoặc và ngoặc kép chưa đóng.
- [x] Dùng tập tài liệu nhỏ có đáp án biết trước để kiểm tra đủ AND/OR/NOT, phrase đúng/sai thứ tự, proximity trong/ngoài khoảng cách, `*` và `?`.

Nghiệm thu: không thể vô tình bỏ điều kiện bắt buộc bằng cú pháp nhập; ví dụ trong đề vẫn có cùng ngữ nghĩa; đủ ca dương và âm cho từng kiểu query.

### Phase 4 — Hoàn thiện CLI Buổi 2–3 (F06)

- [x] Bắt EOFError ở mọi bước nhập để thoát gọn; nếu hỗ trợ Ctrl+C thì xử lý nhất quán.
- [x] Cho nhập lại lựa chọn sai thay vì bắt người dùng nhập lại toàn bộ truy vấn; thống nhất hướng dẫn q ở các bước cho phép thoát.
- [x] Hiển thị số tài liệu thực tế ở Buổi 2 bằng độ dài tập dữ liệu.
- [x] Xử lý lỗi đọc file/encoding khi xem toàn văn bằng thông báo và cho tiếp tục hoặc thoát rõ ràng.
- [x] Test kết thúc đầu vào lúc nhập query/chọn kết quả, lựa chọn không phải số, số ngoài phạm vi và file bị mất sau khi lập chỉ mục.

Nghiệm thu: luồng hợp lệ tìm và xem đúng tài liệu; các lỗi nhập thông thường không tạo traceback.

### Phase 5 — CI và khả năng chạy lại (F04)

- [x] Đổi tên workflow để thể hiện phạm vi Buổi 1–3.
- [x] Chạy compile và unittest riêng từng lab, có thể dùng matrix working-directory. Không gộp import trực tiếp các package cùng tên `src` trong một tiến trình.
- [x] Giữ bước chuẩn bị NLTK và xác nhận dữ liệu tokenizer thực sự tải thành công.
- [ ] Cài đặt sạch trên máy/môi trường khác: chưa thực hiện; bộ nghiệm thu dùng .venv hiện có.
- [x] Giữ requirements hiện tại và phiên bản môi trường đã ghi trong README; không pin thêm khi chưa có bằng chứng cần thiết.

Nghiệm thu: cả ba lab được CI chạy độc lập; lỗi ở bất kỳ lab nào làm job tương ứng thất bại.

### Phase 6 — Đồng bộ tài liệu và nghiệm thu cuối (F05)

- [x] Sửa đường dẫn lệnh kiểm tra trong README Buổi 3; ghi rõ thư mục đứng chạy cho từng nhóm lệnh.
- [x] Cập nhật pipeline Buổi 1, số test thực tế, tổng token nếu thay đổi.
- [x] Ghi quy tắc nhóm optional, cú pháp cho phép và cách rebuild sau khi sửa dữ liệu ở README Buổi 3.
- [x] Bổ sung bảng query và tên tài liệu mong đợi trong báo cáo nghiệm thu, dùng tập dữ liệu kiểm soát.
- [x] Cập nhật README gốc và báo cáo Buổi 1 bằng kết quả sau sửa; không giữ kết luận lỗi cũ như thể vẫn chưa sửa.
- [x] Chạy compile, test cả ba lab và một phiên CLI từng bài; kiểm tra git diff để không lẫn index sinh tự động/cache.
- [x] Buổi 4–5 tiếp tục ghi “Chưa thực hiện”.

Nghiệm thu: các lệnh hướng dẫn chạy đúng từ vị trí được chỉ định; tổng test phản ánh lần chạy cuối; các lỗi F01–F05 đã đóng bằng bằng chứng kiểm tra.

## Thứ tự và giới hạn

Thực hiện Phase 0 → 1 → 2 → 3 → 4 → 5 → 6. Mỗi phase nên có một mốc Git riêng sau khi kiểm thử đạt để dễ kiểm tra và quay lại. Ưu tiên F02 vì mất index đang dùng, tiếp theo F01/F03 vì sai kết quả; sau đó xử lý CI, hướng dẫn và độ bền CLI.

Không cần viết lại toàn bộ ba buổi, thêm web UI, hoặc triển khai đánh giá truy hồi/phân loại văn bản của Buổi 4–5. Những tính năng chính đã đúng đề cần được giữ và kiểm tra hồi quy.
