import pandas as pd
import pytest
from sklearn.pipeline import Pipeline

from src.pipeline import build_pipeline


@pytest.fixture
def frame() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "age": [25, 41, 33, 58, 29, 47],
            "income": [30_000, 82_000, 51_000, 97_000, 42_000, 66_000],
            "region": ["emea", "amer", "emea", "apac", "amer", "emea"],
            "plan": ["free", "pro", "pro", "free", "free", "pro"],
            "churned": [0, 1, 0, 1, 0, 1],
        }
    )


def test_build_pipeline_shape():
    assert isinstance(build_pipeline(), Pipeline)


def test_fit_predict_roundtrip(frame):
    X, y = frame.drop(columns=["churned"]), frame["churned"]
    pipe = build_pipeline().fit(X, y)
    assert pipe.predict(X).shape == (len(frame),)


def test_unseen_category_does_not_raise(frame):
    X, y = frame.drop(columns=["churned"]), frame["churned"]
    pipe = build_pipeline().fit(X, y)
    unseen = X.iloc[[0]].assign(region="antarctica")
    assert pipe.predict(unseen).shape == (1,)
