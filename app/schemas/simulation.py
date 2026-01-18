from pydantic import BaseModel
from typing import Optional, List, Any

class StartSimulationRequest(BaseModel):
    session_id: str
    topic: Optional[str] = "General Training"

class ChatRequest(BaseModel):
    session_id: str
    message: str

class GradeRequest(BaseModel):
    session_id: str

class SimulationResponse(BaseModel):
    session_id: str
    message: str
    turn_count: int

class GradeResponse(BaseModel):
    session_id: str
    score: float
    feedback: str
