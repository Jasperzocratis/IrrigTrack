# 🚀 Quick Start: Python ML API

## ✅ Current Status
- Python 3.13.5 is installed (use `py` command)
- Virtual environment created: `ml_api_env`
- Dependencies need to be installed

## 📋 Step-by-Step Instructions

### Option 1: Use the Batch Script (Easiest)
```bash
start_ml_api.bat
```

This script will:
1. ✅ Check Python installation
2. ✅ Create virtual environment (if needed)
3. ✅ Install dependencies
4. ✅ Start the ML API server

### Option 2: Manual Start

#### Step 1: Install Dependencies
```powershell
.\ml_api_env\Scripts\python.exe -m pip install -r requirements_ml_api.txt
```

#### Step 2: Start Server
```powershell
.\ml_api_env\Scripts\python.exe ml_api_server.py
```

### Option 3: Use `py` Command
```powershell
py -m venv ml_api_env
ml_api_env\Scripts\activate
py -m pip install -r requirements_ml_api.txt
py ml_api_server.py
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

Test in browser: http://127.0.0.1:5000/health

## 🎯 Next Steps

1. Keep the server running (don't close the terminal)
2. Refresh the Usage Overview page in your browser
3. You should see: **✅ Using Python ML Linear Regression** (instead of fallback)

## 🐛 Troubleshooting

### "Module not found" errors
- Make sure virtual environment is activated
- Reinstall: `.\ml_api_env\Scripts\python.exe -m pip install -r requirements_ml_api.txt`

### Port 5000 already in use
- Change port in `ml_api_server.py` (line ~189): `port = 5001`
- Update frontend `.env`: `VITE_PY_API_BASE_URL=http://127.0.0.1:5001`

### Still showing "Laravel Fallback"
- Check server is running: http://127.0.0.1:5000/health
- Check browser console (F12) for errors
- Verify `VITE_PY_API_BASE_URL` in frontend `.env`

