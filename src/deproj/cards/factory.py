from os.path import exists
# noinspection PyPackageRequirements
from yaml import safe_load
import pyjq

from deproj.statsapi import StatsAPI
from deproj.utils import CONFIGS_PATH


def get_config(brand: str, year: int, is_pitcher: bool):
    kind = 'pitcher' if is_pitcher else 'batter'
    config_path = f"{CONFIGS_PATH}/cards/{brand}/{year}-{kind}.yml"
    assert exists(config_path), f"{year} {kind} config not found for {brand} at {config_path}."
    with open(config_path, 'r') as f:
        return safe_load(f)


def get_card_class(brand: str):
    if brand == "panini-donruss-baseball":
        from .brands import PaniniDonrussBaseball
        c = PaniniDonrussBaseball
    # elif brand == "topps-series-1-baseball":
    #
    else:
        raise ModuleNotFoundError(f"no brand module for {brand}")
    return c


def get_value(script: str, value: str, values: dict, b: int, v: int) -> dict:
    assert script is not None, f'{script=} for box {b} value {v}.'
    assert value is not None, f'{value=} for box {b} value {v}.'
    result = pyjq.first(script, values[value])
    return result


def build(brand: str, year: int, person_id: int):
    primary_position = StatsAPI.Person.person(
        path_params={"personId": person_id}
    ).get().obj["people"][0]["primaryPosition"]
    is_pitcher = int(primary_position['code']) == 1
    # noinspection PyPep8Naming
    C = get_card_class(brand)
    config = get_config(brand=brand, year=year, is_pitcher=is_pitcher)

    person = StatsAPI.Person.person(
        path_params={"personId": person_id},
        query_params={
            "site": "en",
            # "group": "pitching" if is_pitcher else "hitting",  # see api/v1/statGroups
            "hydrate": config["person"].get("hydrate", ""),
        }
    ).get().obj["people"][0]

    values = {
        "person": person,
    }

    boxes = [
        C.get_box(box["kind"], *[{
            "name": val.get("name"),
            "value": get_value(val["script"], val["value"], values, b, v)
        } for v, val in enumerate(box["values"])])
        for b, box in enumerate(config["boxes"])
    ]
    return C(*boxes)

# https://img.mlbstatic.com/mlb-photos/image/upload/d_people:generic:action:hero:current.jpg/v1/people/660271/action/hero/current