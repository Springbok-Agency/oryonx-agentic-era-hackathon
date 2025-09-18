import logging
import os

import google.auth
from dotenv import load_dotenv
from google.adk.agents import LlmAgent
from google.adk.tools import AgentTool, FunctionTool
from google.genai import types

from app.product_data_retriever import get_product_data

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

load_dotenv()

# The user has a .env file, so let's use environment variables for the API key.
if not os.getenv("GEMINI_API_KEY"):
    # Fallback to default auth if key not in .env
    _, project_id = google.auth.default()
    os.environ.setdefault("GOOGLE_CLOUD_PROJECT", project_id)


# Sensitive content filter agent
sensitive_content_filter = LlmAgent(
    name="sensitive_content_filter",
    model="gemini-2.5-flash",
    instruction="""You are a content filter that removes sensitive subjects from news/trends data.

    You will receive a JSON array of news/trends and must filter out any content that could be considered:
    - violent
    - sexual
    - hateful
    - discriminatory
    - racist
    - politically sensitive
    - religiously sensitive
    - culturally sensitive
    - otherwise inappropriate

    IMPORTANT: Only return the filtered JSON array, nothing else. Do not add any explanations or additional text.
    """,
    generate_content_config=types.GenerateContentConfig(
        temperature=0.1,  # Low temperature for consistent filtering
        max_output_tokens=1000,
        safety_settings=[
            types.SafetySetting(
                category=types.HarmCategory.HARM_CATEGORY_HARASSMENT,
                threshold=types.HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
            ),
            types.SafetySetting(
                category=types.HarmCategory.HARM_CATEGORY_HATE_SPEECH,
                threshold=types.HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
            ),
            types.SafetySetting(
                category=types.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT,
                threshold=types.HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
            ),
            types.SafetySetting(
                category=types.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
                threshold=types.HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
            ),
            types.SafetySetting(
                category=types.HarmCategory.HARM_CATEGORY_CIVIC_INTEGRITY,
                threshold=types.HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
            ),
        ],
    ),
)

# Product-trend matcher agent
product_trend_matcher = LlmAgent(
    name="product_trend_matcher",
    model="gemini-2.5-flash",
    instruction="""You are a witty content strategist. Your task is to find creative, funny, and compelling connections between products and trending news items.

    You will receive two JSON datasets: one with products, and one with Google trends and news articles.

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
    """,
    generate_content_config=types.GenerateContentConfig(
        temperature=0.3,  # Slightly higher for creative matching
        max_output_tokens=2000,
        safety_settings=[
            types.SafetySetting(
                category=types.HarmCategory.HARM_CATEGORY_HARASSMENT,
                threshold=types.HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
            ),
            types.SafetySetting(
                category=types.HarmCategory.HARM_CATEGORY_HATE_SPEECH,
                threshold=types.HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
            ),
            types.SafetySetting(
                category=types.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT,
                threshold=types.HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
            ),
            types.SafetySetting(
                category=types.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
                threshold=types.HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
            ),
            types.SafetySetting(
                category=types.HarmCategory.HARM_CATEGORY_CIVIC_INTEGRITY,
                threshold=types.HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
            ),
        ],
    ),
)

# Main matchmaker agent that orchestrates the process
matchmaker_agent = LlmAgent(
    name="matchmaker_agent",
    model="gemini-2.5-flash",
    instruction="""You are a marketing matchmaker that finds connections between products and trending topics.

    You can receive trends/news data as input, and you have access to get_product_data to fetch product information.

    Your process:
    1. If you receive trends/news data, first filter it to remove sensitive content
    2. Fetch product data using the get_product_data tool
    3. Find creative matches between products and the filtered trends
    4. Return the matches as a JSON array

    Each match should contain:
    - product_name
    - trend_title
    - trend_description
    - similarity_description

    Return only the final JSON array of matches, nothing else.
    """,
    tools=[AgentTool(sensitive_content_filter), AgentTool(product_trend_matcher), FunctionTool(func=get_product_data)],
    generate_content_config=types.GenerateContentConfig(
        temperature=0.2,  # Balanced for orchestration
        max_output_tokens=1500,
        safety_settings=[
            types.SafetySetting(
                category=types.HarmCategory.HARM_CATEGORY_HARASSMENT,
                threshold=types.HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
            ),
            types.SafetySetting(
                category=types.HarmCategory.HARM_CATEGORY_HATE_SPEECH,
                threshold=types.HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
            ),
            types.SafetySetting(
                category=types.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT,
                threshold=types.HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
            ),
            types.SafetySetting(
                category=types.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
                threshold=types.HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
            ),
            types.SafetySetting(
                category=types.HarmCategory.HARM_CATEGORY_CIVIC_INTEGRITY,
                threshold=types.HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
            ),
        ],
    ),
)
