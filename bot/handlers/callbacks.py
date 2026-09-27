"""
Handles: inline button taps (JOIN, YES, NO).
"""

import logging

from telethon import events

from bot.utils import messages as msg
from bot.core import game_state
from bot.handlers import game as game_handler


log = logging.getLogger(__name__)


def register(client) -> None:

    # ── JOIN button ──────────────────────────────────────
    @client.on(events.CallbackQuery(data=b"join"))
    async def join_callback(event):
        # Delegate to game.py — it owns the join logic
        await game_handler.handle_join(client, event)

    # ── YES (swap confirm) ───────────────────────────────
    @client.on(events.CallbackQuery(data=b"yes"))
    async def yes_callback(event):
        chat_id = event.chat_id
        game = game_state.get_game(chat_id)

        if game is None or game.status != "running":
            await event.answer(msg.NO_ACTIVE_GAME, alert=True)
            return

        # TODO: swap confirm flow (pending confirmation system)
        # Placeholder for now — swap.py executes directly
        await event.answer(msg.SWAP_CONFIRMED, alert=False)

    # ── NO (swap cancel) ─────────────────────────────────
    @client.on(events.CallbackQuery(data=b"no"))
    async def no_callback(event):
        chat_id = event.chat_id
        game = game_state.get_game(chat_id)

        if game is None or game.status != "running":
            await event.answer(msg.NO_ACTIVE_GAME, alert=True)
            return

        # TODO: swap cancel flow (pending confirmation system)
        await event.answer(msg.SWAP_CANCELLED, alert=False)
