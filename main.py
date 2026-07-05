from engine.transcriber import Transcriber
from engine.renderer import Renderer

print("=" * 60)
print("ASGC Reel Engine v1")
print("=" * 60)

# Step 1 - Generate subtitles from voice.mp3
transcriber = Transcriber()
transcriber.generate()

# Step 2 - Render final reel
renderer = Renderer()
renderer.render()

print("\nDone.")