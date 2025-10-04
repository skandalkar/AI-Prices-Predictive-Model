from __future__ import annotations

from typing import List, Tuple

import pandas as pd


CATEGORICAL_FEATURES: List[str] = [
    "product_category",
    "variety",
    "market_region",
    "grade",
]

NUMERIC_FEATURES: List[str] = [
    "quantity_kg",
    "moisture_pct",
    "days_since_harvest",
    "historical_avg_price",
]

TARGET_COLUMN: str = "price_per_kg"

ALL_FEATURES: List[str] = CATEGORICAL_FEATURES + NUMERIC_FEATURES


def validate_and_select_features(df: pd.DataFrame, require_target: bool = False) -> Tuple[pd.DataFrame, pd.Series | None]:
    missing = [c for c in ALL_FEATURES if c not in df.columns]
    if missing:
        raise ValueError(f"Missing required feature columns: {missing}")

    X = df[ALL_FEATURES].copy()
    y = None
    if require_target:
        if TARGET_COLUMN not in df.columns:
            raise ValueError(f"Missing target column '{TARGET_COLUMN}' in training data")
        y = df[TARGET_COLUMN].copy()

    return X, y
