class MotionEngine:
    """
    V4.1 cinematic background motion.
    Adds subtle zoom and fade without breaking renderer.
    """

    def __init__(self, duration=42):
        self.duration = duration

    def background_motion_filter(self):
        return (
            "scale=1200:2134,"
            "zoompan="
            "z='min(zoom+0.0006,1.08)':"
            "x='iw/2-(iw/zoom/2)':"
            "y='ih/2-(ih/zoom/2)':"
            "d=1:"
            "s=1080x1920:"
            "fps=30,"
            "fade=t=in:st=0:d=0.5,"
            f"fade=t=out:st={max(self.duration - 0.8, 1)}:d=0.8"
        )


if __name__ == "__main__":
    print(MotionEngine().background_motion_filter())