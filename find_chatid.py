
import asyncio
from telegram import Bot
from dotenv import load_dotenv
import os

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=TOKEN)

async def main():
    updates = await bot.get_updates()
    for update in updates:
        if update.channel_post:
            print("Kanal chat_id:", update.channel_post.chat.id)
        elif update.message:
            print("Kişisel chat_id:", update.message.chat.id)

if __name__ == "__main__":
    asyncio.run(main())
