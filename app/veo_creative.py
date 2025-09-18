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
            config=types.GenerateVideosConfig(aspectRatio="16:9"),
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
    marketing_plan = ("""
        **Marketing Plan 2: Free Range Eggs & The Giant Pancake**
        
        **The Story:**  Hold onto your spatulas!  Chefs in Amsterdam just flipped the world's largest pancake, 
        shattering previous records and sending delicious aromas across the city!  This incredible feat required not 
        just a massive griddle, but a truly colossal number of eggs.  And we all know that a truly great pancake 
        starts with high-quality ingredients.  That's where our Free Range Eggs come in.  The fluffy texture, 
        the rich flavor, the knowledge that the hens lived happy and free – it all contributes to a record-breaking 
        breakfast.
        
        **Marketing Strategy:**
        **Purpose:** Connect our Free Range Eggs to a fun, trending news story and highlight the superior quality of our eggs.
        **Timing:** Immediate launch to ride the wave of news coverage.  A two-week campaign is ideal.
        **Target Audience:**  Breakfast lovers, health-conscious consumers, and people who appreciate ethically sourced food.
        
        **Tagline:**  "From Our Hens to the World's Largest Pancake: The Secret Ingredient is JUMBO Free Range Eggs."
        
        **Instagram Post Ideas:** **Image:** A split image showing a picture of the giant pancake next to a carton of 
        our Free Range Eggs.  The tagline is overlaid. **Video:** A time-lapse video of pancake batter being poured 
        and cooked, emphasizing the large scale of the operation and the role of our eggs. The tagline is included as 
        text on the video.
        
        **Instagram Caption:**  "They didn't just flip a pancake, they flipped the world!  Discover the secret to 
        truly amazing pancakes: JUMBO Free Range Eggs.  #WorldsLargestPancake #FreeRangeEggs 
        #PancakePerfection #BreakfastGoals""")
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