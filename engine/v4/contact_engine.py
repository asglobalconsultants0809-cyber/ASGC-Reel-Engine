from pathlib import Path


class ContactEngine:
    def __init__(
        self,
        whatsapp="+91 96864 78938",
        email="ansar.shaik@asglobalconsultants.in",
        website="www.asglobalconsultants.in",
        start_time=30.6,
        end_time=9999,
    ):
        self.whatsapp = whatsapp
        self.email = email
        self.website = website
        self.start_time = start_time
        self.end_time = end_time
        self.font_regular = self._find_font(["Montserrat-Regular.ttf", "Poppins-Regular.ttf", "arial.ttf"])
        self.font_bold = self._find_font(["Montserrat-Bold.ttf", "Montserrat-Regular.ttf", "arialbd.ttf", "arial.ttf"])

    def _find_font(self, names):
        roots = [Path("assets/fonts"), Path("C:/Windows/Fonts")]
        for root in roots:
            for name in names:
                path = root / name
                if path.exists():
                    return path.as_posix()
        return None

    def _escape(self, text):
        return (
            str(text)
            .replace("\\", "\\\\")
            .replace(":", "\\:")
            .replace("'", r"\'")
            .replace("%", "%%")
        )

    def _drawtext(self, text, y, fontsize, color="white", bold=False):
        font = self.font_bold if bold else self.font_regular
        fontfile = f"fontfile='{font}':" if font else ""
        return (
            "drawtext="
            f"{fontfile}"
            f"text='{self._escape(text)}':"
            f"fontcolor={color}:"
            f"fontsize={fontsize}:"
            "borderw=3:"
            "bordercolor=black@0.90:"
            "shadowx=2:"
            "shadowy=2:"
            "shadowcolor=black@0.70:"
            "x=(w-text_w)/2:"
            f"y={y}:"
            f"enable='between(t,{self.start_time},{self.end_time})'"
        )

    def filters(self):
        return [
            self._drawtext("Send your resume on WhatsApp", "h-170", 30, "white", True),
            self._drawtext(self.whatsapp, "h-126", 40, "#FFD34D", True),
            self._drawtext(f"{self.email}  |  {self.website}", "h-82", 23, "#D9F2FF", False),
        ]

    def ffmpeg_filter(self):
        return ",".join(self.filters())


if __name__ == "__main__":
    print(ContactEngine().ffmpeg_filter())
