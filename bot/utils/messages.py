"""
All English bot strings — single source of truth.
"""

# ── Game flow ────────────────────────────────────────────
GAME_CREATED = "🎮 Game created. Tap JOIN to enter. ({count}/{max})"
GAME_STARTING = "🎲 Starting game... distributing parchi."

GAME_ALREADY_WAITING = "⚠️ A game is already waiting for players in this chat."
GAME_ALREADY_RUNNING = "⚠️ A game is already running in this chat."

NO_ACTIVE_GAME = "❌ No active game in this chat. Use /startgame to begin."

NOT_ENOUGH_PLAYERS = "❌ Not enough players ({count}/{max}). Need 4 to start."
NOT_IN_GAME = "❌ You are not part of this game."

# ── Join flow ────────────────────────────────────────────
JOIN_SUCCESS = "✅ {name} has joined successfully ({count}/{max})"
JOIN_CONFIRMED = "You have joined the game."
JOIN_ALREADY = "⚠️ You have already joined this game."
JOIN_FULL = "⚠️ The game is already full."
JOIN_CLOSED = "⚠️ This game is no longer accepting players."
JOIN_FAILED = "❌ Could not join. Please try again."
JOIN_TIMEOUT_NOT_ENOUGH = (
    "⏳ Time is up. Only {count}/{max} players joined. Game cancelled."
)

# ── DM / Parchi ──────────────────────────────────────────
PARCHI_FETCHED = "📩 Your parchi have been sent in DM."
PARCHI_SENT_DM = "📩 Parchi sent to your DM."
PARCHI_DM_HEADER = "🎴 Your 4 parchi (hidden until you reveal):"
PARCHI_DM_LINE = "  • Parchi #{slot}"
PARCHI_DM_FOOTER = "Use /myparchi to reveal them."

PARCHI_REVEAL_HEADER = "🎴 Your parchi:"
PARCHI_REVEAL_LINE = "  • Parchi #{slot} → {naam} ({number})"

DM_FAILED = "⚠️ Could not DM {name}. Ask them to start the bot first."
DM_FAILED_SELF = "❌ I could not DM you. Please start the bot in private first."

# ── Turn ─────────────────────────────────────────────────
TURN_ANNOUNCE = "🎯 Turn #{number} — {player}, it's your turn."

# ── Swap ─────────────────────────────────────────────────
SWAP_INVALID_FORMAT = (
    "❌ Invalid swap.\n"
    "Use: /swap @username <number>\n"
    "Or reply to their message with: /swap <number>"
)
SWAP_SUCCESS = "✅ Swap successful.\n{giver} ↔ {taker} (Parchi #{number})"
SWAP_CONFIRMED = "Swap confirmed."
SWAP_CANCELLED = "Swap cancelled."

SWAP_NOT_YOUR_TURN = "❌ It is not your turn. Current turn: {current}"
SWAP_NO_PARCHI = "❌ You do not have a parchi with number {number}."
SWAP_TARGET_NO_PARCHI = "❌ {target} does not have a parchi with number {number}."
SWAP_LIMIT_REACHED = "❌ You already used your swap this turn."
SWAP_TARGET_NOT_FOUND = "❌ Could not find that player in this game."
SWAP_SELF = "❌ You cannot swap with yourself."

# ── Winner / Score ───────────────────────────────────────
WINNER_CHECK_DONE = "🏆 Winner check complete."
WINNER_FOUND = "🏆 {player} wins! +{points} points."
WINNER_NOT_FOUND = "❌ No winner. -{penalty} points for {player}."
SCOREBOARD_HEADER = "📊 Scoreboard"
SCOREBOARD_LINE = "{player}: {points}"
