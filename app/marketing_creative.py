import json
import logging
import os

import google.adk.agents
import google.auth
import google.generativeai as genai
from dotenv import load_dotenv
from google.generativeai import GenerativeModel

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

load_dotenv()

_, project_id = google.auth.default()


# The user has a .env file, so let's use environment variables for the API key.
if os.getenv("GEMINI_API_KEY"):
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
else:
    # Fallback to default auth if key not in .env
    _, project_id = google.auth.default()
    os.environ.setdefault("GOOGLE_CLOUD_PROJECT", project_id)


def marketing_agent(matchmaker_output: str, num_concepts: int = 3) -> str:
    """
    Calls the LMM (GenerativeModel) to create three marketing concepts for social media posts for Instagram, both image and video.
    Each concept includes: a marketing plan, a funny tagline, and the product name.
    Returns a dictionary of concepts.
    """
    lmm_model = GenerativeModel("gemini-2.5-flash")

    prompt = (
        "You are a creative marketing agent. Using the following product-news matches, generate ONE comprehensive marketing plan PER product-news item as a story that can be shared internally with stakeholders and is ready for direct implementation by the marketing team. "
        "For each selected match, generate a separate marketing plan as a distinct text variable. "
        "Select the three best matches based on how well the product connects to the news item and the fun factor. "
        "Do NOT summarize or generalize; instead, weave all points into a concrete, actionable narrative. "
        "Your output should include:\n"
        "- A vivid description of the news items and their connection to the products.\n"
        "- A clear marketing strategy, including purpose, timing, and target audience.\n"
        "- The main tagline, seamlessly integrated into the story and should have a clear reference to the news item to make the connection clear to the audience.\n"
        "- Detailed ideas for both an Instagram image and video post, with the main tagline included. "
        "For the image post, provide:\n"
        "  - Subject: Who or what is in the scene (person, animal, object, or landscape). Make sure it references the product and news item.\n"
        "  - Context: Where is the subject? (indoors, city street, forest, etc.) Make sure it references the news item.\n"
        "  - Action: What is happening in the image? Make sure it references the product and news item.\n"
        "  - Style: The visual aesthetic (cinematic, animated, stop-motion, etc.). Make sure it references the product and news item.\n"
        "  - Composition: How the shot is framed (wide shot, close-up, etc.). \n"
        "  - Ambiance: Mood and lighting (warm tones, blue light, nighttime, etc.).\n"
        "  - Make sure the main tagline is mentioned and both the news item and product are clearly referenced.\n"
        "For the video post, provide:\n"
        "  - Subject: Who or what is in the scene (person, animal, object, or landscape). Make sure it references the product and news item.\n"
        "  - Context: Where is the subject? (indoors, city street, forest, etc.) Make sure it references the news item.\n"
        "  - Action: What is the subject doing (walking, jumping, turning their head, etc.). Make sure it references the product and news item.\n"
        "  - Style: The visual aesthetic (cinematic, animated, stop-motion, etc.).\n"
        "  - Camera motion: How the camera moves (aerial shot, eye-level, top-down, low-angle, etc.).\n"
        "  - Composition: How the shot is framed (wide shot, close-up, etc.).\n"
        "  - Ambiance: Mood, music and lighting (warm tones, blue light, nighttime, etc.).\n"
        "  - Make sure the main tagline is mentioned and both the news item and product are clearly referenced.\n"
        "- A catchy Instagram caption ready for posting.\n"
        "Use the following matches:\n"
        + json.dumps(matchmaker_output[:num_concepts], indent=2)
        + "\nIMPORTANT: Return only the three marketing plans as three, well-written stories and make sure you ask the end user which of the three marketing plans they prefer for further implementation."
    )

    response = lmm_model.generate_content(contents=[prompt])
    
    return response.text
    