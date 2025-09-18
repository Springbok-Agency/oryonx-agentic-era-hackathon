import logging
import os

import google.auth
from google.genai import Client, types

_, project_id = google.auth.default()
os.environ.setdefault("GOOGLE_CLOUD_PROJECT", project_id)
os.environ.setdefault("GOOGLE_CLOUD_LOCATION", "global")
os.environ.setdefault("GOOGLE_GENAI_USE_VERTEXAI", "True")

# Initialize the Gen AI client
client = Client(
    location="us-central1"
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)





def generate_and_show_images(
    marketing_plan: str, brandbook: str = "", number_of_images: int = 1
):
    """
    Generates images using Google Gen AI Imagen model and saves them to GCS bucket.

    Args:
        marketing_plan: Description of the marketing campaign
        brandbook: Optional brand guidelines to follow. If None, uses default brand guide.
        number_of_images: Number of images to generate

    Returns:
        list: List of generated image objects with URIs pointing to GCS bucket
    """
    
    if not brandbook:
        brandbook = (
            """
            Brand Guide: The Taste of Home

            Goal:
            Create a consistent social media presence that is Artisanal, Warm, Authentic, and Personal.

            ------------------------------------------------------------
            1. Color Palette: Earthy & Fresh
            ------------------------------------------------------------
            Primary Colors:
            Terracotta Orange (#D97D51)
            Forest Green (#3A5A40)
            Cream White (#F4F1DE)

            Accent Colors:
            Golden Yellow (#FFC300)
            Soft Blue (#A8DADC)

            ------------------------------------------------------------
            2. Typography: Classic & Clean
            ------------------------------------------------------------
            Headlines: Use a classic serif font (e.g., Lora or Playfair Display)
            Body & Prices: Use a clean sans-serif font (e.g., Lato or Montserrat)

            ------------------------------------------------------------
            3. Photography & Video: Natural & Fun
            ------------------------------------------------------------
            Visual Style:
            Warm and inviting visuals
            Use soft, natural daylight
            Focus on texture and high-quality ingredients
            Natural backgrounds (wood, linen, stone)

            Guidelines:
            Capture genuine, joyful moments with products
            (e.g., tasting, baking, hands-on interactions)
            Include helpful tips in short videos or overlays
            Avoid overly posed or corporate imagery

            ------------------------------------------------------------
            4. Tone of Voice: Warm & Personal
            ------------------------------------------------------------
            Use a conversational, human tone
            Write from a first-person or inclusive "we" perspective

            Example Caption:
            "Mijn absolute favoriet voor het weekend: onze oude boerenkaas. Ik eet 'm het liefst zo uit het vuistje. Geniet ervan!"

            Keywords to Use:
            Enjoy
            Discover
            Tip
            Delicious

            Calls-to-Action:
            Try our favorite
            Let us know what you think!
            Taste the difference
            """
        )

    text_prompt = (
        f"Create a high-quality, visually appealing image that represents the following marketing plan: {marketing_plan}. "
        f"From this marketing plan, use the part that describes the core message or theme to inspire the image. "
        f"The image should be creative, engaging, and suitable for use in a marketing campaign. "
        f"Make sure that the image is relevant to the marketing plan and captures its essence. "
        f"You are allowed to use text in the image. "
        f"Make sure the image aligns with the following brandbook guidelines: {brandbook}."
    )

    logging.info(f"Generating {number_of_images} image(s)...")
    logging.info(f"📝 Prompt: {text_prompt}")
    logging.info("⏳ Please wait...")

    response = client.models.generate_images(
        model="imagen-4.0-generate-001",
        prompt=text_prompt,
        config=types.GenerateImagesConfig(
            aspect_ratio="9:16",
            number_of_images=number_of_images,
            image_size="2k",
            enhance_prompt=True,
            safety_filter_level="BLOCK_ONLY_HIGH",
            person_generation="ALLOW_ALL",
            output_gcs_uri="gs://hackathon_agent_oryonx/images/"
        ),
    )

    logging.info(
        f"Successfully generated {len(response.generated_images)} image(s)!"
    )

    # Convert GCS URIs to public HTTP URLs and log them
    result_images = []
    for i, generated_image in enumerate(response.generated_images):
        if hasattr(generated_image, 'image') and hasattr(generated_image.image, 'uri'):
            image_uri = generated_image.image.uri
            logging.info(f"Image {i + 1} URI: {image_uri}")
            
            # Convert GCS URI to public HTTP URL
            if image_uri.startswith("gs://"):
                bucket_name = image_uri.split("/")[2]
                object_name = "/".join(image_uri.split("/")[3:])
                public_url = f"https://storage.googleapis.com/{bucket_name}/{object_name}"
                logging.info(f"Image {i + 1} public URL: {public_url}")
                
                result_images.append({
                    "image_uri": image_uri,
                    "public_url": public_url,
                    "bucket": bucket_name,
                    "object": object_name
                })
            else:
                result_images.append({"image_uri": image_uri})
        else:
            logging.info(f"Image {i + 1} generated successfully")
            result_images.append(generated_image)
    
    logging.info(
        f"All {len(response.generated_images)} image(s) generated successfully and saved to GCS bucket."
    )
    return result_images


if __name__ == "__main__":
    marketing_plan = "promote the gift card as a perfect present for any occasion, highlighting its versatility and ease of use. use the slogan; om van elke dag een cadeautje the maken (make every day a gift). the target audience is people looking for a convenient and thoughtful gift option for friends and family. the campaign should emphasize the wide range of products available on bol.com that can be purchased with the gift card, making it an ideal choice for birthdays, holidays, and special celebrations."

    logging.info("=" * 60)
    logging.info("IMAGEN AI - MARKETING IMAGE GENERATOR")
    logging.info("=" * 60)

    images = generate_and_show_images(marketing_plan, brandbook=None, number_of_images=1)
    logging.info(f"Images generated successfully: {len(images)} image(s)")
