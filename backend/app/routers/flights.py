"""
Flights router - API endpoints for flight data queries.
"""
from typing import Optional

from fastapi import APIRouter, Query

from app.services.data_processor import (
    get_flight_stats,
    get_flights_list,
    get_delay_by_route,
    get_delay_by_weather,
    get_delay_by_time,
    get_airlines_list,
    get_airports_list,
)

router = APIRouter()


@router.get("", response_model=dict)
async def list_flights(
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(20, ge=1, le=100, description="Items per page"),
    airline: Optional[str] = Query(None, description="Filter by airline code"),
    origin: Optional[str] = Query(None, description="Filter by origin airport"),
    destination: Optional[str] = Query(None, description="Filter by destination"),
    delayed: Optional[bool] = Query(None, description="Filter delayed flights"),
):
    """List flights with pagination and filters."""
    try:
        data = await get_flights_list(
            page=page, limit=limit,
            airline=airline, origin=origin,
            destination=destination, delayed=delayed,
        )
        return {"success": True, "data": data, "message": "OK"}
    except Exception as e:
        return {"success": False, "data": None, "message": str(e)}


@router.get("/stats", response_model=dict)
async def get_stats(
    airline: Optional[str] = Query(None, description="Filter by airline"),
    date_from: Optional[str] = Query(None, description="Start date (YYYY-MM-DD)"),
    date_to: Optional[str] = Query(None, description="End date (YYYY-MM-DD)"),
):
    """Get dashboard statistics."""
    try:
        data = await get_flight_stats(
            airline=airline, date_from=date_from, date_to=date_to,
        )
        has_data = data["total_flights"] > 0
        return {
            "success": True,
            "data": data,
            "message": "OK" if has_data else "No data yet. Upload a CSV dataset first.",
        }
    except Exception as e:
        return {"success": False, "data": None, "message": str(e)}


@router.get("/by-route", response_model=dict)
async def get_by_route(
    top: int = Query(10, ge=1, le=50, description="Top N routes"),
):
    """Get delay statistics grouped by route."""
    try:
        data = await get_delay_by_route(top=top)
        return {"success": True, "data": data, "message": "OK"}
    except Exception as e:
        return {"success": False, "data": [], "message": str(e)}


@router.get("/by-weather", response_model=dict)
async def get_by_weather():
    """Get delay statistics grouped by weather condition."""
    try:
        data = await get_delay_by_weather()
        return {"success": True, "data": data, "message": "OK"}
    except Exception as e:
        return {"success": False, "data": [], "message": str(e)}


@router.get("/by-time", response_model=dict)
async def get_by_time(
    group: str = Query("hour", description="Group by: hour, day, month"),
):
    """Get delay statistics grouped by time."""
    if group not in ("hour", "day", "month"):
        return {"success": False, "data": [], "message": "group must be: hour, day, or month"}
    try:
        data = await get_delay_by_time(group=group)
        return {"success": True, "data": data, "message": "OK"}
    except Exception as e:
        return {"success": False, "data": [], "message": str(e)}


@router.get("/airlines", response_model=dict)
async def list_airlines():
    """Get list of all airlines."""
    try:
        data = await get_airlines_list()
        return {"success": True, "data": data, "message": "OK"}
    except Exception as e:
        return {"success": False, "data": [], "message": str(e)}


@router.get("/airports", response_model=dict)
async def list_airports():
    """Get list of all airports."""
    try:
        data = await get_airports_list()
        return {"success": True, "data": data, "message": "OK"}
    except Exception as e:
        return {"success": False, "data": [], "message": str(e)}
