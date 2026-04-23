import json
from llm import generate_response
from typing import List, Dict

def load_knowledge():
    with open("knowledge_base.json", "r") as f:
        return json.load(f)

def retrieve_answer(query: str, kb: dict, history: List[Dict[str, str]] = None) -> str:
    if history is None:
        history = []
        
    history_str = ""
    for msg in history[-6:]: # get last 6 messages
        history_str += f"{msg['role'].capitalize()}: {msg['content']}\n"

    context = f"""
    Pricing:
    {json.dumps(kb.get('pricing', {}), indent=2)}

    Policies:
    {json.dumps(kb.get('policies', {}), indent=2)}

    Contact:
    {json.dumps(kb.get('contact', {}), indent=2)}
    """

    prompt = f"""
    You are the AutoStream conversational AI agent. 
    Answer the user's latest question naturally, using ONLY the knowledge base information below.
    If the answer is not in the knowledge base, politely say you don't know.
    NOTE: If the user complains about not receiving an email, politely explain that this is a simulated assignment project, and no real emails are actually sent.
    
    Knowledge Base:
    {context}
    
    Conversation History:
    {history_str}

    User's Latest Question: {query}
    """

    return generate_response(prompt)