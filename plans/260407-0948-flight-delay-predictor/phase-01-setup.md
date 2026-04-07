# Phase 01: Setup Environment
Status: ⬜ Pending
Dependencies: None

## Objective
Khởi tạo project với đầy đủ cấu trúc, dependencies, và môi trường phát triển.

## Requirements
### Functional
- [ ] Project React + Vite chạy được (`npm run dev`)
- [ ] Project Python FastAPI chạy được (`uvicorn`)
- [ ] Folder structure chuẩn cho cả frontend và backend

### Non-Functional
- [ ] TypeScript cho frontend
- [ ] Python virtual environment cho backend
- [ ] ESLint + Prettier configured

## Implementation Steps

### Frontend (React + Vite)
1. [ ] Tạo project Vite + React + TypeScript
2. [ ] Install core dependencies: react-router-dom, recharts, axios
3. [ ] Setup ESLint + Prettier
4. [ ] Tạo folder structure:
   ```
   src/
   ├── components/     # UI components
   ├── pages/          # Route pages
   ├── services/       # API calls
   ├── hooks/          # Custom hooks
   ├── utils/          # Utilities
   ├── types/          # TypeScript types
   └── assets/         # Images, icons
   ```
5. [ ] Tạo layout cơ bản (Sidebar + Main content)
6. [ ] Setup routing (Dashboard, Prediction, Data)

### Backend (Python FastAPI)
7. [ ] Tạo Python virtual environment
8. [ ] Install dependencies: fastapi, uvicorn, pandas, scikit-learn, xgboost
9. [ ] Tạo folder structure:
   ```
   backend/
   ├── app/
   │   ├── main.py          # FastAPI app
   │   ├── routers/         # API routes
   │   ├── models/          # Data models
   │   ├── services/        # Business logic
   │   ├── ml/              # ML models
   │   └── utils/           # Utilities
   ├── data/                # Dataset storage
   ├── requirements.txt
   └── .env.example
   ```
10. [ ] Tạo FastAPI app cơ bản với health check endpoint
11. [ ] Setup CORS cho frontend

### General
12. [ ] Tạo .env.example
13. [ ] Tạo .gitignore
14. [ ] Git init + initial commit

## Files to Create/Modify
- `frontend/` - React Vite project
- `backend/` - Python FastAPI project
- `.gitignore` - Git ignore rules
- `.env.example` - Environment variables template

## Test Criteria
- [ ] `npm run dev` chạy thành công (frontend)
- [ ] `uvicorn app.main:app --reload` chạy thành công (backend)
- [ ] Truy cập http://localhost:5173 thấy layout cơ bản
- [ ] Truy cập http://localhost:8000/docs thấy Swagger UI

## Notes
- Phase này là nơi DUY NHẤT chạy npm install / pip install
- Các phase sau chỉ install thêm nếu cần package mới

---
Next Phase: [Phase 02 - Data Pipeline](./phase-02-data-pipeline.md)
