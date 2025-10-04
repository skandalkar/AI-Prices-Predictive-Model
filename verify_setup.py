"""
Verification script to check if all components are properly set up
"""
import os
import sys

def check_file_exists(filepath, description):
    """Check if a file exists and print result"""
    exists = os.path.exists(filepath)
    status = "✓" if exists else "✗"
    print(f"  {status} {description}: {filepath}")
    return exists

def check_directory_exists(dirpath, description):
    """Check if a directory exists and print result"""
    exists = os.path.isdir(dirpath)
    status = "✓" if exists else "✗"
    print(f"  {status} {description}: {dirpath}")
    return exists

def main():
    print("="*60)
    print("Agricultural Product Price Prediction - Setup Verification")
    print("="*60)
    
    results = []
    
    # Check directories
    print("\n1. Directory Structure:")
    results.append(check_directory_exists("data", "Data directory"))
    results.append(check_directory_exists("model", "Model directory"))
    results.append(check_directory_exists("model/saved", "Saved models directory"))
    results.append(check_directory_exists("templates", "Templates directory"))
    
    # Check core files
    print("\n2. Core Files:")
    results.append(check_file_exists("app.py", "Flask application"))
    results.append(check_file_exists("run.py", "Quick start script"))
    results.append(check_file_exists("requirements.txt", "Dependencies file"))
    
    # Check data files
    print("\n3. Data Files:")
    results.append(check_file_exists("data/generate_data.py", "Data generation script"))
    results.append(check_file_exists("data/agricultural_products.csv", "Training dataset"))
    
    # Check model files
    print("\n4. Model Files:")
    results.append(check_file_exists("model/train_model.py", "Model training script"))
    results.append(check_file_exists("model/saved/price_prediction_model.pkl", "Trained model"))
    results.append(check_file_exists("model/saved/label_encoders.pkl", "Label encoders"))
    results.append(check_file_exists("model/saved/feature_columns.json", "Feature configuration"))
    results.append(check_file_exists("model/saved/model_metrics.json", "Model metrics"))
    
    # Check frontend
    print("\n5. Frontend Files:")
    results.append(check_file_exists("templates/index.html", "Web interface"))
    
    # Check documentation
    print("\n6. Documentation:")
    results.append(check_file_exists("README.md", "Main documentation"))
    results.append(check_file_exists("API_DOCUMENTATION.md", "API documentation"))
    results.append(check_file_exists("USAGE_GUIDE.md", "Usage guide"))
    
    # Check test files
    print("\n7. Test Files:")
    results.append(check_file_exists("test_api.py", "API test script"))
    
    # Summary
    print("\n" + "="*60)
    print("Verification Summary")
    print("="*60)
    
    passed = sum(results)
    total = len(results)
    percentage = (passed / total) * 100
    
    print(f"Checks passed: {passed}/{total} ({percentage:.1f}%)")
    
    if passed == total:
        print("\n✓ All components are properly set up!")
        print("\nNext steps:")
        print("1. Install dependencies: pip install -r requirements.txt")
        print("2. Start the application: python3 run.py")
        print("3. Open browser to: http://localhost:5000")
        print("4. Run tests: python3 test_api.py")
        return 0
    else:
        print(f"\n✗ Setup incomplete: {total - passed} component(s) missing")
        print("\nTo complete setup:")
        print("1. Run: python3 data/generate_data.py")
        print("2. Run: python3 model/train_model.py")
        return 1

if __name__ == '__main__':
    sys.exit(main())
