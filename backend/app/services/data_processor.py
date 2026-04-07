"""
Data processor service - handles CSV import, validation, and database operations.
"""
import io
import csv
import logging
from datetime import datetime
from typing import Optional

import pandas as pd
from sqlalchemy import text, func, case, select, desc
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.flight import FlightDB, AirlineDB, AirportDB, Base
from app.services.database import engine, async_session

logger = logging.getLogger(__name__)


# ── Known airlines and airports for auto-population ────────
KNOWN_AIRLINES = {
    "AA": "American Airlines", "DL": "Delta Air Lines",
    "UA": "United Airlines", "WN": "Southwest Airlines",
    "B6": "JetBlue Airways", "AS": "Alaska Airlines",
    "NK": "Spirit Airlines", "F9": "Frontier Airlines",
    "VN": "Vietnam Airlines", "VJ": "VietJet Air",
    "QH": "Bamboo Airways",
}

KNOWN_AIRPORTS = {
    "ATL": ("Hartsfield-Jackson Atlanta", "Atlanta", "GA", 33.64, -84.43),
    "DFW": ("Dallas/Fort Worth Intl", "Dallas", "TX", 32.90, -97.04),
    "DEN": ("Denver International", "Denver", "CO", 39.86, -104.67),
    "ORD": ("O'Hare International", "Chicago", "IL", 41.97, -87.91),
    "LAX": ("Los Angeles Intl", "Los Angeles", "CA", 33.94, -118.41),
    "JFK": ("JFK International", "New York", "NY", 40.64, -73.78),
    "SFO": ("San Francisco Intl", "San Francisco", "CA", 37.62, -122.38),
    "SEA": ("Seattle-Tacoma Intl", "Seattle", "WA", 47.45, -122.31),
    "MIA": ("Miami International", "Miami", "FL", 25.80, -80.29),
    "BOS": ("Boston Logan Intl", "Boston", "MA", 42.37, -71.01),
    "SGN": ("Tan Son Nhat Intl", "Ho Chi Minh", "VN", 10.82, 106.65),
    "HAN": ("Noi Bai International", "Hanoi", "VN", 21.22, 105.81),
    "DAD": ("Da Nang International", "Da Nang", "VN", 16.04, 108.20),
}

REQUIRED_COLUMNS = [
    "flight_number", "airline_code", "origin_airport", "destination_airport",
    "scheduled_departure", "delay_minutes", "is_delayed",
]


async def validate_csv(content: bytes) -> dict:
    """Validate CSV file content and return info."""
    try:
        text_content = content.decode("utf-8")
    except UnicodeDecodeError:
        try:
            text_content = content.decode("latin-1")
        except Exception:
            return {"valid": False, "error": "Cannot decode file. Use UTF-8 encoding."}

    reader = csv.reader(io.StringIO(text_content))
    try:
        headers = next(reader)
    except StopIteration:
        return {"valid": False, "error": "File is empty."}

    headers = [h.strip().lower() for h in headers]

    missing = [col for col in REQUIRED_COLUMNS if col not in headers]
    if missing:
        return {
            "valid": False,
            "error": f"Missing required columns: {', '.join(missing)}",
            "found_columns": headers,
            "required_columns": REQUIRED_COLUMNS,
        }

    row_count = sum(1 for _ in reader)

    return {
        "valid": True,
        "columns": headers,
        "row_count": row_count,
    }


async def import_csv_to_db(content: bytes) -> dict:
    """Import CSV data into the database."""
    start_time = datetime.now()

    try:
        text_content = content.decode("utf-8")
    except UnicodeDecodeError:
        text_content = content.decode("latin-1")

    df = pd.read_csv(io.StringIO(text_content))
    df.columns = [c.strip().lower() for c in df.columns]

    total_rows = len(df)
    if total_rows == 0:
        return {"success": False, "error": "File has no data rows."}

    async with async_session() as session:
        # Populate airlines table
        airline_codes = df["airline_code"].unique()
        for code in airline_codes:
            code = str(code).strip()
            existing = await session.execute(
                select(AirlineDB).where(AirlineDB.code == code)
            )
            if not existing.scalar_one_or_none():
                name = KNOWN_AIRLINES.get(code, f"Airline {code}")
                session.add(AirlineDB(code=code, name=name))

        # Populate airports table
        airport_codes = set(
            df["origin_airport"].unique().tolist() +
            df["destination_airport"].unique().tolist()
        )
        for code in airport_codes:
            code = str(code).strip()
            existing = await session.execute(
                select(AirportDB).where(AirportDB.code == code)
            )
            if not existing.scalar_one_or_none():
                info = KNOWN_AIRPORTS.get(code, (f"Airport {code}", "Unknown", "XX", 0, 0))
                session.add(AirportDB(
                    code=code, name=info[0], city=info[1],
                    state=info[2], latitude=info[3], longitude=info[4],
                ))

        await session.commit()

        # Batch insert flights
        batch_size = 5000
        inserted = 0

        for start_idx in range(0, total_rows, batch_size):
            batch = df.iloc[start_idx:start_idx + batch_size]
            flight_objects = []

            for idx, row in batch.iterrows():
                try:
                    flight = FlightDB(
                        flight_number=str(row.get("flight_number", "")),
                        airline_code=str(row.get("airline_code", "")),
                        origin_airport=str(row.get("origin_airport", "")),
                        destination_airport=str(row.get("destination_airport", "")),
                        scheduled_departure=_parse_datetime(row.get("scheduled_departure")),
                        actual_departure=_parse_datetime(row.get("actual_departure")),
                        scheduled_arrival=_parse_datetime(row.get("scheduled_arrival")),
                        actual_arrival=_parse_datetime(row.get("actual_arrival")),
                        delay_minutes=int(row.get("delay_minutes", 0)),
                        delay_reason=str(row.get("delay_reason", "") or ""),
                        distance=float(row.get("distance", 0) or 0),
                        weather_condition=str(row.get("weather_condition", "") or ""),
                        day_of_week=int(row.get("day_of_week", 0) or 0),
                        month=int(row.get("month", 1) or 1),
                        is_delayed=bool(int(row.get("is_delayed", 0) or 0)),
                    )
                    flight_objects.append(flight)
                except Exception as e:
                    logger.warning(f"Skipping row {idx}: {e}")
                    continue

            session.add_all(flight_objects)
            await session.commit()
            inserted += len(flight_objects)

    duration = (datetime.now() - start_time).total_seconds()

    return {
        "success": True,
        "rows_imported": inserted,
        "total_rows": total_rows,
        "duration_seconds": round(duration, 2),
    }


