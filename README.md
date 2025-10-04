# 🌾 Agricultural Product Price Prediction System

An AI/ML-powered system that predicts prices for agricultural products and provides intelligent pricing suggestions to farmers.

## 🎯 Overview

This system uses machine learning (Random Forest Regressor) to predict agricultural product prices based on multiple factors including product quality, quantity, market demand/supply, weather conditions, regional variations, and more. It helps farmers make informed decisions when pricing their products for sale.

## ✨ Features

- **AI-Powered Price Prediction**: Uses Random Forest algorithm trained on 5000+ records
- **High Accuracy**: 93.94% R² score with Mean Absolute Error of ₹3.00
- **Multiple Products**: Supports 10 agricultural products (Wheat, Rice, Corn, Tomato, Potato, Onion, Cotton, Soybean, Sugarcane, Milk)
- **Smart Suggestions**: Provides contextual pricing recommendations based on market conditions
- **Beautiful Web Interface**: Modern, responsive web portal for farmers
- **REST API**: Complete API for integration with other systems
- **Real-time Predictions**: Instant price calculations based on current market data

## 📊 Supported Products

| Product | Category | Base Price Range |
|---------|----------|------------------|
| Wheat | Grain | ₹17-75/kg |
| Rice | Grain | ₹26-82/kg |
| Corn | Grain | ₹16-71/kg |
| Tomato | Vegetable | ₹19-79/kg |
| Potato | Vegetable | ₹14-67/kg |
| Onion | Vegetable | ₹17-86/kg |
| Cotton | Cash Crop | ₹41-149/kg |
| Soybean | Oil Seed | ₹26-115/kg |
| Sugarcane | Cash Crop | ₹4-20/kg |
| Milk | Dairy | ₹31-141/kg |

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd AI-Prices-Predictive-Model
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the setup script** (Linux/Mac)
   ```bash
   chmod +x setup.sh
   ./setup.sh
   ```

   Or manually run:
   ```bash
   python3 data/generate_data.py
   python3 model/train_model.py
   ```

4. **Start the application**
   ```bash
   python3 run.py
   ```

5. **Access the web portal**
   - Open your browser to: `http://localhost:5000`

## 📁 Project Structure

```
AI-Prices-Predictive-Model/
├── app.py                      # Flask API application
├── run.py                      # Quick start script
├── requirements.txt            # Python dependencies
├── setup.sh                    # Setup script
├── README.md                   # This file
├── API_DOCUMENTATION.md        # API documentation
├── data/
│   ├── generate_data.py        # Data generation script
│   └── agricultural_products.csv  # Generated dataset
├── model/
│   ├── train_model.py          # Model training script
│   └── saved/
│       ├── price_prediction_model.pkl  # Trained model
│       ├── label_encoders.pkl          # Feature encoders
│       ├── feature_columns.json        # Feature configuration
│       └── model_metrics.json          # Model performance metrics
└── templates/
    └── index.html              # Web portal interface
```

## 🧠 How It Works

### 1. Data Collection
The system considers 13 key factors for price prediction:
- Product type and category
- Quality grade (Premium, Grade A, Grade B, Grade C)
- Quantity in kilograms
- Geographic region
- Month and season
- Market demand index (1-10)
- Market supply index (1-10)
- Weather conditions (rainfall, temperature)
- Transport cost per kg
- Storage duration

### 2. Machine Learning Model
- **Algorithm**: Random Forest Regressor
- **Training Data**: 5000 synthetic records based on real market patterns
- **Features**: 13 input features with encoded categorical variables
- **Performance**:
  - R² Score: 0.9394 (93.94% accuracy)
  - Mean Absolute Error: ₹3.00
  - Root Mean Square Error: ₹4.54

### 3. Price Prediction
The model analyzes all input factors and:
1. Predicts the optimal price per kg
2. Provides a confidence interval (±MAE)
3. Calculates total price for the quantity
4. Generates smart pricing suggestions

