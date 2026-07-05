import subprocess
from pathlib import Path

from engine.v3.pipeline import RenderPipeline


class RendererV3:
    def __init__(self):
        self.pipeline = RenderPipeline()

        self.audio = Path("input/voice.mp3")
        self.subtitle = Path("input/captions.srt")
        self.logo = Path("assets/logos/logo.png")

        if not self.logo.exists():
            self.logo = Path("input/Logo.png")

        self.output = Path("output/final_v3_reel.mp4")
        self.output.parent.mkdir(parents=True, exist_ok=True)

    def render(self, job_data=None):
        context = self.pipeline.prepare(job_data)

        background = context["assets"].get_random_background("General")
        export = context["export"]
        template = context["template"]

        width = template["width"]
        height = template["height"]
        fps = template["fps"]

        subtitle_path = str(self.subtitle).replace("\\", "/").replace(":", "\\:")

        subtitle_style = (
            "FontName=Arial,"
            "FontSize=16,"
            "PrimaryColour=&H00FFFFFF,"
            "OutlineColour=&H00000000,"
            "BackColour=&H99000000,"
            "BorderStyle=3,"
            "Outline=1,"
            "Shadow=0,"
            "MarginV=160,"
            "Bold=1,"
            "Alignment=2"
        )

        filter_complex = (
            f"[0:v]scale={width}:{height}:force_original_aspect_ratio=increase,"
            f"crop={width}:{height},fps={fps},format=rgba[video];"
            f"[2:v]format=rgba,scale=140:-1,colorchannelmixer=aa=0.72[logo];"
            f"[video][logo]overlay=W-w-45:45[vlogo];"
            f"[vlogo]subtitles='{subtitle_path}':force_style='{subtitle_style}'[v]"
        )

        command = [
            "ffmpeg",
            "-y",
            "-stream_loop", "-1",
            "-i", str(background),
            "-i", str(self.audio),
            "-i", str(self.logo),
            "-filter_complex", filter_complex,
            "-map", "[v]",
            "-map", "1:a",
            "-c:v", export["video_codec"],
            "-preset", export["preset"],
            "-crf", str(export["crf"]),
            "-pix_fmt", export["pixel_format"],
            "-c:a", export["audio_codec"],
            "-b:a", "128k",
            "-shortest",
            str(self.output),
        ]

        print("=" * 60)
        print("ASGC Renderer V3 - Real Captions")
        print("=" * 60)
        print(f"Background: {background}")
        print(f"Audio: {self.audio}")
        print(f"Subtitles: {self.subtitle}")
        print(f"Logo: {self.logo}")
        print(f"Output: {self.output}")

        result = subprocess.run(command)

        if result.returncode != 0:
            raise RuntimeError("Renderer V3 FFmpeg render failed.")

        print("Renderer V3 completed successfully.")
        return str(self.output)