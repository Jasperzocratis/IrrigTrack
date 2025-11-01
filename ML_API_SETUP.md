# Python ML API Setup Guide

This guide explains how to set up the Python ML API for **Linear Regression forecasting** in the Usage Overview dashboard.

## ✅ Required: Python ML API for Linear Regression

The forecast feature **requires** the Python ML API for accurate Linear Regression predictions. The system will automatically use it when available.

## Quick Start

If you want to use machine learning predictions instead of statistical estimates, follow these steps:

### 1. Quick Start (Windows)

Simply run:
```bash
start_ml_api.bat
```

### 2. Quick Start (Linux/Mac)

Make the script executable and run:
```bash
chmod +x start_ml_api.sh
./start_ml_api.sh
```

### 3. Manual Setup

If you prefer manual setup:

See `ml_api_server.py` in the project root for the complete implementation.

### Install Dependencies

```bash
# Create virtual environment
python -m venv ml_api_env

# Activate virtual environment
# Windows:
ml_api_env\Scripts\activate
# Linux/Mac:
source ml_api_env/bin/activate

# Install required packages
pip install -r requirements_ml_api.txt
```

### Run the ML API Server

```bash
python ml_api_server.py
```

You should see:
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

### 4. Configure Frontend

Make sure your `frontend-vue/.env` file includes:

```env
VITE_PY_API_BASE_URL=http://127.0.0.1:5000
```

### 5. Test the Connection

1. Open the Usage Overview page
2. Click "Generate Forecast"
3. Check browser console (F12) for connection status
4. The forecast should show "ML" badges instead of "Stats" badges

## API Endpoint Specification

### Request Format

**POST** `/predict/consumables/linear`

```json
{
  "items": [
    {
      "item_id": 1,
      "name": "Paper",
      "historical_data": [
        {
          "period": "Q1 2024",
          "timestamp": "2024-01-01",
          "usage": 50,
          "restock_qty": 100,
          "restocked": 1,
          "stock_start": 200,
          "stock_end": 250,
          "net_change": 50
        }
      ],
      "forecast_features": {
        "avg_usage_per_quarter": 45.5,
        "trend": "increasing",
        "volatility": 15.2,
        "restock_frequency": 0.75,
        "current_stock": 150,
        "last_usage": 60,
        "usage_growth_rate": 2.5
      },
      "current_stock": 150
    }
  ]
}
```

### Response Format

```json
{
  "success": true,
  "forecast": [
    {
      "item_id": 1,
      "name": "Paper",
      "predicted_usage": 65,
      "shortage_date": "March 2025",
      "confidence": 0.82,
      "method": "ml"
    }
  ],
  "total_items": 1
}
```

## Statistical Estimates vs ML Predictions

### Statistical Estimates (Current Default)
- ✅ Works immediately, no setup required
- ✅ Fast and reliable
- ✅ Uses historical patterns and trends
- ⚠️ Less sophisticated than ML

### ML Predictions (Optional)
- ✅ More accurate for complex patterns
- ✅ Handles non-linear trends better
- ✅ Can learn from more data points
- ⚠️ Requires Python service running
- ⚠️ Needs sufficient historical data

## Troubleshooting

### "Cannot connect to ML API"
- Ensure Python service is running: `python ml_api_server.py`
- Check if port 5000 is available: `netstat -an | findstr 5000` (Windows) or `lsof -i :5000` (Linux/Mac)
- Verify `VITE_PY_API_BASE_URL` in `.env` file
- Check firewall settings

### "ML API response format invalid"
- Check browser console for actual response
- Verify the Python API returns the expected JSON format
- Ensure `forecast` array is included in response

### Statistical Estimates Are Fine!
Remember: The system works perfectly with statistical estimates. The ML API is optional for enhanced accuracy. The current implementation provides reliable forecasts based on historical analysis.

## Support

If you need help:
1. Check browser console (F12) for detailed error messages
2. Verify the ML API is responding: `curl http://127.0.0.1:5000/health`
3. Review the Python server logs for errors

