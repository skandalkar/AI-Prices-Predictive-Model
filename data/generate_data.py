"""
Generate synthetic agricultural product data for training the price prediction model.
This script creates realistic data based on various factors affecting agricultural prices.
"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

# Set random seed for reproducibility
np.random.seed(42)

# Define agricultural products
products = ['Wheat', 'Rice', 'Corn', 'Tomato', 'Potato', 'Onion', 'Cotton', 'Soybean', 'Sugarcane', 'Milk']

# Define product categories
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

# Define quality grades
quality_grades = ['Premium', 'Grade A', 'Grade B', 'Grade C']

# Define regions
regions = ['North', 'South', 'East', 'West', 'Central']

# Base prices for each product (per kg)
base_prices = {
    'Wheat': 25,
    'Rice': 35,
    'Corn': 22,
    'Tomato': 30,
    'Potato': 20,
    'Onion': 25,
    'Cotton': 60,
    'Soybean': 40,
    'Sugarcane': 3,
    'Milk': 45
}

def generate_dataset(n_samples=5000):
    """Generate synthetic agricultural product dataset"""
    
    data = []
    start_date = datetime(2020, 1, 1)
    
    for i in range(n_samples):
        # Random product
        product = np.random.choice(products)
        category = categories[product]
        
        # Random date in last 4 years
        date = start_date + timedelta(days=np.random.randint(0, 1460))
        month = date.month
        season = 'Winter' if month in [12, 1, 2] else 'Summer' if month in [3, 4, 5] else 'Monsoon' if month in [6, 7, 8] else 'Autumn'
        
        # Quality and quantity
        quality = np.random.choice(quality_grades, p=[0.15, 0.35, 0.35, 0.15])
        quantity = np.random.uniform(10, 1000)  # kg
        
        # Location
        region = np.random.choice(regions)
        
        # Market demand and supply (1-10 scale)
        demand = np.random.uniform(1, 10)
        supply = np.random.uniform(1, 10)
        
        # Weather conditions
        rainfall = np.random.uniform(0, 300)  # mm
        temperature = np.random.uniform(10, 45)  # celsius
        
        # Market factors
        transport_cost = np.random.uniform(2, 15)  # per kg
        storage_days = np.random.randint(0, 30)
        
        # Calculate price with various factors
        base_price = base_prices[product]
        
        # Quality multiplier
        quality_mult = {'Premium': 1.3, 'Grade A': 1.1, 'Grade B': 1.0, 'Grade C': 0.85}[quality]
        
        # Seasonal variation
        seasonal_mult = 1.0
        if product in ['Tomato', 'Potato', 'Onion']:
            seasonal_mult = 1.2 if season in ['Winter', 'Summer'] else 0.9
        
        # Demand-supply ratio effect
        demand_supply_ratio = demand / (supply + 0.1)
        demand_effect = 0.8 + (demand_supply_ratio / 5)  # varies from 0.8 to 1.8
        
        # Region effect (some regions have higher prices)
        region_mult = {'North': 1.05, 'South': 0.95, 'East': 1.0, 'West': 1.1, 'Central': 0.98}[region]
        
        # Quantity discount (bulk orders get slight discount)
        quantity_mult = 1.0 if quantity < 100 else 0.98 if quantity < 500 else 0.95
        
        # Storage degradation
        storage_mult = 1.0 - (storage_days * 0.005)
        
        # Calculate final price
        price = base_price * quality_mult * seasonal_mult * demand_effect * region_mult * quantity_mult * storage_mult
        
        # Add transport cost
        price += transport_cost
        
        # Add some random noise
        price *= np.random.uniform(0.95, 1.05)
        
        # Round to 2 decimal places
        price = round(price, 2)
        
        data.append({
            'product': product,
            'category': category,
            'quality': quality,
            'quantity_kg': round(quantity, 2),
            'region': region,
            'month': month,
            'season': season,
            'demand_index': round(demand, 2),
            'supply_index': round(supply, 2),
            'rainfall_mm': round(rainfall, 2),
            'temperature_celsius': round(temperature, 2),
            'transport_cost': round(transport_cost, 2),
            'storage_days': storage_days,
            'price_per_kg': price
        })
    
    df = pd.DataFrame(data)
    return df

if __name__ == '__main__':
    print("Generating agricultural product dataset...")
    df = generate_dataset(5000)
    
    # Save to CSV
    output_path = 'data/agricultural_products.csv'
    df.to_csv(output_path, index=False)
    print(f"Dataset saved to {output_path}")
    print(f"\nDataset shape: {df.shape}")
    print(f"\nFirst few rows:")
    print(df.head())
    print(f"\nDataset statistics:")
    print(df.describe())
    print(f"\nPrice range by product:")
    print(df.groupby('product')['price_per_kg'].agg(['min', 'max', 'mean']))
