"""
Prediction router - API endpoints for ML prediction and model management.
"""
import logging
from typing import List, Optional

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel

from app.ml.predictor import predictor, train_models
from app.schemas.predict import (
    BatchPredictionResponseSchema,
    ModelInfoResponseSchema,
    PredictionHistoryResponseSchema,
    PredictionResponseSchema,
)
from app.services.prediction_bands import enrich_prediction_bands
from app.services.prediction_explanations import attach_prediction_explanations
from app.services.prediction_history import get_prediction_history, save_prediction_record
from app.services.prediction_recommendations import attach_prediction_recommendations

logger = logging.getLogger(__name__)

router = APIRouter()


class PredictionRequest(BaseModel):
    airline: str
    origin: str
    destination: str
    departure_datetime: str
    weather_condition: Optional[str] = None


def build_enriched_prediction(request: PredictionRequest) -> dict:
    """Build a prediction payload with all derived fields attached."""
    result = predictor.predict(
        airline=request.airline,
        origin=request.origin,
        destination=request.destination,
        departure_datetime=request.departure_datetime,
        weather_condition=request.weather_condition,
    )
    result = enrich_prediction_bands(result)
    result = attach_prediction_recommendations(
        result=result,
        departure_datetime=request.departure_datetime,
        weather_condition=request.weather_condition,
    )
    return attach_prediction_explanations(
        result=result,
        departure_datetime=request.departure_datetime,
        weather_condition=request.weather_condition,
    )


@router.post("", response_model=PredictionResponseSchema)
async def predict_delay(request: PredictionRequest):
    """Predict flight delay probability."""
    try:
        result = build_enriched_prediction(request)

        await save_prediction_record(
            airline_code=request.airline,
            origin=request.origin,
            destination=request.destination,
            departure_datetime=request.departure_datetime,
            result=result,
        )

        return {
            "success": True,
            "data": result,
            "message": "Prediction complete",
        }
    except Exception as e:
        logger.error(f"Prediction failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/batch", response_model=BatchPredictionResponseSchema)
async def predict_batch(requests: List[PredictionRequest]):
    """Batch predict flight delays."""
    if len(requests) > 50:
        raise HTTPException(status_code=400, detail="Maximum 50 predictions per batch")

    try:
        results = []
        for req in requests:
            result = build_enriched_prediction(req)
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
    """Train ML models using the bundled training dataset."""
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


@router.get("/history", response_model=PredictionHistoryResponseSchema)
async def prediction_history(
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(10, ge=1, le=100, description="Items per page"),
    airline: Optional[str] = Query(None, description="Filter by airline code"),
    origin: Optional[str] = Query(None, description="Filter by origin airport"),
    destination: Optional[str] = Query(None, description="Filter by destination airport"),
):
    """Get recent prediction history."""
    try:
        data = await get_prediction_history(
            page=page,
            limit=limit,
            airline=airline,
            origin=origin,
            destination=destination,
        )
        return {
            "success": True,
            "data": data,
            "message": "OK",
        }
    except Exception as e:
        logger.error(f"Prediction history lookup failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/model/info", response_model=ModelInfoResponseSchema)
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
