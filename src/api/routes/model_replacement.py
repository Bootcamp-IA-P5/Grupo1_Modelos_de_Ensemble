"""
Endpoint simple para auto-reemplazo de modelos
"""

from fastapi import APIRouter, HTTPException
from src.api.services.model_manager import model_manager

router = APIRouter()

@router.get("/models/compare")
def compare_models():
    """
    Comparar modelos y ver cuál es el mejor
    """
    try:
        result = model_manager.compare_models()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/models/replace/{model_name}")
def replace_model(model_name: str):
    """
    Reemplazar modelo actual por uno nuevo
    
    Args:
        model_name: random_forest, extra_trees, o xgboost
    """
    try:
        success = model_manager.replace_model(model_name)
        if success:
            return {
                "success": True,
                "current_model": model_manager.get_current_model(),
                "message": f"Modelo reemplazado a: {model_name}"
            }
        else:
            return {
                "success": False,
                "message": f"Modelo {model_name} no disponible"
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/models/current")
def get_current_model():
    """
    Obtener modelo actual
    """
    try:
        current = model_manager.get_current_model()
        return {
            "current_model": current,
            "available_models": model_manager.available_models
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
