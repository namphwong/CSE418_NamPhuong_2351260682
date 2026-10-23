"""Tập 10 tài liệu dùng cho Bài 3.

Đề bài yêu cầu gõ trực tiếp tập tài liệu D vào trong code. Mã tài liệu được
lưu trong index; toàn văn được giữ ở đây để truy xuất sau khi chọn kết quả.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Document:
    document_id: int
    title: str
    content: str


DEFAULT_DOCUMENTS: tuple[Document, ...] = (
    Document(
        1,
        "Lập trình Python",
        "Python là ngôn ngữ lập trình dễ đọc và phù hợp để xây dựng nhiều loại chương trình. "
        "Người học có thể dùng Python để xử lý dữ liệu, tạo ứng dụng web và thực hiện các bài toán tìm kiếm thông tin. "
        "Một chương trình Python thường được chia thành các hàm nhỏ để dễ kiểm tra và bảo trì.",
    ),
    Document(
        2,
        "Xử lý dữ liệu",
        "Xử lý dữ liệu gồm các bước thu thập, làm sạch, biến đổi và phân tích thông tin. "
        "Python cung cấp nhiều thư viện giúp chương trình đọc dữ liệu từ file, loại bỏ dữ liệu sai và tạo ra kết quả dễ hiểu. "
        "Dữ liệu được chuẩn hóa sẽ hỗ trợ tốt cho việc tìm kiếm và xây dựng mô hình.",
    ),
    Document(
        3,
        "Tìm kiếm thông tin",
        "Hệ thống tìm kiếm thông tin tiếp nhận truy vấn của người dùng rồi tìm các tài liệu phù hợp. "
        "Để tìm nhanh, hệ thống có thể xây dựng chỉ mục từ và lưu danh sách tài liệu chứa từng từ. "
        "Kết quả tìm kiếm cần được sắp xếp để tài liệu liên quan xuất hiện trước.",
    ),
    Document(
        4,
        "Trí tuệ nhân tạo",
        "Trí tuệ nhân tạo giúp máy tính thực hiện những nhiệm vụ cần khả năng suy luận hoặc nhận dạng. "
        "Một hệ thống trí tuệ nhân tạo thường sử dụng dữ liệu để học quy luật và tạo ra dự đoán. "
        "Chất lượng dữ liệu và cách đánh giá mô hình có ảnh hưởng lớn đến kết quả.",
    ),
    Document(
        5,
        "Cơ sở dữ liệu",
        "Cơ sở dữ liệu lưu trữ thông tin có cấu trúc để chương trình có thể truy vấn và cập nhật. "
        "Một hệ quản trị cơ sở dữ liệu cần bảo đảm dữ liệu nhất quán, hạn chế trùng lặp và hỗ trợ nhiều người dùng. "
        "Các bảng, khóa và chỉ mục giúp hệ thống làm việc hiệu quả hơn.",
    ),
    Document(
        6,
        "Mạng máy tính",
        "Mạng máy tính kết nối các thiết bị để trao đổi dữ liệu và sử dụng chung tài nguyên. "
        "Trong một hệ thống mạng, máy chủ cung cấp dịch vụ còn máy khách gửi yêu cầu và nhận kết quả. "
        "Thiết kế mạng cần quan tâm đến tốc độ, độ ổn định và an toàn thông tin.",
    ),
    Document(
        7,
        "Hệ điều hành",
        "Hệ điều hành quản lý bộ nhớ, bộ xử lý, file và các thiết bị của máy tính. "
        "Khi một chương trình được chạy, hệ điều hành phân bổ tài nguyên và kiểm soát quá trình thực thi. "
        "Cơ chế phân quyền giúp bảo vệ dữ liệu và ngăn chương trình truy cập trái phép.",
    ),
    Document(
        8,
        "Lập trình web",
        "Lập trình web tạo ra các trang và dịch vụ hoạt động qua mạng Internet. "
        "Một ứng dụng web thường nhận truy vấn HTTP, xử lý dữ liệu ở máy chủ rồi trả kết quả cho trình duyệt. "
        "Ứng dụng có thể kết nối cơ sở dữ liệu để lưu tài khoản, nội dung và lịch sử hoạt động.",
    ),
    Document(
        9,
        "An toàn thông tin",
        "An toàn thông tin tập trung vào việc bảo vệ dữ liệu khỏi mất mát, sửa đổi và truy cập trái phép. "
        "Người dùng nên sử dụng mật khẩu mạnh, xác thực nhiều bước và cập nhật phần mềm thường xuyên. "
        "Trong mạng máy tính, mã hóa và phân quyền giúp giảm nguy cơ lộ thông tin.",
    ),
    Document(
        10,
        "Học máy",
        "Học máy là phương pháp để chương trình học mẫu từ dữ liệu và đưa ra dự đoán cho dữ liệu mới. "
        "Một quy trình học máy thường gồm chuẩn bị dữ liệu, huấn luyện mô hình và đánh giá kết quả. "
        "Python được dùng rộng rãi để xây dựng mô hình phân loại, dự báo và nhận dạng.",
    ),
)


def get_document(documents: tuple[Document, ...], document_id: int) -> Document:
    """Lấy tài liệu theo mã 1-based được lưu trong index."""

    for document in documents:
        if document.document_id == document_id:
            return document
    raise KeyError(f"Không tồn tại mã tài liệu: {document_id}")

