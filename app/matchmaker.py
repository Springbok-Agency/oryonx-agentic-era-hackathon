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

def matchmaker_agent(product_dataframe, trends_news_dataframe):
    '''
    Agent that receives products, google trends and news articles and finds matches between them for marketing purposes.
    '''
    logger.info("Starting matchmaker_agent function.")
    try:
        product_dataframe = json.loads(product_dataframe)
        logger.info("Loaded product_dataframe JSON successfully.")
    except Exception as e:
        logger.error(f"Failed to load product_dataframe JSON: {e}")
        raise

    try:
        trends_news_dataframe = json.loads(trends_news_dataframe)
        logger.info("Loaded trends_news_dataframe JSON successfully.")
    except Exception as e:
        logger.error(f"Failed to load trends_news_dataframe JSON: {e}")
        raise

    genai.configure(api_key="AIzaSyA3fs8OD2JxzzrBb-SyrjUFPJMLxwoNGDw")
    logger.info("Configured generative AI API.")

    model = GenerativeModel("gemini-1.5-flash")
    logger.info("Initialized generative model.")

    system_prompt_sentiment = (
        "You will receive a response from the model that should be a JSON array of news/trends"
        ""
        "You are to delete the sensitive subjects from the json. Sensitive content is defined as any content that could be considered: \n"
        "- violent\n"
        "- sexual\n"
        "- hateful\n"
        "- discriminatory\n"
        "- racist\n"
        "- politically sensitive\n"
        "- religiously sensitive\n"
        "- culturally sensitive\n"
        "- otherwise inappropriate\n"
        ""
        f"This will be your dataset to consider: {trends_news_dataframe}"
        f""
        f"IMPORTANT: Only return the json array, nothing else. Do not add any explanations or additional text. "
        "" )

    logger.info("Sending prompt to model for sensitive subject filtering.")
    news_without_sensitive_subjects = model.generate_content(
        contents=[system_prompt_sentiment]
    )
    logger.info("Received filtered news/trends from model.")

    system_prompt_matching = (
        "You are a witty content strategist. Your task is to find all possible creative, funny, and compelling connections "
        "between products and trending news items using the provided dataframes.\n"
        "You receive two dataframes in json format: one with products, and one with google trends and news articles.\n"
        f"product_dataframe: {json.dumps(product_dataframe)}\n"
        f"trends_news_dataframe: {json.dumps(news_without_sensitive_subjects.text)}\n"
        "Iterate through products and trends/news articles to identify as many matches as possible.\n"
        "For each match, provide:\n"
        "- product_name\n"
        "- trend_title\n"
        "- trend_description\n"
        "- similarity_description: Describe a clear, interesting, and humorous similarity or angle that specifically "
        "mentions both the product and the news item. The connection should be amusing and inspire content creators "
        "to use it.\n"
        "IMPORTANT: Only return the json array, nothing else. Only use the data provided, do not make up any data."
    )

    logger.info("Sending prompt to model for product-news matching.")
    response_matching_process = model.generate_content(
        contents=[system_prompt_matching]
    )
    logger.info("Received matching response from model.")

    try:
        matches = json.loads(response_matching_process.text)
        logger.info("Successfully parsed matches JSON.")
        return matches
    except json.JSONDecodeError:
        logger.error("Error: The model did not return valid JSON.")
        logger.error(f"Raw response: {response_matching_process.text}")
        return None


product_dataframe = '''
[
    {
        "product_id": "1",
        "product_name": "Whole Wheat Bread",
        "product_description": "Freshly baked whole wheat bread loaf.",
        "product_category": "Bakery"
    },
    {
        "product_id": "2",
        "product_name": "Organic Milk",
        "product_description": "1L organic cow milk, pasteurized.",
        "product_category": "Dairy"
    },
    {
        "product_id": "3",
        "product_name": "Free Range Eggs",
        "product_description": "Pack of 12 free range chicken eggs.",
        "product_category": "Dairy"
    },
    {
        "product_id": "4",
        "product_name": "Bananas",
        "product_description": "Fresh yellow bananas, per kg.",
        "product_category": "Produce"
    },
    {
        "product_id": "5",
        "product_name": "Tomato Ketchup",
        "product_description": "500ml bottle of classic tomato ketchup.",
        "product_category": "Condiments"
    },
    {
        "product_id": "6",
        "product_name": "Chicken Breast",
        "product_description": "Boneless skinless chicken breast, per kg.",
        "product_category": "Meat"
    },
    {
        "product_id": "7",
        "product_name": "Cheddar Cheese",
        "product_description": "200g block of mature cheddar cheese.",
        "product_category": "Dairy"
    },
    {
        "product_id": "8",
        "product_name": "Apples",
        "product_description": "Red apples, crisp and juicy, per kg.",
        "product_category": "Produce"
    },
    {
        "product_id": "9",
        "product_name": "Spaghetti Pasta",
        "product_description": "500g pack of dried spaghetti pasta.",
        "product_category": "Pantry"
    },
    {
        "product_id": "10",
        "product_name": "Orange Juice",
        "product_description": "1L bottle of 100% pure orange juice.",
        "product_category": "Beverages"
    }
]
'''

trends_news_dataframe = '''
[
    {
        "trend_id": "1",
        "trend_title": "Prinsjesdag in the Netherlands",
        "trend_description": "Dutch Prinsjesdag is today, marking the annual presentation of the government budget and famous royal hats.",
        "trend_category": "Politics"
    },
    {
        "trend_id": "2",
        "trend_title": "Israel Bombs Gaza",
        "trend_description": "Israel is starting to bomb Gaza amid escalating tensions in the region.",
        "trend_category": "World News"
    },
    {
        "trend_id": "3",
        "trend_title": "Charlie Kirk Murder Suspect Found",
        "trend_description": "Authorities have found a suspect in the murder case of Charlie Kirk.",
        "trend_category": "Crime"
    },
    {
        "trend_id": "4",
        "trend_title": "Famous Hats on Prinsjesdag",
        "trend_description": "A look at all the famous hats worn by Dutch royals and politicians on Prinsjesdag.",
        "trend_category": "Lifestyle"
    },
    {
        "trend_id": "5",
        "trend_title": "CEO Caught Cheating at Coldplay Concert",
        "trend_description": "A famous CEO is caught cheating through a kisscam at a Coldplay concert.",
        "trend_category": "Entertainment"
    },
    {
        "trend_id": "6",
        "trend_title": "Cat Wins Local Election",
        "trend_description": "A cat named Whiskers wins a local election, becoming the honorary mayor for a day.",
        "trend_category": "Fun"
    },
    {
        "trend_id": "7",
        "trend_title": "World's Largest Pancake Flipped",
        "trend_description": "Chefs in Amsterdam flip the world's largest pancake, setting a new record.",
        "trend_category": "Fun"
    },
    {
        "trend_id": "8",
        "trend_title": "Robot Delivers Pizza in Rotterdam",
        "trend_description": "A robot successfully delivers pizza to customers in Rotterdam, delighting locals.",
        "trend_category": "Technology"
    }
]
'''


if __name__ == '__main__':
    logger.info("Script started.")
    matches = matchmaker_agent(product_dataframe, trends_news_dataframe)
    logger.info("Matchmaker agent finished.")
    print(json.dumps(matches, indent=2))