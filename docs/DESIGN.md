# 🎨 DESIGN: Flight Delay Predictor

Ngày tạo: 2026-04-07
Dựa trên: [SPECS](specs/flight-delay-predictor_spec.md)

---

## 1. Cách Lưu Thông Tin (Database)

### 1.1. Sơ đồ tổng quan

```
AIRLINES ──┐
           │ 1:N
           ▼
        FLIGHTS ──────► AIRPORTS (origin)
           │              AIRPORTS (destination)
           │
           ▼
      PREDICTIONS (lịch sử dự đoán)
```

### 1.2. Chi tiết bảng dữ liệu

#### flights (Chuyến bay - BẢNG CHÍNH)
| Cột | Kiểu | Mô tả |
|-----|------|-------|
| id | INTEGER PK | Mã tự tăng |
| flight_number | VARCHAR(10) | Số hiệu (VD: VN123) |
| airline_code | VARCHAR(5) FK | Mã hãng bay → airlines |
| origin_airport | VARCHAR(5) FK | Sân bay đi → airports |
| destination_airport | VARCHAR(5) FK | Sân bay đến → airports |
| scheduled_departure | DATETIME | Giờ khởi hành dự kiến |
| actual_departure | DATETIME | Giờ khởi hành thực tế |
| scheduled_arrival | DATETIME | Giờ đến dự kiến |
| actual_arrival | DATETIME | Giờ đến thực tế |
| delay_minutes | INTEGER | Số phút delay (0 = đúng giờ) |
| delay_reason | VARCHAR(50) | Lý do delay |
| distance | FLOAT | Khoảng cách (miles) |
| weather_condition | VARCHAR(30) | Thời tiết khi bay |
| day_of_week | INTEGER | Thứ (0=Mon, 6=Sun) |
| month | INTEGER | Tháng (1-12) |
| is_delayed | BOOLEAN | True nếu delay > 15 phút |

#### airports (Sân bay)
| Cột | Kiểu | Mô tả |
|-----|------|-------|
| code | VARCHAR(5) PK | Mã IATA (VD: SGN) |
| name | VARCHAR(100) | Tên đầy đủ |
| city | VARCHAR(50) | Thành phố |
| state | VARCHAR(50) | Bang/Tỉnh |
| latitude | FLOAT | Vĩ độ |
| longitude | FLOAT | Kinh độ |

#### airlines (Hãng bay)
| Cột | Kiểu | Mô tả |
|-----|------|-------|
| code | VARCHAR(5) PK | Mã hãng (VD: VN) |
| name | VARCHAR(100) | Tên hãng |

#### predictions (Lịch sử dự đoán)
| Cột | Kiểu | Mô tả |
|-----|------|-------|
| id | INTEGER PK | Mã tự tăng |
| created_at | DATETIME | Thời điểm dự đoán |
| airline_code | VARCHAR(5) | Hãng bay đã chọn |
| origin | VARCHAR(5) | Sân bay đi |
| destination | VARCHAR(5) | Sân bay đến |
| departure_datetime | DATETIME | Ngày giờ khởi hành |
| delay_probability | FLOAT | Xác suất delay (0-1) |
| estimated_delay_min | INTEGER | Ước tính delay (phút) |
| confidence | VARCHAR(10) | Low / Medium / High |

### 1.3. Indexes (Tối ưu tốc độ truy vấn)
- `flights`: index on (airline_code, origin_airport, destination_airport)
- `flights`: index on (scheduled_departure)
- `flights`: index on (is_delayed)
- `predictions`: index on (created_at DESC)

---

## 2. Danh Sách Màn Hình

| # | Tên | Mục đích | Route |
|---|-----|----------|-------|
| 1 | Dashboard | Xem tổng quan delay | `/` |
| 2 | Prediction | Dự đoán delay chuyến bay | `/predict` |
| 3 | Data Management | Import & xem dữ liệu | `/data` |

