import logging
import os
import platform
import subprocess
import time

import google.auth
from google.genai import types
from google.genai import Client


_, project_id = google.auth.default()
os.environ.setdefault("GOOGLE_CLOUD_PROJECT", project_id)
os.environ.setdefault("GOOGLE_CLOUD_LOCATION", "global")
os.environ.setdefault("GOOGLE_GENAI_USE_VERTEXAI", "True")

# Initialize the Gen AI client
client = Client()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)



def generate_and_show_video(marketing_plan: str):
    """
    Generates video using the new Google Gen AI SDK with optional reference images.

    Args:
        marketing_plan: Description of the marketing campaign
    """

    text_prompt = (
        f"Create a high-quality, visually appealing video that represents the following marketing plan: {marketing_plan}. "
        f"The video should be creative, engaging, and suitable for use in a marketing campaign. "
        f"Make sure that the video is relevant to the marketing plan and captures its essence. "
        f"You are allowed to use text in the video."
        f"Make sure the video aligns with the following brandbook guidelines."
    )

    try:
        logging.info(f"📝 Prompt: {text_prompt}")
        logging.info("⏳ Please wait...")

        operation = client.models.generate_videos(
            model="veo-3.0-fast-generate-001",
            prompt=text_prompt,
            config=types.GenerateVideosConfig(aspectRatio="9:16"),
        )

        while not operation.done:
            logging.info("Waiting for video generation to complete...")
            time.sleep(20)
            operation = client.operations.get(operation)

        video_path = "marketing_video.mp4"

        generated_video = operation.response.generated_videos[0]
        client.files.download(file=generated_video.video)
        generated_video.video.save("marketing_video.mp4")
        logging.info(
            "Successfully generated video and saved to videos/marketing_video.mp4"
        )

        logging.info("Video generated successfully and saved to marketing_video.mp4")
        return operation.response.generated_videos[0]

    except Exception as e:
        logging.error(f"Error generating video: {e!s}")
        return {"error": str(e)}


if __name__ == "__main__":
    marketing_plan = """
    **Marketing Plan 2: Organic Milk & Cat Mayor**

    **Story:**  The internet is melting! A cat named Whiskers just won a local election, becoming the honorary mayor for a day.  This furry leader proves that even the most unconventional candidates can win hearts (and votes!). And what does a hard-working (and adorable) mayor deserve after a long day of campaigning?  A refreshing glass of our Organic Milk, of course!  It's the purr-fect way to celebrate a victory, no matter how unexpected.

    **Purpose:** To associate our Organic Milk with the heartwarming and viral story of Whiskers the cat mayor, emphasizing the product's wholesome and refreshing qualities.

    **Timing:**  While the Whiskers story is trending on social media.

    **Target Audience:**  Cat lovers, people who appreciate wholesome products, and those who enjoy sharing lighthearted and feel-good content.

    **Tagline:**  "Whiskers Won the Election, and You'll Win with Our Organic Milk!"


    **Instagram Image Post:**

    **Subject:**  A cute cat (ideally resembling Whiskers) enjoying a small bowl of Organic Milk.
    **Context:** A miniature mayoral office, complete with a tiny desk and chair.
    **Action:** The cat is contentedly lapping up the milk.
    **Style:**  Cute and whimsical, cartoonish, with a touch of vintage charm.
    **Composition:**  Close-up shot focusing on the cat and milk bowl.
    **Ambiance:**  Warm and soft lighting, creating a cozy and playful atmosphere.


    **Instagram Video Post:**

    **Subject:** A montage of short clips of a cat (ideally resembling Whiskers) in different mayoral scenarios: sitting in a tiny chair, “signing” documents, wearing a miniature mayoral sash, and finally enjoying a glass of Organic Milk.
    **Context:**  A set designed like a miniature city hall.
    **Action:** The cat gracefully moves about the miniature office, looking regal and content, and then finally drinks some milk.
    **Style:**  A lighthearted and playful style, with upbeat music.
    **Camera Motion:**  A mix of close-ups and wide shots, with smooth transitions between scenes.
    **Composition:**  A variety of shots to showcase the cat's "mayoral duties" and milk-drinking moment.
    **Ambiance:** Upbeat, playful music; soft, bright lighting.


    **Instagram Caption:**  "Even the purr-fect mayor needs a little refueling! Celebrate Whiskers’ victory (and your day) with our Organic Milk. #CatMayor #WhiskersWins #OrganicGoodness #HappyCatsHappyHumans"
        """
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

    logging.info("=" * 60)
    logging.info("🎨 VEO AI - MARKETING VIDEO GENERATOR")
    logging.info("=" * 60)

    generate_and_show_video(brandbook, marketing_plan)
