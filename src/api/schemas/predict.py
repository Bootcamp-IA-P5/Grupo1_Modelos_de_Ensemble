from pydantic import BaseModel, conlist


class PredictRequest(BaseModel):
    # Pydantic v2: usar min_length/max_length en conlist
    features: conlist(float, min_length=54, max_length=54)


class PredictResponse(BaseModel):
    prediction: int
    class_name: str
    confidence: float
    risk_level: str
    risk_score: int

