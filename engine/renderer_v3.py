import re
import subprocess
from pathlib import Path

from engine.v3.pipeline import RenderPipeline
from engine.v3.job_card_renderer import JobCardRenderer


class RendererV3:
    def __init__(self):
        self.pipeline = RenderPipeline()
        self.audio = Path("input/voice.mp3")
        self.subtitle = Path("input/captions.srt")
        self.logo = Path("assets/logos/logo.png")
        if not self.logo.exists():
            self.logo = Path("input/Logo.png")

        self.output = Path("output/final_v3_reel.mp4")
        self.ass_file = Path("output/v3_clean_captions.ass")
        self.output.parent.mkdir(parents=True, exist_ok=True)

    def _ffmpeg_path(self, path):
        return str(path.resolve()).replace("\\", "/").replace(":", "\\:")

    def _ass_time(self, srt_time):
        value = srt_time.strip().replace(",", ".")
        if value.startswith("00:"):
            value = value[1:]
        return value

    def _clean_ass_text(self, text):
        text = re.sub(r"\s+", " ", text).strip().replace("{", "").replace("}", "")
        words, lines, current = text.split(), [], ""
        for word in words:
            if len((current + " " + word).strip()) <= 36:
                current = (current + " " + word).strip()
            else:
                if current:
                    lines.append(current)
                current = word
        if current:
            lines.append(current)
        return r"\N".join(lines[:2])

    def _create_ass_from_srt(self):
        raw = self.subtitle.read_text(encoding="utf-8", errors="ignore")
        blocks = re.split(r"\n\s*\n", raw.strip())

        header = """[Script Info]
Title: ASGC Clean Captions
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,Arial,44,&H00FFFFFF,&H000000FF,&H00000000,&H00000000,-1,0,0,0,100,100,0,0,1,3,1,2,120,120,470,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
        events = []
        for block in blocks:
            lines = [x.strip() for x in block.splitlines() if x.strip()]
            timing = next((x for x in lines if "-->" in x), None)
            if not timing:
                continue
            start, end = [x.strip() for x in timing.split("-->")]
            text = self._clean_ass_text(" ".join(lines[lines.index(timing) + 1:]))
            if text:
                events.append(f"Dialogue: 0,{self._ass_time(start)},{self._ass_time(end)},Default,,0,0,0,,{text}\n")

        self.ass_file.write_text(header + "".join(events), encoding="utf-8")
        return self.ass_file

    def render(self, job_data=None):
        job_data = job_data or {}
        context = self.pipeline.prepare(job_data)

        background = context["assets"].get_random_background("General")
        export = context["export"]
        template = context["template"]

        width, height, fps = template["width"], template["height"], template["fps"]

        job_card = JobCardRenderer().render(job_data)
        ass_path = self._ffmpeg_path(self._create_ass_from_srt())

        phone = "+91 96864 78938"
        email = "ansar.shaik@asglobalconsultants.in"
        website = "www.asglobalconsultants.in"
        job_title = job_data.get("job_title", "Python Developer")

        filter_complex = (
            f"[0:v]scale={width}:{height}:force_original_aspect_ratio=increase,"
            f"crop={width}:{height},fps={fps},eq=brightness=0.12:contrast=1.18:saturation=1.15,format=rgba[bg];"
            f"[3:v]format=rgba,scale=330:-1,colorchannelmixer=aa=0.93[jobcard];"
            f"[bg][jobcard]overlay=42:430:enable='between(t,2,37)'[v1];"
            f"[2:v]format=rgba,scale=165:-1,colorchannelmixer=aa=0.88[logo];"
            f"[v1][logo]overlay=W-w-42:38[v2];"
            f"[v2]"
            f"drawtext=text='Freshers are welcome.':x=70:y=80:fontsize=62:fontcolor=white:"
            f"font='Arial':borderw=3:bordercolor=black@0.65:enable='between(t,0,6)',"
            f"drawtext=text='Excellent opportunity for {job_title}.':x=75:y=165:fontsize=31:fontcolor=white:"
            f"font='Arial':borderw=2:bordercolor=black@0.50:enable='between(t,0,8)',"
            f"drawtext=text='SEND YOUR RESUME ON WHATSAPP':x=90:y=1490:fontsize=28:fontcolor=white:"
            f"font='Arial':borderw=2:bordercolor=black@0.55,"
            f"drawtext=text='{phone}':x=90:y=1535:fontsize=54:fontcolor=0xFFD12A:"
            f"font='Arial':borderw=3:bordercolor=black@0.55,"
            f"drawtext=text='EMAIL  {email}':x=90:y=1625:fontsize=27:fontcolor=white:"
            f"font='Arial':borderw=2:bordercolor=black@0.55,"
            f"drawtext=text='WEBSITE  {website}':x=90:y=1672:fontsize=27:fontcolor=white:"
            f"font='Arial':borderw=2:bordercolor=black@0.55,"
            f"drawtext=text='LIMITED OPENINGS  •  APPLY TODAY':x=(w-text_w)/2:y=1795:fontsize=33:fontcolor=white:"
            f"font='Arial':borderw=3:bordercolor=black@0.60,"
            f"subtitles='{ass_path}'[v]"
        )

        command = [
            "ffmpeg", "-y",
            "-stream_loop", "-1",
            "-i", str(background),
            "-i", str(self.audio),
            "-i", str(self.logo),
            "-i", str(job_card),
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

        result = subprocess.run(command)
        if result.returncode != 0:
            raise RuntimeError("Renderer V3 FFmpeg render failed.")

        print("Renderer V3 completed successfully.")
        return str(self.output)