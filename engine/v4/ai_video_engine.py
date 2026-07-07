from pathlib import Path


class AIVideoEngine:
    def __init__(self):
        self.base_dir = Path("assets/ai_videos")
        self.fallback_video = Path("assets/backgrounds/General/office.mp4")

    def _safe_name(self, text):
        text = str(text or "job").lower()
        return "".join(c if c.isalnum() else "_" for c in text).strip("_")

    def get_video(self, job_data):
        job_title = self._safe_name(job_data.get("job_title", "job"))

        possible = [
            self.base_dir / "office" / f"{job_title}.mp4",
            self.base_dir / "generic" / f"{job_title}.mp4",
        ]

        for path in possible:
            if path.exists():
                return path

        return self.fallback_video


if __name__ == "__main__":
    print(
        AIVideoEngine().get_video(
            {"job_title": "Python Developer"}
        )
    )