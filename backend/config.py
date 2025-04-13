import os
import logging
#from dotenv import load_dotenv
from google import genai

# Configure logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# # Load environment variables from .env file
# load_dotenv()
# logger.info("Environment variables loaded from .env")

API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    logger.error("GEMINI_API_KEY not set in environment variables.")
    raise Exception("GEMINI_API_KEY not set in environment variables.")

logger.info("Initializing Gemini client with provided API key.")
client = genai.Client(api_key=API_KEY)
logger.info("Gemini client initialized successfully.")
