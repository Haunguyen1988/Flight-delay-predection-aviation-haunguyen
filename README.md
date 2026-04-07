# ✈️ Flight Delay Predictor

AI-powered flight delay prediction and analytics platform built with FastAPI + React + XGBoost/Random Forest.

![Dashboard](docs/screenshots/dashboard.png)

## Features

- **📊 Dashboard** - Real-time analytics with interactive charts
  - Total flights, delay rate, average delay, on-time rate KPIs
  - Top routes by delay rate (horizontal bar chart)
  - Weather impact analysis (pie chart)
  - Monthly delay trend (area chart)
  - Hourly delay pattern (bar chart)

- **🔮 ML Prediction** - Predict delay probability for any flight
  - XGBoost + Random Forest ensemble model
  - 72.7% accuracy on 50K flight dataset
  - Inputs: Airline, Origin, Destination, Date/Time, Weather
  - Output: Delay probability, estimated delay, confidence level

- **📁 Data Management** - Import and manage datasets
  - CSV upload with drag & drop
  - Sample data generator (50K realistic flights)
  - One-click model training
  - Paginated flight data table

## Tech Stack

| Component | Technology |
|-----------|-----------|
| Backend | Python, FastAPI, SQLAlchemy (async) |
| Frontend | React 19, TypeScript, Vite |
| Database | SQLite (aiosqlite) |
| ML Models | XGBoost, Random Forest (scikit-learn) |
| Charts | Recharts |
| Styling | Custom CSS (Dark Theme) |

## Quick Start

### Prerequisites
- Python 3.10+
- Node.js 18+

### Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
.\venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt

# Copy environment config
copy .env.example .env

# Start server
uvicorn app.main:app --reload --port 8000
```

### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Copy environment config
copy .env.example .env

# Start dev server
npm run dev
```

### Quick Data Setup

1. Open http://localhost:5173/data
2. Click **"Generate"** to create 50K sample flights
3. Click **"Train"** to train the ML model
4. Go to **Dashboard** to see analytics
5. Go to **Prediction** to predict delays

Or via API:
```bash
# Generate sample data + import to DB
curl -X POST http://localhost:8000/api/data/generate-sample

# Train ML models
curl -X POST http://localhost:8000/api/predict/train

# Make a prediction
curl -X POST http://localhost:8000/api/predict \
  -H "Content-Type: application/json" \
  -d '{"airline":"AA","origin":"JFK","destination":"LAX","departure_datetime":"2025-12-20 17:30:00","weather_condition":"Snow"}'
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/health` | Health check |
| GET | `/api/flights` | List flights (paginated) |
| GET | `/api/flights/stats` | Dashboard statistics |
| GET | `/api/flights/by-route` | Delay by route |
| GET | `/api/flights/by-weather` | Delay by weather |
| GET | `/api/flights/by-time` | Delay by time period |
| GET | `/api/flights/airlines` | List airlines |
| GET | `/api/flights/airports` | List airports |
| POST | `/api/data/upload` | Upload CSV dataset |
| POST | `/api/data/generate-sample` | Generate sample data |
| POST | `/api/predict` | Predict flight delay |
| POST | `/api/predict/batch` | Batch predictions |
| POST | `/api/predict/train` | Train ML models |
| GET | `/api/predict/model/info` | Model performance info |

## Project Structure

```
flight-delay-predictor/
├── backend/
│   ├── app/
│   │   ├── main.py                 # FastAPI app
│   │   ├── routers/
│   │   │   ├── flights.py          # Flight analytics API
│   │   │   ├── data.py             # Data upload API
│   │   │   └── predict.py          # ML prediction API
│   │   ├── models/
│   │   │   └── flight.py           # SQLAlchemy models
│   │   ├── services/
│   │   │   ├── database.py         # DB connection
│   │   │   ├── data_processor.py   # CSV import + queries
│   │   │   └── data_generator.py   # Sample data generator
│   │   └── ml/
│   │       ├── predictor.py        # ML training + prediction
│   │       └── models/             # Saved model files
│   ├── data/                       # CSV datasets
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── App.tsx                 # Router + Layout
│   │   ├── index.css               # Design system
│   │   ├── components/layout/
│   │   ├── pages/
│   │   │   ├── Dashboard.tsx       # Analytics dashboard
│   │   │   ├── Prediction.tsx      # ML prediction UI
│   │   │   └── DataManagement.tsx  # Data import + table
│   │   ├── hooks/useApi.ts         # API hooks
│   │   ├── services/api.ts         # Axios config
│   │   └── types/flight.ts         # TypeScript types
│   └── package.json
└── README.md
```

## ML Model Details

### Feature Engineering
- **Time features**: hour, day_of_week, month, is_weekend, is_peak_hour, quarter, season
- **Weather**: encoded as numeric (Clear=0, Cloudy=1, Rain=2, Fog=3, Snow=4)
- **Route**: carrier + origin/destination (label encoded)
- **Distance**: raw + categorical buckets

### Model Performance (Ensemble)
| Metric | Score |
|--------|-------|
| Accuracy | 72.7% |
| Precision | 58.1% |
| Recall | 38.4% |
| F1 Score | 46.3% |

### Top Feature Importance
1. Weather condition (48.6%)
2. Peak hour indicator (6.0%)
3. Season (5.9%)
4. Hour of day (4.4%)
5. Month (4.0%)

## License

MIT
