from .config import WIDTH, HEIGHT, SAFE_MARGIN


class LayoutEngine:

    def __init__(self):
        self.width = WIDTH
        self.height = HEIGHT
        self.safe_margin = SAFE_MARGIN

    def get_regions(self):

        content_width = self.width - (self.safe_margin * 2)

        return {
            "hook": {
                "x": self.safe_margin,
                "y": 120,
                "width": content_width,
                "height": 220,
            },

            "job_card": {
                "x": self.safe_margin,
                "y": 380,
                "width": content_width,
                "height": 720,
            },

            "subtitles": {
                "x": self.safe_margin,
                "y": 1180,
                "width": content_width,
                "height": 220,
            },

            "cta": {
                "x": self.safe_margin,
                "y": 1510,
                "width": content_width,
                "height": 150,
            },

            "watermark": {
                "x": self.width - 160,
                "y": 40,
                "width": 100,
                "height": 100,
            }
        }