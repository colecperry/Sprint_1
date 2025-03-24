from fastapi.testclient import TestClient
from CommonAssessmentTool.app.main import app

client = TestClient(app)

# Test listing all available models
def test_list_available_models():
    response = client.get("/models/available")
    assert response.status_code == 200
    models = response.json()["models"]
    assert "logistic_regression" in models
    assert "random_forest" in models
    assert "svm" in models

# Test getting the current model
def test_get_current_model():
    response = client.get("/models/current")
    assert response.status_code == 200
    assert "current_model" in response.json()

# Test switching the model
def test_switch_model_to_random_forest():
    response = client.post("/models/select", json={"model_name": "random_forest"})
    assert response.status_code == 200
    assert response.json()["message"] == "Model set to 'random_forest'"

    # Confirm current model changed
    current = client.get("/models/current").json()["current_model"]
    assert current == "random_forest"

# Test invalid switch handling
def test_switch_model_invalid_name():
    response = client.post("/models/select", json={"model_name": "not_a_model"})
    assert response.status_code == 400
    assert "detail" in response.json()

# Test using active model for prediction
def test_predict_with_valid_input():
    # Set model first
    client.post("/models/select", json={"model_name": "logistic_regression"})

    response = client.post("/models/predict", json={"features": [0.1, 0.2, 0.3, 0.4]})
    assert response.status_code == 200
    assert "prediction" in response.json()

# Test handling errors for active model/prediction
def test_predict_with_invalid_input():
    response = client.post("/models/predict", json={"features": ["invalid", "values"]})
    # FastAPI will return 422 for validation errors unless manually overridden
    assert response.status_code == 422
