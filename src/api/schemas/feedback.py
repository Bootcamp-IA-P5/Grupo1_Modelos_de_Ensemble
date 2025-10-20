from typing import Optional
from pydantic import BaseModel


class FeedbackRequest(BaseModel):
    request_id: str
    predicted_class: int
    correct_class: Optional[int] = None
    notes: Optional[str] = None


class FeedbackResponse(BaseModel):
    status: str
    feedback_id: str
