"""
Handles: /winner and /score.
"""

import logging

from telethon import events

from bot.utils import messages as msg

log = logging.getLogger(__name__)


def register(client) -> None:

    @client.on(events.NewMessage(pattern=r"^/winner$"))
    async def winner_handler(event):
        # TODO: check for 4 same-name parchi
        await event.reply(msg.WINNER_CHECK_DONE)

    @client.on(events.NewMessage(pattern=r"^/score$"))
    async def score_handler(event):
        # TODO: build scoreboard
        await event.reply(msg.SCOREBOARD_HEADER)
