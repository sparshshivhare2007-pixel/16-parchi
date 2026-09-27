"""
Handles: /winner and /score.
"""

import logging

from telethon import events

from bot.utils import messages as msg
from bot.core import game_state
from bot.core.scoring import (
    check_all_winners,
    award_win,
    penalize_wrong_winner,
)
from config import POINTS_WIN, POINTS_WRONG_WINNER


log = logging.getLogger(__name__)


def register(client) -> None:

    # ── /winner ──────────────────────────────────────────
    @client.on(events.NewMessage(pattern=r"^/winner$"))
    async def winner_handler(event):
        chat_id = event.chat_id

        # 1. Game must be running
        game = game_state.get_game(chat_id)
        if game is None or game.status != "running":
            await event.reply(msg.NO_ACTIVE_GAME)
            return

        # 2. Sender must be a player
        sender = await event.get_sender()
        if not game.has_player(sender.id):
            await event.reply(msg.NOT_IN_GAME)
            return

        # 3. Check for a winner — map user_id -> parchi list
        dist_by_name = {
            game.get_player(uid).first_name: parchis
            for uid, parchis in game.distribution.items()
            if game.get_player(uid) is not None
        }

        winner_name = check_all_winners(dist_by_name)

        if winner_name:
            # 4a. Winner found — award points
            winner_player = None
            for p in game.players:
                if p.first_name == winner_name:
                    winner_player = p
                    break

            if winner_player:
                award_win(game.scores, winner_player.user_id)

            game.status = "finished"

            await event.reply(
                msg.WINNER_FOUND.format(
                    player=winner_name, points=POINTS_WIN
                )
            )
            await _send_scoreboard(client, game)
        else:
            # 4b. No winner — penalize the caller
            penalize_wrong_winner(game.scores, sender.id)
            await event.reply(
                msg.WINNER_NOT_FOUND.format(
                    player=sender.first_name, penalty=abs(POINTS_WRONG_WINNER)
                )
            )

    # ── /score ───────────────────────────────────────────
    @client.on(events.NewMessage(pattern=r"^/score$"))
    async def score_handler(event):
        chat_id = event.chat_id
        game = game_state.get_game(chat_id)

        if game is None:
            await event.reply(msg.NO_ACTIVE_GAME)
            return

        await _send_scoreboard(client, game)


# ─────────────────────────────────────────────────────────
# Helper: build and send scoreboard
# ─────────────────────────────────────────────────────────
async def _send_scoreboard(client, game) -> None:
    lines = [msg.SCOREBOARD_HEADER]
    # Sort by score descending
    ranked = sorted(
        game.players,
        key=lambda p: game.scores.get(p.user_id, 0),
        reverse=True,
    )
    for p in ranked:
        lines.append(
            msg.SCOREBOARD_LINE.format(
                player=p.first_name,
                points=game.scores.get(p.user_id, 0),
            )
        )
    await client.send_message(game.chat_id, "\n".join(lines))
