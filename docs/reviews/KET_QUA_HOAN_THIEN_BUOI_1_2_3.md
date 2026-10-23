# Kết quả hoàn thiện Buổi 1–3

Ngày: 23/10/2026. Buổi 4–5 chưa triển khai.

## Kết quả từng phase

| Phase | Công việc đã thực hiện | Bằng chứng |
|---|---|---|
| 0 | Kiểm tra trạng thái Git, giữ hai tài liệu rà soát đang có, chốt mốc | Trước sửa: 82 test đạt; không tạo commit tự động |
| 1 | Tách từng câu trước khi bỏ dấu câu, từ chối so khớp query dấu câu | Regression test kiểm tra token, TF, DF và postings; 56 test Buổi 1 đạt |
| 2 | Ghi index vào thư mục tạm cùng ổ đĩa; commit xong mới thay, khôi phục khi thay lỗi; đóng writer/index; kiểm tra ID trùng | Test nguồn thiếu/rỗng/nội dung sai, generator ghi lỗi, lỗi rename, rebuild lại thành công |
| 3 | Giới hạn toán hạng ở chế độ thân thiện; giữ chế độ advanced; giữ optional đúng ngữ nghĩa đề | Test từ chối OR, field, ngoặc, boost; kiểm tra đầy đủ tập kết quả Boolean/phrase/slop/wildcard |
| 4 | EOF/Ctrl+C thoát gọn; nhập lại lựa chọn sai Buổi 2; số tài liệu thực tế; lỗi đọc file Buổi 3 | Test EOF khi nhập/chọn, dữ liệu tùy chỉnh, file thiếu và UTF-8 lỗi |
| 5 | Workflow matrix chạy độc lập ba lab; tải punkt/punkt_tab với kiểm tra thành công | Đã sửa YAML; chưa chạy GitHub Actions từ xa |
| 6 | Sửa đường dẫn README, số test, mô tả rebuild/query; cập nhật báo cáo cũ | Compile và git diff --check đạt |

## Nghiệm thu tại máy

- Buổi 1: 56/56 test đạt.
- Buổi 2: 14/14 test đạt.
- Buổi 3: 22/22 test đạt.
- Tổng: 92/92, tăng 10 test so với mốc đầu. Một test có thể kiểm tra nhiều trường hợp.
- Compile từng thư mục thành công.
- Sáu script Buổi 1 chạy subprocess với đầu vào mẫu, tất cả exit code 0. Luồng tìm/chọn tài liệu Buổi 2 và Buổi 3 được kiểm tra bằng CLI integration test dùng index tạm.
- Dữ liệu Buổi 1 vẫn có 388 token; query python vẫn trả [1, 2, 10]. Không sửa giá trị kỳ vọng test cũ để che thay đổi kết quả.
- git diff --check không có lỗi khoảng trắng.

## Bảng đáp án truy vấn kiểm soát

Test Buổi 3 tạo ba tài liệu a=`alpha beta gamma`, b=`alpha delta beta`, c=`beta alpha`. Bảng này không áp dụng cho CS-Docs gốc.

| Query | Tài liệu mong đợi |
|---|---|
| alpha AND gamma | a |
| gamma OR delta | a, b |
| alpha NOT delta | a, c |
| "alpha beta" | a |
| "alpha beta"~2 | a, b |
| gam* | a |
| gamm? | a |
| required=alpha; optional=gamma delta | a, b |

## Quy ước và giới hạn kiểm chứng

Các lab chạy độc lập; helper safe_index.py được đặt trong từng lab để script vẫn chạy trực tiếp mà không phụ thuộc đường dẫn import của lab khác. Chỉ hỗ trợ một tiến trình xây index tại một thời điểm. Đây là thay thư mục có khôi phục khi lỗi thao tác, không cam kết giao dịch chống mất điện hoặc truy cập đồng thời. Đóng phiên tìm kiếm trước rebuild trên Windows.

Môi trường kiểm tra là .venv hiện có. Chưa thực hiện cài đặt sạch trên máy khác và chưa push để chạy CI từ xa. Hai bước này cần xác nhận trước khi tuyên bố đã kiểm chứng đa môi trường. Dữ liệu tài liệu và đề Buổi 4–5 được giữ nguyên.

Các checklist trong kế hoạch phản ánh phần đã thực hiện; phần cài đặt sạch để mở. Báo cáo rà soát Buổi 1 giữ ví dụ lỗi cũ làm lịch sử và có ghi rõ đã sửa ở đầu file.
