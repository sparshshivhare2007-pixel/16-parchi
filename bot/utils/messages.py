"""
All English bot strings — single source of truth.
"""

# ── Game flow ────────────────────────────────────────────
GAME_CREATED = "🎮 Game created. Tap JOIN to enter."
GAME_STARTING = "🎲 Starting game... distributing parchi."
JOIN_SUCCESS = "✅ {name} has joined successfully ({count}/{max})"
JOIN_CONFIRMED = "You have joined the game."
PARCHI_FETCHED = "📩 Your parchi have been sent in DM."

# ── Swap ─────────────────────────────────────────────────
SWAP_INVALID_FORMAT = (
    "❌ Invalid swap.\n"
    "Use: /swap @username <number>\n"
    "Or reply to their message with: /swap <number>"
)
SWAP_SUCCESS = "✅ Swap successful."
SWAP_CONFIRMED = "Swap confirmed."
SWAP_CANCELLED = "Swap cancelled."
SWAP_NOT_YOUR_TURN = "❌ It is not your turn. Current turn: {current}"
SWAP_NO_PARCHI = "❌ You do not have a parchi with number {number}."
SWAP_TARGET_NO_PARCHI = "❌ {target} does not have a parchi with number {number}."
SWAP_LIMIT_REACHED = "❌ You already used your swap this turn."

# ── Winner / Score ───────────────────────────────────────
WINNER_CHECK_DONE = "🏆 Winner check complete."
WINNER_FOUND = "🏆 {player} wins! +{points} points."
WINNER_NOT_FOUND = "❌ No winner. -{penalty} points for {player}."
SCOREBOARD_HEADER = "📊 Scoreboard"
SCOREBOARD_LINE = "{player}: {points}"
