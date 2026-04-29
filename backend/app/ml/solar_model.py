import numpy as np
import random


def forecast_solar_output(latitude: float, longitude: float,
                           panel_count: int, panel_watt_peak: float) -> dict:
    """
    Forecast 7-day solar energy output.
    In production: LSTM model trained on NASA POWER irradiance data.
    For demo: physics-based formula + seasonal adjustment.
    """

    # Approximate daily peak sun hours based on latitude
    # Tropical (low lat) → more sun. Higher lat → less sun.
    base_peak_hours = max(3.5, 7.0 - abs(latitude) * 0.05)

    # Simulate 7 days with slight random variation (clouds, etc.)
    forecast = []
    for day in range(7):
        cloud_factor = random.uniform(0.65, 1.0)   # random cloud cover
        peak_hours   = base_peak_hours * cloud_factor
        daily_kwh    = (panel_count * panel_watt_peak * peak_hours) / 1000
        forecast.append(round(daily_kwh, 2))

    total     = round(sum(forecast), 2)
    avg_daily = round(total / 7, 2)

    return {
        "forecast_7_days": forecast,
        "total_kwh": total,
        "avg_daily_kwh": avg_daily
    }
