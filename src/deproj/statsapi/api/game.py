"""
created by nikos at 4/26/21
"""
import datetime

from ..base import MLBStatsAPIEndpointModel
from deproj.utils.stats_api_object import configure_api


YMDTHMS = '%Y-%m-%dT%H:%M:%SZ'
YYYYMMDD_HHMMSS = '%Y%m%d_%H%M%S'
MMDDYYYY_HHMMSS = '%m%d%Y_%H%M%S'


class GameModel(MLBStatsAPIEndpointModel):

    date_formats = {
        'updatedSince': YMDTHMS,
        'timecode': YYYYMMDD_HHMMSS,
        'startTimecode': MMDDYYYY_HHMMSS,
        'endTimecode': MMDDYYYY_HHMMSS
    }

    @configure_api
    def liveGameV1(self, **kwargs):
        return self.get_api_file_object(**kwargs)

    @configure_api
    def liveGameDiffPatchV1(self, **kwargs):
        return self.get_api_file_object(**kwargs)

    @configure_api
    def liveTimestampv11(self, **kwargs):
        return self.get_api_file_object(**kwargs)

    @configure_api
    def currentGameStats(self, **kwargs):
        return self.get_api_file_object(**kwargs)

    @configure_api
    def getGameContextMetrics(self, **kwargs):
        return self.get_api_file_object(**kwargs)

    @configure_api
    def getWinProbability(self, **kwargs):
        return self.get_api_file_object(**kwargs)

    @configure_api
    def boxscore(self, **kwargs):
        return self.get_api_file_object(**kwargs)

    @configure_api
    def content(self, **kwargs):
        return self.get_api_file_object(**kwargs)

    @configure_api
    def colorFeed(self, **kwargs):
        return self.get_api_file_object(**kwargs)

    @configure_api
    def colorTimestamps(self, **kwargs):
        return self.get_api_file_object(**kwargs)

    @configure_api
    def linescore(self, **kwargs):
        return self.get_api_file_object(**kwargs)

    @configure_api
    def playByPlay(self, **kwargs):
        return self.get_api_file_object(**kwargs)

    @property
    def _methods(self) -> dict: return {m.__name__: m for m in (
        self.liveGameV1,
        self.liveGameDiffPatchV1,
        self.liveTimestampv11,
        self.currentGameStats,
        self.getGameContextMetrics,
        self.getWinProbability,
        self.boxscore,
        self.content,
        self.colorFeed,
        self.colorTimestamps,
        self.linescore,
        self.playByPlay
    )}

    @property
    def now_timestamp(self):
        return datetime.datetime.now().strftime(YYYYMMDD_HHMMSS)
