# app/ml/model_manager.py
from CommonAssessmentTool.app.ml.models import load_models

class ModelManager:
    def __init__(self):
        self.models = load_models()
        self.current_model_name = next(iter(self.models))  # Default = first model

    def get_current_model_name(self):
        return self.current_model_name

    def get_available_models(self):
        return list(self.models.keys())

    def set_model(self, model_name: str):
        if model_name not in self.models:
            raise ValueError(f"Model '{model_name}' not found.")
        self.current_model_name = model_name

    def get_model(self):
        return self.models[self.current_model_name]

# Singleton instance
model_manager = ModelManager()
