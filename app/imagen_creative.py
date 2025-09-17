import io
import logging
from pathlib import Path
from PIL import Image
from dotenv import load_dotenv
from google import genai
from google.genai import types
from google.genai.types import Part
from google.oauth2 import service_account

# Configure logging
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

# Load environment variables first
dotenv_path = Path(__file__).parent.parent / '.env'
load_dotenv(dotenv_path=dotenv_path)

# Initialize Google Gen AI Client with Vertex AI backend
client = genai.Client(
    vertexai=True,
    project='qwiklabs-gcp-03-3444594577c6',
    location='us-central1',
    credentials=credentials
)


def generate_and_show_images(brandbook: str, marketing_plan: str, number_of_images: int = 1,
                             reference_images: list = None):
    """
    Generates images using the new Google Gen AI SDK with optional reference images.

    Args:
        brandbook: Brand guidelines to follow
        marketing_plan: Description of the marketing campaign
        number_of_images: Number of images to generate
        reference_images: List of image paths or PIL Images to use as reference
    """
    # Base text prompt
    text_prompt = (
        f"Create a high-quality, visually appealing image that represents the following marketing plan: {marketing_plan}. "
        f"The image should be creative, engaging, and suitable for use in a marketing campaign. "
        f"Make sure that the image is relevant to the marketing plan and captures its essence. "
        f"You are allowed to use text in the image. "
        f"Make sure the image aligns with the following brandbook guidelines: {brandbook}."
    )

    if reference_images:
        text_prompt += (
            f" Use the provided reference image(s) as inspiration and incorporate similar elements, "
            f"products, or styling into the new marketing image. The reference images show products "
            f"or elements that should be featured or represented in the generated marketing material."
        )

    try:
        logging.info(f"🎨 Generating {number_of_images} image(s)...")
        if reference_images:
            logging.info(f"📸 Using {len(reference_images)} reference image(s)")
        logging.info(f"📝 Prompt: {text_prompt}")
        logging.info("⏳ Please wait...")

        # Prepare content parts - start with text prompt
        content_parts = [text_prompt]

        # Add reference images if provided
        if reference_images:
            for i, ref_image in enumerate(reference_images):
                try:
                    if isinstance(ref_image, str):
                        # Handle file path
                        with open(ref_image, 'rb') as f:
                            image_data = f.read()
                        content_parts.append(
                            Part.from_bytes(data=image_data, mime_type="image/jpeg")
                        )
                        logging.info(f"   📁 Added local image: {ref_image}")

                    elif isinstance(ref_image, Image.Image):
                        # Handle PIL Image object
                        buffer = io.BytesIO()
                        ref_image.save(buffer, format='JPEG')
                        image_data = buffer.getvalue()
                        content_parts.append(
                            Part.from_bytes(data=image_data, mime_type="image/jpeg")
                        )
                        logging.info(f"   🖼️  Added PIL Image object {i + 1}")

                except Exception as img_error:
                    logging.warning(f"⚠️  Could not load reference image {i + 1}: {img_error}")
                    continue

        response = client.models.generate_images(
            model='imagen-4.0-generate-001',
            prompt=text_prompt,  # Use text_prompt (string) only
            config=types.GenerateImagesConfig(
                aspect_ratio="16:9",
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


if __name__ == '__main__':
    marketing_plan = "promote the gift card as a perfect present for any occasion, highlighting its versatility and ease of use. use the slogan; om van elke dag een cadeautje te maken (make every day a gift). the target audience is people looking for a convenient and thoughtful gift option for friends and family. the campaign should emphasize the wide range of products available on bol.com that can be purchased with the gift card, making it an ideal choice for birthdays, holidays, and special celebrations."
    brandbook_bol = ("Use colors blue and white, modern and sleek design, minimalistic style, text in bold Arial font. "
                     "The brand is called Rond.com and is a leading e-commerce platform in the Netherlands, known for its wide range of products ")

    logging.info("=" * 60)
    logging.info("🎨 IMAGEN AI - MARKETING IMAGE GENERATOR (MIGRATED)")
    logging.info("=" * 60)
    logging.info("🔄 Now using Google Gen AI SDK instead of deprecated Vertex AI SDK")

    reference_image_paths = [
        "bol.com-cadeaukaart-relatiegeschenk.jpg",
        "Logo_bol.jpg"
    ]
    generate_and_show_images(brandbook_bol, marketing_plan, number_of_images=3, reference_images=reference_image_paths)