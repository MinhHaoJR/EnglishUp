# Ảnh chụp màn hình cho báo cáo

Chụp ngày 10/11/2026 bằng Chrome headless, khung nhìn 1440×900, giao diện sáng, ngôn ngữ giao diện tiếng Việt, đang học tiếng Anh. Dữ liệu là một phiên luyện tập thật trên máy (20 thẻ từ vựng, 1 bài đọc). Ảnh 11–14 dùng tài khoản thử `screenshot@englishup.test` (tên hiển thị "Học viên thử"); mật khẩu chỉ nằm trong file cục bộ `.env.test-account`, không commit. Bảng xếp hạng có 6 học viên demo tạo bằng lệnh `demo`.

| Ảnh | Màn hình | Gợi ý chú thích |
|---|---|---|
| `00-dang-nhap.png` | Đăng nhập | Lối vào riêng: tấm biển xanh nêu ba điều tài khoản mang lại, form đăng nhập/tạo tài khoản bên cạnh; học không cần tài khoản. |
| `00b-dang-nhap-dien-thoai.png` | Đăng nhập trên điện thoại (375px) | Tấm biển xếp trên form; khi tạo tài khoản, danh sách điều kiện mật khẩu đánh dấu ngay khi gõ. |
| `01-tong-quan.png` | Tổng quan | Kế hoạch học hôm nay dạng lộ trình: chặng đã xong có dấu ✓, nút bắt đầu chặng kế tiếp; tiến độ theo kỹ năng và theo tuần. |
| `02-tu-vung-chu-de.png` | Từ vựng, chọn chủ đề | Danh mục chủ đề theo nhóm (Hằng ngày, Công việc & học tập, Chuyên ngành, Ôn thi nâng cao) với số từ mỗi chủ đề. |
| `03-tu-vung-cum-tu.png` | Từ vựng, cụm từ | Mỗi chủ đề chia thành cụm tối đa 20 từ, hai cột "Cần học" và "Đã nhớ", bốn chế độ luyện. |
| `04-the-ghi-nho.png` | Thẻ ghi nhớ | Thẻ đã lật với nghĩa, định nghĩa, ví dụ; bốn mức tự đánh giá cho lịch ôn SM-2 (phím 1–4). |
| `05-luyen-doc.png` | Luyện đọc | Bài đọc ở cột trái, câu hỏi từng câu một ở cột phải. |
| `05b-luyen-doc-tra-tu.png` | Tra từ trong bài đọc | Bấm một từ để xem phiên âm, nghĩa, nghe phát âm và thêm vào sổ từ. |
| `06-luyen-nghe.png` | Luyện nghe | Nghe cả bài hoặc từng câu, chỉnh tốc độ; bản chép lời mở sau khi trả lời. |
| `07-luyen-noi.png` | Luyện nói | Đọc nhại mẫu: nghe mẫu, ghi âm (chỉ trong bộ nhớ), nhận dạng giọng nói tuỳ chọn, tự đánh giá. |
| `08-luyen-viet.png` | Luyện viết | Đề viết thư, đếm từ, tự lưu nháp, nhận xét theo quy tắc không cần mạng. |
| `09-cau-truc-cau.png` | Cấu trúc câu | 100 cấu trúc có ví dụ song ngữ, lọc theo nhóm, chế độ học và luyện điền chỗ trống. |
| `10-dong-nghia.png` | Đồng nghĩa & trái nghĩa | Học theo mức A1–C2, mỗi mục gắn với một nghĩa cụ thể và có ví dụ. |
| `11-tai-khoan.png` | Tài khoản | Hai nửa cạnh nhau: "Chỉ bạn thấy" (email, tổng điểm, điểm hôm nay trên 300, chuỗi ngày, đồng bộ) và "Mọi người thấy" (hàng của bạn trên bảng xếp hạng, xem trước ngay khi sửa tên; không bao giờ hiện email); bên dưới là hành trình học theo ngày với màu từng kỹ năng và huy hiệu. |
| `12-thanh-tich.png` | Thành tích, huy hiệu | Sáu huy hiệu do máy chủ xét sau mỗi lần đồng bộ, kèm điểm thưởng. |
| `12b-bang-xep-hang.png` | Bảng xếp hạng | Xếp hạng theo tuần (giờ Việt Nam) và mọi thời gian; hàng của người học được tô nổi. |
| `13-dua-60-giay.png` | Đua 60 giây | Đề và chấm điểm ở máy chủ; thời gian, điểm ván và combo. |
| `14-tro-giang-ai.png` | Trợ giảng AI, câu trả lời | Lịch sử dạng khung bên trái (khung đang mở có chấm vàng); câu trả lời từ bài học với nguồn [1], [2] gắn nhãn kỹ năng; còn 19/20 câu hôm nay. |
| `14b-tro-giang-moi.png` | Trợ giảng AI, cuộc trò chuyện mới | Bốn câu hỏi gợi ý, mỗi câu một kỹ năng; ô soạn với nút gửi và ghi chú quyền riêng tư. |

Ảnh 14 chụp khi dữ liệu RAG chưa có 100 cấu trúc câu (nạp lúc 15:15 ngày 10/11/2026); câu hỏi trong ảnh là về từ vựng nên không bị ảnh hưởng.

Chụp lại: chạy `npm run dev`, rồi dùng Chrome ở kích thước 1440×900.
