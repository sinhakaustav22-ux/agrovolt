from sqlalchemy.orm import Session
from app.database.db import Farm, Prediction, SensorData
from app.models.schemas import FarmCreate, SensorDataCreate
from datetime import datetime


def get_all_farms(db: Session):
    return db.query(Farm).all()


def get_farm_by_id(db: Session, farm_id: int):
    return db.query(Farm).filter(Farm.id == farm_id).first()


def create_farm(db: Session, farm: FarmCreate):
    db_farm = Farm(**farm.dict())
    db.add(db_farm)
    db.commit()
    db.refresh(db_farm)
    return db_farm


def save_prediction(db: Session, farm_id: int, yield_val: float,
                    solar_kwh: float, irrigation: str):
    pred = Prediction(
        farm_id=farm_id,
        predicted_yield=yield_val,
        predicted_solar_kwh=solar_kwh,
        irrigation_recommendation=irrigation,
        timestamp=datetime.utcnow()
    )
    db.add(pred)
    db.commit()
    return pred


def get_predictions_by_farm(db: Session, farm_id: int):
    return db.query(Prediction).filter(Prediction.farm_id == farm_id).all()


def save_sensor_data(db: Session, data: SensorDataCreate):
    sensor = SensorData(**data.dict())
    db.add(sensor)
    db.commit()
    return sensor