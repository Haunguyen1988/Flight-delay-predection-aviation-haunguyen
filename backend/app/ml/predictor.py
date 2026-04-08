"""
ML Predictor - Feature engineering, model training, and prediction.
Uses XGBoost + Random Forest ensemble for flight delay prediction.
"""
import os
import json
import logging
from datetime import datetime
from typing import Optional, Dict, List

import numpy as np
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score,
    f1_score, classification_report, confusion_matrix,
)
from sklearn.preprocessing import LabelEncoder
from xgboost import XGBClassifier

from app.services.data_generator import TRAINING_SAMPLE_DATASET_PATH

logger = logging.getLogger(__name__)

MODEL_DIR = os.path.join(os.path.dirname(__file__), "models")
os.makedirs(MODEL_DIR, exist_ok=True)

# Paths
XGBOOST_PATH = os.path.join(MODEL_DIR, "xgboost_model.joblib")
RF_PATH = os.path.join(MODEL_DIR, "random_forest_model.joblib")
ENCODERS_PATH = os.path.join(MODEL_DIR, "encoders.joblib")
METRICS_PATH = os.path.join(MODEL_DIR, "metrics.json")
FEATURE_COLS_PATH = os.path.join(MODEL_DIR, "feature_columns.json")


# ── Feature Engineering ─────────────────────────────────────


