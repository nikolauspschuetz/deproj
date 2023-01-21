import abc
import json
import os.path
from typing import List

from deproj.cards.box import Box
from deproj.utils import OUTPUT_PATH


class Card(abc.ABC):

    def __init__(self, brand, *boxes: Box):
        self.brand = brand
        self.boxes: List[Box] = [*boxes]

    @staticmethod
    def makedirs(path):
        if not os.path.exists(os.path.dirname(path)):
            os.makedirs(os.path.dirname(path))

    @staticmethod
    def get_path(brand: str, year: int, person_id: int, ext: str):
        return f"{OUTPUT_PATH}/{brand}/{year}-{person_id}.{ext}"

    @classmethod
    def get_box(cls, kind: str, *vals: dict) -> Box:
        if kind in {"basic", "frame"}:
            return Box(kind, *vals)
        else:
            raise NotImplementedError(f"No box for {kind=}")

    def to_list(self):
        return [b.to_dict() for b in self.boxes]

    def to_console(self, brand: str, year: int, person_id: int, indent=None):
        print(json.dumps({
            "brand": brand,
            "year": year,
            "person_id": person_id,
            "boxes": self.to_list()
        }, indent=indent if indent is None else int(indent)))

    def to_json(self, brand: str, year: int, person_id: int, indent=None):
        path = self.get_path(brand, year, person_id, "json")
        self.makedirs(path)
        with open(path, "w") as f:
            f.write(json.dumps(self.to_list(), indent=indent if indent is None else int(indent)))

    # @abc.abstractmethod
    # def to_csv(self):
    #     pass
    #
    # @abc.abstractmethod
    # def to_png(self):
    #     pass
    #
    # @abc.abstractmethod
    # def to_console(self):
    #     pass
