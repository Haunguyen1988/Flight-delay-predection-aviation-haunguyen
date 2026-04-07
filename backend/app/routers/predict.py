"""
Prediction router - API endpoints for ML prediction and model management.
"""
import logging
from typing import List, Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.ml.predictor import predictor, train_models

logger = logging.getLogger(__name__)

router = APIRouter()


class PredictionRequest(BaseModel):
    airline: str
    origin: str
    destination: str
    departure_datetime: str
    weather_condition: Optional[str] = None


@router.post("", response_model=dict)
async def predict_delay(request: PredictionRequest):
    """Predict flight delay probability."""
    try:
        result = predictor.predict(
            airline=request.airline,
            origin=request.origin,
            destination=request.destination,
            departure_datetime=request.departure_datetime,
            weather_condition=request.weather_condition,
        )

        return {
            "success": True,
            "data": result,
            "message": "Prediction complete",
        }
    except Exception as e:
        logger.error(f"Prediction failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/batch", response_model=dict)
async def predict_batch(requests: List[PredictionRequest]):
    """Batch predict flight delays."""
    if len(requests) > 50:
        raise HTTPException(status_code=400, detail="Maximum 50 predictions per batch")

    try:
        results = []
        for req in requests:
            result = predictor.predict(
                airline=req.airline,
                origin=req.origin,
                destination=req.destination,
                departure_datetime=req.departure_datetime,
                weather_condition=req.weather_condition,
            )
            results.append({
                "input": req.model_dump(),
                "prediction": result,
            })

        return {
            "success": True,
            "data": results,
            "message": f"Predicted {len(results)} flights",
        }
    except Exception as e:
        logger.error(f"Batch prediction failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/train", response_model=dict)
async def train_model():
    """Train ML models using the sample dataset."""
    try:
        metrics = train_models()

        if not metrics.get("success"):
            raise HTTPException(
                status_code=500,
                detail=metrics.get("error", "Training failed"),
            )

        # Reload models
        predictor.load_models()

        return {
            "success": True,
            "data": metrics,
            "message": "Model training complete",
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Training failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/model/info", response_model=dict)
async def get_model_info():
    """Get ML model information and performance metrics."""
    try:
        info = predictor.get_model_info()
        return {
            "success": True,
            "data": info,
            "message": "OK",
        }
    except Exception as e:
        return {
            "success": False,
            "data": {"status": "error"},
            "message": str(e),
        }
