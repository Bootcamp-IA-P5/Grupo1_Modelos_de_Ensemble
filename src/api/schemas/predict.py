from pydantic import BaseModel, conlist


class PredictRequest(BaseModel):
    features: conlist(float, min_items=54, max_items=54)


class PredictResponse(BaseModel):
    prediction: int
    class_name: str
    confidence: float
    risk_level: str
    risk_score: int

