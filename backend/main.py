from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Request
from fastapi.responses import JSONResponse
from agents import property_agent, tenancy_agent
from utils.rag import retrieve_context
import uvicorn
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

app = FastAPI()

# Temporary in-memory session-based conversation store
session_conversations = {}

@app.post("/chat")
async def chat_endpoint(
    request: Request,
    query: str = Form(...),
    file: UploadFile = File(None)
):
    """
    Handle user queries with conversation history context.
    """
    client_ip = request.client.host  # using client IP for identifying the user session

    if client_ip not in session_conversations:
        session_conversations[client_ip] = []

    logger.info("Received /chat request with query: %s", query)

    # Build conversation history context
    conversation_history = session_conversations[client_ip]
    history_context = ""
    for item in conversation_history:
        history_context += f"User: {item['query']}\nAgent: {item['response']}\n"

    # Retrieve additional RAG context
    additional_context = retrieve_context(query)
    logger.info("Retrieved additional RAG context: %s", additional_context)

    combined_context = f"{history_context}\n{additional_context}"

    if file is not None:
        logger.info("File received: %s", file.filename)
        file_bytes = await file.read()
        mime_type = file.content_type
        logger.info("File MIME type: %s", mime_type)

        try:
            response_text = property_agent.process_property_issue(query, file_bytes, combined_context, mime_type)
            agent_name = "Property Agent"
            logger.info("Property Agent response generated successfully")
        except Exception as e:
            logger.exception("Error in Property Agent processing")
            raise HTTPException(status_code=500, detail=str(e))
    else:
        logger.info("Processing Tenancy Agent query")
        try:
            response_text = tenancy_agent.process_tenancy_query(query, combined_context)
            agent_name = "Tenancy Agent"
            logger.info("Tenancy Agent response generated successfully")
        except Exception as e:
            logger.exception("Error in Tenancy Agent processing")
            raise HTTPException(status_code=500, detail=str(e))

    # Update conversation history
    session_conversations[client_ip].append({
        "query": query,
        "response": response_text
    })

    return JSONResponse(content={"agent": agent_name, "response": response_text})


if __name__ == "__main__":
    logger.info("Starting FastAPI server at http://0.0.0.0:8000")
    uvicorn.run(app, host="0.0.0.0", port=8000)
