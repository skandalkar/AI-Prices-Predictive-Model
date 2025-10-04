from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel, Field, field_validator


class ProductFeatures(BaseModel):
    product_category: str
    variety: str
    market_region: str
    grade: str

    quantity_kg: float = Field(ge=0)
    moisture_pct: float = Field(ge=0, le=100)
    days_since_harvest: float = Field(ge=0)
    historical_avg_price: float = Field(ge=0)


class PredictionRequest(BaseModel):
    items: List[ProductFeatures]


class PredictionItem(BaseModel):
    p10: float
    p50: float
    p90: float
    suggested_price: float


class PredictionResponse(BaseModel):
    predictions: List[PredictionItem]


class TrainRequest(BaseModel):
    csv_path: str

    @field_validator("csv_path")
    @classmethod
    def validate_path(cls, v: str) -> str:
        if not v.endswith(".csv"):
            raise ValueError("csv_path must be a .csv file")
        return v


class TrainResponse(BaseModel):
    model_path: str
    metrics: dict
