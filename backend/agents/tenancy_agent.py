import logging
from config import client
from utils.rag import retrieve_context
from google.genai.types import GenerateContentConfig


logger = logging.getLogger(__name__)

# Define the prompt template for tenancy FAQ queries using RAG.
TENANCY_PROMPT_TEMPLATE = (
    "You are a legal and property management expert specializing in tenancy laws and rental agreements.\n"
    "Retrieved Context: {context}\n"
    "User Query: {query}\n"
    "Provide a comprehensive, legally informed answer including any necessary legal conditions and practical advice. "
    "If relevant, ask if more location-specific information is needed."
)

def process_tenancy_query(query: str) -> str:
    """
    Processes tenancy-related queries using a Retrieval-Augmented Generation approach.
    
    Args:
        query (str): The tenancy-related question from the user.
        
    Returns:
        str: The generated answer from the tenancy agent.
    """
    logger.info("Starting process_tenancy_query with query: %s", query)
    try:
        context = retrieve_context(query)
        logger.info("Retrieved context for tenancy query: %s", context)
    except Exception as e:
        logger.exception("Failed to retrieve context")
        raise Exception(f"Context retrieval failed: {str(e)}")
    
    # Fill the prompt template with the retrieved context.
    prompt = TENANCY_PROMPT_TEMPLATE.format(context=context, query=query)
    logger.info("Constructed prompt for tenancy query: %s", prompt)
    
    try:
        logger.info("Generating response using Gemini model for tenancy query")
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=[prompt],
            config=GenerateContentConfig(
                system_instruction=[
                    "You're a property tenancy FAQ agent, analyse the image and provide a solution response, but limit the response size to a 100 words, you can give a small response but dont increase it more than 100 words.",
                ]
            ),
        )
        logger.info("Tenancy response generated successfully")
        return response.text
    except Exception as e:
        logger.exception("Tenancy agent generation failed")
        raise Exception(f"Tenancy agent generation failed: {str(e)}")
