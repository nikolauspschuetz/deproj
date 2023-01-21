from functools import reduce
from os import environ, path

__beta_stats_api_default_version__ = '1.0'


def get(k, d=None):
    return environ.get(k, d)


BETA_STATS_API_VERSION = get('DEPROJ__BETA_STATS_API_VERSION', __beta_stats_api_default_version__)

CONFIGS_PATH = get(
    'DEPROJ__CONFIGS_PATH',
    "%s/configs" % reduce(lambda d, _: path.dirname(d), range(4), path.realpath(__file__))
)

OUTPUT_PATH = get(
    'DEPROJ__OUTPUT_PATH',
    "%s/.out" % reduce(lambda d, _: path.dirname(d), range(4), path.realpath(__file__))
)

JSON_INDENT = get('DEPROJ__JSON_INDENT')

STATS_API_OBJECT__BASE_FILE_PATH = get('DEPROJ__STATS_API_OBJECT__BASE_FILE_PATH', './.var/local/deproj')
STATS_API_OBJECT__MAX_GET_TRIES = int(get('DEPROJ__STATS_API_OBJECT__BASE_FILE_PATH', '5'))
