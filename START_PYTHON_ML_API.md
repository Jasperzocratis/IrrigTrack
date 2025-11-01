# 🚀 How to Start Python ML API Server

## ⚠️ Python Not Installed

The system shows Python is not installed. Follow these steps:

## Step 1: Install Python

### Windows:
1. Download Python from: https://www.python.org/downloads/
2. **IMPORTANT**: During installation, check "Add Python to PATH"
3. Install Python 3.8 or higher
4. Verify installation: Open new terminal and run `python --version`

### Alternative (if Python is installed but not in PATH):
- Use `py` command instead: `py ml_api_server.py`
- Or use full path to Python executable

## Step 2: Start the ML API Server

### Quick Start (Recommended):
```bash
# Windows
start_ml_api.bat

# Or manually:
python -m venv ml_api_env
ml_api_env\Scripts\activate
pip install -r requirements_ml_api.txt
python ml_api_server.py
```

### What You Should See:
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

## Step 3: Verify It's Working

1. Open browser: http://127.0.0.1:5000/health
2. Should return: `{"status":"healthy",...}`
3. Refresh Usage Overview page
4. You should see: ✅ **Using Python ML Linear Regression**

## Troubleshooting

### "Python was not found"
- Install Python from python.org
- Make sure to check "Add Python to PATH" during installation
- Restart terminal after installation

### "pip is not recognized"
- Use: `python -m pip install -r requirements_ml_api.txt`

### Port 5000 already in use
- Change port in `ml_api_server.py` (line ~189): `port = 5001`
- Update frontend `.env`: `VITE_PY_API_BASE_URL=http://127.0.0.1:5001`

### ModuleNotFoundError
- Make sure virtual environment is activated
- Run: `pip install -r requirements_ml_api.txt`

## Current Status

- ✅ Python ML API server files created (`ml_api_server.py`)
- ✅ Dependencies listed (`requirements_ml_api.txt`)
- ✅ Startup scripts created (`start_ml_api.bat`, `start_ml_api.sh`)
- ⚠️ **Python needs to be installed** on your system

Once Python is installed and the server is running, the system will automatically use Python ML Linear Regression instead of the Laravel fallback.

