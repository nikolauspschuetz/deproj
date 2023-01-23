import datetime
import os

from enum import Enum

from .env import CONFIGS_PATH, OUTPUT_PATH, BASE_PATH

BRANDS = os.listdir(f"{CONFIGS_PATH}/cards")


class Output(Enum):
    CONSOLE = "console"
    CSV = "csv"
    JSON = "json"
    PNG = "png"


# noinspection PyPep8Naming
def TZ_America_New_York():
    import pytz

    return pytz.timezone("America/New_York")


def check_response(func):
    """method annotation to check the HTTPStatusCode for boto3 calls"""

    def checker(*args, **kwargs):
        res = func(*args, **kwargs)
        assert (
            res["ResponseMetadata"]["HTTPStatusCode"] == 200
        ), f"{func.__name__} failed: {str(res)}"
        return res

    return checker


def get_current_mlb_datetime() -> datetime.datetime:
    return datetime.datetime.now(tz=TZ_America_New_York())


def get_current_mlb_date() -> datetime.date:
    return get_current_mlb_datetime().date()


date_format = "%Y-%m-%d"
YmdTHMSz_format = "%Y-%m-%dT%H:%M:%S%z"
game_date_format = YmdTHMSz_format
game_timestamp_format = "%Y%m%d_%H%M%S"


def strpdate(string: str) -> datetime.date:
    return datetime.datetime.strptime(string, date_format).date()


def strpdatetime(string: str, _format=game_date_format) -> datetime.datetime:
    return datetime.datetime.strptime(string, _format)


def strfdatetime(_datetime: datetime.datetime, _format=game_date_format) -> str:
    return _datetime.strftime(_format)


def get_output_filepath(brand: str, year: int, name_slug: str, ext: str, i: int = None):
    if i is None:
        filename = f"{year}-{name_slug}"
    else:
        filename = f"{year}-{name_slug}-{i}"
    return f"{OUTPUT_PATH}/{brand}/{filename}.{ext}"


def to_short(filepath: str):
    return filepath.split(BASE_PATH)[-1].lstrip("/")
