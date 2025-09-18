import io
import logging
from pathlib import Path
from PIL import Image
from dotenv import load_dotenv
from google import genai
from google.genai import types
from google.genai.types import Part
from google.oauth2 import service_account

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

credentials = service_account.Credentials.from_service_account_file(
    'service-account.json',
    scopes=[
        'https://www.googleapis.com/auth/cloud-platform',
        'https://www.googleapis.com/auth/generative-language'
    ]
)

dotenv_path = Path(__file__).parent.parent / '.env'
load_dotenv(dotenv_path=dotenv_path)

client = genai.Client(
    vertexai=True,
    project='qwiklabs-gcp-03-3444594577c6',
    location='us-central1',
    credentials=credentials
)


def generate_and_show_images(brandbook: str, marketing_plan: str, number_of_images: int = 1):
    """
    Generates images using the new Google Gen AI SDK with optional reference images.

    Args:
        brandbook: Brand guidelines to follow
        marketing_plan: Description of the marketing campaign
        number_of_images: Number of images to generate
    """

    text_prompt = (
        f"Create a high-quality, visually appealing image that represents the following marketing plan: {marketing_plan}. "
        f"From this marketing plan, use the part that describes the core message or theme to inspire the image. "
        f"The image should be creative, engaging, and suitable for use in a marketing campaign. "
        f"Make sure that the image is relevant to the marketing plan and captures its essence. "
        f"You are allowed to use text in the image. "
        f"Make sure the image aligns with the following brandbook guidelines: {brandbook}."
    )

    try:
        logging.info(f"🎨 Generating {number_of_images} image(s)...")
        logging.info(f"📝 Prompt: {text_prompt}")
        logging.info("⏳ Please wait...")

        response = client.models.generate_images(
            model='imagen-4.0-generate-001',
            prompt=text_prompt,
            config=types.GenerateImagesConfig(
                aspect_ratio="9:16",
                number_of_images=number_of_images,
                image_size="2k",
                enhance_prompt=True,
                safety_filter_level="BLOCK_ONLY_HIGH",
                person_generation="ALLOW_ALL",
            ),
        )

        logging.info(f"✅ Successfully generated {len(response.generated_images)} image(s)!")

        # Display each image
        for i, generated_image in enumerate(response.generated_images):
            logging.info(f"🖼️  Opening Image {i + 1} in your default image viewer...")
            pil_image = generated_image.image
            pil_image.show()

        logging.info(f"🎉 All {len(response.generated_images)} image(s) should now be open in your image viewer.")
        return response.generated_images

    except Exception as e:
        logging.error(f"❌ Error generating images: {str(e)}")
        return {"error": str(e)}
