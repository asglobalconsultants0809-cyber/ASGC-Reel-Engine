import random
from pathlib import Path

from .config import (
    BACKGROUNDS,
    AI_BACKGROUNDS,
    FONTS,
    ICONS,
    LOGOS,
    OVERLAYS,
)


class AssetManager:

    def __init__(self):
        self.backgrounds = BACKGROUNDS
        self.ai_backgrounds = AI_BACKGROUNDS
        self.fonts = FONTS
        self.icons = ICONS
        self.logos = LOGOS
        self.overlays = OVERLAYS

    def get_random_background(self, category="General"):

        folder = self.backgrounds / category

        if not folder.exists():
            folder = self.backgrounds / "General"

        videos = []

        for ext in ("*.mp4", "*.mov", "*.avi", "*.mkv"):
            videos.extend(folder.glob(ext))

        if not videos:
            raise FileNotFoundError(f"No background videos found in {folder}")

        return random.choice(videos)

    def get_logo(self):
        return self.logos / "logo.png"

    def get_watermark(self):
        return self.logos / "watermark.png"

    def get_overlay(self, name):
        return self.overlays / name

    def get_icon(self, name):
        return self.icons / name

    def get_font(self, bold=False):
        if bold:
            return self.fonts / "Montserrat-Bold.ttf"
        return self.fonts / "Montserrat-Regular.ttf"