from fastapi import FastAPI, HTTPException
import json
import os

app = FastAPI()

@app.get("/health")
def health():
    return {"status": "ok", "service": "FireRiskAI"}

@app.get("/model")
def model_info():
    metadata_path = os.path.join("models", "metadata.json")
    if not os.path.exists(metadata_path):
        raise HTTPException(status_code=404, detail="metadata.json not found in models/")
    try:
        with open(metadata_path, "r") as f:
            data = json.load(f)
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to read metadata.json: {str(e)}")