def engineer_features(df: pd.DataFrame) -> pd.DataFrame:
    """Create ML-ready features from raw flight data."""
    features = pd.DataFrame()

    # Time-based features
    if "scheduled_departure" in df.columns:
        dep = pd.to_datetime(df["scheduled_departure"], errors="coerce")
        features["hour"] = dep.dt.hour
        features["day_of_week"] = dep.dt.dayofweek
        features["month"] = dep.dt.month
        features["is_weekend"] = (dep.dt.dayofweek >= 5).astype(int)
        features["is_peak_hour"] = dep.dt.hour.isin([7, 8, 15, 16, 17, 18]).astype(int)
        features["quarter"] = dep.dt.quarter
    else:
        features["hour"] = 12
        features["day_of_week"] = df.get("day_of_week", 0)
        features["month"] = df.get("month", 1)
        features["is_weekend"] = (features["day_of_week"] >= 5).astype(int)
        features["is_peak_hour"] = features["hour"].isin([7, 8, 15, 16, 17, 18]).astype(int)
        features["quarter"] = ((features["month"] - 1) // 3) + 1

    # Season feature
    features["season"] = features["month"].map(
        lambda m: 0 if m in [3, 4, 5] else (1 if m in [6, 7, 8] else (2 if m in [9, 10, 11] else 3))
    )  # 0=Spring, 1=Summer, 2=Fall, 3=Winter

    # Distance
    features["distance"] = df.get("distance", 0).astype(float)
    features["distance_cat"] = pd.cut(
        features["distance"],
        bins=[0, 300, 800, 2000, float("inf")],
        labels=[0, 1, 2, 3],
    ).astype(float).fillna(1)

    # Airline encoding
    features["airline_code"] = df.get("airline_code", "XX")

    # Airport encoding
    features["origin_airport"] = df.get("origin_airport", "XXX")
    features["destination_airport"] = df.get("destination_airport", "XXX")

    # Weather encoding
    weather_map = {"Clear": 0, "Cloudy": 1, "Rain": 2, "Fog": 3, "Snow": 4}
    features["weather_code"] = df.get("weather_condition", "Clear").map(
        lambda x: weather_map.get(str(x), 1)
    )

    return features


# ── Model Training ──────────────────────────────────────────


def train_models(csv_path: str = None, df: pd.DataFrame = None) -> Dict:
    """Train XGBoost and Random Forest models."""
    logger.info("Starting model training...")
    start_time = datetime.now()

    # Load data
    if df is None:
        if csv_path is None:
            csv_path = TRAINING_SAMPLE_DATASET_PATH
        if not os.path.exists(csv_path):
            return {"success": False, "error": f"Dataset not found: {csv_path}"}
        df = pd.read_csv(csv_path)

    logger.info(f"Dataset: {len(df)} rows")

    # Target variable
    if "is_delayed" not in df.columns:
        return {"success": False, "error": "Column 'is_delayed' not found in dataset"}

    y = df["is_delayed"].astype(int)

    # Feature engineering
    features = engineer_features(df)

    # Encode categorical features
    encoders = {}
    categorical_cols = ["airline_code", "origin_airport", "destination_airport"]

    for col in categorical_cols:
        le = LabelEncoder()
        features[col] = le.fit_transform(features[col].astype(str))
        encoders[col] = le

    # Select numeric features only
    feature_columns = [
        "hour", "day_of_week", "month", "is_weekend", "is_peak_hour",
        "quarter", "season", "distance", "distance_cat",
        "airline_code", "origin_airport", "destination_airport",
        "weather_code",
    ]

    X = features[feature_columns].fillna(0)

    # Train/Test Split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    logger.info(f"Train: {len(X_train)}, Test: {len(X_test)}")

    # ── Train XGBoost ───────────────────────────────────────
    xgb_model = XGBClassifier(
        n_estimators=200,
        max_depth=6,
        learning_rate=0.1,
        subsample=0.8,
        colsample_bytree=0.8,
        random_state=42,
        eval_metric="logloss",
        use_label_encoder=False,
    )
    xgb_model.fit(X_train, y_train)
    xgb_pred = xgb_model.predict(X_test)
    xgb_prob = xgb_model.predict_proba(X_test)[:, 1]

    # ── Train Random Forest ─────────────────────────────────
    rf_model = RandomForestClassifier(
        n_estimators=200,
        max_depth=12,
        min_samples_split=5,
        min_samples_leaf=2,
        random_state=42,
        n_jobs=-1,
    )
    rf_model.fit(X_train, y_train)
    rf_pred = rf_model.predict(X_test)
    rf_prob = rf_model.predict_proba(X_test)[:, 1]

    # ── Ensemble (Average Probabilities) ────────────────────
    ensemble_prob = (xgb_prob + rf_prob) / 2
    ensemble_pred = (ensemble_prob >= 0.5).astype(int)

    # ── Evaluate ────────────────────────────────────────────
    metrics = {
        "xgboost": {
            "accuracy": round(accuracy_score(y_test, xgb_pred), 4),
            "precision": round(precision_score(y_test, xgb_pred, zero_division=0), 4),
            "recall": round(recall_score(y_test, xgb_pred, zero_division=0), 4),
            "f1_score": round(f1_score(y_test, xgb_pred, zero_division=0), 4),
        },
        "random_forest": {
            "accuracy": round(accuracy_score(y_test, rf_pred), 4),
            "precision": round(precision_score(y_test, rf_pred, zero_division=0), 4),
            "recall": round(recall_score(y_test, rf_pred, zero_division=0), 4),
            "f1_score": round(f1_score(y_test, rf_pred, zero_division=0), 4),
        },
        "ensemble": {
            "accuracy": round(accuracy_score(y_test, ensemble_pred), 4),
            "precision": round(precision_score(y_test, ensemble_pred, zero_division=0), 4),
            "recall": round(recall_score(y_test, ensemble_pred, zero_division=0), 4),
            "f1_score": round(f1_score(y_test, ensemble_pred, zero_division=0), 4),
        },
        "feature_importance": _get_feature_importance(xgb_model, feature_columns),
        "dataset_size": len(df),
        "train_size": len(X_train),
        "test_size": len(X_test),
        "trained_at": datetime.now().isoformat(),
    }

    # ── Save Models ─────────────────────────────────────────
    joblib.dump(xgb_model, XGBOOST_PATH)
    joblib.dump(rf_model, RF_PATH)
    joblib.dump(encoders, ENCODERS_PATH)

    with open(METRICS_PATH, "w") as f:
        json.dump(metrics, f, indent=2)

    with open(FEATURE_COLS_PATH, "w") as f:
        json.dump(feature_columns, f)

    duration = (datetime.now() - start_time).total_seconds()
    metrics["duration_seconds"] = round(duration, 2)
    metrics["success"] = True

    logger.info(
        f"Training complete in {duration:.1f}s. "
        f"Ensemble accuracy: {metrics['ensemble']['accuracy']}"
    )

    return metrics


def _get_feature_importance(model, feature_names: List[str]) -> List[Dict]:
    """Get feature importance from XGBoost model."""
    importances = model.feature_importances_
    pairs = sorted(zip(feature_names, importances), key=lambda x: x[1], reverse=True)
    return [
        {"feature": name, "importance": round(float(imp), 4)}
        for name, imp in pairs
    ]


# ── Prediction ──────────────────────────────────────────────


class FlightDelayPredictor:
    """Prediction service using trained models."""

    def __init__(self):
        self.xgb_model = None
        self.rf_model = None
        self.encoders = None
        self.feature_columns = None
        self.metrics = None
        self._loaded = False

    def load_models(self) -> bool:
        """Load trained models from disk."""
        try:
            if not os.path.exists(XGBOOST_PATH):
                logger.warning("Models not yet trained.")
                return False

            self.xgb_model = joblib.load(XGBOOST_PATH)
            self.rf_model = joblib.load(RF_PATH)
            self.encoders = joblib.load(ENCODERS_PATH)

            with open(FEATURE_COLS_PATH, "r") as f:
                self.feature_columns = json.load(f)

            with open(METRICS_PATH, "r") as f:
                self.metrics = json.load(f)

            self._loaded = True
            logger.info("Models loaded successfully")
            return True

        except Exception as e:
            logger.error(f"Failed to load models: {e}")
            return False

    @property
    def is_ready(self) -> bool:
        return self._loaded

    def predict(
        self,
        airline: str,
        origin: str,
        destination: str,
        departure_datetime: str,
        weather_condition: Optional[str] = None,
    ) -> Dict:
        """Predict flight delay probability."""
        if not self._loaded:
            if not self.load_models():
                return {
                    "delay_probability": 0.0,
                    "estimated_delay_minutes": 0,
                    "confidence": "N/A",
                    "error": "Model not trained yet. Run training first.",
                }

        # Build input dataframe
        input_data = pd.DataFrame([{
            "airline_code": airline,
            "origin_airport": origin,
            "destination_airport": destination,
            "scheduled_departure": departure_datetime,
            "distance": 0,  # Will be estimated
            "weather_condition": weather_condition or "Clear",
            "day_of_week": 0,  # Will be computed
            "month": 1,  # Will be computed
        }])

        # Engineer features
        features = engineer_features(input_data)

        # Encode categoricals
        for col, encoder in self.encoders.items():
            if col in features.columns:
                val = features[col].iloc[0]
                if val in encoder.classes_:
                    features[col] = encoder.transform(features[col].astype(str))
                else:
                    # Unknown category - use most frequent
                    features[col] = 0

        # Select feature columns
        X = features[self.feature_columns].fillna(0)

        # Predict with both models
        xgb_prob = self.xgb_model.predict_proba(X)[:, 1][0]
        rf_prob = self.rf_model.predict_proba(X)[:, 1][0]

        # Ensemble average
        delay_prob = float((xgb_prob + rf_prob) / 2)

        # Estimate delay duration (based on probability)
        if delay_prob < 0.2:
            est_delay = 0
        elif delay_prob < 0.4:
            est_delay = int(15 + (delay_prob - 0.2) * 100)
        elif delay_prob < 0.6:
            est_delay = int(35 + (delay_prob - 0.4) * 150)
        else:
            est_delay = int(65 + (delay_prob - 0.6) * 200)

        # Confidence level
        prob_diff = abs(xgb_prob - rf_prob)
        if prob_diff < 0.1:
            confidence = "High"
        elif prob_diff < 0.2:
            confidence = "Medium"
        else:
            confidence = "Low"

        return {
            "delay_probability": round(delay_prob, 4),
            "estimated_delay_minutes": est_delay,
            "confidence": confidence,
            "model_scores": {
                "xgboost": round(float(xgb_prob), 4),
                "random_forest": round(float(rf_prob), 4),
            },
        }

    def get_model_info(self) -> Dict:
        """Get model information and metrics."""
        if not self._loaded:
            self.load_models()

        if self.metrics:
            return {
                "status": "trained",
                **self.metrics,
            }

        return {
            "status": "not_trained",
            "accuracy": None,
            "precision": None,
            "recall": None,
            "f1_score": None,
            "trained_at": None,
            "dataset_size": None,
            "features": [],
        }


# Singleton instance
predictor = FlightDelayPredictor()
