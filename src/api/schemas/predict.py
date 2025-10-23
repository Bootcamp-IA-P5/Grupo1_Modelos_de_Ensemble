from pydantic import BaseModel, conlist
from typing import Optional, Dict


class PredictRequest(BaseModel):
    features: conlist(float, min_length=54, max_length=54)
    user_id: Optional[str] = None
    location: Optional[Dict[str, float]] = None


class PredictResponse(BaseModel):
    prediction: int
    class_name: str
    confidence: float
    risk_level: str
    risk_score: int
    processing_time_ms: Optional[float] = None

