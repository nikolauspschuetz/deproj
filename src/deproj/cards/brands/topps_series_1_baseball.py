from typing import List

from deproj.cards import Card
from deproj.cards.box import Box


class ToppsSeries1Baseball(Card):
    def __init__(
        self, year: int, person_id: int, *boxes: Box, name_slug: str, images: List[dict]
    ):
        super(ToppsSeries1Baseball, self).__init__(
            "topps-series-1-baseball",
            year,
            person_id,
            *boxes,
            name_slug=name_slug,
            images=images
        )

    # def to_png(self):
    #     raise NotImplementedError("")
