import datetime
import os
from zoneinfo import ZoneInfo
import json
import logging
import google.adk.agents
import google.auth
from dotenv import load_dotenv
from google.adk import Agent
from google.generativeai import GenerativeModel
import google.generativeai as genai

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)
logger = logging.getLogger(__name__)

load_dotenv()

_, project_id = google.auth.default()
# os.environ.setdefault("GOOGLE_CLOUD_PROJECT", project_id)
# os.environ.setdefault("GOOGLE_CLOUD_LOCATION", "global")
# os.environ.setdefault("GOOGLE_GENAI_USE_VERTEXAI", "True")


def marketing_agent(matchmaker_output, lmm_model=None, num_concepts=3):
  """
  Calls the LMM (GenerativeModel) to create three marketing concepts for social media posts for Instagram, both image and video.
  Each concept includes: a marketing plan, a funny tagline, and the product name.
  """
  if lmm_model is None:
    genai.configure(api_key="AIzaSyA3fs8OD2JxzzrBb-SyrjUFPJMLxwoNGDw")
    lmm_model = GenerativeModel("gemini-1.5-flash")

    prompt = (
        "You are a creative marketing agent. Using the following product-news matches, generate ONE comprehensive marketing plan PER product-news item as a story that can be shared internally with stakeholders and is ready for direct implementation by the marketing team. "
        "For each selected match, generate a separate marketing plan as a distinct text variable. "
        "Select the three best matches based on how well the product connects to the news item and the fun factor. "
        "Do NOT summarize or generalize; instead, weave all points into a concrete, actionable narrative. "
        "Your output should include:\n"
        "- A vivid description of the news items and their connection to the products.\n"
        "- A clear marketing strategy, including purpose, timing, and target audience.\n"
        "- The main tagline, seamlessly integrated into the story and should have a clear reference to the news item to make the connection clear to the audience.\n"
        "- Detailed ideas for both an Instagram image and video post, with the main tagline included. The image and video concepts should be funny, and clearly reference the news item in a creative way.\n"
        "- A catchy Instagram caption ready for posting.\n"
        "Use the following matches:\n" + json.dumps(matchmaker_output[:num_concepts], indent=2) +
        "\nIMPORTANT: Return only the three marketing plans as three, well-written stories and make sure you ask the end user which of the three marketing plans they prefer for further implementation."
    )

  response = lmm_model.generate_content(contents=[prompt])
  try:
    concepts = json.loads(response.text)
    return concepts
  except Exception as e:
    logger.error(f"Failed to parse LMM response: {e}")
    logger.error(f"Raw response: {response.text}")
    return None


matchmaker_dataframe = '''
[
  {
    "product_name": "Whole Wheat Bread",
    "trend_title": "World's Largest Pancake Flipped",
    "trend_description": "Chefs in Amsterdam flip the world's largest pancake, setting a new record.",
    "similarity_description": "From whole wheat bread to the world's largest pancake – both require a bit of kneading (and maybe a *lot* of flipping) to reach perfection!  Imagine a whole wheat pancake – now *that's* a healthy record breaker."
  },
  {
    "product_name": "Organic Milk",
    "trend_title": "Cat Wins Local Election",
    "trend_description": "A cat named Whiskers wins a local election, becoming the honorary mayor for a day.",
    "similarity_description": "Whiskers the cat, the new mayor, might need a glass of organic milk to celebrate. After all, even the most purr-fect politician needs some refueling!"
  },
  {
    "product_name": "Free Range Eggs",
    "trend_title": "World's Largest Pancake Flipped",
    "trend_description": "Chefs in Amsterdam flip the world's largest pancake, setting a new record.",
    "similarity_description": "The world's largest pancake? It probably took a LOT of free-range eggs!  Let's just hope they were ethically sourced, for a truly record-breaking breakfast."
  },
  {
    "product_name": "Bananas",
    "trend_title": "Cat Wins Local Election",
    "trend_description": "A cat named Whiskers wins a local election, becoming the honorary mayor for a day.",
    "similarity_description": "Mayor Whiskers' campaign slogan?  'Going bananas for a better tomorrow!'  (He might have also enjoyed a potassium-rich banana snack during the election campaign)."
  },
  {
    "product_name": "Tomato Ketchup",
    "trend_title": "World's Largest Pancake Flipped",
    "trend_description": "Chefs in Amsterdam flip the world's largest pancake, setting a new record.",
    "similarity_description": "What's better than a giant pancake? A giant pancake with a generous dollop of ketchup! (Okay, maybe not, but it's fun to imagine the possibilities.)"
  },
  {
    "product_name": "Chicken Breast",
    "trend_title": "Robot Delivers Pizza in Rotterdam",
    "trend_description": "A robot successfully delivers pizza to customers in Rotterdam, delighting locals.",
    "similarity_description": "A robot delivering pizza... soon they'll be delivering chicken breast too!  Imagine the efficiency – no more waiting in line at the butcher's."
  },
  {
    "product_name": "Cheddar Cheese",
    "trend_title": "World's Largest Pancake Flipped",
    "trend_description": "Chefs in Amsterdam flip the world's largest pancake, setting a new record.",
    "similarity_description": "A savoury twist on a sweet classic! Imagine a giant cheddar cheese pancake – maybe not a new record, but definitely a new culinary adventure."
  },
  {
    "product_name": "Apples",
    "trend_title": "Prinsjesdag in the Netherlands",
    "trend_description": "Dutch Prinsjesdag is today, marking the annual presentation of the government budget and famous royal hats.",
    "similarity_description": "An apple a day keeps the doctor away... and maybe even keeps the Dutch royal budget in check?  We're reaching for a delicious connection here!"
  },
  {
    "product_name": "Spaghetti Pasta",
    "trend_title": "Cat Wins Local Election",
    "trend_description": "A cat named Whiskers wins a local election, becoming the honorary mayor for a day.",
    "similarity_description": "Mayor Whiskers' inauguration feast?  A mountain of spaghetti, naturally. After all, even a feline leader deserves some delicious carbs."
  },
  {
    "product_name": "Orange Juice",
    "trend_title": "Prinsjesdag in the Netherlands",
    "trend_description": "Dutch Prinsjesdag is today, marking the annual presentation of the government budget and famous royal hats.",
    "similarity_description": "Toasted to the Dutch budget with a glass of refreshing orange juice!  A vitamin C boost for a day of royal pronouncements and political debate."
  }
]
'''


if __name__ == '__main__':
  # Example: use the first three matches from matchmaker_dataframe
  matchmaker_output = json.loads(matchmaker_dataframe)
  concepts = marketing_agent(matchmaker_output)
  print(concepts)
#   if concepts:
#     for i, concept in enumerate(concepts, 1):
#       print(f"Concept {i}:")
#       print(f"Product: {concept['product']}")
#       print(f"Tagline: {concept['tagline']}")
#       print(f"Marketing Plan:\n{concept['marketing_plan']}")
#       print("-"*40)