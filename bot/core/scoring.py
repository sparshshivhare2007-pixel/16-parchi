"""
Scoring, winner check, and scoreboard.
"""

from config import POINTS_WIN, POINTS_WRONG_WINNER


def is_winner(parchi_list: list[dict]) -> bool:
    """Winner = 4 parchi all with the same naam."""
    if not parchi_list:
        return False
    first = parchi_list[0]["naam"]
    return all(p["naam"] == first for p in parchi_list)


def check_all_winners(distribution: dict[str, list[dict]]) -> str | None:
    """Return the name of the winner, or None."""
    for player, parchi_list in distribution.items():
        if is_winner(parchi_list):
            return player
    return None


def apply_points(scores: dict[str, int], player: str, delta: int) -> None:
    """Add delta to a player's score (in place)."""
    scores[player] = scores.get(player, 0) + delta


def award_win(scores: dict[str, int], player: str) -> None:
    apply_points(scores, player, POINTS_WIN)


def penalize_wrong_winner(scores: dict[str, int], player: str) -> None:
    apply_points(scores, player, POINTS_WRONG_WINNER)
