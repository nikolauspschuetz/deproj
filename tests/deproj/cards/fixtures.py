import importlib.resources
from dataclasses import dataclass

from deproj.cli import DEFAULT_PITCHER, DEFAULT_BATTER, DEFAULT_YEAR

# noinspection PyUnresolvedReferences
TEST_OUTPUT__BASE_FILE_PATH = (
    importlib.resources.files("tests").joinpath(f"resources/output").as_posix()
)
PATCH__STATS_API_OBJECT__BASE_FILE_PATH = (
    importlib.resources.files("tests").joinpath(f"resources/statsapi").as_posix()
)
PERSON_IDS = DEFAULT_PITCHER, DEFAULT_BATTER
YEAR = DEFAULT_YEAR  # only testing one year for now/simplicity

PANINI_DONRUSS_BASEBALL, TOPPS_SERIES_1_BASEBALL = (
    "panini-donruss-baseball",
    "topps-series-1-baseball",
)


def get_name_slug(person_id: int) -> str:
    if person_id == DEFAULT_PITCHER:
        name = "chris-bassitt"
    elif person_id == DEFAULT_BATTER:
        name = "nick-ahmed"
    else:
        raise ValueError(f"name_slug for {person_id=} not configured")
    return f"{name}-{person_id}"


@dataclass
class ExpectedBox:
    brand: str
    side: str


EXPECTED_BOX_COUNT = {
    PANINI_DONRUSS_BASEBALL: 6,
    TOPPS_SERIES_1_BASEBALL: 5,  # todo - add the season totals
}
