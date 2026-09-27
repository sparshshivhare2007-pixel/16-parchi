"""
Swap format validation — rejects bare /swap 3.
"""

import re


SWAP_PATTERN = re.compile(r"^/swap(?:\s+@(\w+))?(?:\s+(\d+))?\s*$")


def is_valid_swap_format(event) -> bool:
    """
    A swap is valid only if it is a reply OR contains a @tag.
    Bare `/swap 3` is rejected.
    """
    text = (event.raw_text or "").strip()
    match = SWAP_PATTERN.match(text)
    if not match:
        return False

    tag, number = match.group(1), match.group(2)

    # Must have a number
    if number is None:
        return False

    # Must have reply OR tag
    has_reply = event.is_reply
    has_tag = tag is not None

    return has_reply or has_tag


def parse_swap(event) -> tuple[str | None, int | None]:
    """
    Extract tag and number from a /swap message.
    Returns (tag_or_None, number_or_None).
    """
    text = (event.raw_text or "").strip()
    match = SWAP_PATTERN.match(text)
    if not match:
        return None, None
    tag = match.group(1)
    number = int(match.group(2)) if match.group(2) else None
    return tag, number
