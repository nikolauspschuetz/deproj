"""
created by nikos at 4/26/21
"""
from ..base import MLBStatsAPIEndpointModel
from deproj.utils.stats_api_object import configure_api


class ScheduleModel(MLBStatsAPIEndpointModel):

    @configure_api
    def schedule(self, **kwargs):
        return self.get_api_file_object(**kwargs)

    @configure_api
    def tieGames(self, **kwargs):
        return self.get_api_file_object(**kwargs)

    @configure_api
    def postseasonScheduleSeries(self, **kwargs):
        return self.get_api_file_object(**kwargs)

    @configure_api
    def tuneIn(self, **kwargs):
        return self.get_api_file_object(**kwargs)

    @configure_api
    def scheduleType(self, **kwargs):
        if kwargs:
            raise NotImplementedError("this beta statsapi docs is buggy: will not allow you to pass the scheduleType!")
        return self.get_api_file_object(**kwargs)

    @property
    def _methods(self) -> dict: return {m.__name__: m for m in (
        self.schedule,
        self.tieGames,
        self.postseasonScheduleSeries,
        self.tuneIn,
        self.scheduleType
    )}