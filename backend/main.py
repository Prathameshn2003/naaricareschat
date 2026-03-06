
import os
import sys
import warnings

# Suppress warnings BEFORE importing libraries
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # TensorFlow
warnings.filterwarnings('ignore')  # Suppress all warnings globally

from fastapi import FastAPI, Body
from fastapi.middleware.cors import CORSMiddleware
import joblib
import numpy as np
import pickle
from tensorflow.keras.models import load_model
from datetime import datetime, timedelta
import multiprocessing

# Additional warning suppression
import sklearn
import tensorflow as tf
tf.get_logger().setLevel('ERROR')  # TensorFlow error level
sklearn.set_config(print_changed_only=False)


app = FastAPI(title="NaariCare ML Backend")

# ==========================================
# CORS (React Frontend)
# ==========================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==========================================
# LOAD MODELS
# ==========================================

# PCOS
try:
    rf_model = pickle.load(open("models/pcos/rf_model.pkl", "rb"))
except Exception as e:
    print(f"Warning: Could not load PCOS RF: {e}")
    rf_model = None

try:
    xgb_model = pickle.load(open("models/pcos/xgb_model.pkl", "rb"))
except Exception as e:
    print(f"Warning: Could not load PCOS XGB: {e}")
    xgb_model = None

try:
    knn_model = pickle.load(open("models/pcos/knn_model.pkl", "rb"))
except Exception as e:
    print(f"Warning: Could not load PCOS KNN: {e}")
    knn_model = None

try:
    scaler = pickle.load(open("models/pcos/scaler.pkl", "rb"))
except Exception as e:
    print(f"Warning: Could not load PCOS scaler: {e}")
    scaler = None

try:
    imputer = pickle.load(open("models/pcos/imputer.pkl", "rb"))
except Exception as e:
    print(f"Warning: Could not load PCOS imputer: {e}")
    imputer = None

# MENOPAUSE
try:
    # meno_rf = joblib.load("models/menopause/rf_model.pkl")
    meno_rf = None
except Exception as e:
    print(f"Warning: Could not load menopause RF: {e}")
    meno_rf = None

try:
    meno_scaler = pickle.load(open("models/menopause/scaler.pkl", "rb"))
except Exception as e:
    print(f"Warning: Could not load menopause scaler: {e}")
    meno_scaler = None

try:
    meno_le = pickle.load(open("models/menopause/label_encoder.pkl", "rb"))
except Exception as e:
    print(f"Warning: Could not load menopause label encoder: {e}")
    meno_le = None

# MENSTRUAL
try:
    cycle_model = load_model("models/menstrual/lstm_model.h5", compile=False)
except Exception as e:
    print(f"Warning: Could not load LSTM model: {e}")
    cycle_model = None

try:
    cycle_scaler = pickle.load(open("models/menstrual/scaler.pkl", "rb"))
except Exception as e:
    print(f"Warning: Could not load cycle scaler: {e}")
    cycle_scaler = None

try:
    cycle_knn = pickle.load(open("models/menstrual/knn_model.pkl", "rb"))
except Exception as e:
    print(f"Warning: Could not load cycle KNN: {e}")
    cycle_knn = None

# ==========================================
# ROOT
# ==========================================

@app.get("/")
def root():
    return {"message": "NaariCare ML Backend Running"}

# ==========================================
# MAIN ML API
# ==========================================

