from fastapi import FastAPI

app = FastAPI(title="FireRiskAI API")

@app.get("/health")
def health():
    return {"status": "ok", "service": "FireRiskAI"}
