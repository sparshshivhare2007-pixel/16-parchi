"""
Parchi generation, shuffle, and distribution.
"""

import random


def generate_parchi(players: list[str], per_player: int = 4) -> list[dict]:
    """
    Build all parchi: every player's name × numbers 1..per_player.
    Returns a list of dicts: {"naam": ..., "number": ...}
    """
    parchi = []
    for name in players:
        for number in range(1, per_player + 1):
            parchi.append({"naam": name, "number": number})
    return parchi


def shuffle_parchi(parchi: list[dict]) -> list[dict]:
    """Return a new shuffled list (does not mutate input)."""
    shuffled = parchi.copy()
    random.shuffle(shuffled)
    return shuffled


def distribute(parchi: list[dict], players: list[str], per_player: int = 4) -> dict:
    """
    Distribute shuffled parchi evenly — each player gets `per_player` parchi.
    Returns: {player_name: [parchi, ...], ...}
    """
    distribution = {}
    idx = 0
    for name in players:
        distribution[name] = parchi[idx : idx + per_player]
        idx += per_player
    return distribution
