"""
created by nikos at 4/26/21
"""
from ..base import MLBStatsAPIEndpointModel
from deproj.utils.stats_api_object import configure_api


class StandingsModel(MLBStatsAPIEndpointModel):
    """
    https://statsapi.mlb.com/api/v1/standings/regularSeason?leagueId=103,104&season=2017&date=2017-08-09&hydrate=division,conference,sport,league,team
    """

    @configure_api
    def standings(self, **kwargs):
        return self.get_api_file_object(**kwargs)

    @property
    def _methods(self) -> dict:
        return {m.__name__: m for m in (self.standings,)}