### 4. Intelligent Suggestions
The system provides contextual advice based on:
- Demand-supply dynamics
- Product quality tier
- Seasonal variations
- Storage conditions

## 🌐 Web Portal Features

The farmer-friendly web interface includes:
- **Product Selection**: Choose from 10 agricultural products
- **Quality Grading**: Select product quality level
- **Market Information**: Input current demand/supply indices
- **Weather Data**: Enter rainfall and temperature
- **Logistics**: Specify transport costs and storage duration
- **Instant Results**: Get price predictions in real-time
- **Visual Feedback**: Beautiful, modern UI with clear price displays
- **Smart Suggestions**: Receive AI-powered pricing recommendations

## 🔌 API Usage

### Get Price Prediction

```bash
curl -X POST http://localhost:5000/api/predict \
  -H "Content-Type: application/json" \
  -d '{
    "product": "Wheat",
    "quality": "Grade A",
    "quantity_kg": 100,
    "region": "North",
    "month": 6,
    "season": "Monsoon",
    "demand_index": 7.5,
    "supply_index": 5.0,
    "rainfall_mm": 150.5,
    "temperature_celsius": 28.5,
    "transport_cost": 5.5,
    "storage_days": 10
  }'
```

For complete API documentation, see [API_DOCUMENTATION.md](API_DOCUMENTATION.md)

## 📈 Model Performance

### Training Results
- **Training Set R²**: 0.9858
- **Test Set R²**: 0.9394
- **Mean Absolute Error**: ₹3.00
- **Root Mean Square Error**: ₹4.54

### Feature Importance
Top factors affecting price predictions:
1. Product Type (37.8%)
2. Product Category (28.8%)
3. Supply Index (14.2%)
4. Demand Index (7.1%)
5. Transport Cost (4.5%)

## 🛠️ Technology Stack

- **Backend**: Flask (Python web framework)
- **ML Framework**: scikit-learn
- **Data Processing**: pandas, numpy
- **Model Persistence**: joblib
- **Frontend**: HTML5, CSS3, JavaScript
- **Styling**: Modern gradient design with responsive layout

## 🔄 Retraining the Model

To retrain the model with new data:

1. Update the data generation logic in `data/generate_data.py`
2. Run the data generation:
   ```bash
   python3 data/generate_data.py
   ```
3. Retrain the model:
   ```bash
   python3 model/train_model.py
   ```
4. Restart the Flask application

## 📝 Usage Example

### Python Client

```python
import requests

# Prepare product data
product_data = {
    "product": "Tomato",
    "quality": "Premium",
    "quantity_kg": 50,
    "region": "South",
    "month": 3,
    "season": "Summer",
    "demand_index": 8.0,
    "supply_index": 4.0,
    "rainfall_mm": 50.0,
    "temperature_celsius": 32.0,
    "transport_cost": 8.0,
    "storage_days": 2
}

# Get prediction
response = requests.post(
    'http://localhost:5000/api/predict',
    json=product_data
)

result = response.json()
print(f"Predicted Price: ₹{result['predicted_price_per_kg']}/kg")
print(f"Total Price: ₹{result['total_price']}")
print(f"Suggestion: {result['suggestion']}")
```

## 🎓 Use Cases

1. **Farmers**: Get fair price estimates before selling products
2. **Agricultural Cooperatives**: Standardize pricing across members
3. **Marketplace Platforms**: Provide price guidance to sellers
4. **Government Agencies**: Monitor and regulate agricultural prices
5. **Research**: Study price patterns and market dynamics

## 🤝 Contributing

Contributions are welcome! Areas for improvement:
- Add more agricultural products
- Integrate real-time market data APIs
- Implement historical price tracking
- Add mobile app interface
- Enhance ML model with deep learning
- Multi-language support

## 📄 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

- Dataset inspired by real agricultural market patterns
- Built with modern web technologies and ML best practices
- Designed with farmers' needs in mind

## 📞 Support

For issues, questions, or suggestions, please open an issue on GitHub.

---

**Made with ❤️ for farmers** 
