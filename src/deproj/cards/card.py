import abc
import json
import os.path
from typing import List

from deproj.cards.box import Box
from deproj.utils import get_output_filepath, JSON_INDENT, to_short, Output


class Card(abc.ABC):
    def __init__(
        self,
        brand: str,
        year: int,
        person_id: int,
        *boxes: Box,
        name_slug: str,
        images: List[dict],
    ):
        self.brand = brand
        self.year = year
        self.person_id = person_id
        self.boxes: List[Box] = [*boxes]
        self.name_slug = name_slug
        self.images: List[dict] = images

    def to_list(self):
        return [b.to_dict() for b in self.boxes]

    def to_console(self, *, output: Output = Output.JSON) -> str:
        """return a json representation of the card"""
        if output == Output.JSON:
            return json.dumps(
                {
                    "brand": self.brand,
                    "year": self.year,
                    "person_id": self.person_id,
                    "boxes": self.to_list(),
                },
                indent=JSON_INDENT,
            )
        elif output == Output.CSV:
            return "\n".join(
                [
                    "\n".join([f"csv {i}:", box.to_csv()])
                    for i, box in enumerate(self.boxes)
                ]
            )
        # elif output == Output.PNG:  # todo
        #     self.to_png()
        else:
            raise ValueError(f"to_console for {output=} not configured.")

    def to_json(self, indent=JSON_INDENT) -> str:
        """write a json file for the card and return the filepath"""
        return json.dumps(self.to_list(), indent=indent)

    def write_json(self, *, short: bool = True) -> str:
        """write a json file for the card and return the filepath"""
        filepath = get_output_filepath(self.brand, self.year, self.name_slug, "json")
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, "w") as f:
            f.write(self.to_json())
        return to_short(filepath) if short else filepath

    def to_csvs(self) -> List[str]:
        """write a json file for the card and return the filepath"""
        return [box.to_df().to_csv(index=False) for box in self.boxes]

    def write_csvs(self, *, short: bool = True) -> str:
        """write a json file for the card and return the filepath"""
        filepaths = [
            box.write_csv(self.brand, self.year, self.name_slug, i)
            for i, box in enumerate(self.boxes)
        ]
        if short:
            filepaths = [to_short(f) for f in filepaths]
        return " ".join(filepaths)

    # @abc.abstractmethod
    # def to_png(self):
    #     pass

    # @abc.abstractmethod
    # def write_png(self):
    #     pass