### 2.1. Dashboard Layout

```
┌─────────┬──────────────────────────────────────────────────┐
│         │  Header: Flight Delay Predictor    [Filter ▼]    │
│         ├──────────────────────────────────────────────────┤
│  S      │                                                  │
│  I      │  ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐           │
│  D      │  │Total │ │Delay │ │ Avg  │ │On-   │           │
│  E      │  │Flights│ │Rate  │ │Delay │ │Time  │           │
│  B      │  │125.4K│ │28.3%│ │ 32m  │ │71.7% │           │
│  A      │  └──────┘ └──────┘ └──────┘ └──────┘           │
│  R      │                                                  │
│         │  ┌─────────────────────┐ ┌──────────────────┐   │
│  🏠     │  │                     │ │                  │   │
│  🤖     │  │  Top Routes by      │ │  Delay by        │   │
│  📁     │  │  Delay Rate          │ │  Weather         │   │
│         │  │  (Bar Chart)        │ │  (Donut)         │   │
│         │  │                     │ │                  │   │
│         │  └─────────────────────┘ └──────────────────┘   │
│         │                                                  │
│         │  ┌─────────────────────┐ ┌──────────────────┐   │
│         │  │                     │ │                  │   │
│         │  │  Delay Trend        │ │  Delay by        │   │
│         │  │  by Month           │ │  Time of Day     │   │
│         │  │  (Line Chart)       │ │  (Area Chart)    │   │
│         │  │                     │ │                  │   │
│         │  └─────────────────────┘ └──────────────────┘   │
└─────────┴──────────────────────────────────────────────────┘
```

### 2.2. Prediction Layout

```
┌─────────┬──────────────────────────────────────────────────┐
│         │  Header: Prediction                              │
│         ├──────────────────────────────────────────────────┤
│         │                                                  │
│  S      │  ┌─────────────────────────────────────────┐    │
│  I      │  │  PREDICTION FORM                        │    │
│  D      │  │                                         │    │
│  E      │  │  Airline:     [Vietnam Airlines  ▼]     │    │
│  B      │  │  From:        [SGN - Tan Son Nhat ▼]    │    │
│  A      │  │  To:          [HAN - Noi Bai      ▼]    │    │
│  R      │  │  Date/Time:   [2026-04-15  08:00  ]     │    │
│         │  │                                         │    │
│         │  │         [ 🔮 Predict Delay ]             │    │
│         │  └─────────────────────────────────────────┘    │
│         │                                                  │
│         │  ┌─────────────────────────────────────────┐    │
│         │  │  RESULT                                 │    │
│         │  │                                         │    │
│         │  │     ┌───────────┐                       │    │
│         │  │     │   73%     │   Delay Probability   │    │
│         │  │     │  (Gauge)  │                       │    │
│         │  │     └───────────┘                       │    │
│         │  │                                         │    │
│         │  │  ⏱️ Est. Delay: ~25 minutes              │    │
│         │  │  📊 Confidence: High ✅                  │    │
│         │  └─────────────────────────────────────────┘    │
│         │                                                  │
│         │  ┌─────────────────────────────────────────┐    │
│         │  │  HISTORY (Recent Predictions)           │    │
│         │  │  • VN123 SGN→HAN 08:00 → 73% delay     │    │
│         │  │  • VJ456 DAD→SGN 14:00 → 12% delay     │    │
│         │  └─────────────────────────────────────────┘    │
└─────────┴──────────────────────────────────────────────────┘
```

### 2.3. Data Management Layout

