"""Preprocessing + estimator as ONE Pipeline, so nothing leaks across the split."""

from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

NUMERIC = ["age", "income"]
CATEGORICAL = ["region", "plan"]


def build_pipeline(random_state: int = 0) -> Pipeline:
    numeric = Pipeline(
        [("impute", SimpleImputer(strategy="median")), ("scale", StandardScaler())]
    )
    categorical = Pipeline(
        [
            ("impute", SimpleImputer(strategy="most_frequent")),
            ("encode", OneHotEncoder(handle_unknown="ignore")),
        ]
    )
    pre = ColumnTransformer(
        [("num", numeric, NUMERIC), ("cat", categorical, CATEGORICAL)],
        remainder="drop",
    )
    return Pipeline(
        [
            ("pre", pre),
            ("clf", RandomForestClassifier(n_estimators=200, random_state=random_state)),
        ]
    )
