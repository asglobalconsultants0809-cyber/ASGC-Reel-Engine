import subprocess
from pathlib import Path


class BackgroundVideoEngine:
    def __init__(self, duration=42, fps=30):
        self.duration = duration
        self.fps = fps
        self.output_dir = Path("output/backgrounds")
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def create_video(self, image_path):
        image_path = Path(image_path)

        if not image_path.exists():
            raise FileNotFoundError(f"Missing AI background image: {image_path}")

        output_path = self.output_dir / f"{image_path.stem}_cinematic.mp4"

        command = [
            "ffmpeg",
            "-y",
            "-loop", "1",
            "-i", str(image_path),
            "-vf",
            (
                "scale=1200:2134,"
                "zoompan="
                "z='min(zoom+0.0006,1.08)':"
                "x='iw/2-(iw/zoom/2)':"
                "y='ih/2-(ih/zoom/2)':"
                f"d={self.duration * self.fps}:"
                "s=1080x1920:"
                f"fps={self.fps},"
                "fade=t=in:st=0:d=0.5,"
                f"fade=t=out:st={self.duration - 0.8}:d=0.8,"
                "format=yuv420p"
            ),
            "-t", str(self.duration),
            "-c:v", "libx264",
            "-preset", "medium",
            "-crf", "20",
            "-pix_fmt", "yuv420p",
            str(output_path),
        ]

        result = subprocess.run(command, capture_output=True, text=True)

        if result.returncode != 0:
            print(result.stderr)
            raise RuntimeError("Background video generation failed.")

        return output_path


if __name__ == "__main__":
    path = BackgroundVideoEngine().create_video(
        "assets/ai_backgrounds/office/python_developer_background.png"
    )
    print(path)