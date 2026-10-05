from pathlib import Path

import joblib
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

MODEL_PATH = Path(__file__).resolve().parent / "model.joblib"
SPECIES = ["setosa", "versicolor", "virginica"]

_model = None   # the expert's brain, loaded once and kept in memory


def train():
    """Study phase + exam. Saves the brain to a file and returns the exam score."""
    X, y = load_iris(return_X_y=True)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)            # study
    accuracy = model.score(X_test, y_test) # exam on unseen flowers
    joblib.dump(model, MODEL_PATH)         # save the brain
    return accuracy


def predict(features):
    """Work phase. features = [sepal_length, sepal_width, petal_length, petal_width]."""
    global _model
    if _model is None:                     # first time only
        if not MODEL_PATH.exists():
            train()
        _model = joblib.load(MODEL_PATH)
    return SPECIES[int(_model.predict([features])[0])]