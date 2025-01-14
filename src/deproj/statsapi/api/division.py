"""
created by nikos at 4/26/21
"""
from ..base import MLBStatsAPIEndpointModel
from deproj.utils.stats_api_object import configure_api


class DivisionModel(MLBStatsAPIEndpointModel):
    @configure_api
    def divisions(self, **kwargs):
        return self.get_api_file_object(**kwargs)

    @property
    def _methods(self) -> dict:
        return {m.__name__: m for m in (self.divisions,)}
