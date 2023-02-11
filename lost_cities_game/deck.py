import random
class Deck():
    def __init__(self, cards:list) -> None:
        """TODO: Create docstring."""
        self.list = []
        self.populate_deck(cards)
        self.len = len(cards)

    def populate_deck(self, cards:list):
        """TODO: Create docstring."""
        for card in cards:
            self.list.append(card)

    def shuffle_deck(self):
        """TODO: Create docstring."""
        random.shuffle(self.list )
