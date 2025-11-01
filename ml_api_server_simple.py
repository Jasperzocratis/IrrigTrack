"""
Python ML API Server for Usage Forecasting
Provides Linear Regression forecasting using NumPy only (no scikit-learn)
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
from datetime import datetime, timedelta
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend requests

def linear_regression(X, y):
    """
    Simple Linear Regression implementation using NumPy
    Returns: slope (m), intercept (b), r_squared
    Formula: y = mx + b
    """
    n = len(X)
    if n < 2:
        return 0, np.mean(y) if len(y) > 0 else 0, 0
    
    X = np.array(X).flatten()
    y = np.array(y).flatten()
    
    # Calculate means
    X_mean = np.mean(X)
    y_mean = np.mean(y)
    
    # Calculate slope (m) and intercept (b)
    numerator = np.sum((X - X_mean) * (y - y_mean))
    denominator = np.sum((X - X_mean) ** 2)
    
    if denominator == 0:
        return 0, y_mean, 0
    
    slope = numerator / denominator
    intercept = y_mean - slope * X_mean
    
    # Calculate R-squared
    y_pred = slope * X + intercept
    ss_residual = np.sum((y - y_pred) ** 2)
    ss_total = np.sum((y - y_mean) ** 2)
    
    r_squared = 1 - (ss_residual / ss_total) if ss_total > 0 else 0
    
    return slope, intercept, r_squared

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'ML Forecast API (NumPy Linear Regression)',
        'version': '1.0.0',
        'endpoints': {
            'predict_consumables': '/predict/consumables/linear',
            'health': '/health'
        }
    })

@app.route('/predict/consumables/linear', methods=['POST'])
def predict_consumables():
    """
    Predict next quarter usage using Linear Regression (NumPy implementation)
    
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
                "current_stock": 100
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
            X = np.array(periods)  # Time periods (independent variable)
            y = np.array(usage_values)  # Usage values (dependent variable)
            
            # Train Linear Regression model (using our NumPy implementation)
            slope, intercept, r_squared = linear_regression(X, y)
            
            # Predict next quarter (next period)
            next_period = len(periods)
            predicted_usage = slope * next_period + intercept
            predicted_usage = max(0, round(predicted_usage))  # Ensure non-negative
            
            # Convert R-squared to confidence (clamp between 0.3 and 0.95)
            confidence = max(0.3, min(0.95, abs(r_squared)))
            
            # Estimate shortage date if applicable
            shortage_date = None
            if predicted_usage > 0 and current_stock > 0:
                daily_usage_rate = predicted_usage / 90  # Assuming 90 days per quarter
                if daily_usage_rate > 0:
                    days_until_shortage = current_stock / daily_usage_rate
                    if days_until_shortage < 180:  # Only show if within 6 months
                        shortage_date_obj = datetime.now() + timedelta(days=int(days_until_shortage))
                        shortage_date = shortage_date_obj.strftime('%B %Y')
            
            forecasts.append({
                'item_id': item_id,
                'name': name,
                'predicted_usage': int(predicted_usage),
                'shortage_date': shortage_date,
                'confidence': round(confidence, 3),
                'r_squared': round(r_squared, 3),
                'slope': round(slope, 3),
                'intercept': round(intercept, 3),
                'data_points': len(usage_values),
                'method': 'linear_regression'
            })
            
            logger.info(f"Forecast for {name}: {predicted_usage} units (confidence: {confidence:.2f})")
        
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
    
    logger.info("=" * 60)
    logger.info("🚀 Starting ML Forecast API Server")
    logger.info("=" * 60)
    logger.info(f"📊 Service: Linear Regression Forecasting (NumPy)")
    logger.info(f"🌐 Listening on: http://{host}:{port}")
    logger.info(f"✅ Health check: GET http://{host}:{port}/health")
    logger.info(f"🔮 Forecast endpoint: POST http://{host}:{port}/predict/consumables/linear")
    logger.info("=" * 60)
    
    app.run(host=host, port=port, debug=True)

