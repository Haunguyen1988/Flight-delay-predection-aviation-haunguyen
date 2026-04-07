"""
Data router - API endpoints for data upload and management.
"""
import logging
from fastapi import APIRouter, UploadFile, File, HTTPException

from app.services.data_processor import validate_csv, import_csv_to_db

logger = logging.getLogger(__name__)

router = APIRouter()

MAX_FILE_SIZE = 500 * 1024 * 1024  # 500MB


@router.post("/upload", response_model=dict)
async def upload_csv(file: UploadFile = File(...)):
    """Upload CSV dataset for processing."""
    # Validate file type
    if not file.filename or not file.filename.endswith(".csv"):
        raise HTTPException(
            status_code=400,
            detail="Only CSV files (.csv) are supported.",
        )

    # Read file content
    try:
        content = await file.read()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to read file: {str(e)}")

    # Check file size
    file_size = len(content)
    if file_size == 0:
        raise HTTPException(status_code=400, detail="File is empty.")

    if file_size > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=400,
            detail=f"File too large. Max size is {MAX_FILE_SIZE // (1024*1024)}MB.",
        )

    # Validate CSV structure
    validation = await validate_csv(content)
    if not validation["valid"]:
        raise HTTPException(status_code=400, detail=validation["error"])

    logger.info(
        f"Importing CSV: {file.filename} ({validation['row_count']} rows, "
        f"{file_size / 1024:.0f}KB)"
    )

    # Import to database
    try:
        result = await import_csv_to_db(content)
    except Exception as e:
        logger.error(f"Import failed: {e}")
        raise HTTPException(status_code=500, detail=f"Import failed: {str(e)}")

    if not result.get("success"):
        raise HTTPException(status_code=500, detail=result.get("error", "Unknown error"))

    return {
        "success": True,
        "data": {
            "filename": file.filename,
            "rows_imported": result["rows_imported"],
            "total_rows": result["total_rows"],
            "duration_seconds": result["duration_seconds"],
        },
        "message": f"Successfully imported {result['rows_imported']} flights in {result['duration_seconds']}s",
    }


@router.post("/generate-sample", response_model=dict)
async def generate_sample():
    """Generate sample dataset for testing."""
    try:
        from app.services.data_generator import generate_sample_data
        output_path = generate_sample_data(50000)

        # Read and import the generated file
        with open(output_path, "rb") as f:
            content = f.read()

        result = await import_csv_to_db(content)

        return {
            "success": True,
            "data": {
                "rows_imported": result["rows_imported"],
                "duration_seconds": result["duration_seconds"],
                "file_path": output_path,
            },
            "message": f"Generated and imported {result['rows_imported']} sample flights",
        }
    except Exception as e:
        logger.error(f"Sample generation failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))
