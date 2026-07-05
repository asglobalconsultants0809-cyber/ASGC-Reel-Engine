class TemplateEngine:
    def get_template(self, name="premium_recruitment"):
        return {
            "name": name,
            "format": "instagram_reel",
            "width": 1080,
            "height": 1920,
            "fps": 30,
            "safe_margin": 80,
            "scene_order": ["hook", "job", "skills", "company", "salary", "cta"],
        }