def _parse_datetime(value) -> Optional[datetime]:
    """Parse a datetime value from CSV."""
    if pd.isna(value) or value is None or str(value).strip() == "":
        return None
    try:
        return pd.to_datetime(str(value))
    except Exception:
        return None


# ── Query functions for API ─────────────────────────────────


async def get_flight_stats(
    airline: Optional[str] = None,
    date_from: Optional[str] = None,
    date_to: Optional[str] = None,
) -> dict:
    """Get dashboard statistics."""
    async with async_session() as session:
        query = select(
            func.count(FlightDB.id).label("total"),
            func.sum(case((FlightDB.is_delayed == True, 1), else_=0)).label("delayed"),
            func.avg(
                case((FlightDB.is_delayed == True, FlightDB.delay_minutes), else_=None)
            ).label("avg_delay"),
        )

        if airline:
            query = query.where(FlightDB.airline_code == airline)
        if date_from:
            query = query.where(FlightDB.scheduled_departure >= date_from)
        if date_to:
            query = query.where(FlightDB.scheduled_departure <= date_to)

        result = await session.execute(query)
        row = result.one()

        total = row.total or 0
        delayed = row.delayed or 0
        avg_delay = round(float(row.avg_delay or 0), 1)
        delay_rate = round((delayed / total * 100) if total > 0 else 0, 1)
        ontime_rate = round(100 - delay_rate, 1)

        return {
            "total_flights": total,
            "delayed_count": delayed,
            "delay_rate": delay_rate,
            "avg_delay_minutes": avg_delay,
            "ontime_rate": ontime_rate,
        }


