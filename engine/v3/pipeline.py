from .asset_manager import AssetManager
from .layout_engine import LayoutEngine
from .subtitle_engine import SubtitleEngine
from .animation_engine import AnimationEngine
from .job_card import JobCard
from .exporter import FFmpegExporter
from .scene_engine import SceneEngine
from .timeline_engine import TimelineEngine
from .theme_engine import ThemeEngine
from .template_engine import TemplateEngine
from .brand_engine import BrandEngine


class RenderPipeline:
    def __init__(self):
        self.assets = AssetManager()
        self.layout = LayoutEngine()
        self.subtitles = SubtitleEngine()
        self.animations = AnimationEngine()
        self.exporter = FFmpegExporter()
        self.scenes = SceneEngine()
        self.timeline = TimelineEngine()
        self.theme = ThemeEngine()
        self.template = TemplateEngine()
        self.brand = BrandEngine()

    def prepare(self, job_data=None):
        if job_data is None:
            job_data = {}

        job_card = JobCard(job_data)

        context = {
            "assets": self.assets,
            "layout": self.layout.get_regions(),
            "subtitle_style": self.subtitles.get_style(),
            "job_card": job_card.build(),
            "scenes": self.scenes.build(job_data),
            "timeline": self.timeline.build(job_data),
            "theme": self.theme.get_theme(job_data),
            "template": self.template.get_template(),
            "brand": self.brand.get_brand(),
            "animations": self.animations,
            "export": self.exporter.get_export_settings(),
        }

        return context