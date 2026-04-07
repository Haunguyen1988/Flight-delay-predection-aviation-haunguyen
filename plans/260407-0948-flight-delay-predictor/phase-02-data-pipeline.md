# Phase 02: Data Pipeline
Status: ⬜ Pending
Dependencies: Phase 01

## Objective
Import, xử lý và lưu trữ dataset chuyến bay. Tạo API endpoints để frontend truy vấn dữ liệu.

## Requirements
### Functional
- [ ] Import CSV/Excel dataset chuyến bay
- [ ] Xử lý dữ liệu: clean, transform, feature engineering
- [ ] Lưu vào database (SQLite)
- [ ] API endpoints để query dữ liệu
- [ ] Filter & pagination cho dữ liệu lớn

### Non-Functional
- [ ] Xử lý được dataset 1M+ rows
- [ ] Response time < 2s cho queries

## Implementation Steps
1. [ ] Download sample dataset (Kaggle Flight Delay 2024)
2. [ ] Tạo data processing script (pandas):
   - Clean missing values
   - Parse dates, times
   - Encode categorical variables
   - Feature engineering (day_of_week, hour, season, etc.)
3. [ ] Tạo SQLite database schema:
   - `flights` table: flight info + delay data
   - `airports` table: airport metadata
   - `airlines` table: airline metadata
   - `weather` table: weather conditions (nếu có)
4. [ ] Tạo data import script (CSV → SQLite)
5. [ ] Tạo API endpoints:
   - `GET /api/flights` - List flights (paginated)
   - `GET /api/flights/stats` - Thống kê tổng quan
   - `GET /api/flights/by-route` - Delay theo tuyến bay
   - `GET /api/flights/by-weather` - Delay theo thời tiết
   - `GET /api/flights/by-time` - Delay theo giờ/ngày/mùa
   - `POST /api/data/upload` - Upload CSV file
6. [ ] Tạo data validation (check format, required fields)

## Files to Create/Modify
- `backend/app/routers/flights.py` - Flight API routes
- `backend/app/routers/data.py` - Data upload routes
- `backend/app/models/flight.py` - Flight data model
- `backend/app/services/data_processor.py` - Data processing
- `backend/app/services/database.py` - Database operations
- `backend/data/sample_data.csv` - Sample dataset

## Test Criteria
- [ ] Upload CSV thành công, data lưu vào DB
- [ ] API `/api/flights` trả về data đúng format
- [ ] API `/api/flights/stats` trả về thống kê chính xác
- [ ] Filter by route, weather, time hoạt động đúng
- [ ] Dataset 100K+ rows import trong < 30s

## Notes
- Dùng pandas để xử lý data nặng
- SQLite cho dev, có thể chuyển PostgreSQL cho production
- Cần xử lý class imbalance (majority = on-time flights)

---
Next Phase: [Phase 03 - ML Model](./phase-03-ml-model.md)
