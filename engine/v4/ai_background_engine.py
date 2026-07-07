import base64
import os
from pathlib import Path


class AIBackgroundEngine:
    def __init__(self):
        self.base_dir = Path("assets/ai_backgrounds")
        self.output_dir = Path("output")
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def _category(self, job_data):
        text = " ".join([
            str(job_data.get("job_title", "")),
            str(job_data.get("company", "")),
            str(job_data.get("location", "")),
            " ".join(job_data.get("skills", [])) if isinstance(job_data.get("skills"), list) else ""
        ]).lower()

        if any(x in text for x in ["bank", "finance", "account", "loan", "insurance"]):
            return "banking"
        if any(x in text for x in ["hospital", "nurse", "medical", "doctor", "health"]):
            return "hospital"
        if any(x in text for x in ["warehouse", "logistics", "delivery", "picker", "packer"]):
            return "warehouse"
        if any(x in text for x in ["retail", "sales", "store", "cashier"]):
            return "retail"
        if any(x in text for x in ["python", "developer", "software", "it", "api", "cloud"]):
            return "office"

        return "generic"

    def _prompt(self, job_data, category):
        title = job_data.get("job_title", "Job Opening")
        location = job_data.get("location", "India")

        return f"""
Create a premium vertical 9:16 recruitment reel background for {title} in {location}.
Scene category: {category}.
Modern professional Indian corporate environment.
One realistic professional candidate standing naturally, medium full body, centered-right.
Clean space on left side for job card overlay.
Dark blue and gold corporate lighting.
Premium office recruitment advertising style.
No text, no logos, no watermark, no fake writing.
Photorealistic, cinematic, sharp, high-end social media reel background.
"""

    def generate(self, job_data):
        category = self._category(job_data)
        category_dir = self.base_dir / category
        category_dir.mkdir(parents=True, exist_ok=True)

        safe_title = str(job_data.get("job_title", "job")).lower()
        safe_title = "".join(c if c.isalnum() else "_" for c in safe_title).strip("_")
        output_path = category_dir / f"{safe_title}_background.png"

        if output_path.exists():
            return output_path

        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise RuntimeError("OPENAI_API_KEY not found. Add it first before AI background generation.")

        try:
            from openai import OpenAI
        except ImportError:
            raise RuntimeError("OpenAI package missing. Run: pip install openai")

        client = OpenAI(api_key=api_key)

        result = client.images.generate(
            model="gpt-image-1",
            prompt=self._prompt(job_data, category),
            size="1024x1536",
            quality="high",
            n=1,
        )

        image_base64 = result.data[0].b64_json
        image_bytes = base64.b64decode(image_base64)

        output_path.write_bytes(image_bytes)
        return output_path


if __name__ == "__main__":
    path = AIBackgroundEngine().generate({
        "job_title": "Python Developer",
        "company": "AS Global Consultants",
        "location": "Bangalore",
        "salary": "₹5 LPA",
        "experience": "2+ Years",
        "skills": ["Python", "API", "FFmpeg"],
        "cta": "Apply Now",
    })
    print(path)