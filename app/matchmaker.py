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
) -> dict:
    """
    Agent that receives products, google trends and news articles and finds matches between them for marketing purposes.

    Args:
        product_dataframe_str: A JSON string representing a dataframe of products.
        trends_news_dataframe_str: A JSON string representing a dataframe of trends and news.

    Returns:
        A dictionary of matches. In case of an error, a dictionary with an error message is returned.
    """
    logger.info("Starting matchmaker_agent function.")
    try:
        product_dataframe = json.loads(product_dataframe_str)
        logger.info("Loaded product_dataframe JSON successfully.")
    except json.JSONDecodeError as e:
        logger.error(f"Failed to load product_dataframe JSON: {e}")
        raise

    try:
        trends_news_dataframe = json.loads(trends_news_dataframe_str)
        logger.info("Loaded trends_news_dataframe JSON successfully.")
    except json.JSONDecodeError as e:
        logger.error(f"Failed to load trends_news_dataframe JSON: {e}")
        raise

    # TODO: Use 2.5 Flash
    model = GenerativeModel("gemini-1.5-flash")
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

    This will be your dataset to consider: {trends_news_dataframe}

    IMPORTANT: Only return the json array, nothing else. Do not add any explanations or additional text.
    """

    logger.info("Sending prompt to model for sensitive subject filtering.")
    news_without_sensitive_subjects = model.generate_content(
        contents=[system_prompt_sentiment]
    )
    logger.info("Received filtered news/trends from model.")

    product_dataframe_json = json.dumps(product_dataframe)
    try:
        # The model might return a string that is a JSON-encoded string.
        # Loading it and dumping it again can normalize it.
        filtered_news_obj = json.loads(news_without_sensitive_subjects.text)
        trends_news_dataframe_json = json.dumps(filtered_news_obj)
    except json.JSONDecodeError:
        # If it's not a valid JSON string, use the raw text.
        trends_news_dataframe_json = json.dumps(news_without_sensitive_subjects.text)

    system_prompt_matching = f"""You are a witty content strategist. Your task is to find creative, funny, and compelling connections between products and trending news items using the provided dataframes.

    You receive two dataframes in JSON format: one with products, and one with Google trends and news articles.
    product_dataframe: {product_dataframe_json}
    trends_news_dataframe: {trends_news_dataframe_json}

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

    try:
        matches = json.loads(response_matching_process.text)
        logger.info("Successfully parsed matches JSON.")
        return matches
    except json.JSONDecodeError:
        logger.error("Error: The model did not return valid JSON.")
        logger.error(f"Raw response: {response_matching_process.text}")
        return {
            "error": "Failed to parse model response as JSON",
            "raw_response": response_matching_process.text,
        }
