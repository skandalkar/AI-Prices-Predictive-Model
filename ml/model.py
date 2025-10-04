from __future__ import annotations

import pickle
from dataclasses import dataclass
from typing import Dict, List, Tuple

import numpy as np
import pandas as pd

from .features import (
    CATEGORICAL_FEATURES,
    NUMERIC_FEATURES,
    validate_and_select_features,
)


@dataclass
class TrainingResult:
    model_path: str
    metrics: Dict[str, float]


class QuantileRegressor:
    """
    Lightweight price model using linear least squares for median (P50) and
    empirical residual quantiles for P10/P90. Only relies on numpy/pandas.
    """

    def __init__(self):
        self.design_columns: List[str] = []
        self.coefficients: np.ndarray | None = None  # shape: [n_features]
        self.intercept: float = 0.0
        self.resid_q10: float = 0.0
        self.resid_q90: float = 0.0

    @staticmethod
    def _pinball_loss(y_true: np.ndarray, y_pred: np.ndarray, alpha: float) -> float:
        diff = y_true - y_pred
        loss = np.where(diff >= 0, alpha * diff, (alpha - 1.0) * diff)
        return float(np.mean(loss))

    def _build_design_matrix(self, X: pd.DataFrame) -> pd.DataFrame:
        # One-hot encode categoricals; keep all levels, fill missing with zeros later
        X_cat = pd.get_dummies(
            X[CATEGORICAL_FEATURES].astype("category"),
            dtype=float,
        )
        X_num = X[NUMERIC_FEATURES].astype(float)
        X_design = pd.concat([X_num, X_cat], axis=1)
        return X_design

    def fit(self, df: pd.DataFrame) -> Dict[str, float]:
        X, y = validate_and_select_features(df, require_target=True)

        # Build design matrix and solve least squares with intercept term
        X_design = self._build_design_matrix(X)
        self.design_columns = X_design.columns.tolist()
        X_mat = X_design.to_numpy(dtype=float)
        ones = np.ones((X_mat.shape[0], 1), dtype=float)
        X_ext = np.concatenate([ones, X_mat], axis=1)
        y_vec = y.to_numpy(dtype=float)

        coef_ext, _, _, _ = np.linalg.lstsq(X_ext, y_vec, rcond=None)
        self.intercept = float(coef_ext[0])
        self.coefficients = coef_ext[1:]

        # In-sample residuals
        y_hat = self.intercept + X_mat @ self.coefficients
        residuals = y_vec - y_hat

        # Residual quantiles to approximate predictive quantiles
        self.resid_q10 = float(np.quantile(residuals, 0.10))
        self.resid_q90 = float(np.quantile(residuals, 0.90))

        # Metrics
        mae_p50 = float(np.mean(np.abs(residuals)))
        p10_preds = y_hat + self.resid_q10
        p50_preds = y_hat
        p90_preds = y_hat + self.resid_q90
        metrics: Dict[str, float] = {
            "mae_p50": mae_p50,
            "pinball_loss_q10": self._pinball_loss(y_vec, p10_preds, 0.10),
            "pinball_loss_q50": self._pinball_loss(y_vec, p50_preds, 0.50),
            "pinball_loss_q90": self._pinball_loss(y_vec, p90_preds, 0.90),
        }
        return metrics

    def predict(self, df: pd.DataFrame) -> pd.DataFrame:
        if self.coefficients is None or not self.design_columns:
            raise RuntimeError("Model is not trained")

        X, _ = validate_and_select_features(df, require_target=False)
        X_design = self._build_design_matrix(X)
        # Align columns to training design
        X_aligned = X_design.reindex(columns=self.design_columns, fill_value=0.0)
        X_mat = X_aligned.to_numpy(dtype=float)

        y_hat = self.intercept + X_mat @ self.coefficients
        p10 = y_hat + self.resid_q10
        p50 = y_hat
        p90 = y_hat + self.resid_q90

        result = pd.DataFrame(
            {
                "p10": p10,
                "p50": p50,
                "p90": p90,
            },
            index=X.index,
        )
        result["suggested_price"] = result["p50"].clip(lower=0.0)
        return result

    def save(self, path: str) -> None:
        with open(path, "wb") as f:
            pickle.dump(
                {
                    "design_columns": self.design_columns,
                    "coefficients": self.coefficients,
                    "intercept": self.intercept,
                    "resid_q10": self.resid_q10,
                    "resid_q90": self.resid_q90,
                },
                f,
            )

    @classmethod
    def load(cls, path: str) -> "QuantileRegressor":
        with open(path, "rb") as f:
            obj = pickle.load(f)
        model = cls()
        model.design_columns = obj["design_columns"]
        model.coefficients = np.asarray(obj["coefficients"], dtype=float)
        model.intercept = float(obj["intercept"])
        model.resid_q10 = float(obj["resid_q10"])
        model.resid_q90 = float(obj["resid_q90"])
        return model


def train_and_save_model(train_csv_path: str, model_output_path: str) -> Tuple[str, Dict[str, float]]:
    df = pd.read_csv(train_csv_path)
    model = QuantileRegressor()
    metrics = model.fit(df)
    model.save(model_output_path)
    return model_output_path, metrics