```
┌─────────┬──────────────────────────────────────────────────┐
│         │  Header: Data Management                         │
│         ├──────────────────────────────────────────────────┤
│         │                                                  │
│  S      │  ┌─────────────────────────────────────────┐    │
│  I      │  │  📂 UPLOAD ZONE                         │    │
│  D      │  │                                         │    │
│  E      │  │    Drag & drop CSV file here            │    │
│  B      │  │    or [Browse Files]                     │    │
│  A      │  │                                         │    │
│  R      │  │    ████████████░░░░ 75% uploading...    │    │
│         │  └─────────────────────────────────────────┘    │
│         │                                                  │
│         │  📊 Dataset: 500,000 flights | 12 columns        │
│         │                                                  │
│         │  🔍 [Search...] [Airline ▼] [Airport ▼] [Date ▼]│
│         │                                                  │
│         │  ┌────┬────────┬──────┬──────┬───────┬────┐    │
│         │  │ #  │Flight  │Route │Date  │Delay  │Sta │    │
│         │  ├────┼────────┼──────┼──────┼───────┼────┤    │
│         │  │ 1  │VN123  │SGN→HAN│04/15│ 25min│ 🔴 │    │
│         │  │ 2  │VJ456  │DAD→SGN│04/15│ 0    │ 🟢 │    │
│         │  │ 3  │QH789  │HAN→CXR│04/15│ 45min│ 🔴 │    │
│         │  └────┴────────┴──────┴──────┴───────┴────┘    │
│         │                                                  │
│         │  ◀ 1 2 3 ... 500 ▶                               │
└─────────┴──────────────────────────────────────────────────┘
```

---

## 3. API Design (Cửa để app nói chuyện với server)

### 3.1. Data Endpoints

```
GET /api/flights?page=1&limit=20&airline=VN&delayed=true
→ Trả về danh sách chuyến bay (phân trang, có filter)

GET /api/flights/stats
→ Trả về: { total, delayed_count, delay_rate, avg_delay_min, ontime_rate }

GET /api/flights/by-route?top=10
→ Trả về: [{ route: "SGN→HAN", total: 5000, delayed: 1500, rate: 30% }]

GET /api/flights/by-weather
→ Trả về: [{ weather: "Rain", total: 3000, delayed: 1200, rate: 40% }]

GET /api/flights/by-time?group=hour
→ Trả về: [{ hour: 8, total: 2000, delayed: 400, rate: 20% }]

POST /api/data/upload
→ Input: CSV file (multipart/form-data)
→ Output: { rows_imported: 500000, duration_seconds: 25 }
```

### 3.2. Prediction Endpoints

```
POST /api/predict
→ Input: { airline, origin, destination, datetime }
→ Output: { delay_probability: 0.73, estimated_minutes: 25, confidence: "high" }

POST /api/predict/batch
→ Input: [{ airline, origin, destination, datetime }, ...]
→ Output: [{ delay_probability, estimated_minutes, confidence }, ...]

GET /api/model/info
→ Output: { accuracy, precision, recall, f1, trained_at, features, dataset_size }
```

### 3.3. Response Format (Chuẩn)
```json
{
  "success": true,
  "data": { "..." },
  "message": "Success",
  "timestamp": "2026-04-07T09:51:00Z"
}

// Khi lỗi:
{
  "success": false,
  "error": { "code": "INVALID_FILE", "message": "Chỉ hỗ trợ file CSV" },
  "timestamp": "2026-04-07T09:51:00Z"
}
```

---

## 4. Luồng Hoạt Động

### 4.1. Hành trình: Lần đầu dùng app
```
Mở app → Dashboard (empty state)
  → Thấy "Chưa có dữ liệu"
  → Bấm "Import Data"
  → Trang Data → Kéo thả CSV
  → Processing (progress bar)
  → "500,000 flights imported!"
  → Quay về Dashboard → Thấy biểu đồ ✨
```

### 4.2. Hành trình: Dự đoán delay
```
Mở app → Bấm Prediction (sidebar)
  → Chọn airline, origin, dest, datetime
  → Bấm "🔮 Predict"
  → Loading spinner (< 2s)
  → Gauge chart + kết quả
  → Tự lưu vào history
```

### 4.3. Hành trình: Phân tích data
```
Mở Dashboard → Xem tổng quan
  → Đổi filter (airline, date range)
  → Biểu đồ cập nhật
  → Hover để xem chi tiết
  → Rút kết luận
```

