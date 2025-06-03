# Telegram Instagram Bot

A powerful Telegram bot to interact with Instagram — fetch profile information, download posts and stories from the users you follow — while respecting Instagram's rate limits to minimize the risk of being blocked.

## 🚀 Features

- **Authenticate** with your Instagram account securely.
- **/profile `<username>`**: Retrieve profile picture, full name, follower count, bio and profile URL for any public Instagram account.
- **/download_posts `<username>`**: Download the latest 5 posts of a public account.
- **/download_stories**: Download all current stories of the users you follow.
- **Rate limiting & sessions**: Built on [Instaloader](https://instaloader.github.io/) with automatic throttling and session caching.
- **Web API**: Access the same features through a FastAPI server, served over HTTPS.

## 🔧 Installation

1. Clone the repo:

   ```bash
   git clone https://github.com/ariamehr/telegram-instabot.git
   cd telegram-instabot
   ```

2. Create a Python 3.10+ virtual environment and activate it:

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the project root (see [config.py](config.py)):

   ```ini
   TELEGRAM_TOKEN=your_telegram_bot_token_here
   INSTAGRAM_USER=your_instagram_username
   INSTAGRAM_PASSWORD=your_instagram_password
   # Optional: paths to SSL certificate and key for HTTPS
   SSL_CERTFILE=/path/to/cert.pem
   SSL_KEYFILE=/path/to/key.pem
   ```

5. Run the bot:

   ```bash
   python bot.py
   ```

6. Launch the optional web interface:

   ```bash
   uvicorn web_app:app --reload \
       --ssl-keyfile "$SSL_KEYFILE" --ssl-certfile "$SSL_CERTFILE"
   ```

## ⚙️ Configuration (`config.py`)

```python
import os
from dotenv import load_dotenv

load_dotenv()  # load variables from .env

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")  # Telegram Bot API token
INSTAGRAM_USER = os.getenv("INSTAGRAM_USER")  # Instagram username for login
INSTAGRAM_PASSWORD = os.getenv("INSTAGRAM_PASSWORD")  # Instagram password for login
SESSION_DIR = os.getenv("SESSION_DIR", "sessions")  # directory for Instaloader sessions
SSL_CERTFILE = os.getenv("SSL_CERTFILE")  # path to SSL certificate
SSL_KEYFILE = os.getenv("SSL_KEYFILE")  # path to SSL key
```

## 📜 Usage

Once the bot is running, open Telegram and send:

- `/start` — Show welcome message and available commands.
- `/profile <username>` — Fetch and display profile info.
- `/download_posts <username>` — Download up to 5 latest posts and send them.
- `/download_stories` — Download all current stories from your followees and send a ZIP archive.

## 🛡️ Avoiding Rate Limits

- **Session caching**: Instaloader stores a session file under `sessions/` to reuse authenticated sessions.
- **Throttling**: Automatic sleep between requests (`sleep_range=(1,3)`).

## 💡 Tips

- Keep your bot token and Instagram credentials secret (don't commit `.env` to GitHub).
- For large downloads, consider increasing the sleep range or adding proxy rotation.

## 📄 License

This project is licensed under the [MIT License](LICENSE).
