"""
Handler registration hub.
Every handler module exposes a `register(client)` function.
"""

from bot.handlers import game, swap, winner, callbacks


def register_all_handlers(client) -> None:
    """Register every handler module with the Telethon client."""
    game.register(client)
    swap.register(client)
    winner.register(client)
    callbacks.register(client)
