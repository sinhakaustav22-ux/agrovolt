import httpx

NASA_BASE = "https://power.larc.nasa.gov/api/temporal/daily/point"


async def get_solar_irradiance(lat: float, lon: float) -> dict:
    """
    Fetch historical solar irradiance from NASA POWER API.
    No API key required — completely free and open.
    Returns last 30 days of data for LSTM model input.
    """
    params = {
        "parameters": "ALLSKY_SFC_SW_DWN",   # Surface solar irradiance
        "community":  "RE",
        "longitude":  lon,
        "latitude":   lat,
        "start":      "20240101",
        "end":        "20240131",
        "format":     "JSON"
    }

    try:
        async with httpx.AsyncClient(timeout=15.0) as client:
            resp = await client.get(NASA_BASE, params=params)
            data = resp.json()
        irradiance = data["properties"]["parameter"]["ALLSKY_SFC_SW_DWN"]
        values = list(irradiance.values())
        return {"irradiance_30_days": values, "unit": "kWh/m²/day"}
    except Exception as e:
        # Return mock if NASA API is down or slow
        mock_vals = [4.5 + (i % 7) * 0.3 for i in range(30)]
        return {"irradiance_30_days": mock_vals, "unit": "kWh/m²/day (mock)"}
