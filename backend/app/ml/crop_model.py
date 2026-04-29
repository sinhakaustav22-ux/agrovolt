import numpy as np
import os

# We try to load the saved model. If it doesn't exist yet (not trained),
# we fall back to a formula-based mock so the API still works.

MODEL_PATH = "models_saved/crop_model.pkl"
model = None

try:
    import joblib
    if os.path.exists(MODEL_PATH):
        model = joblib.load(MODEL_PATH)
        print("✅ Crop model loaded from disk")
    else:
        print("⚠️  No saved crop model found — using formula fallback")
except Exception as e:
    print(f"⚠️  Model load error: {e}")


CROP_BASE_YIELDS = {
    0: 3500,   # wheat
    1: 4800,   # rice
    2: 6000,   # vegetables
    3: 2200,   # berries
}


def predict_crop_yield(shading_pct, temperature, soil_moisture,
                       rainfall, crop_type_encoded, panel_tilt) -> dict:
    """
    Predict crop yield in kg/hectare.
    Uses XGBoost model if trained; otherwise uses agronomic formula.
    """
    features = np.array([[shading_pct, temperature, soil_moisture,
                          rainfall, crop_type_encoded, panel_tilt]])

    if model:
        yield_pred = float(model.predict(features)[0])
    else:
        # Formula fallback (good enough for demo)
        base = CROP_BASE_YIELDS.get(crop_type_encoded, 4000)
        shade_factor  = 1 + (0.15 if 20 <= shading_pct <= 40 else -0.1)
        temp_factor   = 1 - abs(temperature - 25) * 0.01
        moist_factor  = 1 + (soil_moisture - 40) * 0.005
        rain_factor   = 1 + min(rainfall, 100) * 0.002
        yield_pred = base * shade_factor * temp_factor * moist_factor * rain_factor

    # Land Equivalent Ratio: agrovoltaic land efficiency metric
    # LER > 1 means dual-use is better than separate plots
    ler = round(1 + (shading_pct * 0.004), 2)

    # Advice
    if yield_pred > 5000:
        rec = "Excellent conditions. Maintain current panel configuration."
    elif yield_pred > 3000:
        rec = "Good yield. Consider increasing shading slightly to reduce heat stress."
    else:
        rec = "Low yield. Reduce shading or switch to shade-tolerant crops."

    return {
        "predicted_yield_kg_per_hectare": round(yield_pred, 2),
        "land_equivalent_ratio": ler,
        "recommendation": rec
    }
