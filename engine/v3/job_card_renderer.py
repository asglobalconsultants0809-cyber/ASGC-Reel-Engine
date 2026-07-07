from pathlib import Path
import textwrap
from PIL import Image, ImageDraw, ImageFont, ImageFilter


class JobCardRenderer:
    WIDTH = 560
    HEIGHT = 820

    def __init__(self):
        self.output = Path("output/job_card.png")
        self.output.parent.mkdir(parents=True, exist_ok=True)

        self.font_bold = self._font("assets/fonts/Montserrat-Bold.ttf", 38)
        self.font_title = self._font("assets/fonts/Montserrat-Bold.ttf", 44)
        self.font_text = self._font("assets/fonts/Poppins-Regular.ttf", 27)
        self.font_small = self._font("assets/fonts/Poppins-Regular.ttf", 22)
        self.font_chip = self._font("assets/fonts/Montserrat-Bold.ttf", 22)

    def _font(self, path, size):
        try:
            return ImageFont.truetype(path, size)
        except Exception:
            return ImageFont.truetype("C:/Windows/Fonts/arial.ttf", size)

    def _rounded_panel(self, img, box, radius, fill, outline=None, width=2):
        draw = ImageDraw.Draw(img)
        draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)

    def _text(self, draw, xy, text, font, fill):
        draw.text(xy, str(text or ""), font=font, fill=fill)

    def _wrap_lines(self, text, chars=18, max_lines=2):
        lines = textwrap.wrap(str(text or ""), width=chars)
        return lines[:max_lines]

    def render(self, job):
        img = Image.new("RGBA", (self.WIDTH, self.HEIGHT), (0, 0, 0, 0))

        shadow = Image.new("RGBA", (self.WIDTH, self.HEIGHT), (0, 0, 0, 0))
        sdraw = ImageDraw.Draw(shadow)
        sdraw.rounded_rectangle((18, 18, self.WIDTH - 18, self.HEIGHT - 18), 44, fill=(0, 0, 0, 130))
        shadow = shadow.filter(ImageFilter.GaussianBlur(16))
        img.alpha_composite(shadow)

        self._rounded_panel(
            img,
            (18, 18, self.WIDTH - 18, self.HEIGHT - 18),
            44,
            (10, 20, 45, 222),
            (27, 130, 255, 210),
            3,
        )

        draw = ImageDraw.Draw(img)

        # Header
        self._text(draw, (48, 48), "AS GLOBAL CONSULTANTS", self.font_small, (91, 192, 255, 255))
        draw.rounded_rectangle((48, 88, 245, 94), 3, fill=(255, 194, 48, 255))

        y = 125

        # Job title
        for line in self._wrap_lines(job.get("job_title", "Job Opening"), 17, 2):
            self._text(draw, (48, y), line, self.font_title, (255, 255, 255, 255))
            y += 54

        y += 22

        info = [
            ("COMPANY", job.get("company", "AS Global Consultants")),
            ("LOCATION", job.get("location", "Bangalore")),
            ("EXPERIENCE", job.get("experience", "Relevant Experience")),
            ("SALARY", job.get("salary", "Best in Industry")),
        ]

        for label, value in info:
            draw.rounded_rectangle((48, y, self.WIDTH - 48, y + 78), 18, fill=(255, 255, 255, 24))
            self._text(draw, (68, y + 10), label, self.font_small, (91, 192, 255, 255))
            self._text(draw, (68, y + 38), value, self.font_text, (255, 255, 255, 255))
            y += 94

        # Skills
        self._text(draw, (48, y), "KEY SKILLS", self.font_small, (255, 194, 48, 255))
        y += 40

        skills = job.get("skills", [])
        if not isinstance(skills, list):
            skills = []

        x = 48
        for skill in skills[:5]:
            label = str(skill)[:16]
            bbox = draw.textbbox((0, 0), label, font=self.font_chip)
            chip_w = bbox[2] - bbox[0] + 38

            if x + chip_w > self.WIDTH - 48:
                x = 48
                y += 48

            draw.rounded_rectangle((x, y, x + chip_w, y + 38), 19, fill=(11, 92, 255, 230))
            self._text(draw, (x + 19, y + 6), label, self.font_chip, (255, 255, 255, 255))
            x += chip_w + 12

        # CTA footer
        footer_y = self.HEIGHT - 115
        draw.rounded_rectangle((48, footer_y, self.WIDTH - 48, footer_y + 65), 24, fill=(255, 194, 48, 255))
        self._text(draw, (145, footer_y + 15), job.get("cta", "APPLY NOW").upper(), self.font_bold, (8, 22, 48, 255))

        img.save(self.output)
        return self.output


if __name__ == "__main__":
    path = JobCardRenderer().render({
        "job_title": "Python Developer",
        "company": "AS Global Consultants",
        "location": "Bangalore",
        "experience": "2+ Years",
        "salary": "₹5 LPA",
        "skills": ["Python", "REST API", "FFmpeg", "Azure", "Windows"],
        "cta": "Apply Now",
    })
    print("Generated:", path)