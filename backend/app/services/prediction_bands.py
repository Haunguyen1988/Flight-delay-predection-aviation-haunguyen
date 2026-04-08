"""Helpers for translating numeric prediction outputs into readable bands."""


def get_risk_band(delay_probability: float) -> str:
    """Map delay probability to a stable risk band."""
    if delay_probability < 0.2:
        return "Very Low"
    if delay_probability < 0.4:
        return "Low"
    if delay_probability < 0.6:
        return "Moderate"
    if delay_probability < 0.8:
        return "High"
    return "Very High"


def get_severity_band(estimated_delay_minutes: int) -> str:
    """Map estimated delay minutes to a readable severity band."""
    if estimated_delay_minutes <= 14:
        return "On Time / Minimal"
    if estimated_delay_minutes <= 29:
        return "Minor"
    if estimated_delay_minutes <= 59:
        return "Moderate"
    if estimated_delay_minutes <= 119:
        return "Major"
    return "Severe"


def enrich_prediction_bands(result: dict) -> dict:
    """Return a prediction payload with risk and severity bands attached."""
    enriched = dict(result)
    delay_probability = float(enriched.get("delay_probability", 0) or 0)
    estimated_delay_minutes = int(enriched.get("estimated_delay_minutes", 0) or 0)
    enriched["risk_band"] = get_risk_band(delay_probability)
    enriched["severity_band"] = get_severity_band(estimated_delay_minutes)
    return enriched
