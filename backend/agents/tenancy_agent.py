import logging
from config import client
from utils.rag import retrieve_context
from google.genai.types import GenerateContentConfig


logger = logging.getLogger(__name__)

TENANCY_PROMPT_TEMPLATE = (
    "You are a legal and property management expert specializing in tenancy laws and rental agreements.\n"
    "Conversation History and Context: {context}\n"
    "User Query: {query}\n"
    "Provide a comprehensive, legally informed answer including any necessary legal conditions and practical advice. "
    "If relevant, ask if more location-specific information is needed."
)

def process_tenancy_query(query: str, combined_context: str = "") -> str:
    """
    Processes tenancy-related queries using context and RAG.

    Args:
        query (str): The tenancy-related question from the user.
        combined_context (str): Context from conversation history + RAG.

    Returns:
        str: Generated response from the tenancy agent.
    """
    logger.info("Starting process_tenancy_query with query: %s", query)

    prompt = TENANCY_PROMPT_TEMPLATE.format(context=combined_context, query=query)
    logger.info("Constructed prompt for tenancy query")

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
        logger.exception("Tenancy Agent generation failed")
        raise Exception(f"Tenancy Agent generation failed: {str(e)}")
