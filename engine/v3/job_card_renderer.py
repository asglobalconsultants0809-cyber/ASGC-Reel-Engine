from pathlib import Path
from PIL import Image, ImageDraw, ImageFont


class JobCardRenderer:

    WIDTH = 520
    HEIGHT = 760

    BG_COLOR = (15, 23, 42, 235)
    PRIMARY = (11, 92, 255)
    WHITE = (255, 255, 255)
    GREY = (210, 210, 210)

    def __init__(self):

        self.output = Path("output/job_card.png")
        self.output.parent.mkdir(parents=True, exist_ok=True)

        self.canvas = Image.new(
            "RGBA",
            (self.WIDTH, self.HEIGHT),
            (0, 0, 0, 0)
        )

        self.draw = ImageDraw.Draw(self.canvas)

        try:
            self.title_font = ImageFont.truetype(
                "C:/Windows/Fonts/arialbd.ttf",
                38
            )

            self.text_font = ImageFont.truetype(
                "C:/Windows/Fonts/arial.ttf",
                26
            )

            self.small_font = ImageFont.truetype(
                "C:/Windows/Fonts/arial.ttf",
                22
            )

        except Exception:

            self.title_font = ImageFont.load_default()
            self.text_font = ImageFont.load_default()
            self.small_font = ImageFont.load_default()

    def draw_background(self):

        self.draw.rounded_rectangle(
            (0, 0, self.WIDTH, self.HEIGHT),
            radius=40,
            fill=self.BG_COLOR,
            outline=self.PRIMARY,
            width=4
        )

    def render(self, job):

        self.draw_background()

        y = 40

        self.draw.text(
            (40, y),
            "AS Global Consultants",
            fill=self.PRIMARY,
            font=self.text_font
        )

        y += 60

        self.draw.text(
            (40, y),
            job.get("job_title", "Job Title"),
            fill=self.WHITE,
            font=self.title_font
        )

        y += 80

        items = [
            ("Company", job.get("company", "")),
            ("Location", job.get("location", "")),
            ("Experience", job.get("experience", "")),
            ("Salary", job.get("salary", "")),
        ]

        for label, value in items:

            self.draw.text(
                (40, y),
                label,
                fill=self.PRIMARY,
                font=self.small_font
            )

            self.draw.text(
                (40, y + 28),
                str(value),
                fill=self.WHITE,
                font=self.text_font
            )

            y += 80

        self.draw.text(
            (40, y),
            "Skills",
            fill=self.PRIMARY,
            font=self.small_font
        )

        y += 35

        skills = job.get("skills", [])

        if isinstance(skills, list):

            for skill in skills[:5]:

                self.draw.text(
                    (60, y),
                    f"• {skill}",
                    fill=self.GREY,
                    font=self.text_font
                )

                y += 38

        self.canvas.save(self.output)

        return self.output


if __name__ == "__main__":

    renderer = JobCardRenderer()

    renderer.render(
        {
            "job_title": "Python Developer",
            "company": "AS Global Consultants",
            "location": "Bangalore",
            "experience": "2+ Years",
            "salary": "₹5 LPA",
            "skills": [
                "Python",
                "REST API",
                "FFmpeg",
                "Azure",
                "Windows"
            ]
        }
    )

    print("Generated:", renderer.output)