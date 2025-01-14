"""
created by nikos at 4/26/21
"""
from ..base import MLBStatsAPIEndpointModel
from deproj.utils.stats_api_object import configure_api


class JobModel(MLBStatsAPIEndpointModel):
    @configure_api
    def getJobsByType(self, **kwargs):
        return self.get_api_file_object(**kwargs)

    @configure_api
    def datacasters(self, **kwargs):
        return self.get_api_file_object(**kwargs)

    @configure_api
    def officialScorers(self, **kwargs):
        return self.get_api_file_object(**kwargs)

    @configure_api
    def umpires(self, **kwargs):
        return self.get_api_file_object(**kwargs)

    @property
    def _methods(self) -> dict:
        return {
            m.__name__: m
            for m in (
                self.getJobsByType,
                self.datacasters,
                self.officialScorers,
                self.umpires,
            )
        }
