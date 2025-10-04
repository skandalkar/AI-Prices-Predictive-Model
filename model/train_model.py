"""
Train machine learning model for agricultural product price prediction.
Uses Random Forest Regressor for accurate price predictions.
"""
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import joblib
import os
import json

def load_and_prepare_data(data_path):
    """Load and prepare data for training"""
    print("Loading data...")
    df = pd.read_csv(data_path)
    
    # Create label encoders
    encoders = {}
    categorical_columns = ['product', 'category', 'quality', 'region', 'season']
    
    for col in categorical_columns:
        encoders[col] = LabelEncoder()
        df[col + '_encoded'] = encoders[col].fit_transform(df[col])
    
    return df, encoders

def create_features(df):
    """Create feature matrix and target variable"""
    feature_columns = [
        'product_encoded', 'category_encoded', 'quality_encoded', 
        'quantity_kg', 'region_encoded', 'month', 'season_encoded',
        'demand_index', 'supply_index', 'rainfall_mm', 
        'temperature_celsius', 'transport_cost', 'storage_days'
    ]
    
    X = df[feature_columns]
    y = df['price_per_kg']
    
    return X, y, feature_columns

def train_model(X, y):
    """Train the price prediction model"""
    print("\nSplitting data into train and test sets...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    print(f"Training set size: {X_train.shape[0]}")
    print(f"Test set size: {X_test.shape[0]}")
    
    # Train Random Forest model
    print("\nTraining Random Forest model...")
    model = RandomForestRegressor(
        n_estimators=200,
        max_depth=20,
        min_samples_split=5,
        min_samples_leaf=2,
        random_state=42,
        n_jobs=-1
    )
    
    model.fit(X_train, y_train)
    
    # Make predictions
    y_pred_train = model.predict(X_train)
    y_pred_test = model.predict(X_test)
    
    # Evaluate model
    print("\n" + "="*50)
    print("MODEL PERFORMANCE")
    print("="*50)
    
    print("\nTraining Set:")
    print(f"MAE: ₹{mean_absolute_error(y_train, y_pred_train):.2f}")
    print(f"RMSE: ₹{np.sqrt(mean_squared_error(y_train, y_pred_train)):.2f}")
    print(f"R² Score: {r2_score(y_train, y_pred_train):.4f}")
    
    print("\nTest Set:")
    mae = mean_absolute_error(y_test, y_pred_test)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred_test))
    r2 = r2_score(y_test, y_pred_test)
    
    print(f"MAE: ₹{mae:.2f}")
    print(f"RMSE: ₹{rmse:.2f}")
    print(f"R² Score: {r2:.4f}")
    
    # Feature importance
    print("\nTop 10 Feature Importances:")
    feature_importance = pd.DataFrame({
        'feature': X.columns,
        'importance': model.feature_importances_
    }).sort_values('importance', ascending=False)
    print(feature_importance.head(10))
    
    metrics = {
        'mae': float(mae),
        'rmse': float(rmse),
        'r2_score': float(r2)
    }
    
    return model, metrics, X_test, y_test, y_pred_test

def save_model(model, encoders, feature_columns, metrics):
    """Save trained model and encoders"""
    print("\nSaving model and encoders...")
    
    os.makedirs('model/saved', exist_ok=True)
    
    # Save model
    joblib.dump(model, 'model/saved/price_prediction_model.pkl')
    print("Model saved to model/saved/price_prediction_model.pkl")
    
    # Save encoders
    joblib.dump(encoders, 'model/saved/label_encoders.pkl')
    print("Encoders saved to model/saved/label_encoders.pkl")
    
    # Save feature columns
    with open('model/saved/feature_columns.json', 'w') as f:
        json.dump(feature_columns, f)
    print("Feature columns saved to model/saved/feature_columns.json")
    
    # Save metrics
    with open('model/saved/model_metrics.json', 'w') as f:
        json.dump(metrics, f, indent=2)
    print("Metrics saved to model/saved/model_metrics.json")

def main():
    print("="*50)
    print("AGRICULTURAL PRODUCT PRICE PREDICTION MODEL")
    print("="*50)
    
    # Load and prepare data
    df, encoders = load_and_prepare_data('data/agricultural_products.csv')
    
    # Create features
    X, y, feature_columns = create_features(df)
    
    # Train model
    model, metrics, X_test, y_test, y_pred_test = train_model(X, y)
    
    # Save model
    save_model(model, encoders, feature_columns, metrics)
    
    print("\n" + "="*50)
    print("MODEL TRAINING COMPLETED SUCCESSFULLY!")
    print("="*50)
    
    # Example prediction
    print("\nExample prediction on test data:")
    sample_idx = 0
    print(f"Actual price: ₹{y_test.iloc[sample_idx]:.2f}")
    print(f"Predicted price: ₹{y_pred_test[sample_idx]:.2f}")

if __name__ == '__main__':
    main()
