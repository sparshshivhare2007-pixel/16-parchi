# Raja Chor Bot

A Telegram bot built with **Telethon** for the classic Indian game
"Raja Bajir Chor Sipahi" — parchi edition.

## Game Summary
- 4 players join via inline button (DM confirmation).
- Bot generates 16 parchi (each player's name × 4 numbers).
- Parchi are shuffled and distributed privately — names stay hidden.
- Fixed rotation: turns swap one parchi per turn.
- `/winner` checks for 4 same-name parchi → +100, else −50.

## Rules (Locked)
| Rule | Value |
|------|-------|
| Swap per turn | 1 only |
| Swap format | Reply or `/swap @user 3` |
| Bare `/swap 3` | Rejected |
| Rotation | Fixed |
| Winner | Manual `/winner` |
| Win | +100 |
| Wrong `/winner` | −50 |
| Language | English only |

## Commands
`/startgame` · `/start` · `/myparchi` · `/swap @user 3` · `/swap 3` (reply) · `/winner` · `/score`

## Stack
- Python 3.11+
- Telethon
- SQLite (SQLAlchemy)

## Setup
```bash
git clone <repo>
cd raja-chor-bot
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env          # fill in API_ID, API_HASH, BOT_TOKEN
python -m bot.main