---

## 5. Checklist Kiểm Tra (Acceptance Criteria)

### Dashboard
- [ ] 4 KPI cards hiển thị đúng số liệu từ API
- [ ] 4 biểu đồ render data trong < 3 giây
- [ ] Filter thay đổi → biểu đồ cập nhật
- [ ] Hover tooltip hiển thị giá trị chính xác
- [ ] Empty state hiển thị đúng khi chưa có data
- [ ] Responsive trên viewport 1280px+

### Prediction
- [ ] Form validate đầy đủ (không cho submit thiếu field)
- [ ] Origin ≠ Destination
- [ ] Kết quả hiển thị trong < 2 giây
- [ ] Gauge chart animate smoothly
- [ ] History list cập nhật sau mỗi prediction
- [ ] Error handling khi server lỗi

### Data Management
- [ ] Drag & drop CSV upload
- [ ] Button upload alternative
- [ ] Progress bar khi processing
- [ ] Reject file không phải CSV
- [ ] Reject file rỗng
- [ ] Cảnh báo file > 500MB
- [ ] Bảng dữ liệu phân trang (20 rows/page)
- [ ] Search & filter hoạt động

---

## 6. Test Cases

### TC-01: Dashboard Happy Path
- **Given:** DB có 10,000 flights (30% delayed)
- **When:** Mở Dashboard
- **Then:** KPI Total = 10,000; Delay Rate = 30%; 4 charts render < 3s

### TC-02: Prediction Happy Path
- **Given:** User ở Prediction page, model trained
- **When:** Chọn VN, SGN→HAN, 08:00, bấm Predict
- **Then:** Kết quả trong < 2s; Gauge 0-100%; Có minutes + confidence

### TC-03: Upload CSV Success
- **Given:** File flights.csv (100K rows, valid format)
- **When:** Drag & drop vào upload zone
- **Then:** Progress bar → "100,000 flights imported" < 30s

### TC-04: Upload Wrong Format
- **Given:** File report.xlsx
- **When:** Upload
- **Then:** Error "Chỉ hỗ trợ file CSV"

### TC-05: Prediction Validation
- **Given:** User ở Prediction page
- **When:** Bấm Predict mà chưa chọn airline
- **Then:** Error "Vui lòng chọn hãng bay"

### TC-06: Dashboard Empty State
- **Given:** DB trống
- **When:** Mở Dashboard
- **Then:** "Chưa có dữ liệu" + nút Import

### TC-07: Dashboard Filter
- **Given:** DB có data nhiều hãng bay
- **When:** Filter airline = "VN"
- **Then:** KPI + charts chỉ hiện data Vietnam Airlines

---

## 7. Design System

### Colors (Dark Theme)
| Token | Value | Usage |
|-------|-------|-------|
| bg-primary | #0F172A | App background |
| bg-card | #1E293B | Card background |
| bg-sidebar | #0B1120 | Sidebar background |
| text-primary | #F8FAFC | Main text |
| text-secondary | #94A3B8 | Secondary text |
| accent-blue | #3B82F6 | Primary accent |
| accent-purple | #7C3AED | Secondary accent |
| success | #22C55E | On-time indicator |
| danger | #EF4444 | Delay indicator |
| warning | #F59E0B | Warning states |
| gradient-start | #1E3A5F | Gradient blue start |
| gradient-end | #4A90D9 | Gradient blue end |

### Typography
- Font: Inter (Google Fonts)
- H1: 28px / bold
- H2: 22px / semibold
- H3: 18px / semibold
- Body: 14px / regular
- Small: 12px / regular

### Spacing & Radius
- Card padding: 24px
- Card border-radius: 12px
- Button border-radius: 8px
- Sidebar width: 240px
- Gap between cards: 16px

---

*Tạo bởi AWF 2.1 - Design Phase*
