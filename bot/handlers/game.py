"""
Handles: /startgame, /start, /myparchi, JOIN flow, join timer.
"""

import asyncio
import logging
import random

from telethon import events, Button

from bot.utils import messages as msg
from bot.core import game_state
from bot.core.parchi import generate_parchi, shuffle_parchi, distribute
from bot.core.rotation import Rotation
from config import JOIN_TIMEOUT_SECONDS, MAX_PLAYERS


log = logging.getLogger(__name__)


# ─────────────────────────────────────────────────────────
# Background: auto-start after join timeout
# ─────────────────────────────────────────────────────────
async def _auto_start_after_timeout(client, chat_id: int) -> None:
    """Wait JOIN_TIMEOUT_SECONDS, then start game if still waiting."""
    await asyncio.sleep(JOIN_TIMEOUT_SECONDS)

    game = game_state.get_game(chat_id)
    if game is None or game.status != "waiting":
        return

    if not game.is_full():
        await client.send_message(
            chat_id,
            msg.JOIN_TIMEOUT_NOT_ENOUGH.format(
                count=game.player_count(),
                max=MAX_PLAYERS,
            ),
        )
        game_state.remove_game(chat_id)
        return

    await _start_game(client, game)


# ─────────────────────────────────────────────────────────
# Core: start the game and distribute parchi
# ─────────────────────────────────────────────────────────
async def _start_game(client, game) -> None:
    """Generate parchi, assign rotation, DM each player their parchi."""
    game.status = "running"

    # 1. Build rotation order (fixed) from current players
    order = [p.first_name for p in game.players]
    game.rotation = Rotation(order)

    # 2. Generate + shuffle parchi
    all_parchi = generate_parchi(order, per_player=4)
    shuffled = shuffle_parchi(all_parchi)

    # 3. Distribute: player.first_name -> [parchi...]
    dist_by_name = distribute(shuffled, order, per_player=4)

    # 4. Map back to user_id and store in game
    game.distribution = {}
    for player in game.players:
        game.distribution[player.user_id] = dist_by_name[player.first_name]

    # 5. Announce in group
    await client.send_message(game.chat_id, msg.GAME_STARTING)

    # 6. DM each player their 4 parchi (with hidden numbers 1..4)
    for player in game.players:
        parchi_list = game.distribution[player.user_id]
        lines = [msg.PARCHI_DM_HEADER]
        for idx, p in enumerate(parchi_list, start=1):
            lines.append(msg.PARCHI_DM_LINE.format(slot=idx))
        lines.append(msg.PARCHI_DM_FOOTER)
        try:
            await client.send_message(player.user_id, "\n".join(lines))
        except Exception as e:
            log.warning("Could not DM %s: %s", player.first_name, e)
            await client.send_message(
                game.chat_id,
                msg.DM_FAILED.format(name=player.first_name),
            )

    # 7. Announce whose turn it is
    current = game.rotation.current()
    await client.send_message(
        game.chat_id,
        msg.TURN_ANNOUNCE.format(player=current, number=1),
    )


# ─────────────────────────────────────────────────────────
# Register handlers
# ─────────────────────────────────────────────────────────
def register(client) -> None:

    # ── /startgame ───────────────────────────────────────
    @client.on(events.NewMessage(pattern=r"^/startgame$"))
    async def startgame_handler(event):
        chat_id = event.chat_id

        if game_state.has_game(chat_id):
            game = game_state.get_game(chat_id)
            if game and game.status == "waiting":
                await event.reply(msg.GAME_ALREADY_WAITING)
                return

        game = game_state.create_game(chat_id, host_id=event.sender_id)

        text = msg.GAME_CREATED.format(count=0, max=MAX_PLAYERS)
        buttons = [[Button.inline("JOIN", data=b"join")]]
        sent = await event.reply(text, buttons=buttons)
        game.join_message_id = sent.id

        # Kick off auto-start timer
        asyncio.create_task(_auto_start_after_timeout(client, chat_id))

    # ── /start ───────────────────────────────────────────
    @client.on(events.NewMessage(pattern=r"^/start$"))
    async def start_handler(event):
        chat_id = event.chat_id
        game = game_state.get_game(chat_id)

        if game is None:
            await event.reply(msg.NO_ACTIVE_GAME)
            return

        if game.status != "waiting":
            await event.reply(msg.GAME_ALREADY_RUNNING)
            return

        if not game.is_full():
            await event.reply(
                msg.NOT_ENOUGH_PLAYERS.format(
                    count=game.player_count(), max=MAX_PLAYERS
                )
            )
            return

        await _start_game(client, game)

    # ── /myparchi ────────────────────────────────────────
    @client.on(events.NewMessage(pattern=r"^/myparchi$"))
    async def myparchi_handler(event):
        chat_id = event.chat_id
        game = game_state.get_game(chat_id)

        if game is None or game.status != "running":
            await event.reply(msg.NO_ACTIVE_GAME)
            return

        parchi_list = game.distribution.get(event.sender_id)
        if not parchi_list:
            await event.reply(msg.NOT_IN_GAME)
            return

        # Reveal in DM only
        lines = [msg.PARCHI_REVEAL_HEADER]
        for idx, p in enumerate(parchi_list, start=1):
            lines.append(
                msg.PARCHI_REVEAL_LINE.format(
                    slot=idx, naam=p["naam"], number=p["number"]
                )
            )
        try:
            await client.send_message(event.sender_id, "\n".join(lines))
            await event.reply(msg.PARCHI_SENT_DM)
        except Exception as e:
            log.warning("DM failed for %s: %s", event.sender_id, e)
            await event.reply(msg.DM_FAILED_SELF)


# ─────────────────────────────────────────────────────────
# Helper exposed for callbacks.py (JOIN tap)
# ─────────────────────────────────────────────────────────
async def handle_join(client, event) -> None:
    """Called from callbacks.py when JOIN button is tapped."""
    chat_id = event.chat_id
    user = await event.get_sender()

    game = game_state.get_game(chat_id)
    if game is None or game.status != "waiting":
        await event.answer(msg.JOIN_CLOSED, alert=True)
        return

    if game.has_player(user.id):
        await event.answer(msg.JOIN_ALREADY, alert=True)
        return

    if game.is_full():
        await event.answer(msg.JOIN_FULL, alert=True)
        return

    added = game.add_player(user.id, user.username, user.first_name)
    if not added:
        await event.answer(msg.JOIN_FAILED, alert=True)
        return

    # Answer in DM
    await event.answer(msg.JOIN_CONFIRMED, alert=False)

    # Announce in group
    count = game.player_count()
    await client.send_message(
        chat_id,
        msg.JOIN_SUCCESS.format(
            name=user.first_name, count=count, max=MAX_PLAYERS
        ),
    )

    # Update the JOIN button message text
    if game.join_message_id:
        try:
            await client.edit_message(
                chat_id,
                game.join_message_id,
                msg.GAME_CREATED.format(count=count, max=MAX_PLAYERS),
                buttons=[[Button.inline("JOIN", data=b"join")]] if not game.is_full() else None,
            )
        except Exception as e:
            log.warning("Could not edit join message: %s", e)

    # If full → start immediately (don't wait for timer)
    if game.is_full():
        await _start_game(client, game)
