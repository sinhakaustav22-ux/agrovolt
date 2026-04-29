from pydantic import BaseModel
from typing import Optional
from datetime import datetime


# ─── Crop ────────────────────────────────────────────────────────────────────

class CropPredictRequest(BaseModel):
    shading_pct: float          # 0–100, how much panel covers the crop area
    temperature: float          # Celsius
    soil_moisture: float        # 0–100%
    rainfall: float             # mm
    crop_type_encoded: int      # 0=wheat, 1=rice, 2=vegetables, 3=berries
    panel_tilt: float           # degrees (0–90)

class CropPredictResponse(BaseModel):
    predicted_yield_kg_per_hectare: float
    land_equivalent_ratio: float
    recommendation: str


# ─── Solar ───────────────────────────────────────────────────────────────────

class SolarForecastRequest(BaseModel):
    latitude: float
    longitude: float
    panel_count: int
    panel_watt_peak: float      # Watts per panel

class SolarForecastResponse(BaseModel):
    forecast_7_days: list       # List of daily kWh predictions
    total_kwh: float
    avg_daily_kwh: float


# ─── Irrigation ──────────────────────────────────────────────────────────────

class IrrigationRequest(BaseModel):
    soil_moisture: float
    temperature: float
    crop_type_encoded: int
    rainfall_last_24h: float
    time_of_day: int            # Hour in 24h format (0–23)

class IrrigationResponse(BaseModel):
    recommendation: str         # "irrigate_now", "irrigate_in_2h", "no_irrigation"
    label: str                  # Human readable
    confidence: float


# ─── Farm ────────────────────────────────────────────────────────────────────

class FarmCreate(BaseModel):
    name: str
    location: str
    latitude: float
    longitude: float
    panel_count: int
    crop_type: str
    area_hectares: float

class FarmResponse(BaseModel):
    id: int
    name: str
    location: str
    latitude: float
    longitude: float
    panel_count: int
    crop_type: str
    area_hectares: float
    created_at: datetime

    class Config:
        from_attributes = True


# ─── Sensor Data ─────────────────────────────────────────────────────────────

class SensorDataCreate(BaseModel):
    farm_id: int
    soil_moisture: float
    temperature: float
    shading_pct: float
