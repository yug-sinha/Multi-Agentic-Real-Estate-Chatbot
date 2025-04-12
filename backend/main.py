from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import JSONResponse
from agents import property_agent, tenancy_agent
from utils.rag import retrieve_context
import uvicorn
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

app = FastAPI()

@app.post("/chat")
async def chat_endpoint(query: str = Form(...), file: UploadFile = File(None)):
    """
    Endpoint to handle user queries:
      - If an image file is provided, route the request to the Property Agent.
      - Otherwise, route to the Tenancy Agent.
    """
    logger.info("Received /chat request with query: %s", query)
    additional_context = retrieve_context(query)
    logger.info("Additional context retrieved for query: %s", additional_context)
    
    if file is not None:
        logger.info("File received: %s", file.filename)
        file_bytes = await file.read()
        mime_type = file.content_type
        logger.info("File MIME type: %s", mime_type)
        try:
            response_text = property_agent.process_property_issue(query, file_bytes, additional_context, mime_type)
            logger.info("Property Agent response generated successfully")
            return JSONResponse(content={"agent": "Property Agent", "response": response_text})
        except Exception as e:
            logger.exception("Error in processing property issue")
            raise HTTPException(status_code=500, detail=str(e))
    else:
        logger.info("No file provided. Processing as tenancy query.")
        try:
            response_text = tenancy_agent.process_tenancy_query(query)
            logger.info("Tenancy Agent response generated successfully")
            return JSONResponse(content={"agent": "Tenancy Agent", "response": response_text})
        except Exception as e:
            logger.exception("Error in processing tenancy query")
            raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    logger.info("Starting FastAPI server on http://0.0.0.0:8000")
    uvicorn.run(app, host="0.0.0.0", port=8000)
