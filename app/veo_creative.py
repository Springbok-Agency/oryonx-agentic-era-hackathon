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
