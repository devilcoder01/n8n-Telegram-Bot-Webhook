#!/usr/bin/env bash
# start.sh - Automate ngrok and FastAPI server startup on Linux
# Usage: from project root: chmod +x start.sh && ./start.sh

# Load environment variables
if [ ! -f .env ]; then
  echo ".env file not found, create one based on README.md" >&2
  exit 1
fi
set -o allexport
source .env
set +o allexport

# Configure ngrok authentication
echo "Configuring ngrok authtoken..."
ngrok config add-authtoken "$NGROK_API_KEY"

# Activate or create virtual environment
echo "Setting up virtual environment..."
if [ -f venv/bin/activate ]; then
  source venv/bin/activate
else
  python3 -m venv venv
  source venv/bin/activate
  pip install -r requirements.txt
fi

# Start API server in background
echo "Starting FastAPI server..."
uv run main.py &
SERVER_PID=$!

echo "FastAPI PID: $SERVER_PID"

# Launch ngrok tunnel
echo "Launching ngrok tunnel..."
ngrok http --url="$NGROK_URL" "$PORT"

# Wait for server to exit (if ever)
wait $SERVER_PID
