"""
created by nikos at 5/2/21
"""
import logging

from . import LOG_LEVEL

_LOG_LEVELS = {
    'ERROR': logging.ERROR,
    'WARNING': logging.WARNING,
    'INFO': logging.INFO,
    'DEBUG': logging.DEBUG
}

root = logging.getLogger('deproj')
root.propagate = False
root.setLevel(logging.DEBUG)
logging_format = [
    # '[%(asctime)s]',
    '{%(filename)s:%(lineno)d}',
    '%(name)s',
    '%(threadName)s',
    '%(levelname)s',
    '-',
    '%(message)s'
]
formatter = logging.Formatter(' '.join(logging_format))

loggers = {}


class LogMixin:

    # noinspection PyUnresolvedReferences,PyAttributeOutsideInit
    @property
    def log(self):
        try:
            return self._log
        except AttributeError:
            self._log = get_logger(self)
            return self._log


# noinspection PyPep8Naming
def get_logger(logMixin: LogMixin):
    global loggers
    name = logMixin.__class__.__module__ + '.' + logMixin.__class__.__name__
    if loggers.get(name) is None:
        loggers[name] = logging.root.getChild(name)
        console = logging.StreamHandler()
        console.setFormatter(formatter)
        loggers[name].addHandler(console)
    return loggers[name]


def set_log_level(level: str = None):
    lls = {*_LOG_LEVELS.keys()}
    assert LOG_LEVEL in lls, f'{LOG_LEVEL} not found in {[*_LOG_LEVELS]}.'
    ll = (level or LOG_LEVEL).upper()
    assert ll in lls, f'{ll} not found in {[*_LOG_LEVELS]}.'
    root.setLevel(_LOG_LEVELS[ll])
