from fastapi import FastAPI, Request
import requests
from dotenv import load_dotenv
import os
from contextlib import asynccontextmanager
import logging
from rich.logging import RichHandler
from rich.console import Console

load_dotenv()
logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    handlers=[RichHandler(markup=True)]
)
logger = logging.getLogger("telegram_bot")
console = Console()

def check_ngrok():
    try:
        r = requests.get("http://127.0.0.1:4040/api/tunnels")
        if r.status_code == 200:
            logger.info("[green]✔ ngrok server is running[/green]")
        else:
            logger.error(f"[red]✖ ngrok API responded with status {r.status_code}[/red]")
    except requests.exceptions.RequestException as e:
        logger.error(f"[red]✖ ngrok server is not running: {e}[/red]")

BOT_TOKEN = os.getenv("BOT_TOKEN")
WEB_HOOK_URL = os.getenv("N8N_WEB_HOOK_URL")
NGROK_URL = os.getenv("NGROK_URL")
PORT = os.getenv("PORT")

async def setup_webhook():
    """
    Sets up the webhook URL for the Telegram Bot API.
    """
    check_ngrok()
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/setWebhook"
    data = {"url": f"{NGROK_URL}/webhook"}
    response = requests.get(url, params=data)
    if response.status_code == 200:
        logger.info("[green]✔ Webhook successfully set up[/green]")
    else:
        logger.error(f"[red]✖ Failed to set up webhook:[/] {response.json()}")

@asynccontextmanager
async def lifespan(app: FastAPI):
    await setup_webhook()
    yield

app = FastAPI(lifespan=lifespan)

@app.post("/webhook")
async def telegram_webhook(request: Request):
    
    data = await request.json()
    
    logger.info(f"[cyan]↪ Received data:[/] {data}")
    
    chat_id = data['message']['chat']['id']  # Extract the chat_id
    text     = data['message']['text']
    
    async def pass_message_to_n8n(text):
        """
        This function sends a request to the n8n-webhook server
        and retrieve the response.
        
        Args:
            text (str): The text received from Telegram
        
        Returns:
            dict: The response from the n8n-webhook server
        """
        url = WEB_HOOK_URL
        response = requests.get(url, data={
            "query": text
        })

        return response.json()
    
    
    async def send_message(chat_id: int, text: str):
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        data = {"chat_id": chat_id, "text": text}
        response = requests.post(url, json=data)
        return response.json()
    
    async def main():
        response = await pass_message_to_n8n(text)
        await send_message(chat_id, response['output'])
        logger.info(f"[green]✔ Message sent successfully[/green]")
        return {"ok": True}
    
    await main()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=int(PORT), reload=True)
    logger.info(f"[green]✔ Server started successfully[/green]")