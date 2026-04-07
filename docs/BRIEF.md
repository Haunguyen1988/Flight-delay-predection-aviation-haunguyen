# 💡 BRIEF: Flight Delay Predictor

**Ngày tạo:** 2026-04-07
**Brainstorm cùng:** User (Product Owner)

---

## 1. VẤN ĐỀ CẦN GIẢI QUYẾT
Hãng bay cần dự đoán chuyến bay nào sẽ bị delay và tìm ra quy luật từ dữ liệu lịch sử để cải thiện vận hành.

## 2. GIẢI PHÁP ĐỀ XUẤT
Web App phân tích & dự đoán delay chuyến bay, hiển thị trực quan bằng dashboard và biểu đồ tương tác.

## 3. ĐỐI TƯỢNG SỬ DỤNG
- **Primary:** Nhân viên hãng bay, Nhà phân tích dữ liệu
- **Secondary:** Researcher (chính user)

## 4. NGHIÊN CỨU THỊ TRƯỜNG
### Đối thủ:
| App | Điểm mạnh | Điểm yếu |
|-----|-----------|----------|
| Cirium | Data khổng lồ, dự đoán chính xác | Enterprise đắt, đóng |
| FlightAware | Tracking realtime, API tốt | Thiên tracking, phí cao |
| Flighty | UX đẹp, AI prediction | Chỉ cho hành khách |
| Power BI + ZoomCharts | Dashboard tùy biến | Không có sẵn ML |

### Điểm khác biệt:
- Miễn phí, mã nguồn mở cho nghiên cứu
- Kết hợp ML prediction + Dashboard analytics + Export báo cáo

## 5. TÍNH NĂNG

### 🚀 MVP (Bắt buộc có):
- [ ] Dashboard tổng quan delay
- [ ] Biểu đồ phân tích theo tuyến bay, thời tiết, giờ bay
- [ ] Dự đoán delay bằng AI/ML
- [ ] Import & xử lý dataset

### 🎁 Phase 2 (Làm sau):
- [ ] Export báo cáo (PDF/Excel)
- [ ] Cảnh báo realtime
- [ ] SHAP - Giải thích lý do dự đoán

### 💭 Backlog (Cân nhắc):
- [ ] Đăng nhập / phân quyền
- [ ] Tích hợp API flight data realtime
- [ ] Responsive mobile

## 6. ƯỚC TÍNH SƠ BỘ
- **Độ phức tạp:** Trung bình - Phức tạp
- **Rủi ro:** Dataset quality, ML model tuning (class imbalance)

## 7. BƯỚC TIẾP THEO
→ Chạy `/plan` để lên thiết kế chi tiết
