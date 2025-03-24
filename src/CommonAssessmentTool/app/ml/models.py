from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.datasets import make_classification

# Generate dummy training data
X, y = make_classification(n_samples=100, n_features=4, random_state=42)

def load_models():
    models = {
        "logistic_regression": LogisticRegression(),
        "random_forest": RandomForestClassifier(),
        "svm": SVC(probability=True),
    }
    for model in models.values():
        model.fit(X, y)
    return models
