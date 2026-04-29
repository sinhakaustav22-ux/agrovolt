import numpy as np
import os

MODEL_PATH = "models_saved/irrigation_model.pkl"
model = None

try:
    import joblib
    if os.path.exists(MODEL_PATH):
        model = joblib.load(MODEL_PATH)
        print("✅ Irrigation model loaded from disk")
    else:
        print("⚠️  No saved irrigation model — using rule-based fallback")
except Exception as e:
    print(f"⚠️  Irrigation model load error: {e}")


LABELS = {
    0: ("irrigate_now",     "💧 Irrigate Now",         "Soil moisture critically low."),
    1: ("irrigate_in_2h",  "⏰ Irrigate in 2 Hours",   "Moisture dropping. Schedule soon."),
    2: ("no_irrigation",   "✅ No Irrigation Needed",   "Soil moisture is adequate."),
}


def recommend_irrigation(soil_moisture, temperature, crop_type_encoded,
                          rainfall_last_24h, time_of_day) -> dict:
    """
    Classify irrigation need into 3 classes.
    Uses Random Forest if trained; else rule-based logic.
    """
    if model:
        features = np.array([[soil_moisture, temperature, crop_type_encoded,
                               rainfall_last_24h, time_of_day]])
        label_idx  = int(model.predict(features)[0])
        proba      = float(model.predict_proba(features).max())
    else:
        # Rule-based fallback
        if soil_moisture < 25 and rainfall_last_24h < 5:
            label_idx = 0
        elif soil_moisture < 45 and temperature > 30:
            label_idx = 1
        else:
            label_idx = 2

        # Mock confidence
        proba = 0.91 if label_idx == 0 else (0.84 if label_idx == 1 else 0.92)

    code, label, reason = LABELS[label_idx]

    return {
        "recommendation": code,
        "label": label,
        "reason": reason,
        "confidence": round(proba, 2)
    }
