# app/ml/router.py

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from CommonAssessmentTool.app.ml.model_manager import get_model_manager

router = APIRouter(prefix="/models", tags=["Machine Learning Models"])

class ModelSelectRequest(BaseModel):
    model_name: str

class PredictRequest(BaseModel):
    features: list[float]

@router.get("/available")
async def list_models():
    return {"models": get_model_manager().get_available_models()}

@router.get("/current")
async def get_current_model():
    return {"current_model": get_model_manager().get_current_model_name()}

@router.post("/select")
async def select_model(request: ModelSelectRequest):
    try:
        get_model_manager().set_model(request.model_name)
        return {"message": f"Model set to '{request.model_name}'"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/predict")
async def predict(request: PredictRequest):
    try:
        model = get_model_manager().get_model()
        prediction = model.predict([request.features])
        return {"prediction": int(prediction[0])}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
