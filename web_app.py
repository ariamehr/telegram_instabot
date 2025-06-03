import asyncio
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from instaloader import Profile

# Reuse the Instaloader instance from bot.py
from bot import L, INSTAGRAM_USER, INSTAGRAM_PASSWORD

app = FastAPI(title="Telegram InstaBot Web API")


@app.on_event("startup")
async def login_instagram():
    """Ensure Instaloader is logged in on startup."""
    if INSTAGRAM_USER and INSTAGRAM_PASSWORD and not L.context.is_logged_in:
        await asyncio.to_thread(L.login, INSTAGRAM_USER, INSTAGRAM_PASSWORD)


@app.get("/profile/{username}")
async def get_profile(username: str):
    """Fetch basic profile information for a given username."""
    try:
        profile = await asyncio.to_thread(Profile.from_username, L.context, username)
        return {
            "username": profile.username,
            "full_name": profile.full_name,
            "followers": profile.followers,
            "profile_pic_url": profile.profile_pic_url,
            "profile_url": f"https://instagram.com/{profile.username}",
        }
    except Exception:
        raise HTTPException(status_code=404, detail="Profile not found")


@app.get("/download_posts/{username}")
async def download_posts(username: str):
    """Download up to 5 latest posts as images and return them as file paths."""
    download_dir = Path("downloads") / username
    download_dir.mkdir(parents=True, exist_ok=True)
    try:
        posts = await asyncio.to_thread(lambda: list(L.get_posts(username))[:5])
        filepaths = []
        for post in posts:
            filepath = await asyncio.to_thread(lambda: L.download_post(post, download_dir))
            filepaths.append(filepath)
        return {"files": filepaths}
    except Exception:
        raise HTTPException(status_code=500, detail="Failed to download posts")


@app.get("/download_stories")
async def download_stories():
    """Download stories from followees and return a ZIP archive."""
    download_dir = Path("downloads") / "stories"
    if download_dir.exists():
        for p in download_dir.iterdir():
            if p.is_file():
                p.unlink()
            else:
                import shutil
                shutil.rmtree(p)
    download_dir.mkdir(parents=True, exist_ok=True)
    try:
        await asyncio.to_thread(L.download_stories, userids=[f.userid for f in L.get_followees()])
        import shutil
        archive_path = shutil.make_archive("stories_archive", 'zip', download_dir)
        return FileResponse(archive_path, filename="stories_archive.zip")
    except Exception:
        raise HTTPException(status_code=500, detail="Failed to download stories")
