from pathlib import Path
import whisper


class Transcriber:

    def __init__(self):

        self.audio = Path("input/voice.mp3")
        self.output = Path("input/captions.srt")

        print("\nLoading Whisper model...")

        self.model = whisper.load_model("base")

    def generate(self):

        print("\nGenerating subtitles...")

        result = self.model.transcribe(str(self.audio))

        with open(self.output, "w", encoding="utf-8") as f:

            for i, segment in enumerate(result["segments"], start=1):

                start = self.format_time(segment["start"])
                end = self.format_time(segment["end"])
                text = segment["text"].strip()

                f.write(f"{i}\n")
                f.write(f"{start} --> {end}\n")
                f.write(f"{text}\n\n")

        print("\nSubtitles generated successfully.")

    def format_time(self, seconds):

        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        milliseconds = int((seconds - int(seconds)) * 1000)

        return (
            f"{hours:02}:{minutes:02}:{secs:02},{milliseconds:03}"
        )