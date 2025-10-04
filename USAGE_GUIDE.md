# 📖 Usage Guide

## Quick Start Guide for Farmers

### Step 1: Access the Portal
Open your web browser and go to: `http://localhost:5000`

### Step 2: Fill in Product Details

#### Basic Information
1. **Select Product**: Choose from the dropdown (e.g., Wheat, Rice, Tomato)
2. **Select Quality**: Choose the quality grade of your product
   - **Premium**: Highest quality, best appearance
   - **Grade A**: Very good quality
   - **Grade B**: Good quality, standard
   - **Grade C**: Acceptable quality

3. **Enter Quantity**: How many kilograms you want to sell

4. **Select Region**: Your geographical location (North, South, East, West, Central)

#### Market & Seasonal Information
5. **Month**: Current month (1=January, 12=December)
6. **Season**: Current season
   - **Winter**: December, January, February
   - **Summer**: March, April, May
   - **Monsoon**: June, July, August
   - **Autumn**: September, October, November

#### Market Conditions
7. **Demand Index** (1-10): How much demand is there for your product?
   - 1-3: Low demand
   - 4-6: Medium demand
   - 7-10: High demand
   
8. **Supply Index** (1-10): How much supply is available in the market?
   - 1-3: Low supply (scarce)
   - 4-6: Medium supply
   - 7-10: High supply (abundant)

#### Environmental Factors
9. **Rainfall (mm)**: Average monthly rainfall in your area
10. **Temperature (°C)**: Average temperature

#### Logistics
11. **Transport Cost (₹/kg)**: Cost to transport product to market
12. **Storage Days**: How long has the product been stored?

### Step 3: Get Price Prediction

Click the **"Predict Price"** button.

### Step 4: Review Results

You'll receive:

1. **Predicted Price per kg**: The AI-recommended price
2. **Price Range**: Confidence interval (minimum to maximum expected price)
3. **Total Price**: Total value for your quantity
4. **Model Accuracy**: How accurate the prediction is (MAE)
5. **Smart Suggestions**: AI-powered pricing advice

---

## Example Scenarios

### Scenario 1: Selling Premium Wheat
```
Product: Wheat
Quality: Premium
Quantity: 500 kg
Region: North
Month: October (10)
Season: Autumn
Demand: 7.5 (High)
Supply: 4.0 (Low-Medium)
Rainfall: 50 mm
Temperature: 25°C
Transport Cost: ₹3/kg
Storage: 5 days

Expected Result: Higher than base price due to premium quality and high demand
```

### Scenario 2: Selling Grade B Tomatoes
```
Product: Tomato
Quality: Grade B
Quantity: 100 kg
Region: South
Month: June (6)
Season: Monsoon
Demand: 5.0 (Medium)
Supply: 7.0 (High)
Rainfall: 200 mm
Temperature: 28°C
Transport Cost: ₹8/kg
Storage: 2 days

Expected Result: Lower price due to high supply and Grade B quality
```

---

## Tips for Best Results

### 1. Accurate Market Assessment
- Check local markets for current demand trends
- Talk to other farmers about supply levels
- Consider seasonal patterns

### 2. Quality Matters
- Better quality = higher prices
- Invest in proper storage to maintain quality
- Grade your products honestly

### 3. Timing is Key
- Sell when demand is high and supply is low
- Consider seasonal variations
- Minimize storage time to maintain freshness

### 4. Minimize Costs
- Optimize transport routes
- Group shipments with other farmers
- Use proper storage to reduce wastage

### 5. Use the Suggestions
- Read the AI-generated suggestions carefully
- They provide market-specific advice
- Consider multiple scenarios before deciding

---

## Understanding the Results

### Price Range
The system shows a range (e.g., ₹32.50 - ₹38.50). This means:
- **Lower bound**: Conservative estimate
- **Predicted price**: Most likely price
- **Upper bound**: Optimistic estimate

### Model Accuracy (MAE)
Mean Absolute Error shows typical prediction variance:
- MAE of ₹3.00 means predictions are typically within ±₹3 of actual prices
- Lower MAE = more accurate predictions

### R² Score
Shows overall model accuracy:
- 0.9394 (93.94%) means the model explains 93.94% of price variation
- Higher is better (maximum is 1.0 or 100%)

---

## Common Questions

### Q: Should I always sell at the predicted price?
A: The predicted price is a guideline. Consider:
- Your immediate need for cash
- Storage costs
- Product perishability
- Local market conditions

### Q: What if actual market prices differ?
A: The model provides estimates based on input factors. Actual prices may vary due to:
- Unforeseen market events
- Government policies
- Local competition
- Product appearance/condition

### Q: How often should I check prices?
A: Check prices:
- Before planning to sell
- After significant weather events
- During harvest seasons
- When market conditions change

### Q: Can I use this for price negotiation?
A: Yes! Use predictions to:
- Set a baseline for negotiations
- Justify your asking price
- Understand fair market value
- Avoid underpricing your products

---

## API Integration for Developers

If you're a developer integrating this system:

### Simple Python Example
```python
import requests

def get_price_prediction(product_data):
    response = requests.post(
        'http://localhost:5000/api/predict',
        json=product_data
    )
    return response.json()

# Example usage
data = {
    "product": "Wheat",
    "quality": "Grade A",
    "quantity_kg": 100,
    # ... other parameters
}

result = get_price_prediction(data)
print(f"Price: ₹{result['predicted_price_per_kg']}/kg")
```

See [API_DOCUMENTATION.md](API_DOCUMENTATION.md) for complete API details.

---

## Troubleshooting

### "Model not loaded" error
**Solution**: Make sure you've run:
```bash
python3 data/generate_data.py
python3 model/train_model.py
```

### Web page not loading
**Solution**: Check if Flask app is running:
```bash
python3 run.py
```

### Prediction seems wrong
**Check**:
1. All input values are realistic
2. Demand/supply indices are accurate
3. Quality grade matches product condition
4. Transport costs are reasonable

### Connection errors
**Solution**: Make sure the server is running on port 5000 and not blocked by firewall.

---

## Best Practices for Farmers

1. **Keep Records**: Track actual selling prices vs predictions
2. **Learn Patterns**: Understand seasonal trends for your products
3. **Network**: Share market information with other farmers
4. **Quality Control**: Maintain high standards for better prices
5. **Plan Ahead**: Use predictions for harvest planning
6. **Stay Informed**: Monitor local market conditions regularly

---

## Support & Feedback

For issues or suggestions:
- Report bugs on GitHub
- Request new features
- Share your experience
- Help improve the system

---

**Remember**: This is a decision support tool. Always use your judgment and local market knowledge when pricing your products.

**Good luck with your sales! 🌾**
