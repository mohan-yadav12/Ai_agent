# AutoStream Conversational AI Agent

This is a LangGraph-based conversational AI agent for AutoStream, a fictional SaaS product that provides automated video editing tools. It implements intent classification, RAG-powered knowledge retrieval, and tool execution (lead capture) with memory management.

## How to run locally

1. **Clone the repository:**
   ```bash
   git clone https://github.com/mohan-yadav12/Ai_agent.git
   cd ai-agent
   ```

2. **Set up a virtual environment (optional but recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   Create a `.env` file in the root directory and add your Google Gemini API key:
   ```env
   GEMINI_API_KEY=your_gemini_api_key_here
   ```

5. **Run the agent:**
   ```bash
   python main.py
   ```
   Interact with the agent in the terminal. Type `exit` to quit.

## Architecture Explanation

This agent is built using **LangGraph** because it natively models complex agent workflows as state machines (graphs). LangGraph's node-edge architecture elegantly handles cyclic routing, ensuring deterministic state transitions—especially when switching from standard Q&A (RAG) into a multi-turn information-gathering sequence (lead capture).

**State Management**: 
State is defined using Python's `TypedDict` and maintained per conversational thread. A continuous `history` buffer tracks the last 6 conversational turns to provide memory. Additionally, state variables like `lead_stage` decouple the "intent detection" flow from the "data collection" flow, preventing endless intent misclassification loops when the user provides single-word responses like a name or email.

## WhatsApp Deployment Question

**How to integrate this agent with WhatsApp using Webhooks:**

1. **Set up a Meta Developer App:** Create a WhatsApp Business account and register an app to obtain an Access Token and Phone Number ID.
2. **Expose a Webhook:** Deploy the agent logic to a web server (e.g., FastAPI or Flask) and expose a `/webhook` endpoint.
3. **Verify the Webhook:** Implement Meta's webhook verification process by echoing the `hub.challenge` token they send during setup.
4. **Handle Incoming Messages:**
   - Meta will send `POST` requests to the `/webhook` with user messages.
   - Parse the incoming JSON to extract the user's phone number and message body.
   - Since LangGraph can store state, map the user's phone number to a unique thread/session ID to maintain their specific conversation state and memory across separate API calls.
5. **Send Responses:** Pass the user's message through the `graph.invoke(state)`, retrieve the `response`, and send a `POST` request back to the WhatsApp Cloud API (`https://graph.facebook.com/v17.0/<PHONE_NUMBER_ID>/messages`) to deliver the agent's reply.
