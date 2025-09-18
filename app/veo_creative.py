import logging
import time
from pathlib import Path
import os
import platform
import subprocess
from dotenv import load_dotenv
from google.genai import types
from google import genai
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

client = genai.Client(api_key="AIzaSyA3fs8OD2JxzzrBb-SyrjUFPJMLxwoNGDw")

def open_file(filepath: str):
    if platform.system() == "Windows":
        os.startfile(filepath)
    elif platform.system() == "Darwin":
        subprocess.run(["open", filepath])
    else:
        subprocess.run(["xdg-open", filepath])

def generate_and_show_video(brandbook: str, marketing_plan: str):
    """
    Generates video using the new Google Gen AI SDK with optional reference images.

    Args:
        brandbook: Brand guidelines to follow
        marketing_plan: Description of the marketing campaign
    """

    text_prompt = (
        f"Create a high-quality, visually appealing video that represents the following marketing plan: {marketing_plan}. "
        f"The video should be creative, engaging, and suitable for use in a marketing campaign. "
        f"Make sure that the video is relevant to the marketing plan and captures its essence. "
        f"You are allowed to use text in the video."
        f"Make sure the video aligns with the following brandbook guidelines: {brandbook}."
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

        video_path="marketing_video.mp4"

        generated_video = operation.response.generated_videos[0]
        client.files.download(file=generated_video.video)
        generated_video.video.save("marketing_video.mp4")
        logging.info(f"✅ Successfully generated video and saved to videos/marketing_video.mp4")

        logging.info("🖼️ Opening Video in your default viewer...")
        open_file(video_path)
        logging.info("🎉 Video should now be open in your video player.")
        return operation.response.generated_videos[0]

    except Exception as e:
        logging.error(f"❌ Error generating video: {str(e)}")
        return {"error": str(e)}


if __name__ == '__main__':
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
    brandbook_voorbeeld = ("Our company is named Jumbo Supermarkten, a leading supermarket chain in the Netherlands. "
                           "We mainly use the colors yellow and black in our branding. Our logo features a bold, "
                           "modern font with a playful touch, often accompanied by a shopping cart icon. We aim to "
                           "convey a sense of affordability, variety, and convenience in our marketing materials. Our "
                           "tone of voice is friendly, approachable, and family-oriented, focusing on the joy of "
                           "shopping and the quality of our products.")

    logging.info("=" * 60)
    logging.info("🎨 VEO AI - MARKETING VIDEO GENERATOR")
    logging.info("=" * 60)

    generate_and_show_video(brandbook_voorbeeld, marketing_plan)