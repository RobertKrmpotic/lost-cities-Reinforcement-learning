import random
class Deck():
    def __init__(self, cards:list) -> None:
        self.list = [] 
        self.populate_deck(cards)
        self.len = len(cards)

    def populate_deck(self, cards:list):
        for card in cards:
            self.list.append(card)
    
    def shuffle_deck(self):
        random.shuffle(self.list )