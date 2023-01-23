import itertools
import json
import typing
import unittest

from itertools import product

from mock import patch

from deproj.cards import build, Card
from deproj.cards.box import Box
from deproj.utils import BRANDS, StatsAPIObject

from .fixtures import *


def patched_build_card(brand: str, year: int, person_id: int) -> Card:
    with patch.object(
        StatsAPIObject, "base_file_path", PATCH__STATS_API_OBJECT__BASE_FILE_PATH
    ), patch.object(StatsAPIObject, "get", autospec=True) as get:

        def mock_get(self, _tries: int = 0):
            return self.load(ext="json.gz")

        get.side_effect = mock_get
        card = build(brand, year, person_id)
    return card


def iter_brands_and_person_ids() -> typing.Iterator[typing.Union[str, int]]:
    for brand, person_id in itertools.product(BRANDS, PERSON_IDS):
        yield brand, person_id


def get_expected_json(brand: str, person_id: int) -> str:
    name_slug = get_name_slug(person_id)
    filename = f"{YEAR}-{name_slug}"
    filepath = f"{TEST_OUTPUT__BASE_FILE_PATH}/{brand}/{filename}.json"
    with open(filepath, "r") as f:
        out = json.load(f)
    expected_json = json.dumps(out, indent=None)
    return expected_json


def get_expected_csv(brand: str, person_id: int, i: int) -> str:
    name_slug = get_name_slug(person_id)
    filename = f"{YEAR}-{name_slug}"
    filepath = f"{TEST_OUTPUT__BASE_FILE_PATH}/{brand}/{filename}-{i}.csv"
    with open(filepath, "r") as f:
        expected_csv = f.read()
    return expected_csv


class TestCard(unittest.TestCase):

    cards = {}

    @classmethod
    def setUpClass(cls) -> None:
        # basically tests that we have and cna use all of our
        from deproj.utils.log import set_log_level

        set_log_level("WARNING")
        for brand, person_id in product(BRANDS, PERSON_IDS):
            card = patched_build_card(brand, YEAR, person_id)
            cls.cards[brand, person_id] = card
            # print(card.to_console(output=Output.CSV))

    def test_to_json(self):
        # check that the json string matches
        for brand, person_id in iter_brands_and_person_ids():
            card: Card = self.cards[brand, person_id]
            is_pitcher = person_id == DEFAULT_PITCHER
            expected_json = get_expected_json(brand, person_id)
            self.assertEqual(
                card.to_json(None),
                expected_json,
                f"{brand=} {is_pitcher=} json output does not match",
            )

    def test_to_csvs(self):
        # check that the csv string matches
        for brand, person_id in iter_brands_and_person_ids():
            is_pitcher = person_id == DEFAULT_PITCHER
            card: Card = self.cards[brand, person_id]
            for i, box in enumerate(card.boxes):
                expected_csv = get_expected_csv(brand, person_id, i)
                self.assertEqual(
                    box.to_csv(),
                    expected_csv,
                    f"{brand=} {is_pitcher=} csv {i} output does not match",
                )

    def test_boxes(self):
        for brand, person_id in iter_brands_and_person_ids():
            card: Card = self.cards[brand, person_id]
            boxes: list[Box] = card.boxes
            is_pitcher = person_id == DEFAULT_PITCHER
            # check that each card one has the right number of boxes
            self.assertEqual(
                len(boxes),
                EXPECTED_BOX_COUNT[brand],
                f"{brand=} {is_pitcher=} box counts do not match",
            )

    # def test_to_png(self):
    #     assert False
