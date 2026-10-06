# BOND VPN 2.0

Telegram VPN shop for BOND VPN. One subscription gives access to all configured locations.

## Included
- 1 / 3 / 6 / 12 month plans
- 1 included device + paid extra devices
- USA, Germany, Spain, Poland, Lithuania nodes
- Promo codes
- Referral program
- Telegram Stars payment
- CryptoBot payment
- Platega adapter placeholder (API credentials/config can be added later)
- Admin commands
- SQLite
- Docker
- H1Cloud VLESS API adapter
- QR-ready subscription/link delivery

## Important
Do NOT put real API tokens into Git or send them in chat. Copy `.env.example` to `.env` and fill secrets locally.

Germany is intentionally disabled until its H1 API URL/token are available.

## Run
```bash
cp .env.example .env
# edit .env
docker compose up -d --build
```

Or locally:
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python bot.py
```

The bot uses polling, so no public HTTPS endpoint is required for Telegram.

## Admin
Set numeric Telegram IDs in `ADMIN_IDS`.
The bot command `/myid` shows a user's Telegram ID.

## H1 API
The project follows the H1Cloud VLESS API pattern used by the public H1Cloud VPN-selling reference project: `/health`, `/create`, `/edit`, `/clients/{name}`.
