from pathlib import Path
from openai import OpenAI

from .config import AI_BACKGROUNDS


class AIBackgroundEngine:

    def __init__(self, api_key=None):

        self.client = OpenAI(api_key=api_key)
        self.output_folder = AI_BACKGROUNDS
        self.output_folder.mkdir(parents=True, exist_ok=True)

    def build_prompt(self, category):

        prompts = {
            "IT": "Modern premium software office, developers coding, multiple monitors, blue corporate lighting, cinematic, ultra realistic, 9:16 vertical, no text, no logo.",
            "Healthcare": "Modern hospital interior, doctors and nurses, premium lighting, ultra realistic, 9:16 vertical, no text.",
            "Banking": "Luxury corporate banking office, finance professionals, ultra realistic, cinematic, 9:16 vertical.",
            "BPO": "Modern customer support office, employees with headsets, premium office, cinematic, 9:16 vertical.",
            "General": "Premium modern corporate office, business professionals, ultra realistic, cinematic, 9:16 vertical."
        }

        return prompts.get(category, prompts["General"])

    def generate_image(self, category):

        prompt = self.build_prompt(category)

        result = self.client.images.generate(
            model="gpt-image-1",
            prompt=prompt,
            size="1024x1792",
        )

        image_bytes = result.data[0].b64_json

        import base64

        image_path = self.output_folder / f"{category.lower()}_background.png"

        with open(image_path, "wb") as f:
            f.write(base64.b64decode(image_bytes))

        return image_path