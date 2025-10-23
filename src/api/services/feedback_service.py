import uuid
from datetime import datetime
from pymongo import MongoClient


class FeedbackService:
    def __init__(self, mongo_client: MongoClient, db_name: str):
        self.collection = mongo_client[db_name]["feedback"]
    
    def store_feedback(self, request_id: str, predicted_class: int, correct_class=None, notes=None):
        feedback_id = str(uuid.uuid4())
        
        doc = {
            "feedback_id": feedback_id,
            "request_id": request_id,
            "predicted_class": predicted_class,
            "correct_class": correct_class,
            "notes": notes,
            "created_at": datetime.utcnow().isoformat()
        }
        
        self.collection.insert_one(doc)
        return {"status": "stored", "feedback_id": feedback_id}
