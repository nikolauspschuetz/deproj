from typing import List

from deproj.cards import Card
from deproj.cards.box import Box


class PaniniDonrussBaseball(Card):
    def __init__(
        self, year: int, person_id: int, *boxes: Box, name_slug: str, images: List[dict]
    ):
        super(PaniniDonrussBaseball, self).__init__(
            "panini-donruss-baseball",
            year,
            person_id,
            *boxes,
            name_slug=name_slug,
            images=images
        )

    # def to_png(self):
    #     # TODO
    #     import cv2
    #     import requests
    #     import numpy as np
    #     from PIL import Image
    #     from io import BytesIO
    #
    #     print()
    #     person_id = int(self.name_slug.split('-')[-1])
    #     for i, image in enumerate(self.images):
    #         url = image["url"].format(person_id=person_id)
    #         res = requests.get(url)
    #
    #         img = Image.open(BytesIO(res.content))
    #
    #         # arr = np.asarray(bytearray(res.content), dtype=np.uint8)
    #         # img = cv2.imdecode(arr, -1)  # 'Load it as it is'
    #         #
    #         # cv2.imshow('lalala', img)
    #         if cv2.waitKey() & 0xff == 27: quit()
