# app/ml/models.py

from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from CommonAssessmentTool.app.ml.ml_utils import extract_features_and_labels
from CommonAssessmentTool.app.database import SessionLocal

def load_models():
    db = SessionLocal()
    try:
        X, y = extract_features_and_labels(db)

        models = {
            "logistic_regression": LogisticRegression(max_iter=1000),
            "random_forest": RandomForestClassifier(),
            "svm": SVC(probability=True),
        }

        for model in models.values():
            model.fit(X, y)

        return models
    finally:
        db.close()

