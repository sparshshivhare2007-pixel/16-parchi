"""
Handles: /startgame, /start, JOIN flow, join timer.
"""

import logging

from telethon import events

from bot.utils import messages as msg

log = logging.getLogger(__name__)


def register(client) -> None:

    @client.on(events.NewMessage(pattern=r"^/startgame$"))
    async def startgame_handler(event):
        # TODO: create game state, post JOIN button
        await event.reply(msg.GAME_CREATED)

    @client.on(events.NewMessage(pattern=r"^/start$"))
    async def start_handler(event):
        # TODO: verify 4 players, start distribution
        await event.reply(msg.GAME_STARTING)

    @client.on(events.NewMessage(pattern=r"^/myparchi$"))
    async def myparchi_handler(event):
        # TODO: fetch player's parchi and DM them
        await event.reply(msg.PARCHI_FETCHED)
