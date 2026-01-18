from fastapi import FastAPI
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

app = FastAPI(title="AI Scenario Trainer API", version="0.1.0")

from app.api import ingest, simulation
app.include_router(ingest.router, prefix="/api/v1", tags=["Ingestion"])
app.include_router(simulation.router, prefix="/api/v1/simulation", tags=["Simulation"])

@app.get("/health")
async def health_check():
    """
    Health check endpoint to verify backend is running.
    """
    return {"status": "ok", "app_name": "ai-scenario-trainer"}

@app.get("/")
async def root():
    return {"message": "Welcome to the AI Scenario Trainer API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
