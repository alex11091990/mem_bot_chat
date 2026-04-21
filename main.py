import asyncio
from telegram import Bot
import os
import requests

TOKEN = os.getenv("TOKEN")
CHAT_ID_1 = os.getenv("CHAT_ID_1")
CHAT_ID_2 = os.getenv("CHAT_ID_2")

VIDEO_URL = "https://drive.google.com/uc?export=download&id=15uMBtP73WGYjSlQpbCByqiX6k52hyKwQ"

bot = Bot(token=TOKEN)

async def send_video():
    try:
        response = requests.get(VIDEO_URL)

        with open("video.mp4", "wb") as f:
            f.write(response.content)

        with open("video.mp4", "rb") as f:
            await bot.send_video(chat_id=CHAT_ID_1, video=f)

        with open("video.mp4", "rb") as f:
            await bot.send_video(chat_id=CHAT_ID_2, video=f)

        print("✅ Видео отправлено")

    except Exception as e:
        print("❌ Ошибка:", e)


async def main():
    await send_video()


if __name__ == "__main__":
    asyncio.run(main())