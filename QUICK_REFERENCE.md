# ⚡ Quick Reference Card

## 🚀 Getting Started (3 Steps)

```bash
# 1. Install
pip install -r requirements.txt

# 2. Run
python3 run.py

# 3. Open
http://localhost:5000
```

---

## 📡 API Endpoints

### Base URL
```
http://localhost:5000
```

### Endpoints Summary

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Web portal |
| GET | `/health` | Health check |
| GET | `/api/products` | List all products |
| GET | `/api/product-info/<product>` | Product details |
| POST | `/api/predict` | Get price prediction |
| GET | `/api/model-info` | Model metrics |

---

## 🔌 Quick API Examples

### cURL
```bash
curl -X POST http://localhost:5000/api/predict \
  -H "Content-Type: application/json" \
  -d '{"product":"Wheat","quality":"Grade A","quantity_kg":100,"region":"North","month":6,"season":"Monsoon","demand_index":7.5,"supply_index":5.0,"rainfall_mm":150.5,"temperature_celsius":28.5,"transport_cost":5.5,"storage_days":10}'
```

### Python
```python
import requests
response = requests.post('http://localhost:5000/api/predict', json={
    "product": "Wheat", "quality": "Grade A", "quantity_kg": 100,
    "region": "North", "month": 6, "season": "Monsoon",
    "demand_index": 7.5, "supply_index": 5.0,
    "rainfall_mm": 150.5, "temperature_celsius": 28.5,
    "transport_cost": 5.5, "storage_days": 10
})
print(response.json())
```

---

## 📊 Input Parameters

| Parameter | Type | Range | Required |
|-----------|------|-------|----------|
| product | string | See list below | ✅ |
| quality | string | Premium/A/B/C | ✅ |
| quantity_kg | number | > 0 | ✅ |
| region | string | N/S/E/W/Central | ✅ |
| month | integer | 1-12 | ✅ |
| season | string | See list below | ✅ |
| demand_index | number | 1-10 | ✅ |
| supply_index | number | 1-10 | ✅ |
| rainfall_mm | number | 0-500 | ✅ |
| temperature_celsius | number | 0-50 | ✅ |
| transport_cost | number | 0-50 | ✅ |
| storage_days | integer | 0-90 | ✅ |

### Products
`Wheat, Rice, Corn, Tomato, Potato, Onion, Cotton, Soybean, Sugarcane, Milk`

### Quality Grades
`Premium, Grade A, Grade B, Grade C`

### Regions
`North, South, East, West, Central`

### Seasons
`Winter, Summer, Monsoon, Autumn`

---

## 📤 Response Format

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
  "suggestion": "Market is balanced. Predicted price is optimal."
}
```

---

## 🛠️ Common Commands

### Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Make setup script executable
chmod +x setup.sh

# Run setup
./setup.sh
```

### Generate Data
```bash
python3 data/generate_data.py
```

### Train Model
```bash
python3 model/train_model.py
```

### Start Server
```bash
# Development
python3 run.py

# Production
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Test
```bash
# Verify setup
python3 verify_setup.py

# Test API
python3 test_api.py
```

---

## 📈 Model Stats

- **Accuracy**: 93.94% (R² Score: 0.9394)
- **MAE**: ±₹3.00
- **Training Data**: 5,000 records
- **Products**: 10 types
- **Features**: 13 inputs

---

## 🔍 Troubleshooting

| Problem | Solution |
|---------|----------|
| Model not loaded | Run `python3 model/train_model.py` |
| Port in use | Change port in `app.py` |
| Import errors | Run `pip install -r requirements.txt` |
| Connection refused | Check if server is running |

---

## 📁 File Structure

```
├── app.py                 # Main Flask application
├── run.py                 # Quick start script
├── requirements.txt       # Dependencies
├── data/
│   ├── generate_data.py   # Data generation
│   └── agricultural_products.csv
├── model/
│   ├── train_model.py     # Model training
│   └── saved/             # Trained models
├── templates/
│   └── index.html         # Web interface
└── *.md                   # Documentation
```

---

## 💰 Price Ranges (₹/kg)

| Product | Min | Max | Avg |
|---------|-----|-----|-----|
| Wheat | 18 | 75 | 35 |
| Rice | 26 | 82 | 44 |
| Corn | 16 | 71 | 31 |
| Tomato | 19 | 79 | 40 |
| Potato | 15 | 67 | 30 |
| Onion | 18 | 86 | 36 |
| Cotton | 42 | 149 | 71 |
| Soybean | 27 | 115 | 49 |
| Sugarcane | 4 | 20 | 11 |
| Milk | 31 | 141 | 55 |

---

## 📚 Documentation Files

- `README.md` - Complete documentation
- `API_DOCUMENTATION.md` - API reference
- `USAGE_GUIDE.md` - User guide for farmers
- `PROJECT_SUMMARY.md` - Project overview
- `QUICK_REFERENCE.md` - This file

---

## ⚙️ Environment Variables (Optional)

```bash
export FLASK_ENV=development
export FLASK_APP=app.py
export FLASK_RUN_PORT=5000
```

---

## 🔗 Useful URLs

- Web Portal: `http://localhost:5000`
- Health Check: `http://localhost:5000/health`
- API Base: `http://localhost:5000/api`
- Model Info: `http://localhost:5000/api/model-info`

---

## 📞 Support

- Check documentation in `*.md` files
- Run `python3 verify_setup.py` to diagnose issues
- Review error logs in console output

---

**Quick Tip**: Bookmark this page for fast reference! 📌
