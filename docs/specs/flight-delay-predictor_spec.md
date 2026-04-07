# 📋 SPECS: Flight Delay Predictor

**Created:** 2026-04-07
**Version:** 1.0 (MVP)

---

## 1. Executive Summary
Web App phân tích và dự đoán delay chuyến bay sử dụng Machine Learning.
Kết hợp dashboard analytics trực quan với ML prediction engine.
Target: Nhân viên hãng bay, nhà phân tích dữ liệu, researcher.

## 2. User Stories

### Nhân viên hãng bay
- Tôi muốn xem tổng quan delay để biết tình hình hiện tại
- Tôi muốn dự đoán chuyến bay nào sẽ delay để chuẩn bị trước
- Tôi muốn xem delay theo tuyến bay để biết tuyến nào có vấn đề

### Nhà phân tích dữ liệu
- Tôi muốn import dataset để phân tích
- Tôi muốn xem biểu đồ phân tích theo nhiều chiều (thời tiết, giờ, mùa)
- Tôi muốn lọc và tìm kiếm dữ liệu chi tiết

### Researcher
- Tôi muốn xem model accuracy và performance metrics
- Tôi muốn thử prediction với nhiều scenarios khác nhau

## 3. Database Design

### Tables:
```
flights:
  - id (PK)
  - flight_number
  - airline_code
  - origin_airport
  - destination_airport
  - scheduled_departure
  - actual_departure
  - scheduled_arrival
  - actual_arrival
  - delay_minutes
  - delay_reason
  - distance
  - weather_condition
  - day_of_week
  - month
  - is_delayed (boolean)

airports:
  - code (PK)
  - name
  - city
  - state
  - latitude
  - longitude

airlines:
  - code (PK)
  - name
```

### Relationships:
- flights.airline_code → airlines.code
- flights.origin_airport → airports.code
- flights.destination_airport → airports.code

## 4. API Contract

### Data Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /api/flights | List flights (paginated) |
| GET | /api/flights/stats | Dashboard statistics |
| GET | /api/flights/by-route | Delay stats by route |
| GET | /api/flights/by-weather | Delay stats by weather |
| GET | /api/flights/by-time | Delay stats by time |
| POST | /api/data/upload | Upload CSV dataset |

### Prediction Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /api/predict | Single flight prediction |
| POST | /api/predict/batch | Batch prediction |
| GET | /api/model/info | Model performance info |

### Response Format
```json
{
  "success": true,
  "data": { ... },
  "message": "Success",
  "timestamp": "2026-04-07T09:48:00Z"
}
```

## 5. UI Components

### Pages
1. **Dashboard** - KPI cards + 4 biểu đồ + filters
2. **Prediction** - Input form + result gauge + history
3. **Data Management** - Data table + upload + filters

### Design System
- **Theme:** Dark mode (primary)
- **Colors:** Blues (#1E3A5F → #4A90D9) + Purple accents (#7C3AED)
- **Font:** Inter (Google Fonts)
- **Charts:** Recharts (consistent style)
- **Border Radius:** 12px (cards), 8px (buttons)

## 6. Tech Stack
| Layer | Technology | Version |
|-------|-----------|---------|
| Frontend Framework | React | 18+ |
| Build Tool | Vite | 5+ |
| Charts | Recharts | 2+ |
| HTTP Client | Axios | 1+ |
| Backend Framework | FastAPI | 0.100+ |
| ML Library | scikit-learn | 1.3+ |
| ML Model | XGBoost | 2+ |
| Data Processing | pandas | 2+ |
| Database | SQLite | 3 |

## 7. Build Checklist (MVP)
- [ ] Phase 01: Setup Environment
- [ ] Phase 02: Data Pipeline
- [ ] Phase 03: ML Model
- [ ] Phase 04: Frontend Dashboard
- [ ] Phase 05: Integration
- [ ] Phase 06: Testing & Polish
