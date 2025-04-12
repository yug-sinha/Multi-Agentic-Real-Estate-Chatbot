from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Request
from fastapi.responses import JSONResponse
from agents import property_agent, tenancy_agent
from utils.rag import retrieve_context
import uvicorn
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

app = FastAPI()

# In-memory store for conversation history and last used agent per user
session_conversations = {}
session_last_agent = {}

@app.post("/chat")
async def chat_endpoint(
    request: Request,
    query: str = Form(...),
    file: UploadFile = File(None)
):
    """
    Handle user queries with conversation history context and smart agent routing.
    """
    client_ip = request.client.host  # Identify user session via IP

    if client_ip not in session_conversations:
        session_conversations[client_ip] = []
        session_last_agent[client_ip] = None

    logger.info("Received /chat request with query: %s", query)

    # Build conversation history context
    conversation_history = session_conversations[client_ip]
    history_context = ""
    for item in conversation_history:
        history_context += f"User: {item['query']}\nAgent: {item['response']}\n"

    # RAG context
    additional_context = retrieve_context(query)
    logger.info("Retrieved additional RAG context: %s", additional_context)

    combined_context = f"{history_context}\n{additional_context}"

    # Routing Logic:
    # If file is provided -> Always Property Agent
    # Else -> Use last agent if exists, else fallback to Tenancy Agent
    use_agent = None

    if file is not None:
        use_agent = "Property Agent"
    elif session_last_agent[client_ip] is not None:
        use_agent = session_last_agent[client_ip]
    else:
        use_agent = "Tenancy Agent"

    logger.info("Selected Agent for this query: %s", use_agent)

    if use_agent == "Property Agent":
        logger.info("File provided or continuing with Property Agent")
        if file is None:
            file_bytes = b''  # Empty byte file for follow-up without file
            mime_type = "image/jpeg"
        else:
            file_bytes = await file.read()
            mime_type = file.content_type
            logger.info("File MIME type: %s", mime_type)

        try:
            response_text = property_agent.process_property_issue(query, file_bytes, combined_context, mime_type)
        except Exception as e:
            logger.exception("Error in Property Agent")
            raise HTTPException(status_code=500, detail=str(e))
    else:
        logger.info("Processing with Tenancy Agent")
        try:
            response_text = tenancy_agent.process_tenancy_query(query, combined_context)
        except Exception as e:
            logger.exception("Error in Tenancy Agent")
            raise HTTPException(status_code=500, detail=str(e))

    # Save latest agent used
    session_last_agent[client_ip] = use_agent

    # Update conversation history
    session_conversations[client_ip].append({
        "query": query,
        "response": response_text
    })

    return JSONResponse(content={"agent": use_agent, "response": response_text})


if __name__ == "__main__":
    logger.info("Starting FastAPI server at http://0.0.0.0:8000")
    uvicorn.run(app, host="0.0.0.0", port=8000)