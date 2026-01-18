from fastapi import APIRouter, HTTPException
from langchain_core.messages import HumanMessage
from app.agents.workflow import app_graph
from app.services.rag_service import query_knowledge_base
from app.schemas.simulation import (
    StartSimulationRequest, 
    ChatRequest, 
    GradeRequest, 
    SimulationResponse, 
    GradeResponse
)

router = APIRouter()

@router.post("/start", response_model=SimulationResponse)
async def start_simulation(request: StartSimulationRequest):
    """
    Start a new roleplay simulation. 
    Loads RAG context and triggers the Architect to design the scenario.
    """
    # 1. Retrieve Context from RAG (using a broad query relative to training manuals)
    # We might assume the topic is broadly "Customer Service" or provided in request
    query = request.topic or "Customer service guidelines and best practices"
    
    # query_knowledge_base returns Document objects. We need the page_content.
    docs = query_knowledge_base(query, k=3)
    if not docs:
        context_str = "No specific training manual rules found. Use general best practices."
    else:
        context_str = "\n".join([d.page_content for d in docs])
        
    # 2. Initialize State
    initial_state = {
        "context": context_str,
        "messages": [],
        "objective": "", # Will be filled by Architect
        "turn_count": 0,
        "grading_requested": False
    }
    
    # 3. Run Graph (Architect)
    # config uses session_id for thread persistence
    config = {"configurable": {"thread_id": request.session_id}}
    
    # We invoke the graph. The conditional entry point checks 'objective'.
    # Since it's empty, it routes to 'architect'.
    result = app_graph.invoke(initial_state, config=config)
    
    # 4. Extract Response
    # Architect adds an AIMessage to messages list.
    messages = result.get("messages", [])
    last_message = messages[-1].content if messages else "Error: No scenario generated."
    
    return SimulationResponse(
        session_id=request.session_id,
        message=str(last_message),
        turn_count=result.get("turn_count", 0)
    )

@router.post("/chat", response_model=SimulationResponse)
async def chat_simulation(request: ChatRequest):
    """
    Continue the conversation. 
    Input user message -> Actor responds.
    """
    config = {"configurable": {"thread_id": request.session_id}}
    
    # 1. Update State with User Message
    # We pass the new message as input. LangGraph merges this into 'messages' list 
    # (assuming we used a custom reducer or default behavior lists usually replace? 
    # StateGraph defaults: if you pass a dict, it replaces the keys.
    # WAIT. Simple StateGraph(TypedDict) replaces values.
    # To append messages, you usually need `Annotated[List[AnyMessage], add_messages]`.
    # I didn't verify State definition in step 102/133.
    # User's step 93 requirement: "Create a TypedDict... messages: List..."
    # If I just use TypedDict, `messages` will be OVERWRITTEN by the return value of node.
    # FIX: I need to ensure the nodes return the FULL list or I change state definition to use `add_messages`.
    # BUT keeping it simple for now: 
    # `app.invoke` merges input. If I pass `messages: [HumanMessage]`, and the state logic is "replace",
    # I lose history!
    # Checking `state.py`: It is a simple TypedDict. 
    # Checking `nodes.py`: `actor_node` does: `conversation = messages + ...` then returns `messages: [response]`.
    # If using standard StateGraph without `add_messages` annotation, this will replace the list with just `[response]`.
    # THIS IS A BUG in the design requested or my implementation.
    # To fix without changing `state.py` (which requires `langgraph` specific imports like `add_messages`),
    # I should MANUALLY append in the node and return the full list.
    # Let's check `nodes.py` again.
    
    # Ref: `actor_node` in `nodes.py`:
    # `messages = state.get("messages", [])`
    # ...
    # returns `{"messages": [response]}`.
    # If LangGraph creates a new state by merging, `messages` becomes keys from return?
    # Yes. So history is lost.
    
    # I will patch usage here:
    # Get current state first?
    # `app_graph.get_state(config).values`
    
    # Actually, the best way in LangGraph is to use `Annotated` with reducers.
    # But sticking to what I have: I will modify `nodes.py` to return FULL history?
    # OR I'll handle it in API?
    # No, nodes must return the update.
    # If I don't use reducers, I must return the full lists.
    # I'll update `nodes.py` in a separate step?
    # Or I can try to use `add_messages` if I can.
    
    # Let's check `state.py`.
    pass
    
    # Re-reading `nodes.py`:
    # `architect_node`: returns `messages: [AIMessage]`.
    # `actor_node`: returns `messages: [response]`.
    # This implies history loss.
    
    # I'll assume for this turn I should fix `nodes.py`?
    # Or just implementation details.
    
    # Let's implement `/chat` assuming `add_messages` behavior or I'll manual append.
    # To hold history in `messages`, I'll fetch state, append user msg, then invoke.
    
    current_state = app_graph.get_state(config).values
    if not current_state:
        raise HTTPException(status_code=404, detail="Session not found. Start a simulation first.")
        
    current_messages = current_state.get("messages", [])
    user_msg_obj = HumanMessage(content=request.message)
    updated_messages = current_messages + [user_msg_obj]
    
    # We pass the FULL updated list to invoke, so that when it runs, state has specific history.
    # But wait, `invoke` input is merged.
    # If I input `{"messages": updated_messages}`, the state entering the *entry point* has this.
    # Then `Actor` runs. `Actor` logic (as written in Step 105) reads `state['messages']`.
    # Then `Actor` returns `{"messages": [response]}`.
    # If I don't change `nodes.py`, the final state will be `[response]`.
    
    # I MUST FIX `nodes.py` to return `messages + [response]`.
    # I will do that via `multi_replace` or just rewrite `nodes.py`.
    # I will include `app/api/simulation.py` logic assuming `nodes.py` will be fixed.
    
    # Back to `/chat`:
    input_update = {"messages": updated_messages, "grading_requested": False}
    result = app_graph.invoke(input_update, config=config)
    
    # Result contains the state after Actor run.
    # If I fix Node to return full list, `result['messages']` is full list.
    final_messages = result.get("messages", [])
    last_response = final_messages[-1].content if final_messages else ""
    
    return SimulationResponse(
        session_id=request.session_id,
        message=str(last_response),
        turn_count=result.get("turn_count", 0)
    )

@router.post("/grade", response_model=GradeResponse)
async def grade_simulation(request: GradeRequest):
    """
    End and Grade the simulation.
    """
    config = {"configurable": {"thread_id": request.session_id}}
    
    import re
    
    # Input triggers 'grading_requested' -> Routes to Coach
    result = app_graph.invoke({"grading_requested": True}, config=config)
    
    feedback = result.get("feedback", "No feedback generated.")
    
    # Extract score (0-10) using Regex
    # Matches "Score: 8", "Score: 9.5", "Score: 8/10", "8.5/10"
    score = 0.0
    match = re.search(r"Score:\s*(\d+(?:\.\d+)?)|(\d+(?:\.\d+)?)/10", feedback, re.IGNORECASE)
    if match:
        score_val = match.group(1) or match.group(2)
        try:
            score = float(score_val)
        except ValueError:
            pass
    
    return GradeResponse(
        session_id=request.session_id,
        score=score,
        feedback=str(feedback)
    )
