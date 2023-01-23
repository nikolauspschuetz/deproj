import logging
from functools import reduce
from os import environ, path

__beta_stats_api_default_version__ = '1.0'


def get(k, d=None):
    return environ.get(k, d)


BASE_PATH = reduce(lambda d, _: path.dirname(d), range(3), path.realpath(__file__))

BETA_STATS_API_VERSION = get('DEPROJ__BETA_STATS_API_VERSION', __beta_stats_api_default_version__)

CONFIGS_PATH = get(
    'DEPROJ__CONFIGS_PATH',
    "%s/deproj/configs" % BASE_PATH
)

OUTPUT_PATH = get(
    'DEPROJ__OUTPUT_PATH',
    "%s/.out" % BASE_PATH
)

_ji = get('DEPROJ__JSON_INDENT')
JSON_INDENT = None if _ji is None else int(_ji)

LOG_LEVEL = get('DEPROJ__LOG_LEVEL', 'debug').upper()

STATS_API_OBJECT__BASE_FILE_PATH = get('DEPROJ__STATS_API_OBJECT__BASE_FILE_PATH', './.var/local/deproj')
STATS_API_OBJECT__MAX_GET_TRIES = int(get('DEPROJ__STATS_API_OBJECT__BASE_FILE_PATH', '5'))
