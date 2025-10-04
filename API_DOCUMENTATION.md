# API Documentation

## Agricultural Product Price Prediction API

Base URL: `http://localhost:5000`

---

## Endpoints

### 1. Get Available Products

**GET** `/api/products`

Returns a list of all available agricultural products in the system.

**Response:**
```json
{
  "products": ["Wheat", "Rice", "Corn", "Tomato", "Potato", "Onion", "Cotton", "Soybean", "Sugarcane", "Milk"]
}
```

---

### 2. Get Product Information

**GET** `/api/product-info/<product>`

Returns detailed information about a specific product.

**Parameters:**
- `product` (path parameter): Name of the product

**Response:**
```json
{
  "product": "Wheat",
  "category": "Grain",
  "available_qualities": ["Premium", "Grade A", "Grade B", "Grade C"],
  "available_regions": ["North", "South", "East", "West", "Central"],
  "available_seasons": ["Winter", "Summer", "Monsoon", "Autumn"]
}
```

---

### 3. Predict Price

**POST** `/api/predict`

Predicts the price for an agricultural product based on various factors.

**Request Body:**
```json
{
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
}
```

**Field Descriptions:**

| Field | Type | Range | Description |
|-------|------|-------|-------------|
| product | string | - | Agricultural product name |
| quality | string | - | Quality grade: "Premium", "Grade A", "Grade B", or "Grade C" |
| quantity_kg | number | > 0 | Quantity in kilograms |
| region | string | - | Region: "North", "South", "East", "West", or "Central" |
| month | integer | 1-12 | Month of sale (1=January, 12=December) |
| season | string | - | Season: "Winter", "Summer", "Monsoon", or "Autumn" |
| demand_index | number | 1-10 | Market demand level (1=Low, 10=High) |
| supply_index | number | 1-10 | Market supply level (1=Low, 10=High) |
| rainfall_mm | number | 0-500 | Average monthly rainfall in millimeters |
| temperature_celsius | number | 0-50 | Average temperature in Celsius |
| transport_cost | number | 0-50 | Transport cost per kg |
| storage_days | integer | 0-90 | Number of days in storage |

**Response:**
```json
{
  "predicted_price_per_kg": 35.50,
  "confidence_interval": {
    "lower": 32.50,
    "upper": 38.50
  },
  "total_price": 3550.00,
  "quantity_kg": 100,
  "model_accuracy": {
    "mae": 3.00,
    "r2_score": 0.9394
  },
  "suggestion": "Market is balanced. Predicted price is optimal. Consider improving storage or processing to upgrade quality for better prices."
}
```

---

### 4. Get Model Information

**GET** `/api/model-info`

Returns information about the ML model's performance metrics.

**Response:**
```json
{
  "metrics": {
    "mae": 3.00,
    "rmse": 4.54,
    "r2_score": 0.9394
  },
  "status": "active",
  "description": "Random Forest Regressor trained on 5000+ agricultural product records"
}
```

---

### 5. Health Check

**GET** `/health`

Checks if the API is running and if the model is loaded.

**Response:**
```json
{
  "status": "healthy",
  "model_loaded": true,
  "encoders_loaded": true
}
```

---

## Error Responses

All endpoints return appropriate HTTP status codes and error messages:

**400 Bad Request:**
```json
{
  "error": "Missing required field: product"
}
```

**500 Internal Server Error:**
```json
{
  "error": "Model not loaded"
}
```

---

## Example Usage

### Python
```python
import requests

url = "http://localhost:5000/api/predict"
data = {
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
}

response = requests.post(url, json=data)
result = response.json()
print(f"Predicted Price: ₹{result['predicted_price_per_kg']}/kg")
```

### cURL
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

### JavaScript (Fetch API)
```javascript
const data = {
  product: "Wheat",
  quality: "Grade A",
  quantity_kg: 100,
  region: "North",
  month: 6,
  season: "Monsoon",
  demand_index: 7.5,
  supply_index: 5.0,
  rainfall_mm: 150.5,
  temperature_celsius: 28.5,
  transport_cost: 5.5,
  storage_days: 10
};

fetch('http://localhost:5000/api/predict', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify(data)
})
.then(response => response.json())
.then(result => {
  console.log(`Predicted Price: ₹${result.predicted_price_per_kg}/kg`);
});
```

---

## Rate Limiting

Currently, there are no rate limits on the API. For production use, consider implementing rate limiting.

---

## CORS

CORS is enabled for all origins in development mode. For production, configure appropriate CORS settings in `app.py`.
