from llm import generate_response
from typing import List, Dict

def detect_intent(user_input: str, history: List[Dict[str, str]] = None) -> str:
    if history is None:
        history = []
        
    history_str = ""
    for msg in history[-6:]: # get last 6 messages
        history_str += f"{msg['role'].capitalize()}: {msg['content']}\n"

    prompt = f"""
    Classify the intent of the final user message into one of three categories:
    - greeting: casual hellos, greetings.
    - inquiry: asking questions about the product, features, or pricing.
    - high_intent: explicitly stating they want to sign up, buy, subscribe, or try a plan.
    
    Context History:
    {history_str}

    Final User Message: {user_input}

    Only return the label exactly as one of the three options: greeting, inquiry, or high_intent. Do not include quotes or extra text.
    """

    intent = generate_response(prompt).strip().lower()
    return intent