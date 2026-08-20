"""GEO service."""

from app.modules.geo_engine.optimizer import score_geo
from app.modules.geo_engine.schemas import GeoReport


class GeoService:
    def analyze(self, markdown: str) -> GeoReport:
        return score_geo(markdown)
