import re
import subprocess
from pathlib import Path

from engine.v3.job_card_renderer import JobCardRenderer
from engine.v4.subtitle_engine import SubtitleEngineV4
from engine.v4.contact_engine import ContactEngine
from engine.v4.motion_engine import MotionEngine


class RendererV4:
    def __init__(self):
        self.width = 1080
        self.height = 1920
        self.fps = 30

        self.background = Path("assets/backgrounds/General/office.mp4")
        self.audio = Path("input/voice.mp3")
        self.logo = self._find_logo()
        self.subtitle_ass = Path("output/v4_subtitles.ass")
        self.synced_subtitle_ass = Path("output/v4_subtitles_synced.ass")
        self.output = Path("output/final_v4_reel.mp4")
        self.output.parent.mkdir(parents=True, exist_ok=True)

        self.subtitle_shift_seconds = -0.85

    def _find_logo(self):
        for path in [Path("assets/logos/logo.png"), Path("input/Logo.png")]:
            if path.exists():
                return path
        return Path("assets/logos/logo.png")

    def _require(self, path, label):
        if not Path(path).exists():
            raise FileNotFoundError(f"Missing {label}: {path}")

    def _ffmpeg_path(self, path):
        p = str(Path(path).resolve()).replace("\\", "/")
        return p.replace(":", "\\:")

    def _ass_time_to_seconds(self, value):
        h, m, s = value.strip().split(":")
        return (int(h) * 3600) + (int(m) * 60) + float(s)

    def _seconds_to_ass_time(self, seconds):
        seconds = max(0, seconds)
        h = int(seconds // 3600)
        seconds -= h * 3600
        m = int(seconds // 60)
        seconds -= m * 60
        return f"{h}:{m:02d}:{seconds:05.2f}"

    def _sync_ass_subtitles(self, ass_path):
        raw = Path(ass_path).read_text(encoding="utf-8", errors="ignore")

        pattern = re.compile(
            r"(?m)^(Dialogue:\s*\d+,)"
            r"(\d+:\d{2}:\d{2}\.\d{2,3}),"
            r"(\d+:\d{2}:\d{2}\.\d{2,3})"
        )

        def repl(match):
            start = self._ass_time_to_seconds(match.group(2)) + self.subtitle_shift_seconds
            end = self._ass_time_to_seconds(match.group(3)) + self.subtitle_shift_seconds

            if end <= 0:
                end = 0.15
            if end <= start:
                end = start + 0.15

            return (
                f"{match.group(1)}"
                f"{self._seconds_to_ass_time(start)},"
                f"{self._seconds_to_ass_time(end)}"
            )

        synced = pattern.sub(repl, raw)
        self.synced_subtitle_ass.write_text(synced, encoding="utf-8")
        return self.synced_subtitle_ass

    def _build_subtitles(self):
        srt = Path("input/captions.srt")

        if srt.exists():
            ass = SubtitleEngineV4().generate()
        elif self.subtitle_ass.exists():
            ass = self.subtitle_ass
        else:
            raise FileNotFoundError(
                "Missing subtitles: input/captions.srt or output/v4_subtitles.ass"
            )

        return self._sync_ass_subtitles(ass)

    def _filters(self, job_card_path, ass_path):
        ass = self._ffmpeg_path(ass_path)
        contact = ContactEngine(start_time=30.6).ffmpeg_filter()
        motion = MotionEngine(duration=42).background_motion_filter()

        return (
            f"[0:v]"
            f"{motion},"
            f"eq=brightness=0.04:contrast=1.08:saturation=1.08,"
            f"format=rgba[bg];"

            f"[2:v]format=rgba,scale=128:-1,colorchannelmixer=aa=0.88[logo];"
            f"[3:v]format=rgba,scale=300:-1,colorchannelmixer=aa=0.74[jobcard];"

            f"[bg][logo]overlay=W-w-34:34:enable='between(t,0,45)'[v1];"
            f"[v1][jobcard]overlay=42:365:enable='between(t,1.2,29.8)'[v2];"

            f"[v2]{contact},subtitles='{ass}'[v]"
        )

    def render(self, job_data=None):
        job_data = job_data or {}

        self._require(self.background, "background video")
        self._require(self.audio, "voice audio")
        self._require(self.logo, "logo")

        job_card = JobCardRenderer().render(job_data)
        ass_path = self._build_subtitles()

        command = [
            "ffmpeg",
            "-y",
            "-stream_loop",
            "-1",
            "-i",
            str(self.background),
            "-i",
            str(self.audio),
            "-i",
            str(self.logo),
            "-i",
            str(job_card),
            "-filter_complex",
            self._filters(job_card, ass_path),
            "-map",
            "[v]",
            "-map",
            "1:a",
            "-c:v",
            "libx264",
            "-preset",
            "medium",
            "-crf",
            "20",
            "-pix_fmt",
            "yuv420p",
            "-c:a",
            "aac",
            "-b:a",
            "160k",
            "-movflags",
            "+faststart",
            "-shortest",
            str(self.output),
        ]

        result = subprocess.run(command, capture_output=True, text=True)

        if result.returncode != 0:
            print(result.stderr)
            raise RuntimeError("Renderer V4 FFmpeg render failed.")

        return str(self.output)


if __name__ == "__main__":
    print(
        RendererV4().render(
            {
                "job_title": "Python Developer",
                "company": "AS Global Consultants",
                "location": "Bangalore",
                "salary": "₹5 LPA",
                "experience": "2+ Years",
                "skills": ["Python", "API", "FFmpeg"],
                "cta": "Apply Now",
            }
        )
    )