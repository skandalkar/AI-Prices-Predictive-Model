from __future__ import annotations

import argparse
from pathlib import Path

from ml.model import train_and_save_model


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--csv", default="/workspace/data/demo_prices.csv")
    parser.add_argument("--out", default="/workspace/models/model.joblib")
    args = parser.parse_args()

    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    model_path, metrics = train_and_save_model(args.csv, args.out)
    print({"model_path": model_path, "metrics": metrics})


if __name__ == "__main__":
    main()
