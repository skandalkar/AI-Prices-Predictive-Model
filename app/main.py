from __future__ import annotations

import os
from pathlib import Path
from typing import List

import pandas as pd
from fastapi import FastAPI, HTTPException

from ml.features import ALL_FEATURES
from ml.model import QuantileRegressor, train_and_save_model
from app.schemas import (
    PredictionItem,
    PredictionRequest,
    PredictionResponse,
    TrainRequest,
    TrainResponse,
)


DEFAULT_MODEL_PATH = os.environ.get("MODEL_PATH", "/workspace/models/model.joblib")

app = FastAPI(title="Agri Price Suggester", version="0.1.0")


def load_or_init_model() -> QuantileRegressor:
    model_path = Path(DEFAULT_MODEL_PATH)
    if model_path.exists():
        return QuantileRegressor.load(str(model_path))
    # cold start: create empty model that will raise if used before training
    return QuantileRegressor()


model = load_or_init_model()


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/predict", response_model=PredictionResponse)
def predict(req: PredictionRequest) -> PredictionResponse:
    # ensure trained coefficients exist
    if getattr(model, "coefficients", None) is None:
        raise HTTPException(status_code=400, detail="Model not trained yet")

    rows: List[dict] = [item.model_dump() for item in req.items]
    df = pd.DataFrame(rows, columns=ALL_FEATURES)
    preds_df = model.predict(df)

    items: List[PredictionItem] = []
    for _, row in preds_df.iterrows():
        items.append(
            PredictionItem(
                p10=float(row.get("p10", 0.0)),
                p50=float(row.get("p50", 0.0)),
                p90=float(row.get("p90", 0.0)),
                suggested_price=float(row.get("suggested_price", 0.0)),
            )
        )
    return PredictionResponse(predictions=items)


@app.post("/train", response_model=TrainResponse)
def train(req: TrainRequest) -> TrainResponse:
    csv_path = req.csv_path
    if not Path(csv_path).exists():
        raise HTTPException(status_code=400, detail=f"Training file not found: {csv_path}")

    # ensure models dir exists
    Path(DEFAULT_MODEL_PATH).parent.mkdir(parents=True, exist_ok=True)

    model_path, metrics = train_and_save_model(csv_path, DEFAULT_MODEL_PATH)

    # reload global model
    global model
    model = QuantileRegressor.load(model_path)

    return TrainResponse(model_path=model_path, metrics=metrics)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", "8000")))
