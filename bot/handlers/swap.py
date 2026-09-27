"""
Handles: /swap command (reply or tag, 1 per turn).
"""

import logging

from telethon import events

from bot.utils import messages as msg
from bot.utils.validators import is_valid_swap_format

log = logging.getLogger(__name__)


def register(client) -> None:

    @client.on(events.NewMessage(pattern=r"^/swap"))
    async def swap_handler(event):
        # Validate format first
        if not is_valid_swap_format(event):
            await event.reply(msg.SWAP_INVALID_FORMAT)
            return

        # TODO: check turn, number match, execute swap
        await event.reply(msg.SWAP_SUCCESS)
