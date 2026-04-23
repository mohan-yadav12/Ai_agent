from agent import build_graph

graph = build_graph()

state = {
    "history": [],
    "user_input": "",
    "intent": "",
    "response": "",
    "name": None,
    "email": None,
    "platform": None,
    "lead_stage": "not_started"
}

print("[AutoStream AI Agent] (type 'exit' to quit)\n")

while True:
    try:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            break

        state["user_input"] = user_input

        # Run the agent graph
        state = graph.invoke(state)

        # Print the response
        print("Agent:", state["response"])
        
        # Update memory (retain last 6 conversational turns = 12 messages)
        state["history"].append({"role": "user", "content": user_input})
        state["history"].append({"role": "assistant", "content": state["response"]})
        
        if len(state["history"]) > 12:
            state["history"] = state["history"][-12:]
            
    except EOFError:
        break
    except KeyboardInterrupt:
        print("\nExiting...")
        break