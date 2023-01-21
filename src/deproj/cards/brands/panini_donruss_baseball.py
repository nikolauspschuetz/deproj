from deproj.cards import Card
from deproj.cards.box import Box


class PaniniDonrussBaseball(Card):

    def __init__(self, *boxes: Box):
        super(PaniniDonrussBaseball, self).__init__('panini-donruss-baseball', *boxes)
