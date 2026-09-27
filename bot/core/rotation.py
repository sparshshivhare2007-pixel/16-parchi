"""
Fixed turn rotation logic.
Order is set once at game start and never changes.
"""


class Rotation:
    def __init__(self, order: list[str]):
        if not order:
            raise ValueError("Rotation order cannot be empty")
        self.order = order
        self.index = 0

    def current(self) -> str:
        """Return the player whose turn it is."""
        return self.order[self.index]

    def next(self) -> str:
        """Advance to next player and return them."""
        self.index = (self.index + 1) % len(self.order)
        return self.current()

    def is_turn(self, player: str) -> bool:
        """Check if it is the given player's turn."""
        return self.current() == player
