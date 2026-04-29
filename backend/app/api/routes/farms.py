from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.db import get_db
from app.database import crud
from app.models.schemas import FarmCreate, FarmResponse, SensorDataCreate
from typing import List

router = APIRouter()


@router.get("/", response_model=List[FarmResponse])
def get_farms(db: Session = Depends(get_db)):
    """Return all farms."""
    return crud.get_all_farms(db)


@router.get("/{farm_id}", response_model=FarmResponse)
def get_farm(farm_id: int, db: Session = Depends(get_db)):
    """Return a specific farm by ID."""
    farm = crud.get_farm_by_id(db, farm_id)
    if not farm:
        raise HTTPException(status_code=404, detail="Farm not found")
    return farm


@router.post("/", response_model=FarmResponse)
def create_farm(farm: FarmCreate, db: Session = Depends(get_db)):
    """Add a new farm."""
    return crud.create_farm(db, farm)


@router.get("/{farm_id}/predictions")
def get_farm_predictions(farm_id: int, db: Session = Depends(get_db)):
    """Get all predictions history for a farm."""
    return crud.get_predictions_by_farm(db, farm_id)


@router.post("/sensor-data")
def post_sensor_data(data: SensorDataCreate, db: Session = Depends(get_db)):
    """
    Endpoint for IoT sensors to push real-time readings.
    In production, sensors POST here on a schedule.
    """
    return crud.save_sensor_data(db, data)
