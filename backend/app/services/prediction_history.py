"""
Helpers for persisting prediction results.

Phase 1 intentionally reuses the existing `predictions` table instead of
introducing a new storage model.
"""
import logging
import math
from datetime import datetime
from typing import Optional

from sqlalchemy import func, select

from app.models.flight import PredictionDB
from app.services.prediction_bands import get_risk_band, get_severity_band
from app.services.database import async_session


logger = logging.getLogger(__name__)


DEPARTURE_DATETIME_FORMATS = (
    "%Y-%m-%d %H:%M:%S",
    "%Y-%m-%dT%H:%M",
    "%Y-%m-%dT%H:%M:%S",
)


def parse_departure_datetime(value: Optional[str]) -> Optional[datetime]:
    """Parse supported departure datetime formats into a datetime object."""
    if not value:
        return None

    normalized = value.strip()
    for datetime_format in DEPARTURE_DATETIME_FORMATS:
        try:
            return datetime.strptime(normalized, datetime_format)
        except ValueError:
            continue

    try:
        return datetime.fromisoformat(normalized.replace("Z", "+00:00"))
    except ValueError:
        return None


def build_prediction_record(
    *,
    airline_code: str,
    origin: str,
    destination: str,
    departure_datetime: Optional[str],
    delay_probability: float,
    estimated_delay_min: int,
    confidence: str,
) -> PredictionDB:
    """Create a PredictionDB instance from request and prediction data."""
    return PredictionDB(
        airline_code=airline_code,
        origin=origin,
        destination=destination,
        departure_datetime=parse_departure_datetime(departure_datetime),
        delay_probability=delay_probability,
        estimated_delay_min=estimated_delay_min,
        confidence=confidence,
    )


def can_persist_prediction(result: dict) -> bool:
    """Return True only when the prediction payload looks successful."""
    required_fields = ("delay_probability", "estimated_delay_minutes", "confidence")
    return not result.get("error") and all(field in result for field in required_fields)


async def save_prediction_record(
    *,
    airline_code: str,
    origin: str,
    destination: str,
    departure_datetime: Optional[str],
    result: dict,
) -> Optional[PredictionDB]:
    """Persist a successful single prediction without crashing the request."""
    if not can_persist_prediction(result):
        return None

    record = build_prediction_record(
        airline_code=airline_code,
        origin=origin,
        destination=destination,
        departure_datetime=departure_datetime,
        delay_probability=float(result["delay_probability"]),
        estimated_delay_min=int(result["estimated_delay_minutes"]),
        confidence=str(result["confidence"]),
    )

    async with async_session() as session:
        try:
            session.add(record)
            await session.commit()
            await session.refresh(record)
            return record
        except Exception:
            await session.rollback()
            logger.exception("Failed to save prediction history record")
            return None


def serialize_prediction_record(record: PredictionDB) -> dict:
    """Convert ORM records into API-safe dictionaries."""
    return {
        "id": record.id,
        "created_at": record.created_at.isoformat() if record.created_at else None,
        "airline": record.airline_code,
        "origin": record.origin,
        "destination": record.destination,
        "departure_datetime": (
            record.departure_datetime.isoformat() if record.departure_datetime else None
        ),
        "delay_probability": record.delay_probability,
        "estimated_delay_minutes": record.estimated_delay_min,
        "risk_band": get_risk_band(record.delay_probability or 0),
        "severity_band": get_severity_band(record.estimated_delay_min or 0),
        "confidence": record.confidence,
    }


async def get_prediction_history(
    *,
    page: int = 1,
    limit: int = 10,
    airline: Optional[str] = None,
    origin: Optional[str] = None,
    destination: Optional[str] = None,
) -> dict:
    """Fetch paginated prediction history ordered by newest first."""
    safe_page = max(page, 1)
    safe_limit = min(max(limit, 1), 100)
    offset = (safe_page - 1) * safe_limit

    filters = []
    if airline:
        filters.append(PredictionDB.airline_code == airline.upper())
    if origin:
        filters.append(PredictionDB.origin == origin.upper())
    if destination:
        filters.append(PredictionDB.destination == destination.upper())

    async with async_session() as session:
        total = await session.scalar(
            select(func.count()).select_from(PredictionDB).where(*filters)
        )

        records = await session.scalars(
            select(PredictionDB)
            .where(*filters)
            .order_by(PredictionDB.created_at.desc(), PredictionDB.id.desc())
            .offset(offset)
            .limit(safe_limit)
        )

        items = [serialize_prediction_record(record) for record in records.all()]

    return {
        "items": items,
        "page": safe_page,
        "limit": safe_limit,
        "total": total or 0,
        "total_pages": math.ceil((total or 0) / safe_limit) if total else 0,
    }
