# Phase 05: Integration
Status: ⬜ Pending
Dependencies: Phase 03, Phase 04

## Objective
Kết nối Frontend ↔ Backend ↔ ML Model. Đảm bảo toàn bộ flow hoạt động end-to-end.

## Requirements
### Functional
- [ ] Dashboard load data từ backend API
- [ ] Prediction form gửi request → nhận kết quả từ ML model
- [ ] Upload CSV → backend xử lý → frontend hiển thị
- [ ] Error handling toàn bộ flow

### Non-Functional
- [ ] API response < 2s
- [ ] Proper error messages cho user
- [ ] CORS configured đúng

## Implementation Steps
1. [ ] Config CORS trên FastAPI cho frontend origin
2. [ ] Tạo API service layer (axios instance + interceptors)
3. [ ] Kết nối Dashboard:
   - Fetch stats từ `/api/flights/stats`
   - Fetch chart data từ `/api/flights/by-route`, `/by-weather`, `/by-time`
4. [ ] Kết nối Prediction:
   - POST form data đến `/api/predict`
   - Hiển thị kết quả prediction
5. [ ] Kết nối Data Management:
   - Fetch flights list từ `/api/flights`
   - Upload CSV qua `/api/data/upload`
6. [ ] Error handling:
   - Network errors → hiển thị "Không kết nối được server"
   - API errors → hiển thị message từ backend
   - Timeout → hiển thị "Quá thời gian, thử lại"
7. [ ] Loading states cho tất cả API calls
8. [ ] Test end-to-end flow:
   - Upload data → Xem dashboard → Predict delay

## Files to Create/Modify
- `src/services/api.ts` - API configuration & service
- `src/hooks/useFlightStats.ts` - Custom hook for stats
- `src/hooks/usePrediction.ts` - Custom hook for prediction
- `backend/app/main.py` - CORS middleware update
- Environment configs (`.env`)

## Test Criteria
- [ ] Dashboard hiển thị live data từ backend
- [ ] Prediction trả kết quả chính xác
- [ ] Upload file xử lý thành công
- [ ] Error messages hiển thị đúng
- [ ] Không có CORS errors

## Notes
- Dùng axios interceptors cho global error handling
- Environment variables cho API base URL
- Consider adding request caching cho dashboard data

---
Next Phase: [Phase 06 - Testing & Polish](./phase-06-testing.md)
