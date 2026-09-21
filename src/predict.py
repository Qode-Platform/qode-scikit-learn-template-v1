"""Score new rows with a persisted pipeline."""

import sys

import joblib
import pandas as pd


def main(model_path: str, data_path: str) -> None:
    pipe = joblib.load(model_path)
    frame = pd.read_csv(data_path)
    frame["score"] = pipe.predict_proba(frame)[:, 1]
    print(frame.to_string(index=False))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
