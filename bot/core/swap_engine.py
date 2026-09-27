"""
Swap validation and execution.
1 swap per turn enforced externally (handler side).
"""


def find_parchi_by_number(parchi_list: list[dict], number: int) -> dict | None:
    """Find a parchi with the given number in a list."""
    for p in parchi_list:
        if p["number"] == number:
            return p
    return None


def can_swap(
    giver_parchi: list[dict],
    taker_parchi: list[dict],
    number: int,
) -> tuple[bool, str]:
    """
    Check if a swap is legal.
    Returns (ok, reason).
    """
    giver = find_parchi_by_number(giver_parchi, number)
    if giver is None:
        return False, "You do not have a parchi with that number."

    taker = find_parchi_by_number(taker_parchi, number)
    if taker is None:
        return False, "Target does not have a parchi with that number."

    return True, "OK"


def execute_swap(
    giver_parchi: list[dict],
    taker_parchi: list[dict],
    number: int,
) -> tuple[list[dict], list[dict]]:
    """
    Swap parchi with matching number between two players.
    Returns (new_giver_list, new_taker_list).
    """
    giver_item = find_parchi_by_number(giver_parchi, number)
    taker_item = find_parchi_by_number(taker_parchi, number)

    new_giver = [taker_item if p is giver_item else p for p in giver_parchi]
    new_taker = [giver_item if p is taker_item else p for p in taker_parchi]

    return new_giver, new_taker
