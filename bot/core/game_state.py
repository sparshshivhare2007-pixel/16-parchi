"""
In-memory game state manager for Raja Chor Bot.

Holds all active games keyed by chat_id.
Each game tracks:
  - host
  - players (joined so far)
  - join message id (for updating count)
  - parchi distribution (player_id -> list of parchi dicts)
  - turn rotation
  - swap-used flag per turn
  - scores
  - status (waiting | running | finished)
"""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Optional

from bot.core.rotation import Rotation


# ─────────────────────────────────────────────────────────
# Player
# ─────────────────────────────────────────────────────────
@dataclass
class Player:
    user_id: int
    username: Optional[str]
    first_name: str


# ─────────────────────────────────────────────────────────
# Game
# ─────────────────────────────────────────────────────────
@dataclass
class Game:
    chat_id: int
    host_id: int
    status: str = "waiting"          # waiting | running | finished
    created_at: float = field(default_factory=time.time)

    players: list[Player] = field(default_factory=list)
    join_message_id: Optional[int] = None    # group message with JOIN button

    # Parchi distribution: user_id -> [ {"naam":..., "number":...}, ... ]
    distribution: dict[int, list[dict]] = field(default_factory=dict)

    # Turn system
    rotation: Optional[Rotation] = None
    swap_used_this_turn: bool = False

    # Scoring
    scores: dict[int, int] = field(default_factory=dict)

    # ── helpers ──────────────────────────────────────────
    def has_player(self, user_id: int) -> bool:
        return any(p.user_id == user_id for p in self.players)

    def add_player(self, user_id: int, username: Optional[str], first_name: str) -> bool:
        """Add player. Returns False if already present or full."""
        if self.has_player(user_id):
            return False
        if len(self.players) >= 4:
            return False
        self.players.append(Player(user_id, username, first_name))
        self.scores[user_id] = self.scores.get(user_id, 0)
        return True

    def player_count(self) -> int:
        return len(self.players)

    def is_full(self) -> bool:
        return len(self.players) >= 4

    def get_player(self, user_id: int) -> Optional[Player]:
        for p in self.players:
            if p.user_id == user_id:
                return p
        return None

    def get_player_by_username(self, username: str) -> Optional[Player]:
        uname = username.lstrip("@").lower()
        for p in self.players:
            if p.username and p.username.lower() == uname:
                return p
        return None

    def current_turn_player(self) -> Optional[Player]:
        if self.rotation is None:
            return None
        name = self.rotation.current()
        for p in self.players:
            if p.first_name == name:
                return p
        return None

    def advance_turn(self) -> None:
        """Move to next player and reset swap flag."""
        if self.rotation is not None:
            self.rotation.next()
        self.swap_used_this_turn = False

    def is_turn_of(self, user_id: int) -> bool:
        cur = self.current_turn_player()
        return cur is not None and cur.user_id == user_id


# ─────────────────────────────────────────────────────────
# Global registry
# ─────────────────────────────────────────────────────────
_games: dict[int, Game] = {}


# ─────────────────────────────────────────────────────────
# Public API
# ─────────────────────────────────────────────────────────
def create_game(chat_id: int, host_id: int) -> Game:
    """Create a new game in a chat (replaces existing one)."""
    game = Game(chat_id=chat_id, host_id=host_id)
    _games[chat_id] = game
    return game


def get_game(chat_id: int) -> Optional[Game]:
    return _games.get(chat_id)


def remove_game(chat_id: int) -> None:
    _games.pop(chat_id, None)


def has_game(chat_id: int) -> bool:
    return chat_id in _games


def all_games() -> dict[int, Game]:
    return _games
