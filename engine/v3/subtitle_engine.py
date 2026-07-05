from .config import (
    SUBTITLE_FONT_SIZE,
    SUBTITLE_MAX_LINES,
)

from .utils import wrap_text


class SubtitleEngine:

    def __init__(self):
        self.font_size = SUBTITLE_FONT_SIZE
        self.max_lines = SUBTITLE_MAX_LINES
        self.max_chars = 42
        self.margin_bottom = 220

    def get_style(self):
        return {
            "font_size": self.font_size,
            "max_lines": self.max_lines,
            "margin_bottom": self.margin_bottom,
            "alignment": "center",
        }

    def split_text(self, text):
        lines = wrap_text(text, self.max_chars)
        return lines[:self.max_lines]