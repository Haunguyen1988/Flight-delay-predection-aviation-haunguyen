# Phase 04: Frontend Dashboard
Status: ⬜ Pending
Dependencies: Phase 02, Phase 03

## Objective
Xây dựng giao diện dashboard hiển thị data analytics và prediction interface.

## Requirements
### Functional
- [ ] Dashboard tổng quan: tổng chuyến bay, % delay, avg delay time
- [ ] Biểu đồ delay theo tuyến bay (Bar chart)
- [ ] Biểu đồ delay theo thời tiết (Pie/Donut chart)
- [ ] Biểu đồ delay theo giờ/ngày/mùa (Line/Area chart)
- [ ] Trang Prediction: form nhập thông tin → kết quả dự đoán
- [ ] Trang Data: xem & lọc dữ liệu chuyến bay
- [ ] Upload CSV file

### Non-Functional
- [ ] UI đẹp, modern, dark theme
- [ ] Responsive (desktop first)
- [ ] Loading states & error handling
- [ ] Smooth animations

## Implementation Steps

### Layout & Navigation
1. [ ] Tạo App Layout: Sidebar + Header + Main Content
2. [ ] Setup React Router:
   - `/` → Dashboard
   - `/predict` → Prediction
   - `/data` → Data Management
3. [ ] Tạo Sidebar navigation component
4. [ ] Tạo Header component (title, theme toggle)

### Dashboard Page
5. [ ] Tạo KPI Cards: Total flights, Delay %, Avg delay minutes, On-time %
6. [ ] Biểu đồ 1: Top 10 Routes by Delay Rate (Horizontal Bar)
7. [ ] Biểu đồ 2: Delay by Weather Condition (Donut Chart)
8. [ ] Biểu đồ 3: Delay vs Time of Day (Area Chart)
9. [ ] Biểu đồ 4: Delay Trend by Month (Line Chart)
10. [ ] Filter controls: date range, airline, airport
11. [ ] Auto-refresh data

### Prediction Page
12. [ ] Form: chọn airline, origin, destination, datetime
13. [ ] "Predict" button → call API
14. [ ] Result display:
    - Gauge chart: xác suất delay (0-100%)
    - Estimated delay minutes
    - Confidence level (Low/Medium/High)
15. [ ] History: danh sách predictions đã thực hiện

### Data Management Page
16. [ ] Data table: hiển thị flights (paginated)
17. [ ] Search & filter (airline, route, date range, delay status)
18. [ ] Upload CSV: drag & drop hoặc button
19. [ ] Upload progress bar
20. [ ] Data summary sau khi upload

### UI Components (Reusable)
21. [ ] Card component
22. [ ] Chart wrapper component
23. [ ] Loading spinner / skeleton
24. [ ] Error boundary component
25. [ ] File upload component

## Files to Create/Modify
- `src/pages/Dashboard.tsx` - Dashboard page
- `src/pages/Prediction.tsx` - Prediction page
- `src/pages/DataManagement.tsx` - Data page
- `src/components/layout/Sidebar.tsx` - Navigation
- `src/components/layout/Header.tsx` - App header
- `src/components/charts/DelayByRoute.tsx` - Route bar chart
- `src/components/charts/DelayByWeather.tsx` - Weather donut
- `src/components/charts/DelayByTime.tsx` - Time area chart
- `src/components/charts/DelayTrend.tsx` - Monthly trend
- `src/components/charts/PredictionGauge.tsx` - Gauge chart
- `src/components/ui/KPICard.tsx` - Stat cards
- `src/components/ui/DataTable.tsx` - Data table
- `src/components/ui/FileUpload.tsx` - CSV upload
- `src/services/api.ts` - API service
- `src/types/flight.ts` - TypeScript types

## Test Criteria
- [ ] Dashboard hiển thị đúng 4 KPI cards
- [ ] 4 biểu đồ render đúng data
- [ ] Prediction form submit → hiển thị kết quả
- [ ] Upload CSV → thấy data trong table
- [ ] Filter hoạt động đúng
- [ ] Responsive trên desktop (1280px+)
- [ ] Loading states hiển thị khi fetching

## Notes
- Dark theme mặc định (modern, dễ nhìn data)
- Dùng Recharts cho tất cả biểu đồ (nhất quán)
- Skeleton loading cho UX tốt hơn
- Color palette: blues + purples (aviation theme)

---
Next Phase: [Phase 05 - Integration](./phase-05-integration.md)
