#!/usr/bin/env python3
"""
telegram_instabot: A Telegram bot for downloading Instagram posts and stories and fetching profile information.
"""

import os
import logging
import shutil
import asyncio
from pathlib import Path

from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import FSInputFile
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from instaloader import Instaloader, Profile, exceptions
from dotenv import load_dotenv

# Load configuration
from config import TELEGRAM_TOKEN, INSTAGRAM_USER, INSTAGRAM_PASSWORD, SESSION_DIR

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
)
logger = logging.getLogger(__name__)

# Initialize Telegram bot and dispatcher
bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()

# Prepare Instaloader
session_path = Path(SESSION_DIR)
session_path.mkdir(exist_ok=True)
L = Instaloader(
    sleep=True,
    sleep_range=(1, 3),  # throttle requests to avoid rate limits
    download_comments=False,
    save_metadata=False,
    sessionfile=str(session_path / f"{INSTAGRAM_USER}.session")
)

async def startup_handler():
    """Login to Instagram on startup."""
    if INSTAGRAM_USER and INSTAGRAM_PASSWORD:
        try:
            L.login(INSTAGRAM_USER, INSTAGRAM_PASSWORD)
            logger.info("✅ Logged in to Instagram.")
        except exceptions.BadCredentialsException:
            logger.error("❌ Invalid Instagram credentials.")
        except Exception as e:
            logger.error(f"❌ Error during Instagram login: {e}")

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    keyboard = ReplyKeyboardBuilder()
    keyboard.button(text="/profile <username>")
    keyboard.button(text="/download_posts <username>")
    keyboard.button(text="/download_stories")
    keyboard.adjust(1)
    await message.reply(
        "👋 Welcome to *InstaDownloader Bot*!
"
        "Use the following commands:
"
        "- /profile `<username>`
"
        "- /download_posts `<username>`
"
        "- /download_stories",
        parse_mode="Markdown",
        reply_markup=keyboard.as_markup(resize_keyboard=True)
    )

@dp.message(Command("profile"))
async def cmd_profile(message: types.Message):
    args = message.get_args().strip()
    if not args:
        return await message.reply("Usage: /profile <username>")
    username = args

    try:
        profile = await asyncio.to_thread(Profile.from_username, L.context, username)
        caption = (
            f"👤 *{profile.username}*
"
            f"🔖 Full Name: {profile.full_name}
"
            f"👥 Followers: {profile.followers}
"
            f"🔗 https://instagram.com/{profile.username}"
        )
        await message.reply_photo(profile.profile_pic_url, caption=caption, parse_mode="Markdown")
    except exceptions.ProfileNotExistsException:
        await message.reply("❌ Profile not found.")
    except Exception as e:
        logger.error(f"Error fetching profile: {e}")
        await message.reply("❌ Could not fetch profile info.")

@dp.message(Command("download_posts"))
async def cmd_download_posts(message: types.Message):
    args = message.get_args().strip()
    if not args:
        return await message.reply("Usage: /download_posts <username>")
    username = args
    download_dir = Path("downloads") / username
    download_dir.mkdir(parents=True, exist_ok=True)

    await message.reply("⏳ Downloading latest posts...")
    try:
        posts = await asyncio.to_thread(lambda: list(L.get_posts(username))[:5])
        for post in posts:
            filepath = await asyncio.to_thread(lambda: L.download_post(post, download_dir))
            await message.reply_photo(FSInputFile(filepath))
    except Exception as e:
        logger.error(f"Error downloading posts: {e}")
        await message.reply("❌ Failed to download posts.")

@dp.message(Command("download_stories"))
async def cmd_download_stories(message: types.Message):
    download_dir = Path("downloads") / "stories"
    if download_dir.exists():
        shutil.rmtree(download_dir)
    download_dir.mkdir(parents=True)

    await message.reply("⏳ Downloading stories of your followees...")
    try:
        await asyncio.to_thread(L.download_stories, userids=[f.userid for f in L.get_followees()])
        archive_path = shutil.make_archive("stories_archive", 'zip', download_dir)
        await message.reply_document(FSInputFile(archive_path))
    except Exception as e:
        logger.error(f"Error downloading stories: {e}")
        await message.reply("❌ Failed to download stories.")

if __name__ == "__main__":
    from aiogram import executor

    dp.startup.register(startup_handler)
    executor.start_polling(dp, skip_updates=True)
