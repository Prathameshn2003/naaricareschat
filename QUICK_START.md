# NaariCare ML System - Quick Start Guide

## What's Running

✅ **Backend Server:** `http://127.0.0.1:8001`  
✅ **Frontend Dev Server:** `http://localhost:8080`

## How to Test

### Option 1: Command Line Tests
```bash
# Test individual API endpoints
python backend/test_api.py

# Run full end-to-end tests
python backend/test_e2e.py
```

### Option 2: Manual Testing
```bash
# Test PCOS prediction
curl -X POST http://127.0.0.1:8001/ml-predict \
  -H "Content-Type: application/json" \
  -d '{
    "model_type": "pcos",
    "input_data": {
      "age": 28,
      "weight": 65,
      "bmi": 24,
      "cycleRegular": true,
      "cycleLength": 28,
      "weightGain": false,
      "hairGrowth": false,
      "skinDarkening": false,
      "hairLoss": false,
      "pimples": false,
      "fastFood": false,
      "regularExercise": true,
      "follicleLeft": 5,
      "follicleRight": 6,
      "endometrium": 8
    }
  }'
```

### Option 3: Frontend Testing
1. Open `http://localhost:8080` in your browser
2. Navigate to a module that uses ML predictions (PCOS, Menstrual, etc.)
3. Fill in the form with test data
4. Submit to see predictions
5. Check browser console for API calls

## API Endpoints

### Main Endpoint
```
POST /ml-predict
```

**Request Format:**
```json
{
  "model_type": "pcos|menopause|cycle",
  "input_data": { /* model-specific fields */ }
}
```

**Response Format:**
```json
{
  "fallback": false,
  "prediction": { /* model-specific results */ }
}
```

## Model Details

### PCOS Model
- **Input:** Age, weight, BMI, cycle info, hormonal markers, ultrasound data
- **Output:** `{hasPCOS: boolean, riskPercentage: number}`
- **Files:** 
  - `backend/models/pcos/rf_model.pkl`
  - `backend/models/pcos/xgb_model.pkl`
  - `backend/models/pcos/knn_model.pkl`
  - `backend/models/pcos/scaler.pkl`

### Menstrual Cycle Model
- **Input:** Previous 3 cycle lengths, last period start date
- **Output:** `{predictedStartDate: string, averageCycleLength: number, cycleVariability: number, isIrregular: boolean}`
- **Files:**
  - `backend/models/menstrual/lstm_model.h5`
  - `backend/models/menstrual/scaler.pkl`
  - `backend/models/menstrual/knn_model.pkl`

### Menopause Model
- **Status:** ⚠️ Not available (fallback mode)
- **Files:**
  - `backend/models/menopause/scaler.pkl` ✓
  - `backend/models/menopause/label_encoder.pkl` ✓
  - `backend/models/menopause/rf_model.pkl` ✗ (missing)

## Restarting Servers

### Stop Backend
```bash
# Using PowerShell - find the process using port 8001
Get-NetTCPConnection -LocalPort 8001 | Stop-Process -Force
```

### Restart Backend
```bash
cd backend
"..\.venv\Scripts\python.exe" -m uvicorn main:app --host 127.0.0.1 --port 8001
```

### Restart Frontend
```bash
npm run dev
```

## Troubleshooting

### Port Already in Use
```powershell
# Kill process on port 8001
taskkill /F /IM python.exe

# Or find and kill specific port
netstat -ano | findstr :8001
taskkill /PID <PID> /F
```

### Backend Not Starting
Check these issues in order:
1. All dependencies installed: `pip install -r requirements.txt`
2. Virtual environment active: check `.venv` directory
3. Model files exist: `backend/models/*/`
4. No permissions issues on model files

### Frontend Won't Connect
1. Verify backend is running: `curl http://127.0.0.1:8001/`
2. Check browser console for CORS errors
3. Verify Supabase ML_API_URL environment variable is set (for production)

## Development Notes

- Backend uses graceful fallback for missing models
- Frontend has local prediction logic as backup
- Both PCOS and Menstrual models are fully operational
- Menopause model returns fallback (can be enabled when RF model is available)

## File Locations

```
NaariCare App/
├── backend/
│   ├── main.py (FastAPI server)
│   ├── requirements.txt
│   ├── models/
│   │   ├── pcos/
│   │   ├── menstrual/
│   │   └── menopause/
│   ├── test_api.py (unit tests)
│   └── test_e2e.py (integration tests)
├── src/
│   └── lib/
│       └── ml-predictions.ts (frontend ML interface)
└── supabase/
    └── functions/
        └── ml-predict/
            └── index.ts (Supabase edge function)
```
