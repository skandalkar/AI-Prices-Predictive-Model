"""
Test script for Agricultural Product Price Prediction API
Tests all API endpoints to ensure system is working correctly
"""
import requests
import json
import sys

BASE_URL = 'http://localhost:5000'

def test_health_check():
    """Test health check endpoint"""
    print("\n1. Testing Health Check...")
    try:
        response = requests.get(f'{BASE_URL}/health', timeout=5)
        data = response.json()
        print(f"   Status: {response.status_code}")
        print(f"   Response: {json.dumps(data, indent=2)}")
        assert response.status_code == 200
        assert data['status'] == 'healthy'
        print("   ✓ Health check passed")
        return True
    except requests.exceptions.ConnectionError:
        print("   ✗ Connection error - make sure Flask app is running")
        return False
    except Exception as e:
        print(f"   ✗ Health check failed: {e}")
        return False

def test_get_products():
    """Test get products endpoint"""
    print("\n2. Testing Get Products...")
    try:
        response = requests.get(f'{BASE_URL}/api/products', timeout=5)
        data = response.json()
        print(f"   Status: {response.status_code}")
        print(f"   Products: {', '.join(data['products'])}")
        assert response.status_code == 200
        assert len(data['products']) > 0
        print("   ✓ Get products passed")
        return True
    except Exception as e:
        print(f"   ✗ Get products failed: {e}")
        return False

def test_get_product_info():
    """Test get product info endpoint"""
    print("\n3. Testing Get Product Info...")
    try:
        response = requests.get(f'{BASE_URL}/api/product-info/Wheat', timeout=5)
        data = response.json()
        print(f"   Status: {response.status_code}")
        print(f"   Product: {data['product']}")
        print(f"   Category: {data['category']}")
        assert response.status_code == 200
        assert data['product'] == 'Wheat'
        print("   ✓ Get product info passed")
        return True
    except Exception as e:
        print(f"   ✗ Get product info failed: {e}")
        return False

def test_model_info():
    """Test model info endpoint"""
    print("\n4. Testing Get Model Info...")
    try:
        response = requests.get(f'{BASE_URL}/api/model-info', timeout=5)
        data = response.json()
        print(f"   Status: {response.status_code}")
        print(f"   MAE: ₹{data['metrics']['mae']}")
        print(f"   R² Score: {data['metrics']['r2_score']}")
        assert response.status_code == 200
        assert 'metrics' in data
        print("   ✓ Get model info passed")
        return True
    except Exception as e:
        print(f"   ✗ Get model info failed: {e}")
        return False

def test_predict_price():
    """Test price prediction endpoint"""
    print("\n5. Testing Price Prediction...")
    
    test_data = {
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
    
    try:
        response = requests.post(
            f'{BASE_URL}/api/predict',
            json=test_data,
            timeout=5
        )
        data = response.json()
        print(f"   Status: {response.status_code}")
        print(f"   Predicted Price: ₹{data['predicted_price_per_kg']}/kg")
        print(f"   Total Price: ₹{data['total_price']}")
        print(f"   Confidence Range: ₹{data['confidence_interval']['lower']} - ₹{data['confidence_interval']['upper']}")
        print(f"   Suggestion: {data['suggestion'][:80]}...")
        assert response.status_code == 200
        assert 'predicted_price_per_kg' in data
        assert data['predicted_price_per_kg'] > 0
        print("   ✓ Price prediction passed")
        return True
    except Exception as e:
        print(f"   ✗ Price prediction failed: {e}")
        return False

def test_multiple_products():
    """Test predictions for multiple products"""
    print("\n6. Testing Multiple Product Predictions...")
    
    products = [
        {"product": "Rice", "quality": "Premium", "quantity_kg": 50},
        {"product": "Tomato", "quality": "Grade A", "quantity_kg": 25},
        {"product": "Milk", "quality": "Premium", "quantity_kg": 100}
    ]
    
    try:
        for prod in products:
            test_data = {
                "product": prod["product"],
                "quality": prod["quality"],
                "quantity_kg": prod["quantity_kg"],
                "region": "South",
                "month": 3,
                "season": "Summer",
                "demand_index": 6.0,
                "supply_index": 5.0,
                "rainfall_mm": 100.0,
                "temperature_celsius": 30.0,
                "transport_cost": 5.0,
                "storage_days": 5
            }
            
            response = requests.post(
                f'{BASE_URL}/api/predict',
                json=test_data,
                timeout=5
            )
            data = response.json()
            print(f"   {prod['product']}: ₹{data['predicted_price_per_kg']}/kg (Total: ₹{data['total_price']})")
        
        print("   ✓ Multiple product predictions passed")
        return True
    except Exception as e:
        print(f"   ✗ Multiple product predictions failed: {e}")
        return False

def main():
    """Run all tests"""
    print("="*60)
    print("Agricultural Product Price Prediction API Tests")
    print("="*60)
    
    tests = [
        test_health_check,
        test_get_products,
        test_get_product_info,
        test_model_info,
        test_predict_price,
        test_multiple_products
    ]
    
    results = []
    for test in tests:
        results.append(test())
    
    print("\n" + "="*60)
    print("Test Summary")
    print("="*60)
    passed = sum(results)
    total = len(results)
    print(f"Passed: {passed}/{total}")
    
    if passed == total:
        print("✓ All tests passed!")
        sys.exit(0)
    else:
        print(f"✗ {total - passed} test(s) failed")
        sys.exit(1)

if __name__ == '__main__':
    main()
