from PIL import Image, ImageDraw, ImageFont, ImageFilter
from pathlib import Path


class TemplateRenderer:
    def __init__(self):
        self.out_dir = Path("output/v5")
        self.out_dir.mkdir(parents=True, exist_ok=True)

        self.card_w = 720
        self.card_h = 960

        self.font_title = self.font("arialbd.ttf", 72)
        self.font_title_small = self.font("arialbd.ttf", 58)
        self.font_brand = self.font("arialbd.ttf", 30)
        self.font_company = self.font("arial.ttf", 42)
        self.font_label = self.font("arialbd.ttf", 26)
        self.font_value = self.font("arialbd.ttf", 42)
        self.font_skill = self.font("arialbd.ttf", 28)
        self.font_cta = self.font("arialbd.ttf", 54)

    def font(self, name, size):
        try:
            return ImageFont.truetype(name, size)
        except:
            return ImageFont.load_default()

    def rounded(self, d, box, r, fill, outline=None, width=1):
        d.rounded_rectangle(box, radius=r, fill=fill, outline=outline, width=width)

    def text_fit(self, d, text, max_width, font_big, font_small):
        if d.textlength(text, font=font_big) <= max_width:
            return font_big
        return font_small

    def draw_icon_location(self, d, x, y, color):
        d.ellipse((x, y, x + 54, y + 54), outline=color, width=3)
        d.ellipse((x + 18, y + 12, x + 36, y + 30), fill=color)
        d.polygon([(x + 27, y + 48), (x + 14, y + 26), (x + 40, y + 26)], fill=color)

    def draw_icon_bag(self, d, x, y, color):
        d.rounded_rectangle((x + 6, y + 18, x + 52, y + 52), radius=8, outline=color, width=3)
        d.arc((x + 18, y + 4, x + 40, y + 28), 180, 360, fill=color, width=3)
        d.line((x + 6, y + 31, x + 52, y + 31), fill=color, width=3)

    def draw_icon_salary(self, d, x, y, color):
        d.ellipse((x, y, x + 54, y + 54), outline=color, width=3)
        d.text((x + 16, y + 5), "₹", font=self.font_value, fill=color)

    def render(self, job):
        navy = (5, 16, 42, 235)
        blue = (68, 180, 255, 255)
        yellow = (255, 199, 49, 255)
        white = (255, 255, 255, 255)
        soft = (210, 220, 235, 255)
        line = (95, 160, 210, 120)

        img = Image.new("RGBA", (self.card_w, self.card_h), (0, 0, 0, 0))

        shadow = Image.new("RGBA", img.size, (0, 0, 0, 0))
        sd = ImageDraw.Draw(shadow)
        sd.rounded_rectangle((28, 28, self.card_w - 18, self.card_h - 18), radius=42, fill=(0, 0, 0, 170))
        shadow = shadow.filter(ImageFilter.GaussianBlur(18))
        img.alpha_composite(shadow)

        d = ImageDraw.Draw(img)

        self.rounded(
            d,
            (20, 20, self.card_w - 25, self.card_h - 25),
            42,
            fill=navy,
            outline=blue,
            width=3,
        )

        d.text((70, 70), "AS GLOBAL CONSULTANTS", font=self.font_brand, fill=white)
        d.text((70, 112), "CONNECTING TALENT, BUILDING FUTURES", font=self.font_label, fill=blue)

        d.rounded_rectangle((70, 190, 210, 202), radius=6, fill=yellow)

        title = job.get("job_title", "Python Developer")
        title_font = self.text_fit(d, title, 560, self.font_title, self.font_title_small)

        words = title.split()
        if len(words) >= 2:
            first = " ".join(words[:-1])
            last = words[-1]
            d.text((70, 250), first, font=title_font, fill=white)
            d.text((70, 330), last, font=title_font, fill=yellow)
            company_y = 425
        else:
            d.text((70, 285), title, font=title_font, fill=white)
            company_y = 395

        d.text((70, company_y), job.get("company", "AS Global Consultants"), font=self.font_company, fill=soft)
        d.line((70, company_y + 75, self.card_w - 70, company_y + 75), fill=line, width=2)

        rows = [
            ("location", "LOCATION", job.get("location", "Bangalore")),
            ("experience", "EXPERIENCE", job.get("experience", "2+ Years")),
            ("salary", "SALARY", job.get("salary", "₹5 LPA")),
        ]

        y = company_y + 120

        for icon, label, value in rows:
            if icon == "location":
                self.draw_icon_location(d, 80, y, yellow)
            elif icon == "experience":
                self.draw_icon_bag(d, 80, y, yellow)
            else:
                self.draw_icon_salary(d, 80, y, yellow)

            d.text((165, y), label, font=self.font_label, fill=blue)
            d.text((165, y + 34), value, font=self.font_value, fill=white)
            y += 105
            d.line((70, y - 20, self.card_w - 70, y - 20), fill=(68, 180, 255, 70), width=1)

        d.text((90, y + 10), "KEY SKILLS", font=self.font_brand, fill=white)
        d.rounded_rectangle((70, y + 14, 78, y + 48), radius=4, fill=yellow)

        skills = job.get("skills", ["Python", "API", "FFmpeg"])
        x = 70
        sy = y + 75

        for skill in skills[:4]:
            tw = d.textlength(skill, font=self.font_skill)
            pill_w = int(tw + 52)
            self.rounded(d, (x, sy, x + pill_w, sy + 58), 29, fill=yellow)
            d.text((x + 26, sy + 13), skill, font=self.font_skill, fill=(5, 16, 42, 255))
            x += pill_w + 22

        self.rounded(d, (70, self.card_h - 135, self.card_w - 70, self.card_h - 55), 26, fill=yellow)

        cta = job.get("cta", "APPLY NOW").upper()
        tw = d.textlength(cta, font=self.font_cta)
        d.text(((self.card_w - tw) / 2, self.card_h - 122), cta, font=self.font_cta, fill=(5, 16, 42, 255))

        output = self.out_dir / "premium_template_card.png"
        img.save(output)
        return str(output)


if __name__ == "__main__":
    job = {
        "job_title": "Python Developer",
        "company": "AS Global Consultants",
        "location": "Bangalore",
        "experience": "2+ Years",
        "salary": "₹5 LPA",
        "skills": ["Python", "API", "FFmpeg"],
        "cta": "Apply Now",
    }

    print(TemplateRenderer().render(job))
    Set-Content engine\v5\template_renderer.py