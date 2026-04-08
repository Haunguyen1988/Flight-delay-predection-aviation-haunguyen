"""Rule-based operational recommendations for prediction results."""
from typing import List, Optional

from app.services.prediction_history import parse_departure_datetime


PEAK_HOURS = {7, 8, 15, 16, 17, 18}
ADVERSE_WEATHER = {"RAIN", "FOG", "SNOW"}


def generate_prediction_recommendations(
    *,
    departure_datetime: Optional[str],
    weather_condition: Optional[str],
    confidence: str,
    risk_band: str,
    severity_band: str,
    prediction_error: Optional[str] = None,
) -> List[str]:
    """Generate a small set of actionable recommendations."""
    recommendations: List[str] = []
    normalized_weather = (weather_condition or "Clear").upper()
    parsed_departure = parse_departure_datetime(departure_datetime)

    if prediction_error:
        recommendations.append(
            "Train or reload model artifacts before relying on this prediction"
        )

    if normalized_weather in ADVERSE_WEATHER:
        recommendations.append("Monitor weather-related disruption risk closely")

    if parsed_departure and parsed_departure.hour in PEAK_HOURS:
        recommendations.append("Consider additional departure buffer during peak hour")

    if confidence == "Low":
        recommendations.append("Use caution because model confidence is low")

    if risk_band in {"High", "Very High"} or severity_band in {"Major", "Severe"}:
        recommendations.append("Review downstream rotation impact if delay occurs")

    if not recommendations:
        recommendations.append(
            "Current conditions look manageable; continue standard pre-departure monitoring"
        )

    deduplicated: List[str] = []
    for item in recommendations:
        if item not in deduplicated:
            deduplicated.append(item)

    return deduplicated[:4]


def attach_prediction_recommendations(
    *,
    result: dict,
    departure_datetime: Optional[str],
    weather_condition: Optional[str],
) -> dict:
    """Return the prediction payload with recommendations attached."""
    enriched = dict(result)
    enriched["recommendations"] = generate_prediction_recommendations(
        departure_datetime=departure_datetime,
        weather_condition=weather_condition,
        confidence=str(enriched.get("confidence", "Low")),
        risk_band=str(enriched.get("risk_band", "Moderate")),
        severity_band=str(enriched.get("severity_band", "Moderate")),
        prediction_error=enriched.get("error"),
    )
    return enriched
