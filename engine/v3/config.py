from pathlib import Path

# =========================
# Project Paths
# =========================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

ASSETS = PROJECT_ROOT / "assets"
INPUT = PROJECT_ROOT / "input"
OUTPUT = PROJECT_ROOT / "output"

BACKGROUNDS = ASSETS / "backgrounds"
AI_BACKGROUNDS = ASSETS / "ai_backgrounds"

FONTS = ASSETS / "fonts"
ICONS = ASSETS / "icons"
LOGOS = ASSETS / "logos"
OVERLAYS = ASSETS / "overlays"

# =========================
# Video Settings
# =========================

WIDTH = 1080
HEIGHT = 1920
FPS = 30

# =========================
# Theme
# =========================

PRIMARY_COLOR = "#0B5FFF"
SECONDARY_COLOR = "#F5A623"
SAFE_MARGIN = 80

# =========================
# Watermark
# =========================

WATERMARK_WIDTH = 100
WATERMARK_OPACITY = 0.65
WATERMARK_POSITION = "top-right"

# =========================
# Job Card
# =========================

CARD_RADIUS = 35
CARD_PADDING = 40

# =========================
# Subtitle
# =========================

SUBTITLE_FONT_SIZE = 24
SUBTITLE_MAX_LINES = 2

# =========================
# Export
# =========================

VIDEO_CODEC = "libx264"
AUDIO_CODEC = "aac"
PIX_FMT = "yuv420p"
CRF = 18
PRESET = "medium"