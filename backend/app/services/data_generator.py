"""
Sample dataset generator for development and testing.
Generates realistic flight delay data.
"""
import csv
import os
import random
from datetime import datetime, timedelta


AIRLINES = [
    ("AA", "American Airlines"),
    ("DL", "Delta Air Lines"),
    ("UA", "United Airlines"),
    ("WN", "Southwest Airlines"),
    ("B6", "JetBlue Airways"),
    ("AS", "Alaska Airlines"),
    ("NK", "Spirit Airlines"),
    ("F9", "Frontier Airlines"),
    ("VN", "Vietnam Airlines"),
    ("VJ", "VietJet Air"),
]

AIRPORTS = [
    ("ATL", "Hartsfield-Jackson Atlanta", "Atlanta", "GA", 33.6407, -84.4277),
    ("DFW", "Dallas/Fort Worth International", "Dallas", "TX", 32.8998, -97.0403),
    ("DEN", "Denver International", "Denver", "CO", 39.8561, -104.6737),
    ("ORD", "O'Hare International", "Chicago", "IL", 41.9742, -87.9073),
    ("LAX", "Los Angeles International", "Los Angeles", "CA", 33.9425, -118.4081),
    ("JFK", "John F. Kennedy International", "New York", "NY", 40.6413, -73.7781),
    ("SFO", "San Francisco International", "San Francisco", "CA", 37.6213, -122.3790),
    ("SEA", "Seattle-Tacoma International", "Seattle", "WA", 47.4502, -122.3088),
    ("MIA", "Miami International", "Miami", "FL", 25.7959, -80.2870),
    ("BOS", "Boston Logan International", "Boston", "MA", 42.3656, -71.0096),
    ("SGN", "Tan Son Nhat International", "Ho Chi Minh", "VN", 10.8188, 106.6520),
    ("HAN", "Noi Bai International", "Hanoi", "VN", 21.2212, 105.8070),
    ("DAD", "Da Nang International", "Da Nang", "VN", 16.0439, 108.1994),
]

WEATHER_CONDITIONS = [
    "Clear", "Clear", "Clear", "Clear",  # 40% clear
    "Cloudy", "Cloudy",                   # 20% cloudy
    "Rain", "Rain",                       # 20% rain
    "Snow",                               # 10% snow
    "Fog",                                # 10% fog
]

DELAY_REASONS = [
    "Weather", "Weather",
    "Air Traffic Control",
    "Carrier Delay",
    "Late Aircraft",
    "Security",
    "National Aviation System",
]

# Delay probability by weather
WEATHER_DELAY_PROB = {
    "Clear": 0.12,
    "Cloudy": 0.20,
    "Rain": 0.40,
    "Snow": 0.55,
    "Fog": 0.45,
}

# Delay probability by hour (higher during peak hours)
HOUR_DELAY_FACTOR = {
    5: 0.8, 6: 0.9, 7: 1.0, 8: 1.1, 9: 1.0,
    10: 0.9, 11: 0.85, 12: 0.9, 13: 0.95, 14: 1.0,
    15: 1.1, 16: 1.2, 17: 1.3, 18: 1.25, 19: 1.15,
    20: 1.0, 21: 0.95, 22: 0.85, 23: 0.8,
}

SERVICE_DIR = os.path.dirname(__file__)
APP_DIR = os.path.abspath(os.path.join(SERVICE_DIR, ".."))
BACKEND_DIR = os.path.abspath(os.path.join(APP_DIR, ".."))

TRAINING_SAMPLE_DATASET_PATH = os.path.join(APP_DIR, "data", "sample_flights.csv")
QUICK_SAMPLE_DATASET_PATH = os.path.join(BACKEND_DIR, "data", "quick_sample_flights.csv")

DEFAULT_TRAINING_SAMPLE_SIZE = 50000
DEFAULT_QUICK_SAMPLE_SIZE = 10


