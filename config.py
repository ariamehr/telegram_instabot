import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Telegram Bot API token
TELEGRAM_TOKEN: str = os.getenv("TELEGRAM_TOKEN", "")
# Instagram credentials for login
INSTAGRAM_USER: str = os.getenv("INSTAGRAM_USER", "")
INSTAGRAM_PASSWORD: str = os.getenv("INSTAGRAM_PASSWORD", "")
# Directory where Instaloader will store session files
SESSION_DIR: str = os.getenv("SESSION_DIR", "sessions")

# Optional SSL certificate and key for running the web server over HTTPS
SSL_CERTFILE: str | None = os.getenv("SSL_CERTFILE")
SSL_KEYFILE: str | None = os.getenv("SSL_KEYFILE")
