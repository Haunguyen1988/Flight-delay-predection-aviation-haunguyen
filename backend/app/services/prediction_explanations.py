"""Lightweight rule-based explanations for prediction results."""
from typing import List, Optional

from app.services.prediction_history import parse_departure_datetime


def generate_prediction_explanations(
    *,
    departure_datetime: Optional[str],
    weather_condition: Optional[str],
    confidence: str,
) -> List[dict]:
    """Generate a small set of plain-language explanation drivers."""
    explanations: List[dict] = []
    parsed_departure = parse_departure_datetime(departure_datetime)
    normalized_weather = (weather_condition or "Clear").upper()

    if normalized_weather in {"SNOW", "FOG"}:
        explanations.append({
            "factor": "Weather",
            "impact": "high",
            "message": "Snow or fog conditions can quickly reduce airport and en-route reliability",
        })
    elif normalized_weather == "RAIN":
        explanations.append({
            "factor": "Weather",
            "impact": "medium",
            "message": "Rain can slow airport surface operations and increase spacing requirements",
        })
    else:
        explanations.append({
            "factor": "Weather",
            "impact": "low",
            "message": "Benign weather keeps disruption pressure lower than adverse conditions",
        })

    if parsed_departure and parsed_departure.hour in {7, 8, 15, 16, 17, 18}:
        explanations.append({
            "factor": "Departure Timing",
            "impact": "medium",
            "message": "This departure sits in a peak traffic bank when congestion risk usually increases",
        })
    else:
        explanations.append({
            "factor": "Departure Timing",
            "impact": "low",
            "message": "This departure time sits outside the busiest peak-hour windows",
        })

    if parsed_departure and parsed_departure.month in {12, 1, 2}:
        explanations.append({
            "factor": "Season",
            "impact": "medium",
            "message": "Winter schedules often face more operational variability and weather sensitivity",
        })
    elif parsed_departure and parsed_departure.month in {6, 7, 8}:
        explanations.append({
            "factor": "Season",
            "impact": "medium",
            "message": "Summer demand and convective weather can increase delay pressure",
        })
    else:
        explanations.append({
            "factor": "Season",
            "impact": "low",
            "message": "The selected month is outside the most disruption-prone seasonal peaks",
        })

    if confidence == "Low":
        explanations.append({
            "factor": "Model Agreement",
            "impact": "medium",
            "message": "The underlying models disagree more than usual, so this prediction should be treated cautiously",
        })
    else:
        explanations.append({
            "factor": "Model Agreement",
            "impact": "low",
            "message": "The underlying models are reasonably aligned on this prediction",
        })

    return explanations[:4]


def attach_prediction_explanations(
    *,
    result: dict,
    departure_datetime: Optional[str],
    weather_condition: Optional[str],
) -> dict:
    """Return the prediction payload with explanation items attached."""
    enriched = dict(result)
    enriched["explanations"] = generate_prediction_explanations(
        departure_datetime=departure_datetime,
        weather_condition=weather_condition,
        confidence=str(enriched.get("confidence", "Low")),
    )
    return enriched
