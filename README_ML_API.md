# Python ML API Quick Start

## 🚀 Starting the Python ML API Server

### Windows:
```bash
start_ml_api.bat
```

### Linux/Mac:
```bash
chmod +x start_ml_api.sh
./start_ml_api.sh
```

### Manual Start:
```bash
# Create virtual environment (if not exists)
python -m venv ml_api_env

# Activate virtual environment
# Windows:
ml_api_env\Scripts\activate
# Linux/Mac:
source ml_api_env/bin/activate

# Install dependencies
pip install -r requirements_ml_api.txt

# Start server
python ml_api_server.py
```

## ✅ Verify It's Running

Once started, you should see:
```
============================================================
🚀 Starting ML Forecast API Server
============================================================
📊 Service: Linear Regression Forecasting
🌐 Listening on: http://0.0.0.0:5000
✅ Health check: GET http://0.0.0.0:5000/health
🔮 Forecast endpoint: POST http://0.0.0.0:5000/predict/consumables/linear
============================================================
```

## 🔍 Test the API

Open browser or use curl:
```
http://127.0.0.1:5000/health
```

Should return:
```json
{
  "status": "healthy",
  "service": "ML Forecast API",
  "version": "1.0.0"
}
```

## ⚙️ Frontend Configuration

Make sure `frontend-vue/.env` has:
```env
VITE_PY_API_BASE_URL=http://127.0.0.1:5000
```

Then restart your frontend dev server.

## 🐛 Troubleshooting

1. **Port 5000 already in use**: 
   - Change port in `ml_api_server.py`: `port = 5001`
   - Update `.env`: `VITE_PY_API_BASE_URL=http://127.0.0.1:5001`

2. **Python not found**:
   - Install Python 3.8+ from python.org
   - Verify: `python --version`

3. **Dependencies fail to install**:
   - Update pip: `python -m pip install --upgrade pip`
   - Try: `pip install -r requirements_ml_api.txt --no-cache-dir`

4. **Module not found errors**:
   - Make sure virtual environment is activated
   - Reinstall: `pip install -r requirements_ml_api.txt`

## 📊 How It Works

1. Laravel backend prepares historical usage data
2. Frontend sends data to Python ML API
3. Python uses scikit-learn LinearRegression for predictions
4. Results displayed in Usage Overview dashboard

