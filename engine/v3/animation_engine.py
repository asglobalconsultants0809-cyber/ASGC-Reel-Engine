class AnimationEngine:

    def __init__(self):
        self.default_duration = 0.4

    def fade_in(self, start=0.0):
        return {
            "type": "fade_in",
            "start": start,
            "duration": self.default_duration,
        }

    def fade_out(self, start):
        return {
            "type": "fade_out",
            "start": start,
            "duration": self.default_duration,
        }

    def slide_up(self, start=0.0, distance=40):
        return {
            "type": "slide_up",
            "start": start,
            "distance": distance,
            "duration": self.default_duration,
        }

    def zoom_in(self, start=0.0, scale=1.1):
        return {
            "type": "zoom_in",
            "start": start,
            "scale": scale,
            "duration": self.default_duration,
        }