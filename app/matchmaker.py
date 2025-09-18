import json
import logging
import os

import google.auth
import google.generativeai as genai
from dotenv import load_dotenv
from google.generativeai import GenerativeModel

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

load_dotenv()

# The user has a .env file, so let's use environment variables for the API key.
if os.getenv("GEMINI_API_KEY"):
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
else:
    # Fallback to default auth if key not in .env
    _, project_id = google.auth.default()
    os.environ.setdefault("GOOGLE_CLOUD_PROJECT", project_id)


def matchmaker_agent(
    product_dataframe_str: str, trends_news_dataframe_str: str
) -> str:
    """
    Matches products to trending topics and news for marketing purposes.

    Args:
        product_dataframe_str (str): JSON string of product data.
        trends_news_dataframe_str (str): JSON string of trends and news data.

    Returns:
        list[dict]: Each dict contains:
            - product_name (str)
            - trend_title (str)
            - trend_description (str)
            - similarity_description (str)
        Returns an empty list if no matches are found or on error.
    """
    logger.info("Starting matchmaker_agent function.")

    model = GenerativeModel("gemini-2.5-flash")
    logger.info("Initialized generative model.")

    system_prompt_sentiment = f"""You will receive a response from the model that should be a JSON array of news/trends.

    You are to delete the sensitive subjects from the json. Sensitive content is defined as any content that could be considered:
    - violent
    - sexual
    - hateful
    - discriminatory
    - racist
    - politically sensitive
    - religiously sensitive
    - culturally sensitive
    - otherwise inappropriate

    This will be your dataset to consider: {trends_news_dataframe_str}

    IMPORTANT: Only return the json array, nothing else. Do not add any explanations or additional text.
    """

    logger.info("Sending prompt to model for sensitive subject filtering.")
    news_without_sensitive_subjects = model.generate_content(
        contents=[system_prompt_sentiment]
    )
    logger.info("Received filtered news/trends from model.")

    filtered_news_obj = json.loads(news_without_sensitive_subjects.text)
    trends_news_dataframe_str = json.dumps(filtered_news_obj)



    system_prompt_matching = f"""You are a witty content strategist. Your task is to find creative, funny, and compelling connections between products and trending news items using the provided dataframes.

    You receive two dataframes in JSON format: one with products, and one with Google trends and news articles.
    product_dataframe_str: {product_dataframe_str}
    trends_news_dataframe_str: {trends_news_dataframe_str}

    Your job is to critically evaluate each possible match. Only create a match if there is a clear, logical, and relevant and funny connection between the product and the news/trend item. Avoid forced or nonsensical matches. Do not match items that have no meaningful or interesting relationship.

    For each match, provide:
    - product_name
    - trend_title
    - trend_description
    - similarity_description: Describe a clear, interesting, and humorous similarity or angle that specifically mentions both the product and the news item. The connection should be amusing and inspire content creators to use it.

    IMPORTANT:
    - Only return the JSON array, nothing else.
    - Only use the data provided, do not make up any data.
    - Do not make more than 10 matches.
    - If no good matches exist, return an empty array.
    """

    logger.info("Sending prompt to model for product-news matching.")
    response_matching_process = model.generate_content(
        contents=[system_prompt_matching]
    )
    logger.info("Received matching response from model.")

    return response_matching_process.text
