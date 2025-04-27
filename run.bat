@echo off
REM run.bat - Automate ngrok and API server startup
REM Usage: Run from project root in cmd.exe

REM Load environment variables from .env
for /f "usebackq tokens=1* delims==" %%A in (".env") do (
    set "%%A=%%~B"
)

REM Configure ngrok authentication
ECHO Configuring ngrok authtoken...
.\ngrok.exe config add-authtoken %NGROK_API_KEY%

REM Start API server in new window
ECHO Starting API server...
start "API Server" cmd /k "cd /d %~dp0 && call.\.venv\Scripts\activate && uv run main.py"

REM Launch ngrok tunnel
ECHO Launching ngrok tunnel...
.\ngrok.exe http --url=%NGROK_URL% %PORT%

PAUSE