from fastapi import APIRouter, HTTPException
import os
from pymongo import MongoClient
from src.api.schemas.feedback import FeedbackRequest, FeedbackResponse
from src.api.services.feedback_service import FeedbackService

router = APIRouter()

# Cliente MongoDB global
_mongo_client = None
_feedback_service = None

def _get_mongo():
    global _mongo_client
    if _mongo_client is None:
        uri = os.getenv("MONGO_URI")
        if not uri:
            raise HTTPException(status_code=500, detail="MONGO_URI not configured")
        try:
            _mongo_client = MongoClient(uri)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to connect MongoDB: {str(e)}")
    return _mongo_client

def _get_feedback_service():
    global _feedback_service
    if _feedback_service is None:
        mongo_client = _get_mongo()
        db_name = os.getenv("MONGODB_DATABASE", "grupo1_modelos_de_ensemble")
        _feedback_service = FeedbackService(mongo_client, db_name)
    return _feedback_service

@router.post("/feedback", response_model=FeedbackResponse)
def post_feedback(feedback: FeedbackRequest):
    try:
        feedback_service = _get_feedback_service()
        result = feedback_service.store_feedback(
            request_id=feedback.request_id,
            predicted_class=feedback.predicted_class,
            correct_class=feedback.correct_class,
            notes=feedback.notes
        )
        return FeedbackResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