@app.post("/ml-predict")
def ml_predict(data: dict = Body(...)):

    model_type = data.get("model_type")
    input_data = data.get("input_data")

    # ================= PCOS =================
    if model_type == "pcos":

        if rf_model is None or xgb_model is None or knn_model is None or scaler is None or imputer is None:
            return {
                "fallback": True,
                "error": "PCOS model not available"
            }

        cycle_val = 1 if input_data["cycleRegular"] else 0

        X = np.array([
            input_data["age"],
            input_data["weight"],
            input_data["bmi"],
            cycle_val,
            input_data["cycleLength"],
            int(input_data["weightGain"]),
            int(input_data["hairGrowth"]),
            int(input_data["skinDarkening"]),
            int(input_data["hairLoss"]),
            int(input_data["pimples"]),
            int(input_data["fastFood"]),
            int(input_data["regularExercise"]),
            input_data["follicleLeft"],
            input_data["follicleRight"],
            input_data["endometrium"]
        ]).reshape(1, -1)

        X = imputer.transform(X)
        X = scaler.transform(X)

        rf_pred = rf_model.predict(X)[0]
        xgb_pred = xgb_model.predict(X)[0]
        knn_pred = knn_model.predict(X)[0]

        final_pred = 1 if (rf_pred + xgb_pred + knn_pred) >= 2 else 0

        cycle_score = 1 if cycle_val == 0 else 0
        hormonal_score = (
            int(input_data["hairGrowth"]) +
            int(input_data["skinDarkening"]) +
            int(input_data["hairLoss"]) +
            int(input_data["pimples"])
        )

        ultrasound_score = 1 if (input_data["follicleLeft"] + input_data["follicleRight"]) >= 10 else 0
        metabolic_score = 1 if input_data["bmi"] >= 25 else 0

        total_score = (
            2 * cycle_score +
            2 * ultrasound_score +
            hormonal_score +
            metabolic_score
        )

        risk_percentage = int((total_score / 9) * 100)
        risk_percentage = max(30, risk_percentage) if final_pred else 10

        return {
            "fallback": False,
            "prediction": {
                "hasPCOS": bool(final_pred),
                "riskPercentage": risk_percentage
            }
        }

    # ================= MENOPAUSE =================
    elif model_type == "menopause":

        if meno_rf is None or meno_scaler is None or meno_le is None:
            return {
                "fallback": True,
                "error": "Menopause model not available"
            }

        inputs = [
            input_data["age"],
            input_data["estrogenLevel"],
            input_data["fshLevel"],
            input_data["yearsSinceLastPeriod"],
            int(input_data["irregularPeriods"]),
            int(input_data["missedPeriods"]),
            int(input_data["hotFlashes"]),
            int(input_data["nightSweats"]),
            int(input_data["sleepProblems"]),
            int(input_data["vaginalDryness"]),
            int(input_data["jointPain"])
        ]

        X = meno_scaler.transform([inputs])

        probs = meno_rf.predict_proba(X)[0]
        stage_index = probs.argmax()
        stage = meno_le.inverse_transform([stage_index])[0]

        return {
            "fallback": False,
            "prediction": {
                "stage": stage,
                "riskPercentage": int(probs[stage_index] * 100)
            }
        }

    # ================= CYCLE =================
    elif model_type == "cycle":

        # Handle different input formats
        if "cycleHistory" in input_data:
            # Frontend format: cycleHistory array
            cycle_history = input_data["cycleHistory"]
            if len(cycle_history) >= 3:
                prev1 = cycle_history[-1]  # Most recent
                prev2 = cycle_history[-2]  # Second most recent
                prev3 = cycle_history[-3]  # Third most recent
            else:
                # Fallback to average if not enough history
                avg_cycle = input_data.get("averageCycleLength", 28)
                prev1 = prev2 = prev3 = avg_cycle
        else:
            # Legacy format with prev1, prev2, prev3
            prev1 = input_data.get("prev1", input_data.get("averageCycleLength", 28))
            prev2 = input_data.get("prev2", prev1)
            prev3 = input_data.get("prev3", prev1)

        predicted_cycle = int((prev1*0.4 + prev2*0.3 + prev3*0.3))

        last_date_str = input_data["lastPeriodStart"]
        if isinstance(last_date_str, str):
            # Handle ISO string format
            if last_date_str.endswith('Z'):
                last_date = datetime.strptime(last_date_str, "%Y-%m-%dT%H:%M:%S.%fZ")
            else:
                last_date = datetime.fromisoformat(last_date_str.replace('Z', '+00:00'))
        else:
            # Handle Date object (shouldn't happen in API)
            last_date = datetime.now()

        next_date = last_date + timedelta(days=predicted_cycle)

        variation = max(prev1, prev2, prev3) - min(prev1, prev2, prev3)

        return {
            "fallback": False,
            "prediction": {
                "predictedStartDate": str(next_date.date()),
                "averageCycleLength": predicted_cycle,
                "cycleVariability": variation,
                "isIrregular": variation > 7
            }
        }

    return {"fallback": True, "error": "Invalid model type"}


# ==========================================
# WINDOWS SAFE START
# ==========================================

if __name__ == "__main__":
    multiprocessing.freeze_support()

    import uvicorn

    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )
