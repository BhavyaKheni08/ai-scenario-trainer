from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
from app.agents.state import SimulationState
from app.agents.nodes import architect_node, actor_node, coach_node

# Define a routing function to decide where to start
def route_start(state: SimulationState):
    # Check for grading request
    if state.get("grading_requested"):
        return "coach"
        
    # If there is no objective, we need to design the scenario
    if not state.get("objective"):
        return "architect"
        
    # Otherwise, we are in the chat loop
    return "actor"

# Create the graph
workflow = StateGraph(SimulationState)

# Add Nodes
workflow.add_node("architect", architect_node)
workflow.add_node("actor", actor_node)
workflow.add_node("coach", coach_node)

# Add Edges
# Based on state, we route to Architect, Actor, or Coach
workflow.set_conditional_entry_point(
    route_start,
    {
        "architect": "architect",
        "actor": "actor",
        "coach": "coach"
    }
)

# Architect generates the FIRST message, then stops to wait for user
workflow.add_edge("architect", END)

# Actor generates a RESPONSE, then stops to wait for user
workflow.add_edge("actor", END)

# Coach generates feedback, then stops
workflow.add_edge("coach", END)

# Initialize memory for persistence
memory = MemorySaver()

# Compile the graph
app_graph = workflow.compile(checkpointer=memory)
