import io
import logging
from config import client
from google.genai.types import GenerateContentConfig

logger = logging.getLogger(__name__)

def process_property_issue(query: str, image_bytes: bytes, combined_context: str = "", mime_type: str = "image/jpeg") -> str:
    """
    Processes a property issue query by sending both text and an image to the Gemini model.

    Args:
        query (str): The textual component of the user query.
        image_bytes (bytes): Raw bytes of the uploaded image.
        combined_context (str): Context from previous conversation + RAG.
        mime_type (str): The MIME type of the image.

    Returns:
        str: Response from the Gemini model.
    """
    logger.info("Starting process_property_issue")

    image_stream = io.BytesIO(image_bytes)

    try:
        logger.info("Uploading image with MIME type: %s", mime_type)
        uploaded_file = client.files.upload(file=image_stream, config={"mime_type": mime_type})
        logger.info("Image uploaded successfully")
    except Exception as e:
        logger.exception("Image upload failed")
        raise Exception(f"Image upload failed: {str(e)}")

    prompt = (
        f"Conversation History and Context:\n{combined_context}\n"
        f"User Query: {query}\n"
        "Analyze the provided image for property issues (e.g., water damage, mold, cracks, poor lighting, broken fixtures). "
        "Return a troubleshooting diagnosis and recommendations."
    )

    logger.info("Constructed prompt for property issue")

    try:
        logger.info("Generating response using Gemini model for property issue")
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=[prompt, uploaded_file],
            config=GenerateContentConfig(
                system_instruction=[
                    "You're a property damage resolvent agent, analyse the image and provide a solution response, but limit the response size to a 100 words, you can give a small response but dont increase it more than 100 words.",
                ]
            ),
        )
        logger.info("Response generated successfully for property issue")
        return response.text
    except Exception as e:
        logger.exception("Property Agent generation failed")
        raise Exception(f"Property Agent generation failed: {str(e)}")
