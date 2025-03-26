from CommonAssessmentTool.app.ml.models import load_models

class ModelManager:
    def __init__(self):
        self.models = None
        self.current_model_name = None

    def _ensure_models_loaded(self):
        if self.models is None:
            print("🔁 Loading ML models...")
            self.models = load_models()
            self.current_model_name = next(iter(self.models))

    def get_current_model_name(self):
        self._ensure_models_loaded()
        return self.current_model_name

    def get_available_models(self):
        self._ensure_models_loaded()
        return list(self.models.keys())

    def set_model(self, model_name: str):
        self._ensure_models_loaded()
        if model_name not in self.models:
            raise ValueError(f"Model '{model_name}' not found.")
        self.current_model_name = model_name

    def get_model(self):
        self._ensure_models_loaded()
        return self.models[self.current_model_name]


# ✅ Singleton instance (lazy-loaded)
_model_manager_instance: ModelManager | None = None

def get_model_manager() -> ModelManager:
    global _model_manager_instance
    if _model_manager_instance is None:
        _model_manager_instance = ModelManager()
    return _model_manager_instance
