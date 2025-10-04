"""
Quick start script to run the Agricultural Product Price Prediction system.
This script checks if the model is trained, and if not, trains it automatically.
"""
import os
import subprocess
import sys

def check_model_exists():
    """Check if trained model exists"""
    return os.path.exists('model/saved/price_prediction_model.pkl')

def check_data_exists():
    """Check if dataset exists"""
    return os.path.exists('data/agricultural_products.csv')

def main():
    print("="*60)
    print("Agricultural Product Price Prediction System")
    print("="*60)
    print()
    
    # Check if data exists
    if not check_data_exists():
        print("Dataset not found. Generating sample data...")
        try:
            subprocess.run([sys.executable, 'data/generate_data.py'], check=True)
            print("✓ Dataset generated successfully!")
        except subprocess.CalledProcessError as e:
            print(f"✗ Error generating data: {e}")
            return
        print()
    else:
        print("✓ Dataset found")
    
    # Check if model exists
    if not check_model_exists():
        print("Trained model not found. Training model...")
        print("This may take a few minutes...")
        try:
            subprocess.run([sys.executable, 'model/train_model.py'], check=True)
            print("✓ Model trained successfully!")
        except subprocess.CalledProcessError as e:
            print(f"✗ Error training model: {e}")
            return
        print()
    else:
        print("✓ Trained model found")
    
    print()
    print("="*60)
    print("Starting Flask application...")
    print("="*60)
    print()
    print("Open your browser to: http://localhost:5000")
    print("Press Ctrl+C to stop the server")
    print()
    
    # Run Flask app
    try:
        subprocess.run([sys.executable, 'app.py'])
    except KeyboardInterrupt:
        print("\n\nServer stopped.")

if __name__ == '__main__':
    main()
