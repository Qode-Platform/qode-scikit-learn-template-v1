"""Fit, cross-validate, persist: `python -m src.train data/train.csv`."""

import argparse
from pathlib import Path

import joblib
import pandas as pd
from sklearn.model_selection import cross_val_score, train_test_split

from src.pipeline import build_pipeline


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("data", nargs="?", default="data/train.csv")
    parser.add_argument("--target", default="churned")
    parser.add_argument("--out", default="artifacts/model.joblib")
    args = parser.parse_args()

    frame = pd.read_csv(args.data)
    X = frame.drop(columns=[args.target])
    y = frame[args.target]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=0, stratify=y
    )

    pipe = build_pipeline()
    scores = cross_val_score(pipe, X_train, y_train, cv=5, scoring="roc_auc")
    print(f"cv roc_auc: {scores.mean():.3f} +/- {scores.std():.3f}")

    pipe.fit(X_train, y_train)
    print(f"holdout accuracy: {pipe.score(X_test, y_test):.3f}")

    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(pipe, args.out)


if __name__ == "__main__":
    main()
