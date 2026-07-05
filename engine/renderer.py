import json
import random
import subprocess
from pathlib import Path


class Renderer:

    def __init__(self):

        with open("config.json", "r", encoding="utf-8") as f:
            self.config = json.load(f)

        self.video_cfg = self.config["video"]
        self.audio_cfg = self.config["audio"]
        self.logo_cfg = self.config["logo"]
        self.subtitle_cfg = self.config["subtitles"]

        # Random Background Selection
        self.background_folder = Path("input/backgrounds")

        videos = []

        for ext in ("*.mp4", "*.mov", "*.mkv", "*.avi"):
            videos.extend(self.background_folder.glob(ext))

        if not videos:
            raise FileNotFoundError("No background videos found in input/backgrounds")

        self.video = random.choice(videos)

        print(f"\nSelected Background : {self.video.name}")

        self.audio = Path(self.audio_cfg["input"])
        self.logo = Path(self.logo_cfg["input"])
        self.subtitle = self.subtitle_cfg["input"].replace("\\", "/")

        self.output = Path(self.video_cfg["output"])
        self.output.parent.mkdir(exist_ok=True)

    def render(self):

        subtitle_style = (
            f"FontName={self.subtitle_cfg['font']},"
            f"FontSize={self.subtitle_cfg['font_size']},"
            "PrimaryColour=&H00FFFFFF,"
            "OutlineColour=&H00000000,"
            "BorderStyle=1,"
            f"Outline={self.subtitle_cfg['outline']},"
            f"Shadow={self.subtitle_cfg['shadow']},"
            f"MarginV={self.subtitle_cfg['margin_bottom']},"
            f"Bold={1 if self.subtitle_cfg['bold'] else 0},"
            "Alignment=2"
        )

        logo_width = self.logo_cfg["width"]
        margin_x = self.logo_cfg["margin_x"]
        margin_y = self.logo_cfg["margin_y"]

        position = self.logo_cfg["position"].lower()

        if position == "top-right":
            overlay = f"W-w-{margin_x}:{margin_y}"
        elif position == "top-left":
            overlay = f"{margin_x}:{margin_y}"
        elif position == "bottom-right":
            overlay = f"W-w-{margin_x}:H-h-{margin_y}"
        elif position == "bottom-left":
            overlay = f"{margin_x}:H-h-{margin_y}"
        else:
            overlay = f"W-w-{margin_x}:{margin_y}"

        filter_complex = (
            f"[0:v]scale=-2:{self.video_cfg['height']},"
            f"crop={self.video_cfg['width']}:{self.video_cfg['height']}[video];"
            f"[2:v]scale={logo_width}:-1[logo];"
            f"[video][logo]overlay={overlay},"
            f"subtitles='{self.subtitle}':force_style='{subtitle_style}'[v]"
        )

        command = [
            "ffmpeg",
            "-y",

            "-stream_loop", "-1",

            "-i", str(self.video),
            "-i", str(self.audio),
            "-i", str(self.logo),

            "-filter_complex", filter_complex,

            "-map", "[v]",
            "-map", "1:a",

            "-c:v", "libx264",
            "-preset", "ultrafast",
            "-threads", "2",
            "-crf", "28",
            "-pix_fmt", "yuv420p",

            "-c:a", "aac",
            "-b:a", "128k",

            "-shortest",

            str(self.output)
        ]

        print("\nRunning FFmpeg...\n")

        result = subprocess.run(command)

        if self.output.exists():
            print("\nRender completed successfully.")
            return

        if result.returncode != 0:
            raise RuntimeError("FFmpeg failed and no output video was created.")