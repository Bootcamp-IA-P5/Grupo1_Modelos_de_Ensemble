from typing import Optional
from pydantic import BaseModel


class MetricsEvent(BaseModel):
    request_id: str
    timestamp: str
    model_version: str
    latency_ms: int
    status: str
    input: Optional[dict] = None
    output: Optional[dict] = None
    client: Optional[dict] = None
    feedback: Optional[dict] = None
