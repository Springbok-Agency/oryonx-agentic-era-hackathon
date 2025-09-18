import logging
import os

import google.auth

_, project_id = google.auth.default()
os.environ.setdefault("GOOGLE_CLOUD_PROJECT", project_id)
os.environ.setdefault("GOOGLE_CLOUD_LOCATION", "global")
os.environ.setdefault("GOOGLE_GENAI_USE_VERTEXAI", "True")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


def generate_and_show_video(marketing_plan: str, brandbook: str | None = None):
    """
    Placeholder for video generation until VEO model is available.

    Args:
        marketing_plan: Description of the marketing campaign
        brandbook: Optional brand guidelines to follow. If None, uses default brand guide.

    Returns:
        dict: Placeholder response indicating video generation is unavailable
    """

    if brandbook is None:
        brandbook = "Default brand guidelines"

    text_prompt = (
        f"Create a high-quality, visually appealing video that represents the following marketing plan: {marketing_plan}. "
        f"The video should be creative, engaging, and suitable for use in a marketing campaign. "
        f"Make sure that the video is relevant to the marketing plan and captures its essence. "
        f"You are allowed to use text in the video. "
        f"Make sure the video aligns with the following brandbook guidelines: {brandbook}."
    )

    try:
        logging.info(f"📝 Prompt: {text_prompt}")
        logging.info("⏳ Please wait...")

        # Note: veo-3.0-fast-generate-001 model is not available in this environment
        logging.info("Video generation temporarily unavailable - model not found")
        return {
            "placeholder": True,
            "message": "Video generation feature is temporarily unavailable. The veo-3.0-fast-generate-001 model is not accessible in the current environment.",
            "prompt_used": text_prompt
        }

    except Exception as e:
        logging.error(f"Error generating video: {e!s}")
        return {"error": str(e)}


if __name__ == "__main__":
    marketing_plan = "Test marketing plan"

    logging.info("=" * 60)
    logging.info("🎨 VEO AI - MARKETING VIDEO GENERATOR (SAFE)")
    logging.info("=" * 60)

    video = generate_and_show_video(marketing_plan, brandbook=None)
    logging.info(f"Video result: {video}")