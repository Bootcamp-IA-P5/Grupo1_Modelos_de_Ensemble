from .health import router as health_router
from .model import router as model_router
from .metrics import router as metrics_router
from .predict import router as predict_router
from .feedback import router as feedback_router
from .database import router as database_router
from .test_storage import router as test_storage_router

__all__ = ["health_router", "model_router", "metrics_router", "predict_router", "feedback_router", "database_router", "test_storage_router"]
