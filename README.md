# Telegram Bot Webhook

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

This approach ensures a consistent webhook URL and simplifies the development workflow.
## Project Structure

```
Telegram_Bot_Webhook/
├─ main.py            # FastAPI app & webhook logic
├─ .env               # Environment variables
├─ requirements.txt   # Dependencies
├─ start.ps1          # PowerShell script
└─ run.bat            # CMD script