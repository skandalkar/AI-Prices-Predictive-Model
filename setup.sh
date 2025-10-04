#!/bin/bash
# Setup script for Agricultural Product Price Prediction System

echo "========================================"
echo "Agricultural Price Prediction Setup"
echo "========================================"
echo ""

# Create necessary directories
echo "Creating directories..."
mkdir -p data
mkdir -p model/saved
mkdir -p templates

# Install dependencies
echo ""
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Generate dataset
echo ""
echo "Generating agricultural product dataset..."
python data/generate_data.py

# Train model
echo ""
echo "Training machine learning model..."
python model/train_model.py

echo ""
echo "========================================"
echo "Setup completed successfully!"
echo "========================================"
echo ""
echo "To start the application, run:"
echo "  python app.py"
echo ""
echo "Then open your browser to: http://localhost:5000"
echo ""