def _generate_sample_data(num_flights: int, output_path: str) -> str:
    """Generate a sample flight delay dataset."""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # Date range: 12 months
    start_date = datetime(2025, 1, 1)
    end_date = datetime(2025, 12, 31)
    date_range = (end_date - start_date).days

    rows = []
    for i in range(num_flights):
        # Random date and time
        random_day = random.randint(0, date_range)
        random_hour = random.choices(
            list(HOUR_DELAY_FACTOR.keys()),
            weights=list(HOUR_DELAY_FACTOR.values()),
            k=1
        )[0]
        random_minute = random.randint(0, 59)
        scheduled_dep = start_date + timedelta(days=random_day, hours=random_hour, minutes=random_minute)

        # Random airline and route
        airline_code, airline_name = random.choice(AIRLINES)
        origin = random.choice(AIRPORTS)
        dest = random.choice([a for a in AIRPORTS if a[0] != origin[0]])

        # Flight number
        flight_number = f"{airline_code}{random.randint(100, 9999)}"

        # Distance (approximate based on coords)
        dist = ((origin[4] - dest[4]) ** 2 + (origin[5] - dest[5]) ** 2) ** 0.5 * 69
        distance = round(dist, 1)

        # Weather
        weather = random.choice(WEATHER_CONDITIONS)

        # Month-based seasonality (winter has more delays)
        month = scheduled_dep.month
        month_factor = 1.0
        if month in [12, 1, 2]:  # Winter
            month_factor = 1.3
        elif month in [6, 7, 8]:  # Summer storms
            month_factor = 1.15

        # Calculate delay probability
        base_prob = WEATHER_DELAY_PROB.get(weather, 0.15)
        hour_factor = HOUR_DELAY_FACTOR.get(random_hour, 1.0)
        delay_prob = min(base_prob * hour_factor * month_factor, 0.85)

        # Determine delay
        is_delayed = random.random() < delay_prob
        if is_delayed:
            # Delay duration: exponential-ish distribution
            delay_minutes = int(random.expovariate(1 / 35)) + 15  # Min 15 min
            delay_minutes = min(delay_minutes, 300)  # Max 300 min
            delay_reason = random.choice(DELAY_REASONS)
        else:
            delay_minutes = max(0, int(random.gauss(0, 5)))  # Small variance
            delay_reason = ""

        # Actual departure
        actual_dep = scheduled_dep + timedelta(minutes=delay_minutes)

        # Flight duration (based on distance)
        flight_duration_min = max(60, int(distance / 8) + random.randint(-10, 10))
        scheduled_arr = scheduled_dep + timedelta(minutes=flight_duration_min)
        actual_arr = actual_dep + timedelta(minutes=flight_duration_min + random.randint(-5, 5))

        day_of_week = scheduled_dep.weekday()

        rows.append({
            "flight_number": flight_number,
            "airline_code": airline_code,
            "origin_airport": origin[0],
            "destination_airport": dest[0],
            "scheduled_departure": scheduled_dep.strftime("%Y-%m-%d %H:%M:%S"),
            "actual_departure": actual_dep.strftime("%Y-%m-%d %H:%M:%S"),
            "scheduled_arrival": scheduled_arr.strftime("%Y-%m-%d %H:%M:%S"),
            "actual_arrival": actual_arr.strftime("%Y-%m-%d %H:%M:%S"),
            "delay_minutes": delay_minutes,
            "delay_reason": delay_reason,
            "distance": distance,
            "weather_condition": weather,
            "day_of_week": day_of_week,
            "month": month,
            "is_delayed": 1 if delay_minutes >= 15 else 0,
        })

    # Write CSV
    fieldnames = list(rows[0].keys())
    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"[OK] Generated {num_flights} flights -> {output_path}")
    return output_path


def generate_quick_sample_data(
    num_flights: int = DEFAULT_QUICK_SAMPLE_SIZE,
    output_path: str | None = None,
) -> str:
    """Generate a small demo dataset for quick seeding into the app."""
    return _generate_sample_data(
        num_flights=num_flights,
        output_path=output_path or QUICK_SAMPLE_DATASET_PATH,
    )


def generate_training_sample_data(
    num_flights: int = DEFAULT_TRAINING_SAMPLE_SIZE,
    output_path: str | None = None,
) -> str:
    """Generate the larger dataset used for model training."""
    return _generate_sample_data(
        num_flights=num_flights,
        output_path=output_path or TRAINING_SAMPLE_DATASET_PATH,
    )


if __name__ == "__main__":
    generate_training_sample_data()