async def get_flights_list(
    page: int = 1,
    limit: int = 20,
    airline: Optional[str] = None,
    origin: Optional[str] = None,
    destination: Optional[str] = None,
    delayed: Optional[bool] = None,
) -> dict:
    """Get paginated flight list."""
    async with async_session() as session:
        count_q = select(func.count(FlightDB.id))
        data_q = select(FlightDB)

        if airline:
            count_q = count_q.where(FlightDB.airline_code == airline)
            data_q = data_q.where(FlightDB.airline_code == airline)
        if origin:
            count_q = count_q.where(FlightDB.origin_airport == origin)
            data_q = data_q.where(FlightDB.origin_airport == origin)
        if destination:
            count_q = count_q.where(FlightDB.destination_airport == destination)
            data_q = data_q.where(FlightDB.destination_airport == destination)
        if delayed is not None:
            count_q = count_q.where(FlightDB.is_delayed == delayed)
            data_q = data_q.where(FlightDB.is_delayed == delayed)

        total_result = await session.execute(count_q)
        total = total_result.scalar() or 0

        offset = (page - 1) * limit
        data_q = data_q.order_by(desc(FlightDB.scheduled_departure)).offset(offset).limit(limit)

        result = await session.execute(data_q)
        flights = result.scalars().all()

        return {
            "flights": [
                {
                    "id": f.id,
                    "flight_number": f.flight_number,
                    "airline_code": f.airline_code,
                    "origin": f.origin_airport,
                    "destination": f.destination_airport,
                    "scheduled_departure": str(f.scheduled_departure) if f.scheduled_departure else None,
                    "delay_minutes": f.delay_minutes,
                    "delay_reason": f.delay_reason,
                    "weather": f.weather_condition,
                    "is_delayed": f.is_delayed,
                }
                for f in flights
            ],
            "total": total,
            "page": page,
            "limit": limit,
            "total_pages": max(1, -(-total // limit)),
        }


async def get_delay_by_route(top: int = 10) -> list:
    """Get delay statistics grouped by route."""
    async with async_session() as session:
        query = text("""
            SELECT 
                origin_airport || ' -> ' || destination_airport as route,
                origin_airport,
                destination_airport,
                COUNT(*) as total_flights,
                SUM(CASE WHEN is_delayed = 1 THEN 1 ELSE 0 END) as delayed_flights,
                ROUND(CAST(SUM(CASE WHEN is_delayed = 1 THEN 1 ELSE 0 END) AS FLOAT) / COUNT(*) * 100, 1) as delay_rate,
                ROUND(AVG(CASE WHEN is_delayed = 1 THEN delay_minutes ELSE NULL END), 1) as avg_delay
            FROM flights
            GROUP BY origin_airport, destination_airport
            HAVING COUNT(*) >= 10
            ORDER BY delay_rate DESC
            LIMIT :top
        """)
        result = await session.execute(query, {"top": top})
        rows = result.fetchall()

        return [
            {
                "route": row[0],
                "origin": row[1],
                "destination": row[2],
                "total_flights": row[3],
                "delayed_flights": row[4],
                "delay_rate": row[5] or 0,
                "avg_delay_minutes": row[6] or 0,
            }
            for row in rows
        ]


async def get_delay_by_weather() -> list:
    """Get delay statistics grouped by weather condition."""
    async with async_session() as session:
        query = text("""
            SELECT 
                weather_condition,
                COUNT(*) as total,
                SUM(CASE WHEN is_delayed = 1 THEN 1 ELSE 0 END) as delayed,
                ROUND(CAST(SUM(CASE WHEN is_delayed = 1 THEN 1 ELSE 0 END) AS FLOAT) / COUNT(*) * 100, 1) as rate
            FROM flights
            WHERE weather_condition != '' AND weather_condition IS NOT NULL
            GROUP BY weather_condition
            ORDER BY rate DESC
        """)
        result = await session.execute(query)
        rows = result.fetchall()

        return [
            {"weather": row[0], "total": row[1], "delayed": row[2], "rate": row[3] or 0}
            for row in rows
        ]


async def get_delay_by_time(group: str = "hour") -> list:
    """Get delay statistics grouped by time period."""
    async with async_session() as session:
        if group == "hour":
            query = text("""
                SELECT 
                    CAST(strftime('%H', scheduled_departure) AS INTEGER) as label,
                    COUNT(*) as total,
                    SUM(CASE WHEN is_delayed = 1 THEN 1 ELSE 0 END) as delayed,
                    ROUND(CAST(SUM(CASE WHEN is_delayed = 1 THEN 1 ELSE 0 END) AS FLOAT) / COUNT(*) * 100, 1) as rate
                FROM flights
                WHERE scheduled_departure IS NOT NULL
                GROUP BY label
                ORDER BY label
            """)
        elif group == "day":
            query = text("""
                SELECT 
                    day_of_week as label,
                    COUNT(*) as total,
                    SUM(CASE WHEN is_delayed = 1 THEN 1 ELSE 0 END) as delayed,
                    ROUND(CAST(SUM(CASE WHEN is_delayed = 1 THEN 1 ELSE 0 END) AS FLOAT) / COUNT(*) * 100, 1) as rate
                FROM flights
                GROUP BY day_of_week
                ORDER BY day_of_week
            """)
        else:
            query = text("""
                SELECT 
                    month as label,
                    COUNT(*) as total,
                    SUM(CASE WHEN is_delayed = 1 THEN 1 ELSE 0 END) as delayed,
                    ROUND(CAST(SUM(CASE WHEN is_delayed = 1 THEN 1 ELSE 0 END) AS FLOAT) / COUNT(*) * 100, 1) as rate
                FROM flights
                GROUP BY month
                ORDER BY month
            """)

        result = await session.execute(query)
        rows = result.fetchall()

        month_names = ["", "Jan", "Feb", "Mar", "Apr", "May", "Jun",
                       "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        day_names = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

        output = []
        for row in rows:
            label = row[0]
            if group == "hour":
                label = f"{int(label):02d}:00"
            elif group == "day":
                label = day_names[int(label)] if int(label) < 7 else str(label)
            elif group == "month":
                label = month_names[int(label)] if 1 <= int(label) <= 12 else str(label)

            output.append({
                "label": str(label),
                "total": row[1],
                "delayed": row[2],
                "rate": row[3] or 0,
            })

        return output


async def get_airlines_list() -> list:
    """Get list of all airlines in database."""
    async with async_session() as session:
        result = await session.execute(
            select(AirlineDB).order_by(AirlineDB.name)
        )
        airlines = result.scalars().all()
        return [{"code": a.code, "name": a.name} for a in airlines]


async def get_airports_list() -> list:
    """Get list of all airports in database."""
    async with async_session() as session:
        result = await session.execute(
            select(AirportDB).order_by(AirportDB.name)
        )
        airports = result.scalars().all()
        return [
            {"code": a.code, "name": a.name, "city": a.city}
            for a in airports
        ]
