from os.path import exists

# noinspection PyPackageRequirements
from yaml import safe_load
import pyjq

from deproj.cards.box import Box
from deproj.statsapi import StatsAPI
from deproj.utils import CONFIGS_PATH


VALUES = {}


def get_config(brand: str, year: int, is_pitcher: bool):
    kind = "pitcher" if is_pitcher else "batter"
    config_path = f"{CONFIGS_PATH}/cards/{brand}/{year}-{kind}.yml"
    assert exists(
        config_path
    ), f"{year} {kind} config not found for {brand} at {config_path}."
    with open(config_path, "r") as f:
        return safe_load(f)


def get_card_class(brand: str):
    if brand == "panini-donruss-baseball":
        from .brands import PaniniDonrussBaseball

        c = PaniniDonrussBaseball
    elif brand == "topps-series-1-baseball":
        from .brands import ToppsSeries1Baseball

        c = ToppsSeries1Baseball
    else:
        raise ModuleNotFoundError(f"no brand module for {brand}")
    return c


def add_vs_team_total(config: dict, year: int, person: dict):
    global VALUES
    value = "vsTeamTotal"
    is_pitcher = int(person["primaryPosition"]["code"]) == 1
    team = person["currentTeam"]
    team_id = team["id"]
    teams = (
        StatsAPI.Team.teams(path_params={"teamId": ""}, query_params={"sportId": 1})
        .get()
        .obj["teams"]
    )
    vs_team_ids = [t["id"] for t in teams if t["id"] != team_id]
    group = "pitching" if is_pitcher else "batting"
    hydrate = config[value].get("hydrate", "")
    vs_teams = [
        StatsAPI.Person.person(
            path_params={"personId": person["id"]},
            query_params={
                "hydrate": hydrate.format(
                    group=group, opposingTeamId=vs_team_id, season=year - 1
                )
            },
        )
        .get()
        .obj["people"][0]
        for vs_team_id in vs_team_ids
    ]
    vs_teams = [stat for vt in vs_teams if "stats" in vt for stat in vt["stats"]]
    VALUES[value] = vs_teams


def add_value(value: str, config: dict, year: int):
    global VALUES
    person = VALUES["person"]
    if value == "vsTeamTotal":
        add_vs_team_total(config, year, person)
    else:
        raise ValueError(f"add_value not configured for {value}")


def get_value(script: str, value: str, config: dict, year: int, b: int, v: int) -> dict:
    global VALUES
    assert script is not None, f"{script=} for box {b} value {v}."
    assert value is not None, f"{value=} for box {b} value {v}."
    if value not in VALUES:
        add_value(value, config, year)
    result = pyjq.first(script, VALUES[value])
    return result


def build(brand: str, year: int, person_id: int):
    global VALUES
    primary_position = (
        StatsAPI.Person.person(path_params={"personId": person_id})
        .get()
        .obj["people"][0]["primaryPosition"]
    )
    is_pitcher = int(primary_position["code"]) == 1
    card_class = get_card_class(brand)
    config = get_config(brand=brand, year=year, is_pitcher=is_pitcher)

    person = (
        StatsAPI.Person.person(
            path_params={"personId": person_id},
            query_params={
                "site": "en",
                # "group": "pitching" if is_pitcher else "hitting",  # see api/v1/statGroups
                "hydrate": config["person"].get("hydrate", ""),
            },
        )
        .get()
        .obj["people"][0]
    )

    VALUES = {"person": person}

    boxes = [
        Box(
            box["kind"],
            box["side"],
            *[
                {
                    "name": val.get("name"),
                    "value": get_value(val["script"], val["value"], config, year, b, v),
                }
                for v, val in enumerate(box["values"])
            ],
        )
        for b, box in enumerate(config["boxes"])
    ]

    return card_class(
        year, person_id, *boxes, name_slug=person["nameSlug"], images=config["images"]
    )
