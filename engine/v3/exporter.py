from .config import VIDEO_CODEC, AUDIO_CODEC, PIX_FMT, CRF, PRESET


class FFmpegExporter:

    def __init__(self):
        self.video_codec = VIDEO_CODEC
        self.audio_codec = AUDIO_CODEC
        self.pixel_format = PIX_FMT
        self.crf = CRF
        self.preset = PRESET

    def get_export_settings(self):
        return {
            "video_codec": self.video_codec,
            "audio_codec": self.audio_codec,
            "pixel_format": self.pixel_format,
            "crf": self.crf,
            "preset": self.preset,
            "format": "mp4",
        }