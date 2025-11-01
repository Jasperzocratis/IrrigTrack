"""
Python ML API Server for Usage Forecasting
Provides Linear Regression forecasting for next quarter usage predictions
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from sklearn.linear_model import LinearRegression
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend requests

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'ML Forecast API',
        'version': '1.0.0',
        'endpoints': {
            'predict_consumables': '/predict/consumables/linear',
            'health': '/health'
        }
    })

@app.route('/predict/consumables/linear', methods=['POST'])
def predict_consumables():
    """
    Predict next quarter usage using Linear Regression
    
    Expected request format:
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
                        ...
                    }
                ],
                "forecast_features": {...},
                "current_stock": 150
            }
        ]
    }
    """
    try:
        data = request.json
        if not data or 'items' not in data:
            return jsonify({
                'success': False,
                'error': 'Invalid request format. Expected "items" array.'
            }), 400
        
        items = data.get('items', [])
        logger.info(f"Received forecast request for {len(items)} items")
        
        forecasts = []
        
        for item in items:
            item_id = item.get('item_id')
            name = item.get('name', f'Item {item_id}')
            historical_data = item.get('historical_data', [])
            forecast_features = item.get('forecast_features', {})
            current_stock = item.get('current_stock', 0)
            
            if not historical_data:
                logger.warning(f"No historical data for item {item_id}, using fallback")
                avg_usage = forecast_features.get('avg_usage_per_quarter', 0)
                forecasts.append({
                    'item_id': item_id,
                    'name': name,
                    'predicted_usage': round(avg_usage) if avg_usage else 0,
                    'confidence': 0.3,
                    'method': 'average_fallback'
                })
                continue
            
            # Extract usage values from historical data
            usage_values = []
            periods = []
            
            for idx, data_point in enumerate(historical_data):
                usage = data_point.get('usage', 0)
                if usage > 0:  # Only include non-zero usage
                    usage_values.append(usage)
                    periods.append(idx)
            
            # Need at least 2 data points for linear regression
            if len(usage_values) < 2:
                logger.warning(f"Insufficient data points ({len(usage_values)}) for item {item_id}")
                avg_usage = np.mean(usage_values) if usage_values else forecast_features.get('avg_usage_per_quarter', 0)
                forecasts.append({
                    'item_id': item_id,
                    'name': name,
                    'predicted_usage': round(avg_usage),
                    'confidence': 0.3,
                    'method': 'average'
                })
                continue
            
            # Prepare data for Linear Regression
            X = np.array(periods).reshape(-1, 1)  # Time periods (independent variable)
            y = np.array(usage_values)  # Usage values (dependent variable)
            
            # Train Linear Regression model
            model = LinearRegression()
            model.fit(X, y)
            
            # Predict next quarter (next period)
            next_period = len(periods)
            predicted_usage = model.predict([[next_period]])[0]
            predicted_usage = max(0, round(predicted_usage))  # Ensure non-negative
            
            # Calculate R-squared (coefficient of determination) for confidence
            y_pred = model.predict(X)
            ss_residual = np.sum((y - y_pred) ** 2)
            ss_total = np.sum((y - np.mean(y)) ** 2)
            
            if ss_total > 0:
                r_squared = 1 - (ss_residual / ss_total)
            else:
                r_squared = 0
            
            # Convert R-squared to confidence (clamp between 0.3 and 0.95)
            confidence = max(0.3, min(0.95, abs(r_squared)))
            
            # Calculate potential shortage date (optional)
            shortage_date = None
            if predicted_usage > 0 and current_stock > 0:
                # Estimate days until stock runs out
                # Assumes usage is distributed evenly over 90 days (1 quarter)
                daily_usage_rate = predicted_usage / 90
                if daily_usage_rate > 0:
                    days_until_shortage = current_stock / daily_usage_rate
                    if days_until_shortage < 180:  # Only show if within 6 months
                        shortage_date_obj = datetime.now() + timedelta(days=int(days_until_shortage))
                        shortage_date = shortage_date_obj.strftime('%B %Y')
            
            # Get model parameters
            slope = model.coef_[0] if len(model.coef_) > 0 else 0
            intercept = model.intercept_ if hasattr(model, 'intercept_') else 0
            
            forecasts.append({
                'item_id': item_id,
                'name': name,
                'predicted_usage': int(predicted_usage),
                'shortage_date': shortage_date,
                'confidence': round(confidence, 2),
                'r_squared': round(r_squared, 4),
                'slope': round(slope, 2),
                'intercept': round(intercept, 2),
                'data_points': len(usage_values),
                'method': 'linear_regression'
            })
            
            logger.info(f"Forecast for item {item_id} ({name}): {predicted_usage} units (confidence: {confidence:.2%})")
        
        logger.info(f"Successfully generated forecasts for {len(forecasts)} items")
        
        return jsonify({
            'success': True,
            'forecast': forecasts,
            'total_items': len(forecasts),
            'method': 'linear_regression'
        })
    
    except Exception as e:
        logger.error(f"Error generating forecasts: {str(e)}", exc_info=True)
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Failed to generate forecasts'
        }), 500

if __name__ == '__main__':
    host = '0.0.0.0'
    port = 5000
    
    print('=' * 60)
    print('🚀 Starting ML Forecast API Server')
    print('=' * 60)
    print(f'📊 Service: Linear Regression Forecasting')
    print(f'🌐 Listening on: http://{host}:{port}')
    print(f'✅ Health check: GET http://{host}:{port}/health')
    print(f'🔮 Forecast endpoint: POST http://{host}:{port}/predict/consumables/linear')
    print('=' * 60)
    print('Press Ctrl+C to stop the server')
    print()
    
    app.run(host=host, port=port, debug=True)

