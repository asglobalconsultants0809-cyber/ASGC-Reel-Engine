import re
import textwrap
from pathlib import Path


class SubtitleEngineV4:
    def __init__(self):
        self.input_srt = Path("input/captions.srt")
        self.output_ass = Path("output/v4_subtitles.ass")
        self.output_ass.parent.mkdir(parents=True, exist_ok=True)

    def _ass_time(self, value):
        value = value.strip().replace(",", ".")
        if value.startswith("00:"):
            value = value[1:]
        return value

    def _clean_text(self, text):
        text = re.sub(r"\s+", " ", text).strip()
        text = text.replace("{", "").replace("}", "")

        # Fix Whisper phone-number transcription
        if re.fullmatch(r"[0-9,\s]+\.?", text):
            digits = re.sub(r"\D", "", text)
            if len(digits) >= 10:
                return "+91 96864 78938"

        text = text.replace("A S Global Consultants", "AS Global Consultants")
        text = text.replace("BTEC", "B.Tech")
        text = text.replace("BE and B.Tech", "BE and B.Tech")

        return text

    def _wrap_2_lines(self, text, width=32):
        text = self._clean_text(text)
        lines = textwrap.wrap(text, width=width)
        return r"\N".join(lines[:2])

    def generate(self):
        raw = self.input_srt.read_text(encoding="utf-8", errors="ignore")
        blocks = re.split(r"\n\s*\n", raw.strip())

        header = """[Script Info]
Title: ASGC V4 Subtitles
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,Arial,36,&H00FFFFFF,&H000000FF,&H00000000,&H00000000,-1,0,0,0,100,100,0,0,1,3,1,2,120,120,430,1

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
            text_lines = lines[lines.index(timing) + 1:]
            text = self._wrap_2_lines(" ".join(text_lines))

            if text:
                events.append(
                    f"Dialogue: 0,{self._ass_time(start)},{self._ass_time(end)},Default,,0,0,0,,{text}\n"
                )

        self.output_ass.write_text(header + "".join(events), encoding="utf-8")
        return self.output_ass


if __name__ == "__main__":
    path = SubtitleEngineV4().generate()
    print("Generated:", path)