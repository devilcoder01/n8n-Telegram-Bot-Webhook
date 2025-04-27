# Telegram Bot Webhook for n8n

> **Disclaimer**: This application is designed to work exclusively with Telegram bots. It does not support Telegram channels or other Telegram triggers.

A FastAPI application that connects Telegram Bot messages with n8n workflows.

## Features

- Automatic Telegram webhook setup
- n8n workflow integration
- Rich terminal logging
- Local development with ngrok

## Setup

1. Place `ngrok.exe` in project root
2. Create `.env` file:
   ```
   BOT_TOKEN=<telegram_bot_token>
   N8N_WEB_HOOK_URL=<n8n_webhook_url>
   NGROK_URL=<ngrok_url>
   PORT=8000
   NGROK_API_KEY=<ngrok_authtoken>
   ```

## Installation

### Using UV (Recommended)

1. Install UV:
   ```
   pip install uv
   ```

2. Run uv:
   ```
   uv run
   ```

### Using pip

```
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Usage

### Start with scripts

- CMD (Windows): `run.bat`
- Linux/macOS: `./start.sh`

### Manual start

1. Start ngrok: `ngrok http --url=%NGROK_URL% %PORT%`
2. Run server: `uv run main.py`

### Recommendation: Static ngrok URL

For a more seamless experience, it is recommended to generate a static `ngrok_url` from the [ngrok dashboard](https://dashboard.ngrok.com/). Using a static URL eliminates the need to update the `NGROK_URL` in the `.env` file every time you restart `ngrok`. 

Steps to set up a static `ngrok_url`:
1. Log in to your ngrok account.
2. Navigate to the (https://dashboard.ngrok.com/domains) section in the dashboard.
3. create a custom subdomain (e.g., `your-app-name.ngrok.io`).
4. Update the `NGROK_URL` in your `.env` file with the reserved domain.

## Integrating with n8n

To connect this application with n8n, use the Webhook Trigger node instead of the Telegram Trigger node. Configure the webhook path to `/telegram` (or any custom path of your choice). If you choose a custom path, ensure that the same path is updated in the `.env` file. Additionally, set the "Respond with" option in the Webhook Trigger node to "First Entry JSON" for proper functionality.



