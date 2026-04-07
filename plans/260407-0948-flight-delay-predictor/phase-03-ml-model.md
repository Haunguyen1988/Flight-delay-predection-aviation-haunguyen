# Phase 03: ML Model
Status: ⬜ Pending
Dependencies: Phase 02

## Objective
Xây dựng model Machine Learning để dự đoán delay chuyến bay. Tạo API prediction endpoint.

## Requirements
### Functional
- [ ] Train model dự đoán xác suất delay
- [ ] Train model dự đoán số phút delay (regression)
- [ ] API endpoint nhận input → trả prediction
- [ ] Hiển thị confidence score
- [ ] Lưu model đã train để reuse

### Non-Functional
- [ ] Accuracy > 75% (classification)
- [ ] Prediction time < 500ms
- [ ] Model size < 100MB

## Implementation Steps

### Data Preparation
1. [ ] Feature selection:
   - `airline` - Hãng bay
   - `origin` - Sân bay đi
   - `destination` - Sân bay đến
   - `scheduled_departure` - Giờ khởi hành dự kiến
   - `day_of_week` - Thứ trong tuần
   - `month` - Tháng
   - `distance` - Khoảng cách
   - `weather_condition` - Thời tiết (nếu có)
2. [ ] Train/Test split (80/20)
3. [ ] Handle class imbalance (SMOTE / class weights)
4. [ ] Feature encoding (LabelEncoder / OneHotEncoder)

### Model Training
5. [ ] Train Random Forest classifier
6. [ ] Train XGBoost classifier
7. [ ] Train XGBoost regressor (dự đoán phút delay)
8. [ ] Model comparison & evaluation:
   - Accuracy, Precision, Recall, F1-score
   - Confusion Matrix
   - ROC-AUC curve
9. [ ] Hyperparameter tuning (GridSearch / RandomSearch)
10. [ ] Select best model, save with joblib/pickle

### API Integration
11. [ ] Tạo prediction endpoint:
    - `POST /api/predict` - Nhận flight info → trả prediction
    - Input: airline, origin, dest, datetime, weather
    - Output: delay_probability, estimated_delay_minutes, confidence
12. [ ] Tạo model info endpoint:
    - `GET /api/model/info` - Accuracy, features, training date
13. [ ] Tạo batch prediction endpoint:
    - `POST /api/predict/batch` - Dự đoán nhiều chuyến cùng lúc

## Files to Create/Modify
- `backend/app/ml/train.py` - Training script
- `backend/app/ml/predictor.py` - Prediction service
- `backend/app/ml/features.py` - Feature engineering
- `backend/app/ml/evaluate.py` - Model evaluation
- `backend/app/routers/predict.py` - Prediction API routes
- `backend/app/ml/models/` - Saved model files

## Test Criteria
- [ ] Model accuracy > 75% trên test set
- [ ] API `/api/predict` trả kết quả trong < 500ms
- [ ] Prediction output có đủ: probability, minutes, confidence
- [ ] Batch prediction xử lý 100 flights trong < 5s
- [ ] Model persist & reload thành công

## Notes
- XGBoost thường cho kết quả tốt nhất cho dạng data này
- Cần tune threshold cho classification (không chỉ dùng 0.5)
- SMOTE giúp model học tốt hơn class "delayed" (minority class)
- Có thể thêm SHAP explanation ở Phase 2 (sau MVP)

---
Next Phase: [Phase 04 - Frontend Dashboard](./phase-04-frontend-dashboard.md)
