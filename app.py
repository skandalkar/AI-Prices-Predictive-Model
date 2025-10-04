"""
Flask API for Agricultural Product Price Prediction
Provides REST endpoints for price prediction and serves the web portal
"""
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import joblib
import json
import numpy as np
import pandas as pd
import os

app = Flask(__name__)
CORS(app)

# Load model and encoders
MODEL_PATH = 'model/saved/price_prediction_model.pkl'
ENCODERS_PATH = 'model/saved/label_encoders.pkl'
FEATURES_PATH = 'model/saved/feature_columns.json'
METRICS_PATH = 'model/saved/model_metrics.json'

# Global variables for model
model = None
encoders = None
feature_columns = None
model_metrics = None

def load_model_components():
    """Load model, encoders, and configuration"""
    global model, encoders, feature_columns, model_metrics
    
    try:
        model = joblib.load(MODEL_PATH)
        encoders = joblib.load(ENCODERS_PATH)
        
        with open(FEATURES_PATH, 'r') as f:
            feature_columns = json.load(f)
        
        with open(METRICS_PATH, 'r') as f:
            model_metrics = json.load(f)
        
        print("Model components loaded successfully!")
        return True
    except Exception as e:
        print(f"Error loading model components: {e}")
        return False

@app.route('/')
def home():
    """Serve the main web portal"""
    return render_template('index.html')

@app.route('/api/products', methods=['GET'])
def get_products():
    """Get list of available products"""
    if encoders is None:
        return jsonify({'error': 'Model not loaded'}), 500
    
    products = encoders['product'].classes_.tolist()
    return jsonify({'products': products})

@app.route('/api/product-info/<product>', methods=['GET'])
def get_product_info(product):
    """Get information about a specific product"""
    if encoders is None:
        return jsonify({'error': 'Model not loaded'}), 500
    
    # Get category for the product
    try:
        categories = {
            'Wheat': 'Grain',
            'Rice': 'Grain',
            'Corn': 'Grain',
            'Tomato': 'Vegetable',
            'Potato': 'Vegetable',
            'Onion': 'Vegetable',
            'Cotton': 'Cash Crop',
            'Soybean': 'Oil Seed',
            'Sugarcane': 'Cash Crop',
            'Milk': 'Dairy'
        }
        
        return jsonify({
            'product': product,
            'category': categories.get(product, 'Unknown'),
            'available_qualities': encoders['quality'].classes_.tolist(),
            'available_regions': encoders['region'].classes_.tolist(),
            'available_seasons': encoders['season'].classes_.tolist()
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/predict', methods=['POST'])
def predict_price():
    """Predict price for agricultural product"""
    if model is None or encoders is None:
        return jsonify({'error': 'Model not loaded'}), 500
    
    try:
        data = request.json
        
        # Validate required fields
        required_fields = [
            'product', 'quality', 'quantity_kg', 'region', 
            'month', 'season', 'demand_index', 'supply_index',
            'rainfall_mm', 'temperature_celsius', 'transport_cost', 'storage_days'
        ]
        
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Get category for product
        categories = {
            'Wheat': 'Grain',
            'Rice': 'Grain',
            'Corn': 'Grain',
            'Tomato': 'Vegetable',
            'Potato': 'Vegetable',
            'Onion': 'Vegetable',
            'Cotton': 'Cash Crop',
            'Soybean': 'Oil Seed',
            'Sugarcane': 'Cash Crop',
            'Milk': 'Dairy'
        }
        category = categories.get(data['product'], 'Unknown')
        
        # Encode categorical variables
        try:
            product_encoded = encoders['product'].transform([data['product']])[0]
            category_encoded = encoders['category'].transform([category])[0]
            quality_encoded = encoders['quality'].transform([data['quality']])[0]
            region_encoded = encoders['region'].transform([data['region']])[0]
            season_encoded = encoders['season'].transform([data['season']])[0]
        except Exception as e:
            return jsonify({'error': f'Invalid categorical value: {str(e)}'}), 400
        
        # Create feature vector
        features = [
            product_encoded,
            category_encoded,
            quality_encoded,
            float(data['quantity_kg']),
            region_encoded,
            int(data['month']),
            season_encoded,
            float(data['demand_index']),
            float(data['supply_index']),
            float(data['rainfall_mm']),
            float(data['temperature_celsius']),
            float(data['transport_cost']),
            int(data['storage_days'])
        ]
        
        # Make prediction
        features_array = np.array([features])
        predicted_price = model.predict(features_array)[0]
        
        # Calculate confidence interval (based on model's MAE)
        mae = model_metrics.get('mae', 5.0)
        confidence_lower = max(0, predicted_price - mae)
        confidence_upper = predicted_price + mae
        
        # Calculate total price for the quantity
        total_price = predicted_price * float(data['quantity_kg'])
        
        response = {
            'predicted_price_per_kg': round(predicted_price, 2),
            'confidence_interval': {
                'lower': round(confidence_lower, 2),
                'upper': round(confidence_upper, 2)
            },
            'total_price': round(total_price, 2),
            'quantity_kg': float(data['quantity_kg']),
            'model_accuracy': {
                'mae': round(model_metrics.get('mae', 0), 2),
                'r2_score': round(model_metrics.get('r2_score', 0), 4)
            },
            'suggestion': generate_suggestion(predicted_price, data)
        }
        
        return jsonify(response)
    
    except Exception as e:
        return jsonify({'error': f'Prediction failed: {str(e)}'}), 500

def generate_suggestion(predicted_price, data):
    """Generate pricing suggestion for farmer"""
    demand = float(data['demand_index'])
    supply = float(data['supply_index'])
    quality = data['quality']
    
    suggestions = []
    
    # Demand-supply analysis
    if demand > supply * 1.5:
        suggestions.append("High demand detected! You can price slightly above the predicted value.")
    elif supply > demand * 1.5:
        suggestions.append("High supply in market. Consider competitive pricing near the predicted value.")
    else:
        suggestions.append("Market is balanced. Predicted price is optimal.")
    
    # Quality-based suggestion
    if quality == 'Premium':
        suggestions.append("Premium quality products can command 10-15% higher prices in the right market.")
    elif quality == 'Grade C':
        suggestions.append("Consider improving storage or processing to upgrade quality for better prices.")
    
    # Seasonal advice
    season = data['season']
    if season == 'Monsoon':
        suggestions.append("Monsoon season: Ensure proper storage to maintain quality.")
    
    return " ".join(suggestions)

@app.route('/api/model-info', methods=['GET'])
def get_model_info():
    """Get model performance metrics"""
    if model_metrics is None:
        return jsonify({'error': 'Model not loaded'}), 500
    
    return jsonify({
        'metrics': model_metrics,
        'status': 'active',
        'description': 'Random Forest Regressor trained on 5000+ agricultural product records'
    })

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'model_loaded': model is not None,
        'encoders_loaded': encoders is not None
    })

if __name__ == '__main__':
    print("Starting Agricultural Product Price Prediction API...")
    
    # Load model components
    if load_model_components():
        print("Model loaded successfully!")
    else:
        print("Warning: Model not loaded. Please train the model first by running:")
        print("  python data/generate_data.py")
        print("  python model/train_model.py")
    
    # Run Flask app
    app.run(debug=True, host='0.0.0.0', port=5000)
