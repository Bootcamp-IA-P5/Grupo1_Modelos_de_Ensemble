from typing import Optional, Dict
from pydantic import BaseModel, Field


class FeatureStats(BaseModel):
    min: Optional[float] = None
    max: Optional[float] = None
    mean: Optional[float] = None


class InputInfo(BaseModel):
    source: Optional[str] = Field(default="web")
    feature_stats: Optional[FeatureStats] = None


class OutputInfo(BaseModel):
    predicted_class: int
    confidence: float
    risk_level: Optional[str] = None
    risk_score: Optional[int] = None


class ClientInfo(BaseModel):
    ip: Optional[str] = None
    user_agent: Optional[str] = None


class FeedbackInfo(BaseModel):
    has_feedback: bool = False
    correct_class: Optional[int] = None


class MetricsEvent(BaseModel):
    request_id: str
    timestamp: str
    model_version: str
    latency_ms: int
    status: str
    input: Optional[InputInfo] = None
    output: OutputInfo
    client: Optional[ClientInfo] = None
    feedback: Optional[FeedbackInfo] = None

