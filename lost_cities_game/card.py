class Card:
    def __init__(self, number:int, colour:str) -> None:
        """TODO: Create docstring."""
        self.number = number
        self.colour = colour
        self.wager = self._is_wager(self.number)

    def _is_wager(self,number):
        """TODO: Create docstring."""
        if number == 0:
            return True

    def __str__(self):
        """TODO: Create docstring."""
        return f"{self.colour} {self.number}"
