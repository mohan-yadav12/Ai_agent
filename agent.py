from typing import TypedDict, Optional, List, Dict, Any
from langgraph.graph import StateGraph, END

from intent import detect_intent
from rag import load_knowledge, retrieve_answer
from tools import mock_lead_capture
from llm import extract_lead_info

kb = load_knowledge()

class AgentState(TypedDict):
    history: List[Dict[str, str]]
    user_input: str
    intent: str
    response: str
    name: Optional[str]
    email: Optional[str]
    platform: Optional[str]
    lead_stage: str # "not_started", "gathering", "completed"

def intent_node(state: AgentState):
    if state.get("lead_stage") == "gathering":
        state["intent"] = "high_intent"
    else:
        state["intent"] = detect_intent(state["user_input"], state.get("history", []))
    return state

def rag_node(state: AgentState):
    answer = retrieve_answer(state["user_input"], kb, state.get("history", []))
    state["response"] = answer
    return state

def lead_node(state: AgentState):
    state["lead_stage"] = "gathering"
    
    # Try to extract new info from current input
    extracted = extract_lead_info(state["user_input"])
    
    if extracted.get("name") and not state.get("name"):
        state["name"] = extracted["name"]
    if extracted.get("email") and not state.get("email"):
        state["email"] = extracted["email"]
    if extracted.get("platform") and not state.get("platform"):
        state["platform"] = extracted["platform"]
        
    if not state.get("name"):
        state["response"] = "Great! I can help you set that up. First, what's your name?"
    elif not state.get("email"):
        state["response"] = f"Nice to meet you, {state['name']}! What's the best email to reach you?"
    elif not state.get("platform"):
        state["response"] = "Thanks! Lastly, which content platform do you primarily use (e.g., YouTube, Instagram)?"
    else:
        # All info gathered, response will be handled by tool_node
        pass
        
    return state

def tool_node(state: AgentState):
    mock_lead_capture(state["name"], state["email"], state["platform"])
    state["response"] = f"You're all set, {state['name']}! Our team will contact you at {state['email']} about your {state['platform']} channel."
    state["lead_stage"] = "completed"
    
    # Optional: reset lead info if you want them to be able to do it again
    # state["name"] = None
    # state["email"] = None
    # state["platform"] = None
    return state

def router(state: AgentState):
    if state["intent"] == "high_intent":
        return "lead"
    return "rag"

def lead_router(state: AgentState):
    if state.get("name") and state.get("email") and state.get("platform"):
        return "tool"
    return END

def build_graph():
    graph = StateGraph(AgentState)

    graph.add_node("intent", intent_node)
    graph.add_node("rag", rag_node)
    graph.add_node("lead", lead_node)
    graph.add_node("tool", tool_node)

    graph.set_entry_point("intent")

    graph.add_conditional_edges("intent", router, {
        "rag": "rag",
        "lead": "lead"
    })

    graph.add_edge("rag", END)

    graph.add_conditional_edges("lead", lead_router, {
        END: END,
        "tool": "tool"
    })

    graph.add_edge("tool", END)

    return graph.compile()