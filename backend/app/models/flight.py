"""
Flight data models - SQLAlchemy ORM + Pydantic schemas.
"""
from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import DeclarativeBase, relationship


# SQLAlchemy Base
class Base(DeclarativeBase):
    pass


# ── SQLAlchemy ORM Models ──────────────────────────────────────


class AirlineDB(Base):
    __tablename__ = "airlines"

    code = Column(String(5), primary_key=True)
    name = Column(String(100), nullable=False)

    flights = relationship("FlightDB", back_populates="airline")


class AirportDB(Base):
    __tablename__ = "airports"

    code = Column(String(5), primary_key=True)
    name = Column(String(100), nullable=False)
    city = Column(String(50))
    state = Column(String(50))
    latitude = Column(Float)
    longitude = Column(Float)


class FlightDB(Base):
    __tablename__ = "flights"

    id = Column(Integer, primary_key=True, autoincrement=True)
    flight_number = Column(String(10))
    airline_code = Column(String(5), ForeignKey("airlines.code"))
    origin_airport = Column(String(5), ForeignKey("airports.code"))
    destination_airport = Column(String(5), ForeignKey("airports.code"))
    scheduled_departure = Column(DateTime)
    actual_departure = Column(DateTime)
    scheduled_arrival = Column(DateTime)
    actual_arrival = Column(DateTime)
    delay_minutes = Column(Integer, default=0)
    delay_reason = Column(String(50))
    distance = Column(Float)
    weather_condition = Column(String(30))
    day_of_week = Column(Integer)
    month = Column(Integer)
    is_delayed = Column(Boolean, default=False)

    airline = relationship("AirlineDB", back_populates="flights")


class PredictionDB(Base):
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    airline_code = Column(String(5))
    origin = Column(String(5))
    destination = Column(String(5))
    departure_datetime = Column(DateTime)
    delay_probability = Column(Float)
    estimated_delay_min = Column(Integer)
    confidence = Column(String(10))


# ── Pydantic Response Schemas ──────────────────────────────────


class FlightStatsResponse(BaseModel):
    total_flights: int
    delayed_count: int
    delay_rate: float
    avg_delay_minutes: float
    ontime_rate: float


class FlightListResponse(BaseModel):
    flights: List[dict]
    total: int
    page: int
    limit: int
    total_pages: int


class RouteDelayResponse(BaseModel):
    route: str
    origin: str
    destination: str
    total_flights: int
    delayed_flights: int
    delay_rate: float
    avg_delay_minutes: float
