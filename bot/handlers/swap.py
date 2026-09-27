"""
Handles: /swap command (reply or tag, 1 per turn).
"""

import logging

from telethon import events

from bot.utils import messages as msg
from bot.utils.validators import is_valid_swap_format, parse_swap
from bot.core import game_state
from bot.core.swap_engine import can_swap, execute_swap


log = logging.getLogger(__name__)


def register(client) -> None:

    @client.on(events.NewMessage(pattern=r"^/swap"))
    async def swap_handler(event):
        chat_id = event.chat_id

        # ── 1. Game check ───────────────────────────────
        game = game_state.get_game(chat_id)
        if game is None or game.status != "running":
            await event.reply(msg.NO_ACTIVE_GAME)
            return

        # ── 2. Sender must be a player ──────────────────
        sender = await event.get_sender()
        if not game.has_player(sender.id):
            await event.reply(msg.NOT_IN_GAME)
            return

        # ── 3. Format check (reply or tag) ──────────────
        if not is_valid_swap_format(event):
            await event.reply(msg.SWAP_INVALID_FORMAT)
            return

        tag, number = parse_swap(event)
        if number is None:
            await event.reply(msg.SWAP_INVALID_FORMAT)
            return

        # ── 4. Turn check ───────────────────────────────
        if not game.is_turn_of(sender.id):
            current = game.current_turn_player()
            current_name = current.first_name if current else "Unknown"
            await event.reply(msg.SWAP_NOT_YOUR_TURN.format(current=current_name))
            return

        # ── 5. One swap per turn ────────────────────────
        if game.swap_used_this_turn:
            await event.reply(msg.SWAP_LIMIT_REACHED)
            return

        # ── 6. Resolve target player ────────────────────
        target = None

        # Case A: reply to someone's message
        if event.is_reply:
            replied = await event.get_reply_message()
            if replied:
                replied_sender = await replied.get_sender()
                if replied_sender and game.has_player(replied_sender.id):
                    target = game.get_player(replied_sender.id)

        # Case B: tag
        if target is None and tag:
            target = game.get_player_by_username(tag)

        if target is None:
            await event.reply(msg.SWAP_TARGET_NOT_FOUND)
            return

        # ── 7. Can't swap with yourself ─────────────────
        if target.user_id == sender.id:
            await event.reply(msg.SWAP_SELF)
            return

        # ── 8. Get both parchi lists ────────────────────
        giver_parchi = game.distribution.get(sender.id, [])
        taker_parchi = game.distribution.get(target.user_id, [])

        ok, reason = can_swap(giver_parchi, taker_parchi, number)
        if not ok:
            # Pick the right localized message
            if "You do not have" in reason:
                await event.reply(msg.SWAP_NO_PARCHI.format(number=number))
            elif "Target does not have" in reason:
                await event.reply(
                    msg.SWAP_TARGET_NO_PARCHI.format(
                        target=target.first_name, number=number
                    )
                )
            else:
                await event.reply(reason)
            return

        # ── 9. Execute swap ─────────────────────────────
        new_giver, new_taker = execute_swap(giver_parchi, taker_parchi, number)
        game.distribution[sender.id] = new_giver
        game.distribution[target.user_id] = new_taker

        # ── 10. Mark swap used + advance turn ───────────
        game.swap_used_this_turn = True
        game.advance_turn()

        # ── 11. Confirm in group (no names revealed) ────
        await event.reply(
            msg.SWAP_SUCCESS.format(
                giver=sender.first_name,
                taker=target.first_name,
                number=number,
            )
        )

        # ── 12. Announce next turn ──────────────────────
        next_player = game.current_turn_player()
        if next_player:
            await client.send_message(
                chat_id,
                msg.TURN_ANNOUNCE.format(
                    player=next_player.first_name,
                    number=game.rotation.index + 1,
                ),
            )
