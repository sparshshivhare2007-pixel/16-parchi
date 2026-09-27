"""
Handles: inline button taps (JOIN, YES, NO).
"""

import logging

from telethon import events

from bot.utils import messages as msg

log = logging.getLogger(__name__)


def register(client) -> None:

    @client.on(events.CallbackQuery(data=b"join"))
    async def join_callback(event):
        # TODO: add player, update count, announce in group
        await event.answer(msg.JOIN_CONFIRMED, alert=False)

    @client.on(events.CallbackQuery(data=b"yes"))
    async def yes_callback(event):
        # TODO: confirm swap
        await event.answer(msg.SWAP_CONFIRMED, alert=False)

    @client.on(events.CallbackQuery(data=b"no"))
    async def no_callback(event):
        # TODO: cancel swap
        await event.answer(msg.SWAP_CANCELLED, alert=False)
