"""AEO service."""

from app.modules.aeo_engine.optimizer import score_aeo
from app.modules.aeo_engine.schemas import AeoReport


class AeoService:
    def analyze(self, markdown: str) -> AeoReport:
        return score_aeo(markdown)
