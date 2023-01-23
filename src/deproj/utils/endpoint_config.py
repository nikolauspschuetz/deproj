"""
created by nikos at 5/12/21
"""
# noinspection PyPackageRequirements
import yaml

from . import CONFIGS_PATH


class EndpointConfig(object):
    _instance = None
    config = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(EndpointConfig, cls).__new__(cls)
            # Put any initialization here.
            with open(f"{CONFIGS_PATH}/statsapi/endpoint-model.yml", 'r') as f:
                cls._instance.config = yaml.safe_load(f)

        return cls._instance
