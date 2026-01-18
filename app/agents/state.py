from typing import List, TypedDict, Optional
from langchain_core.messages import AnyMessage

class SimulationState(TypedDict):
    messages: List[AnyMessage]
    context: str
    objective: str
    feedback: Optional[str]
    turn_count: int
    grading_requested: Optional[bool]
