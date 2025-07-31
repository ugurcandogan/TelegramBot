from telegram import Bot
from dotenv import load_dotenv
import os
import asyncio

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=TOKEN)

async def main():
    await bot.delete_webhook()
    print("Webhook silindi.")

if __name__ == "__main__":
    asyncio.run(main())
