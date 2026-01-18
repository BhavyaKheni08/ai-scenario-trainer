from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from app.agents.state import SimulationState

# Initialize LLM
llm = ChatOllama(model="llama3", base_url="http://localhost:11434")

def architect_node(state: SimulationState) -> SimulationState:
    """
    Scenario Architect: Generates the initial scenario and objective.
    """
    context = state.get("context", "")
    
    prompt = f"""You are an expert instructional designer. Based on the provided training manual context: {context}, generate a specific, difficult roleplay scenario for a student.
    
    Output the initial Agent message that starts the roleplay.
    Before the message, clearly state the hidden objective/persona in a separate line starting with 'OBJECTIVE:'.
    """
    
    response = llm.invoke([SystemMessage(content=prompt)])
    content = response.content
    
    # Parse objective and initial message
    # This is a naive parser; in production, you might want structured output or JSON
    objective = "Test the user on handling difficult situations."
    initial_message = content
    
    if "OBJECTIVE:" in content:
        parts = content.split("OBJECTIVE:")
        if len(parts) > 1:
            # Maybe the architect explains things first, or puts objective first
            # Let's assume the format might be mixed.
            # For robustness, we'll try to extract the objective line.
            lines = content.split('\n')
            obj_lines = [line for line in lines if "OBJECTIVE:" in line]
            if obj_lines:
                objective = obj_lines[0].replace("OBJECTIVE:", "").strip()
            
            # The rest is the scenario description/intro message
            # We'll stick to the raw content for the message if parsing is complex, 
            # or just filter out the objective line.
            initial_message = content.replace(f"OBJECTIVE: {objective}", "").strip()
            
    # Update state: The architect sets the initial AI message and the objective
    return {
        "objective": objective,
        "messages": [AIMessage(content=initial_message)],
        "turn_count": 0
    }

def actor_node(state: SimulationState) -> SimulationState:
    """
    The Actor: Roleplays based on the objective.
    """
    objective = state.get("objective", "")
    messages = state.get("messages", [])
    
    system_prompt = f"""You are a roleplay actor. Your goal is to test the user. Stick to this persona: {objective}.
    Respond to the user's last message naturally. Do not break character.
    """
    
    # Construct message history for the LLM
    # We include the system prompt + recent history
    conversation = [SystemMessage(content=system_prompt)] + messages
    
    response = llm.invoke(conversation)
    
    # Append response to existing messages to preserve history
    return {
        "messages": messages + [response],
        "turn_count": state["turn_count"] + 1
    }

def coach_node(state: SimulationState) -> SimulationState:
    """
    The Coach: Grades the conversation.
    """
    messages = state.get("messages", [])
    context = state.get("context", "")
    
    prompt = f"""You are a grading system. Analyze the following conversation history against the rules in the manual.
    
    Manual Context:
    {context}
    
    Conversation History:
    {messages}
    
    Provide a score (0-10) and actionable feedback.
    """
    
    response = llm.invoke([SystemMessage(content=prompt)])
    
    return {
        "feedback": response.content
    }
